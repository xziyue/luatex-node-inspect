import json

with open("../temp.json", "r") as infile:
    obj = json.load(infile)
   
with open("../temp.json", "w") as outfile:
    json.dump(obj, outfile, indent=2)
