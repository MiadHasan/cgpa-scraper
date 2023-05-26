from collections import defaultdict
from logging import raiseExceptions
from bs4 import BeautifulSoup as bs
import requests


id = input("Enter ID: ")
password = input("Enter Password: ")

# studentPass = {"rashed": "28010324", "miad": "34815793", "irfan": "60943145"}

# if id == "1704118" and password == "0":
#     password = studentPass["miad"]

s = requests.Session()

URL = "https://course.cuet.ac.bd/"
LOGIN_ROUTE = "index.php/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "origin": URL,
    "referer": URL + LOGIN_ROUTE,
}

login_payload = {
    "user_email": id,
    "user_password": password,
    "loginuser": "Sign In",
}

try:
    login_req = s.post(URL, headers=HEADERS, data=login_payload)
    result = s.get(URL + "result_published.php").text
    if "set-cookie" in login_req.headers.keys():
        raiseExceptions()
except:
    print("Login failed!")
    quit()

soup = bs(result, "lxml")
scraped_result = soup.find_all("td")

grades = {
    "A+": 4.0,
    "A": 3.75,
    "A-": 3.5,
    "B+": 3.25,
    "B": 3.0,
    "B-": 2.75,
    "C+": 2.5,
    "C": 2.25,
    "D": 2,
    "F": 0,
}
results = defaultdict(lambda: defaultdict(dict))

for index, course in enumerate(scraped_result):
    if "Level" in course.text:
        results[course.text][scraped_result[index - 2].text]["credit"] = float(
            scraped_result[index - 1].text
        )
        results[course.text][scraped_result[index - 2].text]["grade"] = scraped_result[
            index + 2
        ].text


def calculate_cgpa(courses):
    total_credit = 0
    grade_times_credit = 0
    for course in courses:
        if grades[courses[course]["grade"]] != 0:
            total_credit += courses[course]["credit"]
            grade_times_credit += (
                courses[course]["credit"] * grades[courses[course]["grade"]]
            )
    return round(grade_times_credit / total_credit, 2)


total_cgpa = 0
print("\nTerm              GPA")
for semester in results:
    results[semester]["CGPA"] = calculate_cgpa(results[semester])
    total_cgpa += results[semester]["CGPA"]
    print(f"{semester}: {results[semester]['CGPA']}")

if len(list(results.keys())) != 0:
    final_cgpa = round(total_cgpa / len(list(results.keys())), 2)
    print(f"Final CGPA: {final_cgpa}")
