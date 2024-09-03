from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json
from flask import Flask, request, jsonify
import sys
from pathlib import Path

sys.path.append('../')
import search
import crawlers_parse_python
import atexit

app = Flask(__name__)
CORS(app)


# Load phone data from JSON file
def load_phone_data():
    with open("phones.json") as f:
        phones = json.load(f)
    return phones


# API endpoint to get phone data
@app.route("/api/phones", methods=["GET"])
def get_phones():
    brand = request.args.get('brand')
    color = request.args.get('color')
    phones_data = load_phone_data()
    # Filter phones based on query parameters
    filtered_phones = [phone for phone in phones_data if
                       (brand is None or phone['brand'] == brand) and (
                               color is None or phone['color'] == color)]

    return jsonify(filtered_phones)


@app.route("/search/")
def search_ph():
    phones_data = load_phone_data()
    brands = list(set([b["brand"].title() for b in phones_data]))
    models = list(set([b["model"].title() for b in phones_data if b["model"]]))
    memory = list(set(
        [int(b["memory"]) for b in phones_data if b["memory"]]))
    ram = list(set([int(b["ram"]) for b in phones_data if b["ram"]]))
    return render_template(
        "phones.html",
        brands=sorted(brands),
        models=sorted(models),
        memory=sorted(memory),
        ram=sorted(ram),
    )


@app.route('/go_data', methods=['POST'])
def go_data():
    # Process form data here
    data = request.form
    filters = {k: v for k, v in data.items() if v.strip()}
    qry = filters.get("brand", "") + " " + filters.get("model", "")
    qry = qry.strip().lower()

    with open("specs.json", "r") as f:
        phones_specs = json.loads(f.read())
    try:
        specs = phones_specs[qry]
    except KeyError:
        specs = None
    else:
        specs["name"] = qry.title()
    #
    elements = []
    phones_data = load_phone_data()
    links = []
    # print(filters)
    for phone in phones_data:
        keys = list(phone.keys())
        total_filters = len(filters)
        for key in keys:
            if key in filters:
                if phone[key] and filters[key].lower() == phone[key].lower():
                    total_filters -= 1
        # print(total_filters)
        if total_filters == 0:
            links.append(phone['url'])
    print(links)
    results = search.get_prices(links)
    # with open("data2.json", "r") as f:
    #     results = json.loads(f.read())

    return render_template("show_data.html",
                           results=results,
                           specs=specs)


def on_exit():
    print("images deleted")
    folder = "static/images/"
    path = Path(folder)
    # Iterate over all files in the directory and its subdirectories
    for file_path in path.rglob('*'):
        if file_path.is_file():
            try:
                file_path.unlink()  # Delete the file
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")
                pass
    print("Images have ben deleted")


# Register the exit function
# atexit.register(on_exit)

if __name__ == "__main__":
    app.run(debug=True)
