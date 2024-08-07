import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import urllib.parse
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pytz

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

required_tasks = ["Getting Started with Google Kubernetes Engine",
                  "Google Cloud Fundamentals: Core Infrastructure",
                  "Essential Google Cloud Infrastructure: Foundation",
                  "Essential Google Cloud Infrastructure: Core Services",
                  "Optimize Costs for Google Kubernetes Engine",
                  "Build Infrastructure with Terraform on Google Cloud"]

sheet_id = os.environ.get("SHEET_ID")
sheet_name = urllib.parse.quote("Form Responses 1")
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url)

# rename columns Student ID to ID and Public Profile URL to Public Profile
df.rename(columns={"Student ID": "ID",
          "Public Profile Url": "Public Profile"}, inplace=True)

# print(df.columns)
# remove other columns
df = df[["ID", "Public Profile"]]

# extract row with duplicate Public Profile
duplicated_profile = df[df.duplicated(subset="Public Profile", keep=False)]

# if there is duplicate ID, keep the last one
df.drop_duplicates(subset="ID", keep="last", inplace=True)


def get_task_name(div):
    return div.find("span", class_="ql-title-medium l-mts").text.strip()


def get_task_date(div):
    date_time_str = div.find(
        "span", class_="ql-body-medium l-mbs").text.strip().replace("Earned ", "").replace(" EDT", "").replace(" EST", "")
    try:
        return datetime.strptime(date_time_str, '%b  %d, %Y')
    except Exception as ex:
        print(date_time_str)
        return pd.NaT


def convert(tup):
    di = {}
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di


def get_tasks(x):
    id = x['ID']
    url = x['Public Profile']
    page = requests.get(x['Public Profile'])
    soup = BeautifulSoup(page.content, "html.parser")
    profile_badges = soup.find_all("div", class_="profile-badge")
    tasks = list(
        map(lambda b: (get_task_name(b), get_task_date(b)), profile_badges))
    x["ID"] = id
    x["Public Profile"] = url
    for k, v in tasks:
        x[k] = v
    for task in required_tasks:
        if task not in x:
            x[task] = pd.NaT
    return x


left_cols = ['ID', 'Public Profile']


def generate_report(result):
    result = result[left_cols +
                    [col for col in result.columns if col not in left_cols]]
    required_column = left_cols + required_tasks
    return result, result[required_column]


def convert_to_x(row):
    r = []
    for index, value in row.items():
        if index not in left_cols:
            r.append("" if value is pd.NaT else "X")
        else:
            r.append(value)
    return pd.Series(r, index=row.index)


result = df.apply(get_tasks, axis=1)
result.sort_values(by=['ID'], inplace=True)
report_all, report_required = generate_report(result)

result = result.apply(convert_to_x, axis=1)
report_all_X, report_require_X = generate_report(result)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')

non_mark_cols = ['ID', 'Public Profile', 'Finished', 'Complete All']

# in report_require_X dataframe, except ID and Public Profile, if all other columns are X, then mark to a new completed column
def get_completed(row):
    for index, value in row.items():
        if index not in non_mark_cols:
            if value != "X":
                return "No"
    return "Yes"

def count_X(row):
    no_x = 0
    for index, value in row.items():
        if index not in non_mark_cols:
            if value == "X":
                no_x += 1
    return no_x


report_require_X = report_require_X.copy()
report_require_X.loc[:, 'Finished'] = report_require_X.apply(
    count_X, axis=1)
report_require_X.loc[:, 'Complete All'] = report_require_X.apply(
    get_completed, axis=1)

# Reorder 'Complete All' and 'Finished' columns to the second column
cols = list(report_require_X.columns)
cols = [cols[0]] + [cols[-1]] + [cols[-2]] + cols[1:-2]
report_require_X = report_require_X[cols]

# Write each dataframe to a different worksheet.
report_require_X.to_excel(writer, sheet_name='Required X')
report_all_X.to_excel(writer, sheet_name='All X')
report_required.to_excel(writer, sheet_name='Required Date')
report_all.to_excel(writer, sheet_name='All Date')

# Close the Pandas Excel writer and output the Excel file.
writer.close()

report_require_X.to_html("table.html")
# Read report.html file and save to a variable
table = open("table.html").read()
template = env.get_template("report.html")

# Get Hong kong time
tz = pytz.timezone('Asia/Hong_Kong')
datetime_HK = datetime.now(tz)
# Render report.html with data
report_html = template.render(
    table=table, now=datetime_HK.strftime("%d/%m/%Y %H:%M:%S"), time_zone="Hong Kong")
# save report.html
with open("report.html", "w") as f:
    f.write(report_html)
# remove table.html
os.remove("table.html")

report_require_X.to_csv("report.csv")
