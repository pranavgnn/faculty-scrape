import requests
import os
from bs4 import BeautifulSoup
import json

base_url = "https://manipal.edu"
scraped_data = {}

response = requests.get(base_url + "/mit/department-faculty.html")
if (response.status_code != 200):
    print("Failed to retrieve HTML.")
    os._exit(0)

soup = BeautifulSoup(response.text, "html.parser")

container = soup.find("div", {"class": "departments-accordion-comp js-departments-faculty-comp"})
departments = container.find_all("div", {"class": "departments-accordion-wp js-dep-accordion-wp"})

def scrape_department(department):
    heading_link = department.find("a", {"class": "title-link"})
    members = department.find_all("a", {"class": "members-wp"})

    department_name = heading_link.text.strip()[14:]
    scraped_members = []

    for member in members:
        scraped_members.append(scrape_member(member))
    
    scraped_data[department_name] = scraped_members

def scrape_member(member):
    h4 = member.find("h4")
    p = member.find_all("p")
    img = member.find("img")

    name = h4.text.strip()
    designation = p[0].text.strip()
    email = p[1].text.strip()
    image_url = base_url + img["data-src"].replace(" ", "%20") if ("data-src" in img.attrs) else ""

    return {
        "name": name,
        "designation": designation,
        "email": email,
        "image_url": image_url,
    }

for department in departments:
    scrape_department(department)

with open("output.json", "w") as file:
    json.dump(scraped_data, file)