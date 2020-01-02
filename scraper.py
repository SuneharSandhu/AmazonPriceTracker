import requests
from bs4 import BeautifulSoup
import smtplib
import time
import json  # this is only used to print the dictionary in a json format : not necessary

SECONDS_IN_DAY = 86400

URL = 'https://www.amazon.com/iBUYPOWER-Computer-Element-9260-i7-9700F/dp/B07V34QQ3C?ref_=Oct_s9_apbd_otopr_hd_bw_b9NFlZb_2&pf_rd_r=ZQ47PGW9VM1Z12D8Y8JE&pf_rd_p=a2ecba9d-c39a-5ab0-a2cf-8db477dd992b&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&pf_rd_i=8588809011&th=1'

def price_check():

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    details = {'name' : '', 'price' : 0, 'deal' : True, 'url' : ''}
    _url = extract_url(URL)

    if URL == "":
        details = None
    else:
        page = requests.get(URL, headers=headers)
        soup1 = BeautifulSoup(page.content, 'html.parser')
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

        title = soup2.find(id="productTitle").get_text().strip()
        price = soup2.find(id="priceblock_dealprice")
        if price is None:
            details['deal'] = False
            price = soup2.find(id="priceblock_ourprice")
        if title is not None and price is not None:
            price = price.get_text().strip()
            converted_price = convert_price(price)
            compare_price = converted_price

            details['name'] = title
            details['price'] = price
            details['url'] = _url
        else:
            return None

        if converted_price < compare_price:
            send_mail()

    print(json.dumps(details, indent=4))

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('sunehar.sandhu@gmail.com', 'Rutgers2020')

    subject = 'Price went down!'
    body = f'Check the amazon link {URL}'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        'sunehar.sandhu@gmail.com',
        'sunehar.sandhu@gmail.com',
        msg
    )

    print('Email has been sent!')

    server.quit()

def convert_price(price):
    price = int(price.replace('$', '').replace(',', '')[:-3])
    return price

def extract_url(url):
    if url.find('www.amazon.com') != -1:
        index = url.find('/dp/')
        if index != -1:
            index2 = index + 14
            url = 'https://www.amazon.com' + url[index:index2]
        else:
            index = url.find('/gp/')
            if index != -1:
                index2 = index + 22
                url = 'https://www.amazon.com' + url[index:index2]
            else:
                url = None
    else:
        url = None

    return url

# Set to check prices every day
# while True:
#     print(price_check())
#     time.sleep(SECONDS_IN_DAY);

price_check()
