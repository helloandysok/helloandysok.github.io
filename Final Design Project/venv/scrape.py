import requests
import traceback
import smtplib
import time
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle
# For Realtime database
from firebase import firebase
# Initialize Admin SDK from Firebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('amzspy-ed060-firebase-adminsdk-ombif-5fa1965a13.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Get a URL from the user
URL = input("Copy & Paste The Amazon URL You Would Like To Price Track: ")

# For utilizing the Chrome Browser
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

# User info:
email_list = input("Enter Your Email: (Ex: andysok@gmail.com) ")


# OOP Component of Polymorphism
def discount_conversion(a, b):
    return a * b


def price_check():
    # Get the page you're searching for
    new_page = requests.get(URL, headers=headers)

    # Used to bypass anti-scraping
    new_soup_old = BeautifulSoup(page.content, "html.parser")

    # Used to gather data on Amazon product page
    new_soup = BeautifulSoup(soup_old.prettify(), "html.parser")

    # Find the title
    new_title = soup.find(id="productTitle").get_text()

    # Find the full price
    new_full = soup.find(class_="priceBlockStrikePriceString a-text-strike").get_text()

    # Find the price
    new_price = soup.find(id="priceblock_ourprice").get_text()

    # Strip the price of non-numbers
    new_stripped = new_price.strip("$ ,")
    new_stripped_full = new_full.strip("$ ,")

    # Replace the commas with empty character
    new_replacer = new_stripped.replace(",", "")
    new_replace_full = new_stripped_full.replace(",", "")

    # Find the dot in the price
    new_find_dot = new_replacer.find(".")
    new_find_full = new_replace_full.find(".")

    # Convert the price by removing the cents
    new_changer = new_replacer[0:new_find_dot]
    new_change_full = new_replace_full[0:new_find_full]

    # The price, fully converted
    new_converter = float(new_changer)
    new_convert_full = float(new_change_full)

    # Store the current price for comparison
    new_current_price = new_converter
    new_current_full = new_convert_full
    return new_current_price


def sender(email_list):

    # Connect email server and email account
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    # Starts the encrypted communication with the server
    server.starttls()
    server.ehlo()
    server.login('endlesskhaiandy@gmail.com', 'ivdnvcsckaporjco')

    # Email message to send to list / Add the URL variable in the body of the email
    subject = 'New Amazon Product Price Alert!'
    body = 'Hey Smart Shopper, a product you want has a lower price! ' \
           'Check it out by clicking the link: ', URL
    msg = f"Subject: {subject}\n\n{body}"

    # Send the mail!
    server.sendmail('endlesskhaiandy@gmail.com', email_list, msg)

    # Email Confirmation
    print('Thanks for your patience; Check your email! ')

    # Terminate
    server.quit()


# Run the price tracker
# Track price for user
# Get the page you're searching for
page = requests.get(URL, headers=headers)

# Used to bypass anti-scraping
soup_old = BeautifulSoup(page.content, "html.parser")

# Used to gather data on Amazon product page
soup = BeautifulSoup(soup_old.prettify(), "html.parser")

# Find the title
title = soup.find(id="productTitle").get_text()

# Find the full price
full = soup.find(class_="priceBlockStrikePriceString a-text-strike").get_text()

# Find the price
price = soup.find(id="priceblock_ourprice").get_text()

# Strip the price of non-numbers
stripped = price.strip("$ ,")
stripped_full = full.strip("$ ,")

# Replace the commas with empty character
replacer = stripped.replace(",", "")
replace_full = stripped_full.replace(",", "")

# Find the dot in the price
find_dot = replacer.find(".")
find_full = replace_full.find(".")

# Convert the price by removing the cents
changer = replacer[0:find_dot]
change_full = replace_full[0:find_full]

# The price, fully converted
converter = float(changer)
convert_full = float(change_full)

# Store the current price for comparison
current_price = converter
current_full = convert_full

temp_price = current_price

# Print the original price, product title, and current sale price
print("Your Product: ")
print(title.strip())
print("Your List Price: ")
print(full)
print("Your Price: ")
print(price)

# input, Lambda & polymorphism to determine discount
# discount = float(input("How big of a discount are you looking for? (Ex: 10 for 10% off) "))
get_discount = (lambda a, b, c, d: ((a / b) - c) * d)(current_price, current_full, 1, -1)
percentage_shift = round(discount_conversion(float(get_discount), 100), 2)

print("Current Discount: ")
print(percentage_shift,"%")


# Realtime database creation
firebase = firebase.FirebaseApplication("https://amzspy-ed060.firebaseio.com/", None)
data = {
    'Email': email_list,
    'Old Price': temp_price,
}
# Just to verify if database received user
result = firebase.post('/amzspy-ed060/User', data)
print(" ")
print(result)
print(" ")

# Call price check function
price_check()

# Check hourly for price shifts
while price_check() >= temp_price:
    print("Your product is not at the desired discount yet. We will check hourly to see any price differences.")
    print("You will receive an email in your inbox once your discount is available..")
    time.sleep(3600)
    price_check()


# Send email if the price is lowered
if price_check() < temp_price:
    sender(email_list)


