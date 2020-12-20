import pandas as pd
from datetime import datetime

months_dict = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


def created_at_to_datetime(created_at):
    created_at = created_at.split(sep=" ")
    created_at = months_dict[created_at[1]] + "/" + created_at[2] + "/" + created_at[-1] + " " + created_at[3]
    created_at = datetime.strptime(created_at, '%m/%d/%Y %H:%M:%S')
    return created_at


df = pd.read_csv("./data/dates.csv", sep=",")
print(df.head())


