import smtplib
import requests
from bs4 import BeautifulSoup

PRICE_BORDER = 300000
URL = 'Product url, what you would like to check'
headers = {
    "User-Agent": 'Your user agent (Write into google "my user agent, and copy that")'}


def request_to_shop(page_url):
    page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Section of the information parsing, find the information sections from the page's html
    # (F12 - Elements and use the (Ctrl + Shift + C) possibility)
    title = soup.find(class_='col-lg-6 col-md-6 col-sm-6 col-xs-12').get_text()
    price = soup.find(class_='price').get_text()

    # I had to convert the price to float and
    # i had to make some changes with the format as well because of the spaces
    convert_price = float(price.strip()[0:7].replace(" ", ""))
    print(title.strip().split(',')[-1].strip().split('\n')[0])
    print(price.strip())
    return convert_price


def price_check(actual_price, price_border):
    if actual_price < price_border:
        send_mail()
        print('Mail has been sent!')


def send_mail():
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('from_mail_address', 'password')

    subject = 'Check the Product!'
    body = 'Here is the link:' + URL
    message = f"Subject:  {subject}\n\n{body}"

    smtp.sendmail('from_mail_address', 'to_mail_address', message)
    smtp.quit()


actual_price = request_to_shop(URL)
price_check(actual_price, PRICE_BORDER)
