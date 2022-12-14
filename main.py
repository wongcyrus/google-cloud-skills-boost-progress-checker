import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


required_tasks = ["Getting Started with Google Kubernetes Engine",
                  "Google Cloud Fundamentals: Core Infrastructure",
                  "Essential Google Cloud Infrastructure: Foundation",
                  "Automating Infrastructure on Google Cloud with Terraform",
                  "Essential Google Cloud Infrastructure: Core Services",
                  "Optimize Costs for Google Kubernetes Engine",
                  "Logging, Monitoring and Observability in Google Cloud",
                  "Reliable Google Cloud Infrastructure: Design and Process"]

df = pd.read_excel("Students.xlsx")


def get_task_name(div):
    return div.find("span", class_="ql-subhead-1 l-mts").text.strip()


def get_task_date(div):
    date_time_str = div.find(
        "span", class_="ql-body-2 l-mbs").text.strip().replace("Earned ", "").replace(" EDT", "").replace(" EST", "")
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

# Write each dataframe to a different worksheet.
report_require_X.to_excel(writer, sheet_name='Required X')
report_all_X.to_excel(writer, sheet_name='All X')
report_required.to_excel(writer, sheet_name='Required Date')
report_all.to_excel(writer, sheet_name='All Date')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

report_require_X.to_html("report.html")
report_require_X.to_csv("report.csv")
