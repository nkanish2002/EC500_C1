from pymongo import MongoClient, ASCENDING
from requests import get
from os.path import isfile


def get_json(url):
    req = get(url)
    if req.status_code == 200:
        return req.json()
    return None


def upload_data(db, collection, index, data):
    coll = db[collection]
    # coll.create_index(['code', ASCENDING], unique=True)
    coll.insert_many(data)
    return len(data)


def search(db, collection, query = {}):
    return db[collection].find(query)

def update(db, collection, data, params):
    for each in params:
        data[each] = params[each]
    return db[collection].save(data)

def main(url, mongo_str):
    mongo_db = "test_db"
    mongo_collection = "airports"
    index = "code"
    
    print("Connecting to Database")
    cli = MongoClient(mongo_str)
    db = cli[mongo_db]
    print("Fetching Data: HTTP GET\n%s" % url)
    data = get_json(url)

    print("Uploding data to db")
    upload_data(db, mongo_collection, index, data)

    print("Searching for row with column: value | 'code': 'AAL'")
    dat = search(db, mongo_collection, {"code": "AAL"})
    print("Found %s entries." % dat.count())
    if dat.count() > 0:
        print(dat[0])
        params = {
            "email": "eng@bu.edu",
            "phone": "8978979676"
        }
        print("Updating entry with data")
        print(params)
        update(db, mongo_collection, dat[0], params)
    
    print("Done, disconnecting")


if __name__ == "__main__":
    JSON_URL = "https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762"\
                "c09b519f40397e4c3e100b097d861f5588/airports.json"
    MONGO_STR = "mongodb://localhost:27017"
    main(JSON_URL, MONGO_STR)
