import csv
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 '
    'Safari/537.36'}


def checkAlive(uri):
    try:
        resp = requests.get(uri, stream=False,
                            allow_redirects=True, headers=headers, timeout=20)

        resp.status_code
        return resp.status_code
    except Exception as e:
        print("Failed with error:")
        print(e)
        return 404


def getStatus(fileName):
    with open(fileName) as f, open('dataset-new2.csv', 'w') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        writer.writerow(["uri", "status_code"])
        for row in reader:
            uri = row[0]
            statusCode = checkAlive(uri)
            print(uri)
            print(str(statusCode) + "\n")
            writer.writerow([uri, statusCode])


if __name__ == "__main__":
    getStatus('./dataset.csv')
