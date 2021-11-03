import json

jsonshit = None

with open("/Users/edcarron/code/journo_play/firstTranscript.txt") as f:
    jsonshit = f.read()

jsonshit = jsonshit.replace('93', '')
jsonshit = jsonshit.replace('94', '')
jsonshit = jsonshit.replace('/', '')
jsonshit = jsonshit.replace('[', '')
jsonshit = jsonshit.replace(']', '')
jsonshit = jsonshit.replace('\\', '')
jsonshit = jsonshit.replace('\'', '')
jsonshit = jsonshit.replace(',', '')

splitObjs = jsonshit.split("{")

splitsplit = [x.splitlines() for x in splitObjs]

jsongood = []

for exercise in splitsplit[2:]:

    title = ''
    lines = []

    for line in exercise:
        if 'title' in line:
            title = line
            continue

        lines.append(line.strip())

    jsongood.append({"title": title,
                     "text": lines})

splitsplit

with open('/Users/edcarron/CSharpProjects/literacyToolBox/literacyToolBox/Properties/transcripts/EmptyJSONFile.json', 'w+') as f:
    # this would place the entire output on one line
    # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
    json.dump(jsongood, f)