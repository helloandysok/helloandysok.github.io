import * as requests from 'requests';
import * as traceback from 'traceback';
import * as smtplib from 'smtplib';
import * as time from 'time';
import {BeautifulSoup} from 'bs4';
import {fromstring} from 'lxml/html';
import {cycle} from 'itertools';
import * as firebase_admin from 'firebase_admin';
import {credentials, firestore} from 'firebase_admin';
var URL, cred, db, default_app, headers;
cred = new credentials.Certificate("amzspy-ed060-firebase-adminsdk-ombif-5fa1965a13.json");
default_app = firebase_admin.initialize_app(cred);
db = firestore.client();
URL = input("Copy & Paste The Amazon URL You Would Like To Price Track: ");
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"};
function discount_conversion(a, b) {
    return (a / b);
}

function saveToFirebase(email_list) {
    var emailObj = {
        email: email_list
    }
    firebase.database().ref('users').push().set(emailObj)
        .then(function(snapshot)) {
            console.log("Email saved to database! ");
        }, function(error) {
            console.log("Could not save email. ");
        }
}

function price_tracker() {
    var change_full, changer, convert_full, converter, current_full, current_price, discount, email_list, find_dot, find_full, full, get_discount, page, percentage_shift, price, replace_full, replacer, soup, soup_old, stripped, stripped_full, title;
    page = requests.get(URL, {"headers": headers});
    soup_old = new BeautifulSoup(page.content, "html.parser");
    soup = new BeautifulSoup(soup_old.prettify(), "html.parser");
    title = soup.find({"id": "productTitle"}).get_text();
    full = soup.find({"class_": "priceBlockStrikePriceString a-text-strike"}).get_text();
    price = soup.find({"id": "priceblock_ourprice"}).get_text();
    stripped = price.strip("$ ,");
    stripped_full = full.strip("$ ,");
    replacer = stripped.replace(",", "");
    replace_full = stripped_full.replace(",", "");
    find_dot = replacer.find(".");
    find_full = replace_full.find(".");
    changer = replacer.slice(0, find_dot);
    change_full = replace_full.slice(0, find_full);
    converter = Number.parseFloat(changer);
    convert_full = Number.parseFloat(change_full);
    current_price = converter;
    current_full = convert_full;
    console.log("Your Product: ");
    console.log(title.strip());
    console.log("Your List Price: ");
    console.log(full);
    console.log("Your Price: ");
    console.log(price);
    discount = Number.parseFloat(input("How big of a discount are you looking for? (Ex: 10 for 10% off) "));
    get_discount = (a, b, c, d) => {
    return (((a / b) - c) * d);
}(current_price, current_full, 1, (- 1));
    percentage_shift = discount_conversion(Number.parseFloat(discount), 100);
    email_list = input("Enter Your Email: (Ex: andysok@gmail.com) ");
    saveToFirebase(email_list);
    while ((get_discount <= percentage_shift)) {
        console.log("Your product is not at the desired discount yet. We will check hourly to see any price differences.");
        console.log("You will receive an email in your inbox once your discount is available..");
        time.sleep(3600);
    }
    if ((get_discount >= percentage_shift)) {
        sender(email_list);
    }
}
function sender(email_list) {
    var body, msg, server, subject;
    server = new smtplib.SMTP("smtp.gmail.com", 587);
    server.ehlo();
    server.starttls();
    server.ehlo();
    server.login("endlesskhaiandy@gmail.com", "ivdnvcsckaporjco");
    subject = "New Amazon Product Price Alert!";
    body = ["Hey Smart Shopper, a product you want has a lower price! Check it out by clicking the link: ", URL];
    msg = `Subject: ${subject}

${body}`
;
    server.sendmail("endlesskhaiandy@gmail.com", email_list, msg);
    console.log("Thanks for your patience; Check your email! ");
    server.quit();
}
price_tracker();

<!-- The core Firebase JS SDK is always required and must be listed first -->
<script src="https://www.gstatic.com/firebasejs/7.8.0/firebase-app.js"></script>

<!-- TODO: Add SDKs for Firebase products that you want to use
     https://firebase.google.com/docs/web/setup#available-libraries -->
<script src="https://www.gstatic.com/firebasejs/7.8.0/firebase-analytics.js"></script>

<script>
  // Your web app's Firebase configuration
  var firebaseConfig = {
    apiKey: "AIzaSyB8eBVmASaUYLEGJC3sqvbynBwHKMMZskU",
    authDomain: "amzspy-ed060.firebaseapp.com",
    databaseURL: "https://amzspy-ed060.firebaseio.com",
    projectId: "amzspy-ed060",
    storageBucket: "amzspy-ed060.appspot.com",
    messagingSenderId: "1053203861155",
    appId: "1:1053203861155:web:4f0f3a0d478237367fb916",
    measurementId: "G-7JRT4L9GPK"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  firebase.analytics();
</script>

//# sourceMappingURL=scrape.js.map
