from pymongo import MongoClient
import gridfs
import os
from dotenv import load_dotenv

# Kết nối với MongoDB Atlas
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(
    mongodb_uri,
    tls=True,
    tlsAllowInvalidCertificates=True,
    retryWrites=True
)

# Truy cập vào database và collection
db = client["db_iot"]

fs = gridfs.GridFS(db)

collection_relay = db["relay"]  # Sensor collection
collection_sensor = db["sensor"]  # Sensor collection
collection_user = db["users"]  # User collection