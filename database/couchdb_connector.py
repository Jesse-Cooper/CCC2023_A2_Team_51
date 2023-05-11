import couchdb

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

    def put(self, doc):
        """
        Put document onto the couchdb datebase

        Parameters:
            doc: the doc to put
        """
        self.database.save(doc)
