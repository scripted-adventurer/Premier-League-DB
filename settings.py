import os

database = {
 'host': os.environ['PLDB_HOST'],   # default is 'localhost',
 'port': int(os.environ['PLDB_PORT']),   # default is 27017
 'user': os.environ['PLDB_USER'],
 'password': os.environ['PLDB_PASSWORD'],
 'db': os.environ['PLDB_DB']
}