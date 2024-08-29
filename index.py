import re

brands = [
    "apple", "xiaomi", "samsung", "google", "motorola"
]
phoness = {
    "samsung": {
        "galaxy s24 ultra", "galaxy s24 plus", "galaxy s24",
        "galaxy s23 ultra", "galaxy s23 plus", "galaxy s23",
        "galaxy s22 ultra", "galaxy s22 plus", "galaxy s22",
        "galaxy s21 ultra", "galaxy s21 plus", "galaxy s21",
        "note 20 ultra", "note 20", "note 10 plus", "note 10",

        # a
        "galaxy a14", "galaxy a33", "galaxy a04",
        "galaxy a15", "galaxy a25", "galaxy a35", "galaxy a45", "galaxy a55",
        "galaxy a54", "galaxy a53", "galaxy a52", "galaxy a51",

        # z fold
        "galaxy z fold 5", "galaxy z fold 4", "galaxy z fold 3",
        "galaxy z fold 6",

        # z flip
        "galaxy z flip 5", "galaxy z flip 4", "galaxy z flip 3",

        # tab
        "galaxy tab s9", "galaxy tab s8 ultra", "galaxy tab s8",
        "galaxy j8", "galaxy j7", "galaxy j6",
        "galaxy m54", "galaxy m53", "galaxy m52",
        "galaxy f41", "galaxy f62"
    },
    "google": {
        "pixel 9",
        "pixel 9 pro",
        "pixel 9 xl",
        "pixel 9 a",
        "pixel 8",
        "pixel 8 pro",
        "pixel 8 xl",
        "pixel 7a",
        "pixel 7",
        "pixel 7 pro",
        "pixel 7 xl",
        "pixel 6a",
        "pixel 6",
        "pixel 6 pro",
        "pixel 6 xl",
        "nexus 5x",
    }
}

phones = {
    "samsung": [
        "galaxy s24 ultra",
        "galaxy s24+",
        "galaxy s24",
        "galaxy z fold5",
        "galaxy z flip5",
        "galaxy a54 5g",
        "galaxy a34 5g",
        "galaxy a14"
    ],
    "apple": [
        "iphone 15 pro max",
        "iphone 15 pro",
        "iphone 15 plus",
        "iphone 15",
        "iphone 14 pro max",
        "iphone 14 pro",
        "iphone 14 plus",
        "iphone 14",
        "iphone se (3rd generation)"
    ],
    "google": [
        "pixel 8 pro",
        "pixel 8",
        "pixel 7a",
        "pixel fold",
        "pixel 7 pro",
        "pixel 7",
        "pixel 6a"
    ],
    "xiaomi": [
        "xiaomi 13 ultra",
        "xiaomi 13 pro",
        "xiaomi 13",
        "redmi note 12 pro+",
        "redmi note 12 pro",
        "redmi note 12",
        "poco f5 pro",
        "poco x5 pro",
        "mi 11 ultra"
    ],
    "motorola": [
        "moto edge 40 pro",
        "moto edge 30 ultra",
        "moto g stylus 5g (2023)",
        "moto g power (2023)",
        "moto g play (2023)",
        "moto g pure",
        "moto razr+ (2023)",
        "moto edge 20"
    ]
}


def get_brand(ar):
    vals = ar.split()
    while vals:
        var = vals.pop(0)
        if var not in phoness:
            continue
        else:
            return var
    return None


def get_model(ar, brand):
    result = ""
    for model in phoness[brand]:
        if model.replace(" ", "") in ar.replace(" ", ""):
            if len(model) > len(result):
                result = model
    return None if result == "" else result


def get_ram(ar):
    pattern = r"(\d{1,3})gb\s*ram"
    match = re.search(pattern, ar)
    if match:
        ram = match.group(1)
        ram_str = "gb ram"
        try:
            start = ar.index(str(ram) + ram_str)
        except ValueError:
            return None, None
        length = len(str(ram) + ram_str)
        return start, length
    return None, None

def get_memory(ar):
    pattern = r"(\d{1,3})(tb|gb)"

    match = re.search(pattern, ar)
    if match:

        mem = match.group(1)
        if int(mem) > 5:
            mem_str = "gb"
        else:
            mem_str = "tb"
        try:
            start = ar.index(str(mem) + mem_str)
        except ValueError:
            return None, None, None

        length = len(str(mem) + mem_str)
        return start, length, mem_str
    # else
    return None, None, None






    # match = re.search(pattern, str_arg)
    # if match:
    #     memory = match.group(1)
    #     index = str_arg.index(memory)
    #     str_arg = str_arg[:index] + str_arg[index + len(memory) + 2 + 1:]
    # else:
    #     memory = 0
    # pass

def get_dual_sim(ar):
    args = [
        "dual (sim+sim)",
        "dual sim",
    ]
    for arg in args:
        if arg in ar:
            index = ar.index(arg)
            return index, len(arg)
    return None, None


def get_connectivity(ar):
    pos = None
    lng = 2
    try:
        pos = ar.index(" 5g ")
    except ValueError:
        if ar.startswith("5g"):
            pos = 0
        elif ar.endswith("5g"):
            pos = len(ar) - len("5g") - 1
    else:
        lng += 1
    return pos, lng

def get_color(ar):
    return ar.strip()

def gett(arg):
    name, url = arg
    name = name.replace(",", "").lower().strip()
    brand = get_brand(name)
    data = {"url": url}
    if brand:
        data["brand"] = brand

        name = " ".join(name.split(brand)[1:]).strip()

        model = get_model(name, brand)
        data["model"] = model
        if model:
            index = 0
            index_str = 0
            model_no_space = model.replace(" ", "")
            # remove cases like galaxy fold6
            while index < len(model_no_space):
                if model_no_space[index] != name[index_str]:
                    break
                index_str += 1
                index += 1
                if name[index_str] == ' ':
                    index_str += 1

            name = name[index_str:].strip()

        start, length = get_ram(name)
        ram = None
        if start:
            ram = name[start: start + length].split("gb")[0]
            name = name[:start] + name[start + length:].strip()
        data["ram"] = ram

        start, length = get_dual_sim(name)
        dual_sim = False
        if start is not None:
            dual_sim = True
            name = name[:start] + name[start + length:].strip()
        data["dual_sim"] = dual_sim

        start, length, mem_type = get_memory(name)
        mem = None
        if start is not None:
            mem = name[start: start + length].split(mem_type)[0]
            name = name[:start] + name[start + length:].strip()
        data["memory"] = mem

        start, length = get_connectivity(name)
        f_g = False
        if start is not None:
            f_g = True
            name = name[:start] + name[start + length:].strip()
        data["connectivity"] = f_g

        color = get_color(name)
        color = color if color else None
        data["color"] = color
        return data

    return {}


