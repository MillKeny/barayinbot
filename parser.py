import urllib.request, json, re
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

def remove_all_expressions_blocks(text):
    lines = text.splitlines()
    result = []
    skipping = False

    for line in lines:
        if line.strip() == "===== Արտահայտություններ =====":
            skipping = True
            continue
        if skipping and line.startswith("=") and line.strip() != "===== Արտահայտություններ =====":
            skipping = False  # Found end of block
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
        "Հատուկ անուն": []
    }
    mas = ""

    with urllib.request.urlopen("https://hy.wiktionary.org/w/api.php?format=json&action=query&titles=" + quote(word) + "&rvprop=content&prop=revisions&redirects=1") as url:
        data = json.load(url)
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
                if "-hy-ած-" in line:
                    mas = "Ածական"
                elif "-hy-գո-" in line:
                    mas = "Գոյական"
                elif "-hy-շաղ-" in line:
                    mas = "Շաղկապ"
                elif "-hy-եղբ-" in line:
                    mas = "Վերաբերական"
                elif "-hy-թվ-" in line:
                    mas = "Թվական"
                elif "-hy-դեր-" in line:
                    mas = "Դերանուն"
                elif "-hy-բայ-" in line:
                    mas = "Բայ"
                elif "-hy-մակ-" in line:
                    mas = "Մակբայ"
                elif "-hy-կապ-" in line:
                    mas = "Կապ"
                elif "-hy-ձա-" in line:
                    mas = "Ձայնարկություն"
                elif "-hy-բաց-" in line:
                    mas = "Բացատրություն"
                elif "-hy-հատ-" in line:
                    mas = "Հատուկ անուն"

            if line.startswith('# ') or line.startswith('* '):
                # print(line)
                line = line.replace('# ', '')
                line = line.replace('* ', '')
                line = line.replace('[', '')
                line = line.replace(']', '')
                line = remove_nested_blocks(line, "{{", "}}")
                # line = remove_nested_blocks(line, "[[", "]]")
                if not bool(re.fullmatch(r"[a-zA-Z]+", line)) and line != '':
                    line = line.strip()
                    if bool(re.fullmatch(r"[ա-ֆԱ-Ֆ]+", line[0])):
                        try:
                            res[mas].append(line)
                        except KeyError:
                            continue

    return res

# print(getDefs("դուռ"))