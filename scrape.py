import requests
import traceback
import smtplib
import time
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle


# Copy/Paste Input
URL = input("Copy & Paste The Amazon URL You Would Like To Price Track: ")

# URL I'm testing.
#URL = "https://www.amazon.com/Razer-Blade-Gaming-Laptop-2019/dp/B07QB1DH5N"

# For utilizing the Chrome Browser
headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}


# def get_discount(a, b, c, d):
   #return ((a/b) - c) * d

# def discount_shift(a, b):
    #return a / b

def price_tracker():

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

    # Testing
    print("Your List Price: ")
    print(full)
    print("Your Product: ")
    print(title.strip())
    print("Your Price: ")
    print(price)

    # Lambda
    discount = float(input("How big of a discount are you looking for? (Ex: 10 for 10% off) "))
    get_discount = (lambda a, b, c, d: ((a/b) - c) * d)(current_price, current_full, 1, -1)
    convert_discount = (lambda a, b: a / b)(float(discount), 100)

    if get_discount >= convert_discount:
        sender()

# TEST: Send the email if the price drops
    # if current_price < 3000:
        # sender()


def sender():

    # Connect email server and email account
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    # Starts the encrypted communication with the server
    server.starttls()
    server.ehlo()
    server.login('endlesskhaiandy@gmail.com', 'ivdnvcsckaporjco')

    # TEST: Email message to send to list / Add the URL variable in the body of the email
    subject = 'New Amazon Product Price Alert!'
    body = 'Hey Smart Shopper, a product you want has a lower price! ' \
           'Check it out by clicking the link: ', URL
    msg = f"Subject: {subject}\n\n{body}"

    email_sender = input("Enter Your Email: (Ex: andysok@gmail.com) ")
    server.sendmail('endlesskhaiandy@gmail.com', email_sender, msg)

    # Email Confirmation
    print('Thank you for your patience; Check your email! ')

    # Terminate
    server.quit()


while True:

    # Check the price every hour until the price changes
    # Need to have SQL database update every hour instead of program
    price_tracker()
    time.sleep(3600)

# Add javascript integration for website

# Add SQL database for website
