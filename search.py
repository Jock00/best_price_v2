import argparse
import json
from database.db_scripts import PhonesDB
from crawler_parse import Parser
from scrapy.crawler import CrawlerProcess

def search_in_db(db_name, args):
    db = PhonesDB(db_name)
    phones_in_db = db.check_records(args)
    db.close_connection()
    return phones_in_db


def get_prices(urls):

    file = "output.json"
    process = CrawlerProcess(settings={
        'LOG_ENABLED': False,
        #         # 'LOG_LEVEL': 'INFO',
        'FEEDS': {
            file: {
                'format': 'json',
                'overwrite': True,
            },
        },
    })

    # Start the crawling process
    process.crawl(Parser, urls=urls)
    process.start()

    with open(file, "r") as f:
        data = json.loads(f.read())

    # Sort the data by price in ascending order
        sorted_data = sorted(data, key=lambda x: x['price'])
        return sorted_data
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
