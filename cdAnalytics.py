from __future__ import print_function
import csv
import json
from datetime import datetime
from pprint import pprint
import numpy as np
from scipy.integrate import simps
from numpy import trapz


def daysFromToday(date):
    # ran on Thursday, August 17, 2017
    try:
        date_format = "%Y-%m-%d"
        # a = datetime.today()
        a = datetime.strptime("2012-08-17", "%Y-%m-%d")
        b = datetime.strptime(date, date_format)
        delta = b - a
        return delta.days
    except Exception:
        return 0


def modDateFormat(date):
    # 2012-06-06T13:37:19 to 2012-06-06
    try:
        newDate = datetime.strptime(
            date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        return newDate
    except Exception:
        return date


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
    with open('./data/cd-json2.csv', 'r') as f, open('./data/cd-stats2.csv', 'w') as out:
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


def mergeDates():
    with open('./data/dataset-cleaned.csv', 'r') as f, \
            open('./data/cd-json2.csv', 'r') as f2, \
            open('./data/cd-dataset-merge.csv', 'w') as out:

        r1 = csv.reader(f)
        r2 = csv.reader(f2)
        writer = csv.writer(out)

        writer.writerow(["URI", "Actual Creation Date", "Actual Age",
                         "Estimated Creation Date", "Estimated Age",
                         "EstimatedFormatted",
                         "Archives",
                         "Twitter.com",
                         "Bitly.com",
                         "Backlinks",
                         "Bing.com",
                         "Last Modified",
                         "Google.com",
                         "Pubdate tag"
                         ])
        for row in r1:
            uri = row[0]
            date = row[1]
            for j in r2:
                uri2 = j[0]
                if uri == uri2:
                    cdJson = j[1]
                    # loads a string first, then a dictionary....
                    cdJson = json.loads(json.loads(cdJson))
                    # print(cdJson)
                    actAge = abs(daysFromToday(date))
                    estDate = modDateFormat(
                        cdJson["Estimated Creation Date"].strip())
                    estAge = abs(daysFromToday(estDate))
                    writer.writerow([uri, date, actAge, estDate, estAge,
                                     cdJson["Estimated Creation Date"],
                                     cdJson["Archives"]["Earliest"],
                                     cdJson["Twitter.com"],
                                     cdJson["Bitly.com"],
                                     cdJson["Backlinks"],
                                     cdJson["Bing.com"],
                                     cdJson["Last Modified"],
                                     cdJson["Google.com"],
                                     cdJson["Pubdate tag"]])
                    break


def findContributions():
    services = ["Archives",
                "Twitter.com",
                "Bitly.com",
                "Backlinks",
                "Bing.com",
                "Last Modified",
                "Google.com",
                "Pubdate tag"]
    sums = {}
    for i in services:
        sums[i] = {}
        sums[i]["best-estimate"] = 0
        sums[i]["contributions"] = 0
        sums[i]["auc"] = 0.0
        sums[i]["ages"] = []

    with open('./data/cd-dataset-merge.csv') as f:
        reader = csv.reader(f)
        next(f, None)

        for row in reader:
            estDate = row[5]

            # skip rows with no estimation
            if row[3] is "":
                continue

            for j in range(6, 14):
                serviceDate = row[j].strip()
                if estDate == serviceDate:
                    # print(estDate + " vs " + serviceDate)
                    sums[services[j - 6]]["best-estimate"] += 1
                    sums[services[j - 6]]["contributions"] += 1
                    sums[services[j - 6]
                         ]["ages"].append(abs(daysFromToday(modDateFormat(serviceDate))))
                    break
                elif len(serviceDate) > 0:
                    sums[services[j - 6]]["contributions"] += 1
                    sums[services[j - 6]
                         ]["ages"].append(abs(daysFromToday(modDateFormat(serviceDate))))

        for key in sums:
            if len(sums[key]["ages"]) > 0:
                sums[key]["auc"] = calculateAUC(sums[key]["ages"])
            sums[key].pop("ages", None)
        pprint(sums, indent=4)


def calculateAUC(arr):
    # The y values.  A numpy array is used here,
    # but a python list could also be used.
    y = np.array(arr)

    # Compute the area using the composite trapezoidal rule.
    area1 = trapz(y, dx=0.0001)
    # print("area =", area1)

    # Compute the area using the composite Simpson's rule.
    area2 = simps(y, dx=0.0001)
    # print("area =", area2)

    avg = (area1 + area2) / 2
    print("avg = ", avg)

    return avg


def fixActualDates():
    # make estimated dates that are older than the original the original dates
    # cd-dataset-merge-fixed.csv
    with open('./data/cd-dataset-merge.csv', 'r') as f1, \
            open('./data/cd-dataset-merge-fixed.csv', 'w') as f2:
        reader = csv.reader(f1)
        writer = csv.writer(f2)
        counter = 0
        foundEquals = 0
        for i, row in enumerate(reader):
            if i == 0:
                writer.writerow(row)
                continue
            temp = row
            if len(row[3]) > 0:
                estimatedAge = int(row[4].strip())
                actualAge = int(row[2].strip())
                if estimatedAge > actualAge:
                    temp[1] = row[3]
                    temp[2] = estimatedAge
                    print(actualAge, "vs", estimatedAge)
                if estimatedAge == int(temp[2]):
                    foundEquals += 1
                counter += 1
            writer.writerow(temp)
        print("total rows with estimated age=", counter)
        print("Pairs found equal", foundEquals)


if __name__ == "__main__":
    cdGetJson()
    mergeDates()
    findContributions()
    fixActualDates()
