#!/usr/bin/python
import logging
import sys
from flask import Flask, request, abort
from flask_restful import reqparse, Api, Resource
from dnszone import DnsZone
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import certifi
import json
from datetime import datetime


def read_configuration(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config["mongodb_uri"]


# Configuratiebestand
config_file = "mddns-api-config.json"
mongodb_uri = read_configuration(config_file)

# MongoDB Atlas cluster
ca = certifi.where()
mongo_client: MongoClient = MongoClient(mongodb_uri, tlsCAFile=ca)

# MongoDB database en collection
database: Database = mongo_client.get_database("mddns-database")
userCollection: Collection = database.get_collection("users")
recordCollection: Collection = database.get_collection("records")

domain_name = "mddns.local"
dns_zone = DnsZone(domain_name, "172.201.251.154")

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

api = Api(app)

DEBUG = True  # zet op False wanneer klaar met testen en troubleshooten

parser = reqparse.RequestParser()
parser.add_argument('subdomain')
parser.add_argument('ip')
parser.add_argument('code')
parser.add_argument('value')


# Valideer de opgegeven API keys
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        valid_api_keys = userCollection.distinct("api-key")
        if api_key in valid_api_keys:
            return func(*args, **kwargs)
        else:
            abort(401, 'Unauthorized: Invalid API Key')

    return wrapper


class NewSubDomain(Resource):
    # Endpoint voor het toevoegen van een nieuw subdomein.
    # Voorbeeld curl -X POST https://<ip_of_server>:<port>/subdomain/new -H "Content-type: application/json" -H "X-API-Key: your_api_key" -d "{ \"subdomain\" : \"miro\", \"ip\" : \"1.1.1.1\" }"
    @require_api_key
    def post(self):
        args = parser.parse_args()
        api_key = request.headers.get('X-API-Key')
        if DEBUG:
            app.logger.warning(f"DEBUG: NewSubDomain.post() <- {args}")
        # Haal alle variabelen op
        subdomain = args['subdomain']
        fqdn = f"{subdomain}.{domain_name}"
        ipv4 = args['ip']
        timestamp = datetime.now()
        # CHECK of het record al bestaat
        check_exists = recordCollection.find_one({"subdomain": subdomain})
        if check_exists:
            abort(409, f"Record with subdomain {subdomain} already exists.")
        # Voeg het nieuwe record toe door middel van de dns_zone module
        dns_zone.add_address(fqdn, ipv4)
        # Schrijf het nieuwe record weg in de database
        record = {"api-key": api_key, "subdomain": subdomain, "ipv4": ipv4, "timestamp": timestamp}
        recordCollection.insert_one(record)
        return {'status': 'ok'}


class EditSubDomain(Resource):
    # Endpoint voor het verwijderen van een subdomein.
    # Voorbeeld curl -X DELETE https://<ip_of_server>:<port>/subdomain/name/test -H "X-API-Key: your_api_key"
    @require_api_key
    def delete(self, sub_domain):
        api_key = request.headers.get('X-API-Key')
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.delete(\"{sub_domain}\")")
        fqdn = f"{sub_domain}.{domain_name}"
        # Verwijder het record door middel van de dns_zone module
        dns_zone.clear_address(fqdn)
        # Verwijder het record uit de database
        recordCollection.delete_one({"subdomain": sub_domain})
        return {'status': 'ok'}

    # Endpoint voor het bijwerken van een subdomein.
    # Voorbeeld curl -X PUT https://<ip_of_server>:<port>/subdomain/name/test -H "Content-type: application/json" -H "X-API-Key: your_api_key" -d "{ \"ip\" : \"1.1.1.1\" }"
    @require_api_key
    def put(self, sub_domain):
        api_key = request.headers.get('X-API-Key')
        args = parser.parse_args()
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.put(\"{sub_domain}\") <- {args}")
        fqdn = f"{sub_domain}.{domain_name}"
        ipv4 = args['ip']
        timestamp = datetime.now()
        # Update het record door middel van de dns_zone module
        dns_zone.update_address(fqdn, ipv4)
        # Update het record in de database
        recordCollection.update_one({"subdomain": sub_domain},
                                    {"api-key": api_key, "subdomain": sub_domain, "ipv4": ipv4, "timestamp": timestamp})
        return {'status': 'ok'}

    # Endpoint voor het ophalen van details van een subdomein.
    # Voorbeeld curl https://<ip_of_server>:<port>/subdomain/name/test -H "X-API-Key: your_api_key"
    @require_api_key
    def get(self, sub_domain):
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.get(\"{sub_domain}\")")
        # Check the status of the A record for the sub_domain
        fqdn = f"{sub_domain}.{domain_name}"
        domain_details = dns_zone.check_address(fqdn)
        return domain_details


# Definieer endpoints hieronder.
# Als een deel van de URL een variabele is, gebruik dan haakjes, bijvoorbeeld <sub_domain>
api.add_resource(NewSubDomain, '/subdomain/new')
api.add_resource(EditSubDomain, '/subdomain/name/<sub_domain>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
