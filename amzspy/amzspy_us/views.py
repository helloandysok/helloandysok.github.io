from django.shortcuts import render, redirect
from .models import User, Send
from .forms import UserForm
from django.contrib import messages
from django.http import HttpResponse
from .tasks import sleepy


# Create your views here.


def home(request):
    import requests
    import traceback
    import smtplib
    import time
    from bs4 import BeautifulSoup
    from lxml.html import fromstring
    from itertools import cycle

    # For Realtime database

    if request.method == 'POST':

        # Get a URL from the user
        URL = request.POST.get('amzurl', None)

        # For utilizing the Chrome Browser
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

        # User info:
        email_list = request.POST.get('email', None)

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

            # Terminate
            server.quit()

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

        # Store old price
        temp_price = current_price

        send = Send(sendurl=URL, sendemail=email_list, sendprice=temp_price)
        send.save()

        verify = send.sendprice

        # input, Lambda & polymorphism to determine discount
        # discount = float(input("How big of a discount are you looking for? (Ex: 10 for 10% off) "))
        get_discount = (lambda a, b, c, d: ((a / b) - c) * d)(current_price, current_full, 1, -1)
        percentage_shift = round(discount_conversion(float(get_discount), 100), 2)

        # Call price check function
        price_check()

        # Check hourly for price shifts
        while price_check() >= verify:
            messages.success(request, {'The Product: ': title})
            messages.success(request, {'The Current Price: ': price})
            messages.success(request, {'The Current Discount In Percentage: ': percentage_shift})
            sleepy.delay(3600)
            return render(request, "home.html", messages.success(request, {'Product Imported! We Will Email You For Any Price Drops!'}))

        # Send email if the price is lowered
        if price_check() < verify:
            sender(email_list)
            messages.success(request, {'The Product: ': title})
            messages.success(request, {'The Current Price: ': price})
            messages.success(request, {'The Current Discount In Percentage: ': percentage_shift})
            return render(request, "home.html", messages.success(request, {'Product Successfully Imported! Check Your Inbox For Any Notifications!'}))

        return render(request, "home.html", messages.success(request, {'Imports Completed.'}))
    else:
        return render(request, "home.html", {})

