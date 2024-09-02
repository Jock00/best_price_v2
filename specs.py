import json

import requests
from lxml.html import fromstring

url = "https://www.dxomark.com/smartphones/"
var = "var smartphonesAsJson = "


if __name__ == "__main__":
    r = requests.get(url)
    data = fromstring(r.text)
    script = data.xpath(f"//*[contains(text(), '{var}')]//text()")[0]
    script = script.split(var)[-1].strip().split(";")[0].strip()
    json_data = json.loads(script)

    results = {}
    for elem in json_data:
        name = elem["name"].lower().split("5g")[0].replace("+", " plus ")
        name = name.replace("  ", " ").split("(")[0].strip()
        image = elem["image"]
        selfie = elem.get("selfie", {}).get("score", None)
        audio = elem.get("audio", {}).get("score", None)
        mobile = elem.get("mobile", {}).get("score", None)
        display = elem.get("display", {}).get("score", None)
        battery = elem.get("battery", {}).get("score", None)
        result = {
            "selfie": selfie,
            "audio": audio,
            "mobile": mobile,
            "display": display,
            "battery": battery,
            "image": image
        }
        results[name] = result
    results = dict(sorted(results.items()))
    # return results
    with open("flask-backend/specs.json", "w") as f:
        f.write(json.dumps(results, indent=4))