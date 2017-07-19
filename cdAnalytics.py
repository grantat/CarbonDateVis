import csv
import json


def modDateFormat(date):
    print()


def checkNotEmpty(val):
    if len(val) > 1:
        return True
    else:
        return False


def parseJson(cdJson):
    # print(cdJson["Estimated Creation Date"])
    output = []
    output.append(cdJson["URI"])
    # for each key check if empty. URI should never be nil
    output.append(checkNotEmpty(cdJson["Estimated Creation Date"]))
    # check what is happening here
    try:
        output.append(checkNotEmpty(cdJson["Archives"]["Earliest"]))
    except:
        output.append(False)
    output.append(checkNotEmpty(cdJson["Twitter.com"]))
    output.append(checkNotEmpty(cdJson["Bitly.com"]))
    output.append(checkNotEmpty(cdJson["Backlinks"]))
    output.append(checkNotEmpty(cdJson["Bing.com"]))
    output.append(checkNotEmpty(cdJson["Last Modified"]))
    output.append(checkNotEmpty(cdJson["Google.com"]))
    output.append(checkNotEmpty(cdJson["Pubdate tag"]))

    return output


def cdGetJson():
    with open('./cd-json.csv', 'r') as f, open('./cd-stats.csv', 'w') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        next(f, None)
        writer.writerow(["URI", "Estimated Creation Date", "Archives",
                         "Twitter",
                         "Bitly", "Backlinks", "Bing", "Last Modified",
                         "Google", "Pubdate"])
        for row in reader:
            cdJson = row[1]
            # loads a string first, then a dictionary....
            cdJson = json.loads(json.loads(cdJson))
            fields = parseJson(cdJson)
            writer.writerow(fields)


if __name__ == "__main__":
    cdGetJson()
