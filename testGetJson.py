import csv
import json

with open('./cd-json.csv') as f:
    reader = csv.reader(f)
    next(f, None)
    for row in reader:
        cdJson = row[1]
        cdJson = json.loads(cdJson)
        print(cdJson)
