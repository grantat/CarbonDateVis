import csv
import json
import requests
import os


def getCDJson(uri):
    try:
        carbonDateURI = "http://localhost:8888/cd?url=" + uri
        resp = requests.get(carbonDateURI, stream=True, allow_redirects=True,
                            headers={'User-Agent': 'Mozilla/5.0'})

        if resp.status_code == 200:
            # count through json arr
            print(resp.text)

            resp.text
            return resp.text
        else:
            return resp.text

    except KeyboardInterrupt:
        print()
        exit()
    except Exception as e:
        print("Failed with exception:")
        print(e)
        exit()


def setWriteType(fileName):
    if os.path.isfile(fileName):
        return 'a'
    else:
        return 'w'


def findLastUriWritten(outFile):
    with open(outFile, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        count = len(data)
        print(count)
        print(data[count - 1])
        if count > 1:
            row = data[count - 1]
            uri = row[0]
            return uri
        else:
            # err
            exit()


def checkDataset(fileName):
    outFile = './data/cd-json2.csv'
    writeType = setWriteType(outFile)
    with open(fileName) as f, open(outFile, writeType) as out:
        reader = csv.reader(f)
        writer = csv.writer(out)

        i = 1
        if writeType == 'a':
            # continue past last uri written
            lastUri = findLastUriWritten(outFile)
            canStart = False
            for row in reader:
                uri = row[0]
                if canStart:
                    cdJson = getCDJson(uri)
                    print(i)
                    print(uri)
                    outJson = json.dumps(cdJson, indent=4, sort_keys=False)
                    writer.writerow([uri, outJson])
                if uri == lastUri:
                    canStart = True

                i += 1
        else:
            writer.writerow(["uri", "carbondate_json"])
            for row in reader:
                uri = row[0]
                cdJson = getCDJson(uri)
                print(i)
                print(uri)
                outJson = json.dumps(cdJson, indent=4, sort_keys=False)
                writer.writerow([uri, outJson])
                i += 1


if __name__ == "__main__":
    checkDataset('./data/dataset-cleaned.csv')
