from pymongo import MongoClient
import gridfs
import os
from dotenv import load_dotenv
import sys
from Adafruit_IO import MQTTClient


mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(
    mongodb_uri,
)

AIO_USERNAME = os.getenv("ADAFRUIT_AIO_USERNAME")
AIO_KEY = os.getenv("ADAFRUIT_AIO_KEY")

db = client["db_iot"]

fs = gridfs.GridFS(db)

collection_relay = db["relay"]  
collection_sensor = db["sensor"]  
collection_user = db["users"]  
collection_relay_history = db["relay_history"]

def connected(client):
    print("Ket noi thanh cong ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def publish_to_adafruit(feed, value):
    print("Ket noi voi adafruit ...")
    client.publish(feed, value)