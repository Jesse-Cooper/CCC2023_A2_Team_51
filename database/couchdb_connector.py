import couchdb
import json
import csv

USERNAME = "admin"
PASSWORD = "admin"
HOST = "172.26.136.58"
PORT = "5984"
DATABASE = "twitter"

class Connector:

    def __init__(self, username=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE):
        """
        Connector initialization

        Parameters:
            username: couchdb username; default = "admin"
            password: couchdb password; default = "admin"
            host:     couchdb host ip address; default = "172.26.136.58"
            port:     couchdb port; default = "5984"
            database: couchdb database to connect; will create a new database if cannot find it;
                      default = "twitter"
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        self.server = couchdb.Server(f"http://{self.username}:{self.password}@{self.host}:{self.port}")
        
        try:
            self.database = self.server[database]
        except:
            self.database = self.server.create(database)

    def _put_doc(self, doc):
        self.database.save(doc)

    def _put_docs(self, docs):
        for doc in docs:
            self._put_doc(doc)

    def put(self, doc):
        """
        Put document onto the couchdb datebase

        Parameters:
            doc: the doc to put
        """
        if isinstance(doc, dict):
            self._put_doc(doc)
            return
        
        if isinstance(doc, list):
            self._put_docs(doc)
            return

        if isinstance(doc, str):

            if doc.split('.')[-1] == "json":
                with open(doc, "r") as file:
                    doc_json = json.load(file)
                self.put(doc_json)
                return
    
            if doc.split('.')[-1] == "csv":
                with open(doc, "r") as file:
                    rows = csv.DictReader(file)
                    for row in rows:
                        self._put_doc(row)
                return
