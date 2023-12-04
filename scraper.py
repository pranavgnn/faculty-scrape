import requests
from bs4 import BeautifulSoup

base_url = "https://manipal.edu"

class Scraper:
    def __init__(self):
        self.data = {}
    
    def get_page(self):
        response = requests.get(base_url + "/mit/department-faculty.html")

        if (response.status_code != 200):
            return
        
        return BeautifulSoup(response.text, "html.parser")

    def get_departments(self):
        soup = self.get_page()
        
        if soup is None:
            return

        container = soup.find("div", {"class": "departments-accordion-comp js-departments-faculty-comp"})
        departments = container.find_all("div", {"class": "departments-accordion-wp js-dep-accordion-wp"})

        return departments

    def scrape_department(self, department):
        heading_link = department.find("a", {"class": "title-link"})
        members = department.find_all("a", {"class": "members-wp"})

        department_name = heading_link.text.strip()[14:]
        scraped_members = []

        for member in members:
            scraped_members.append(self.scrape_member(member))
        
        self.data[department_name] = scraped_members
    
    def scrape_departments(self):
        departments = self.get_departments()

        if (departments is None):
            return
        
        for department in departments:
            self.scrape_department(department)

    def scrape_member(self, member):
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

    def scrape(self):
        self.scrape_departments()
        return self.data