from crawler_discovery import discovery
import index
import json

# model = "basic_model_23"
# nlp = index_string.load_model(model)

all_phones = discovery()
result = []
for phone in all_phones:
    brand = index.get_brand(phone[0].lower())
    if not brand:
        continue
    data = index.gett(phone)
    result.append(data)

with open("flask-backend/phones.json", "w") as f:
    f.write(json.dumps(result, indent=4))
        # print(json.dumps(data, indent=4))

# all_phones = altex_phones + vexio_phones + qm_mobile
# index_string.store_data(nlp, all_phones)
# index_string.store_data(nlp, vexio_phones)