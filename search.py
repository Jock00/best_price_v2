import argparse
import json
# from database.db_scripts import PhonesDB
# from crawler_parse import Parser
# from scrapy.crawler import CrawlerProcess
import crawlers_parse_python
import time

def search_in_db(db_name, args):
    db = PhonesDB(db_name)
    phones_in_db = db.check_records(args)
    db.close_connection()
    return phones_in_db


def get_prices(urls):
    results = []
    for url in urls:
        if "vexio.ro" in url:
            res = crawlers_parse_python.get_data_vexio.delay(url)
        elif "altex.ro" in url:
            res = crawlers_parse_python.get_data_altex.delay(url)
        elif "telefonultau.eu" in url:
            res = crawlers_parse_python.get_data_telefonul_tau.delay(url)
        elif "quickmobile.ro" in url:
            res = crawlers_parse_python.get_data_quickmobile.delay(url)
        else:
            continue
        results.append(res.get(timeout=50))
    results = sorted(results, key=lambda x: x["price"])
    with open("data2.json", "w") as f:
        f.write(json.dumps(results, indent=4))
    return results

    # with open(file, "r") as f:
    #     data = json.loads(f.read())
    #
    # # Sort the data by price in ascending order
    #     sorted_data = sorted(data, key=lambda x: x['price'])
    #     return sorted_data
        # f.write(json.dumps(sorted_data))
    # Print the sorted data
    #     print(json.dumps(sorted_data, indent=4))


    #
    # for phone in results:
    #     if "https://altex.ro" in phone:
    #         print("daaa")
    #         a = crawl_altex.delay(phone)
    #     else:
    #         print("vexio")
    #         a = 2
        # price = a.get(timeout=50)

        # final[phone] = price

        # break
    # sorted_dict = dict(sorted(final.items(), key=lambda item: item[1]))
    # print(json.dumps(sorted_dict, indent=4))
    # run crawiling with celery
