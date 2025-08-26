import urllib.request, json, re
import requests
from urllib.parse import quote

def remove_nested_blocks(text, start, end):
    result = []
    depth = 0
    i = 0
    while i < len(text):
        if text[i:i+len(start)] == start:
            depth += 1
            i += len(start)
            continue
        if text[i:i+len(end)] == end and depth > 0:
            depth -= 1
            i += len(end)
            continue
        if depth == 0:
            result.append(text[i])
        i += 1
    return ''.join(result)
    
def italicize_nested_blocks(text, start="{{", end="}}"):
    result = []
    buffer = []
    depth = 0
    skipping = False
    i = 0

    while i < len(text):
        if text[i:i+len(start)] == start:
            if depth == 0:
                buffer = []
                skipping = False
            depth += 1
            i += len(start)

            if depth == 1 and (text[i:i+len("օրինակ")] == "օրինակ" or text[i:i+len("օրն")] == "օրն" or text[i:i+len("Հեղինակ")] == "Հեղինակ"):
                skipping = True
            continue

        if text[i:i+len(end)] == end and depth > 0:
            depth -= 1
            i += len(end)
            if depth == 0:
                if not skipping:
                    result.append("<i>" + ''.join(buffer) + "</i>")
            continue

        if depth > 0:
            buffer.append(text[i])
        else:
            result.append(text[i])
        i += 1

    return ''.join(result)

def checkexp(text, exp):
    return bool(re.match(fr"^=+\s*{exp}\s*=+$", text))

def remove_all_expressions_blocks(text):
    lines = text.splitlines()
    result = []
    skipping = False

    for line in lines:
        if checkexp(line.strip(), "Արտահայտություններ") or checkexp(line.strip(), "Աղբյուրներ") or checkexp(line.strip(), "Խոնարհում"):
            skipping = True
            continue
        if skipping and line.startswith("="):
            skipping = False
        if not skipping:
            result.append(line)

    return "\n".join(result)

def getDefs(word):
    if word == 'պոծոկ':
        return {"Վիիիի աղջիիի": ['Դուք մտաք "Պոծոկ" գաղտնի ակումբ']}

    res = {
        "Գոյական": [],
        "Ածական": [],
        "Բայ": [],
        "Շաղկապ": [],
        "Վերաբերական": [],
        "Թվական": [],
        "Դերանուն": [],
        "Մակբայ": [],
        "Կապ": [],
        "Ձայնարկություն": [],
        "Բացատրություն": [],
        "Հատուկ անուն": [],
        "Անգլերեն": [],
        "Ռուսերեն": []
    }
    mas = ""

    url = ("https://hy.wiktionary.org/w/api.php?"
           f"format=json&action=query&titles={quote(word)}"
           "&rvprop=content&prop=revisions&redirects=1")

    r = requests.get(url, headers={
        "User-Agent": "Barayinbot (https://t.me/barayinbot)"
    })
    r.raise_for_status()
    data = r.json()
    data = str(data).replace('\\n', '\n')

    # data = remove_nested_blocks(data, "{{", "}}")
    # data = remove_nested_blocks(data, "[[", "]]")

    data = remove_all_expressions_blocks(data)


    for line in data.splitlines():
        header = re.findall(r"^=+\s*(.*?)\s*=+$", line)

        if header:
            header = header[0]
            if header in res:
                mas = header
        else:
            if "-ած-" in line:
                mas = "Ածական"
            elif "-գո-" in line:
                mas = "Գոյական"
            elif "-շաղ-" in line:
                mas = "Շաղկապ"
            elif "-եղբ-" in line:
                mas = "Վերաբերական"
            elif "-թվ-" in line:
                mas = "Թվական"
            elif "-դեր-" in line:
                mas = "Դերանուն"
            elif "-բայ-" in line:
                mas = "Բայ"
            elif "-մակ-" in line:
                mas = "Մակբայ"
            elif "-կապ-" in line:
                mas = "Կապ"
            elif "-ձա-" in line:
                mas = "Ձայնարկություն"
            elif "-բաց-" in line:
                mas = "Բացատրություն"
            elif "-հատ-" in line:
                mas = "Հատուկ անուն"
            elif "-en-" in line:
                mas = "Անգլերեն"
            elif "-ru-" in line:
                mas = "Ռուսերեն"

        if line.startswith('# ') or line.startswith('* '):
            # print(line)
            line = line.replace('# ', '')
            line = line.replace('* ', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('|', ' ')
            line = line.replace("'}}}}}", '')
            # line = remove_nested_blocks(line, "{{", "}}")
            # line = remove_nested_blocks(line, "[[", "]]")
            line = italicize_nested_blocks(line)
            # print(line)
            if line != '':
                line = line.strip()
                try:
                    res[mas].append(line)
                except KeyError:
                    continue

    return res

print(getDefs("բասկերեն"))