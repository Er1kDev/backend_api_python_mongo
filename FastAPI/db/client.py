# Gestion conexion a la base de datos mongodb

from pymongo import MongoClient

# Conexion a la base de datos local
# db_client = MongoClient().local

# Base de datos Remota

db_client = MongoClient(
    "mongodb+srv://erikdev:felipex64@cluster0.xf1hvua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
).test
