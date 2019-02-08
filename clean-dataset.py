import csv
from datetime import datetime


def beforeArchiveDate(date):
    ''' Check if date younger than 1995-01-01T12:00:00
        input format: 2012-06-06
    '''
    try:
        d1 = datetime.strptime(date, '%Y-%m-%d').date()
        d2 = datetime.strptime("1995-01-01T12:00:00",
                               '%Y-%m-%dT%H:%M:%S').date()
        if d1 < d2:
            return True

        return False
    except Exception:
        return True


def parseCSV(filename):
    ''' Open csv and parse
    '''
    with open(filename, 'r') as f, \
            open('./data/dataset-beforearchive.csv', 'w') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        for row in reader:
            if beforeArchiveDate(row[1]):
                writer.writerow(row)


if __name__ == "__main__":
    parseCSV("./data/dataset-cleaned.csv")
