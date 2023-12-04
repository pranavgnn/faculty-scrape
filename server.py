from flask import Flask, render_template
from scraper import Scraper

app = Flask(__name__)
scraper = Scraper()

data = scraper.scrape()

@app.route("/")
def home():
    return render_template("index.html", data=[ [key, len(members)] for key, members in data.items() ])

@app.route("/<dept>")
def department(dept):
    dept = dept.replace("-", " ")
    return render_template("department.html", department_name=dept, members=data[dept])

if __name__ == "__main__":
    app.run()