import sys
import pymongo

uri = "mongodb+srv://holynekk:NJewUzbcrKI1ahAU@cluster0.4lqjrbr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
try:
    client = pymongo.MongoClient(uri)
    # return a friendly error if a URI error is thrown
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

# use a database named "myDatabase"
mongodb = client.cengMarketplace