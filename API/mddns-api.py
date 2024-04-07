#!/usr/bin/python
import logging
import sys
import json
from flask import Flask, request, abort
from flask_restful import reqparse, Api, Resource
from dnszone import DnsZone

domain_name = "mddns.local"
dns_zone = DnsZone(domain_name, "172.201.251.154")

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

api = Api(app)

DEBUG = True   # zet op False wanneer klaar met testen en troubleshooten

parser = reqparse.RequestParser()
parser.add_argument('subdomain')
parser.add_argument('ip')
parser.add_argument('code')
parser.add_argument('value')


# Haal de api keys op uit het bestand
with open('api_keys.json', 'r') as f:
    VALID_API_KEYS = json.load(f)


# Valideer de opgegeven API keys
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key in VALID_API_KEYS:
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
        if DEBUG:
            app.logger.warning(f"DEBUG: NewSubDomain.post() <- {args }")
        subdomain = args['subdomain']
        fqdn = f"{subdomain}.{domain_name}"
        ipv4 = args['ip']
        dns_zone.add_address(fqdn, ipv4)
        return {'status': 'ok'}

class EditSubDomain(Resource):
    # Endpoint voor het verwijderen van een subdomein.
    # Voorbeeld curl -X DELETE https://<ip_of_server>:<port>/subdomain/name/test -H "X-API-Key: your_api_key"
    @require_api_key
    def delete(self, sub_domain):
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.delete(\"{sub_domain}\")")
        fqdn = f"{sub_domain}.{domain_name}"
        dns_zone.clear_address(fqdn)
        return {'status': 'ok'}

    # Endpoint voor het bijwerken van een subdomein.
    # Voorbeeld curl -X PUT https://<ip_of_server>:<port>/subdomain/name/test -H "Content-type: application/json" -H "X-API-Key: your_api_key" -d "{ \"ip\" : \"1.1.1.1\" }"
    @require_api_key
    def put(self, sub_domain):
        args = parser.parse_args()
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.put(\"{sub_domain}\") <- {args }")
        fqdn = f"{sub_domain}.{domain_name}"
        ipv4 = args['ip']
        update_result = dns_zone.update_address(fqdn, ipv4)
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
    app.run(debug=True, host='0.0.0.0', port=80)
