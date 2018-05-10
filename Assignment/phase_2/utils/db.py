from pymongo import MongoClient


class Mongo:
    def __init__(self, default_db="test"):
        """
        Mongo DB connection pool
        Configuration DFUNC_MONGO_URL: (default) mongodb://localhost:27017/
            (link: https://docs.mongodb.com/manual/reference/connection-string/)
        """
        self.mongo_cli = MongoClient()
        self.default_db = default_db

    def get_database(self, db=None, collection=None):
        """
        Function to get a specific DB or Collection
        :param db: Database name
        :param collection: Collection name
        :return: Returns cursor of the DB or collection
        """
        db = db or self.default_db
        if collection is None:
            return self.mongo_cli[db]
        else:
            return self.mongo_cli[db][collection]

    def close(self):
        """
        Closes Mongo Connection
        :return:
        """
        self.mongo_cli.close()
