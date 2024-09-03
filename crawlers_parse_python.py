# celery -A crawlers_parse_python worker --loglevel=info
from celery import Celery
import time
import requests
from lxml.html import fromstring
import re
import json
import os

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'
app = Celery('parsers', broker=BROKER_URL, backend=BACKEND_URL, )
app.conf.broker_connection_retry_on_startup = True
app.conf.update(
    result_expires=3600,
)

vexio_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
}
altex_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',

}

val = 1

# vexio
@app.task
def get_data_vexio(link):
    def clean_json_string(json_string):
        json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
        return json_string
    r = requests.get(link, headers=vexio_headers)

    response = fromstring(r.text)
    # Extract data you want from the page
    script = response.xpath(
        "//*[@type='application/ld+json']//text()"
    )[-1]
    # print(script)
    data = json.loads(clean_json_string(script))

    name = data["name"]

    price = data["offers"]["price"]

    try:
        rating = data["aggregateRating"]["ratingValue"]
    except KeyError:
        rating = None

    elem = {
        "url": link,
        "price": float(price),
        "name": name,
        "shop": "vexio",
        "rating": rating,
        "rpr": None,
        "resealed": []
    }

    return elem

# altex
@app.task
def get_data_altex(link):
    def clean_json_string(json_string):
        json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
        return json_string
    # print("Start")
    r = requests.get(link, headers=vexio_headers)

    response = fromstring(r.text)
    # Extract data you want from the page
    script = response.xpath(
        "//*[@type='application/ld+json']//text()"
    )[0]
    # print(script)
    data = json.loads(clean_json_string(script))

    name = data["name"]
    image = data["image"][0]
    price = data["offers"][0]["priceSpecification"]["price"]
    rating = data["aggregateRating"]["ratingValue"]

    script = response.xpath(
        "//*[@id='__NEXT_DATA__']//text()"
    )[0]
    product = json.loads(script)["props"]["initialReduxState"]["catalog"][
        "currentProduct"]["product"]
    rpr = product["msrp_price"]

    resealed = []
    for res in product["resealed"]:
        res_price = res["price"]["selling_price"]
        res_reason = res["resealed_reasons"]
        res_phone = {
            "price": res_price,
            "reason": res_reason
        }
        resealed.append(res_phone)

    elem = {
        "url": link,
        "price": float(price),
        "name": name,
        "shop": "altex",
        "rating": rating,
        "rpr": rpr,
        "resealed": resealed
    }

    return elem


# telefonul tau
@app.task
def get_data_telefonul_tau(url):

    r = requests.get(url)
    data = json.loads(r.text)

    link = data["url"]

    name = data["name"]

    price = data["price"]

    rating = data["rating"]

    rpr = None

    resealed = []

    elem = {
        "url": link,
        "price": float(price),
        "name": name,
        "shop": "telefonul_tau",
        "rating": rating,
        "rpr": rpr,
        "resealed": resealed
    }

    return elem
