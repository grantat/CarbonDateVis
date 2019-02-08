import csv
import json
import datetime


def enforceDateFormat(date):
    # same format but when returns '01' for january instead of '1'
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    newDate = datetime.date.strftime(dt, "%Y-%m-%d")
    return newDate


def stripDate(date):
    dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    newDate = datetime.date.strftime(dt, "%Y-%m-%d")
    return newDate


def cdGetJson():
    with open('./data/cd-json.csv', 'r') as f, open('./data/dataset.csv', 'r') as orig, \
            open('./data/date-compare.csv', 'w') as out:
        reader = csv.reader(f)
        origReader = csv.reader(orig)
        writer = csv.writer(out)
        next(f, None)

        writer.writerow(["URI", "dataset-date", "carbondate-date"])
        for row in reader:
            cdJson = row[1]
            # loads a string first, then a dictionary....
            cdJson = json.loads(json.loads(cdJson))
            uri = cdJson["URI"]
            for j in origReader:
                ouri = j[0]
                # print(ouri, "vs", uri)
                if(uri == ouri):
                    origDate = enforceDateFormat(j[1])
                    cdDate = stripDate(cdJson["Estimated Creation Date"])
                    print(origDate, "vs", cdDate)
                    continue
            # writer.writerow(fields)


if __name__ == "__main__":
    cdGetJson()
