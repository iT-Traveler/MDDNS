import json
import random
import string
import certifi
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def read_configuration(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config["mongodb_uri"]


mongodb_uri = read_configuration("webapp\mddns-gui-config.json")
ca = certifi.where()
mongo_client: MongoClient = MongoClient(mongodb_uri, tlsCAFile=ca)
# MongoDB database en collection
database: Database = mongo_client.get_database("mddns-database")
userCollection: Collection = database.get_collection("users")


def generate_api_key(length=32):
    """Generate a random API key."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def read_api_key_by_oauthkey(oauthkey):
    your_api_key = userCollection.find_one({'oauth-key': oauthkey})['api-key']
    return your_api_key


def check_user_exists_by_oauthkey(oauthkey, email):
    check_user = userCollection.find_one({'oauth-key': oauthkey})
    if not check_user:
        apikey = generate_api_key()
        userinfo = {'e-mail': email, 'api-key': apikey, 'oauth-key': oauthkey}
        userCollection.insert_one(userinfo)
    return
