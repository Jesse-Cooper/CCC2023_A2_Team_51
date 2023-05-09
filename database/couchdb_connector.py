import couchdb

USERNAME = "admin"
PASSWORD = "admin"
HOST = "172.26.136.58"
PORT = "5984"
DATABASE = "twitter"

class Connector:

    def __init__(self, username=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        self.server = couchdb.Server(f"http://{self.username}:{self.password}@{self.host}:{self.port}")
        
        try:
            self.database = self.server[database]
        except:
            self.database = self.server.create(database)

    def put(self, doc):
        self.database.save(doc)
