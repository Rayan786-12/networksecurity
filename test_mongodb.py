
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Rayanaipoweredml:Rayan786@cluster0.igyjh2r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tls=true"

# Create a new client and connect to the server
client = MongoClient(uri,tls=True)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)