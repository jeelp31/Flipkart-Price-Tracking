# All the libraries Used:-


import matplotlib.pyplot as plt
import smtplib
import datetime as dt
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import pandas
from datetime import date


a = ""
os.chmod('price_list.csv', 0o777)
d = date.fromordinal(730920)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
plt.style.use('bmh')
df = pd.read_csv('price_list.csv')


# Writing Budget Of The Product:-


if os.path.getsize("my_url.txt") == 0:
    b = str(input("Enter Your Budget For The Product::"))
    with open("my_url.txt", mode="w") as price_list:
        write_url = price_list.write(str(b))

with open("my_url.txt") as url:
    url = str(url.read())

if os.path.getsize("my_budget.txt") == 0:
    c = int(input("Enter Your Budget For The Product::"))
    with open("my_budget.txt", mode="w") as price_list:
        write_budget = price_list.write(str(c))

with open("my_budget.txt") as budget:
    budget = int(budget.read())

price_data = pandas.read_csv("price_list.csv")
data_dict = price_data.to_dict()


# Collecting Price From Website:-


response = requests.get(url)
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page, "html.parser")
price_tag = soup.find(name="div", class_="_30jeq3 _16Jk6d")
price = price_tag.get_text()


# Converting Price To Integer:-


def getnumber(word):
    combine = ""
    complete = []
    for letter in word:
        if combine:
            if combine.isdigit() == letter.isdigit():
                combine += letter
            else:
                complete.append(combine)
                combine = letter
        else:
            combine = letter
    if combine:
        complete.append(combine)
    numbers = [word for word in complete if word.isdigit()]
    return numbers



def convert(list_price):
    s = [str(i) for i in list_price]
    res = int("".join(s))
    return (res)


# Adding Daily Prices To Data:-


price1 = getnumber(price)
data = int(convert(price1))
now = dt.datetime.now()
month = now.month - 1
day = now.day
price_info = pandas.read_csv("price_list.csv")
price_info.loc[day-1, months[month]] = data
price_info.to_csv("price_list.csv", index=False)
min_price_of_month = price_info[months[month - 1]].min()
date_min_price = price_info[price_info[months[month - 1]] == price_info[months[month - 1]].min()]


# Plotting Graph


x = df['Unnamed: 0']
y = df[months[month]]
plt.xlabel(months[month], fontsize=9)
plt.ylabel("Price", fontsize=8)
graph = plt.bar(x, y)
plt.draw()
plt.savefig("my_graph.jpg")


# Sending Email:-


my_email = "ENTER YOUR EMAIL ID"
password = "EMAIL ID PASSWORD"

if data < budget:
    if os.path.getsize("my_email.txt") == 0:
        a = str(input("Enter Your Email address::"))
        with open("my_email.txt", mode="w") as price_list:
            write_email = price_list.write(str(a))

    with open("my_email.txt") as email_id:
        content = email_id.read()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=content,
            msg="Subject:Price Alert\n\nCongratulations The Price of the product has dropped below your budget!"
        )


# Sending Email For Prediction Of Future Price:-


if day == 1:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=content,
            msg=f"Subject:Future Predicted Price\n\nThe Min Price of the Product was on the Date {date_min_price.Days.item()}\n\nAnd the Min Price was {min_price_of_month}\n\n"
        )
