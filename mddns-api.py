#!/usr/bin/python
import logging
import sys
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from dnszone import DnsZone

from mongodb_functions import *
u = UserFunctions()

dns_zone = DnsZone("mddns.local", "172.201.251.154")

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

api = Api(app)

DEBUG = True   # zet op False wanneer klaar met testen en troubleshooten

parser = reqparse.RequestParser()
parser.add_argument('subdomain')
parser.add_argument('ip')
parser.add_argument('code')
parser.add_argument('value')

class NewSubDomain(Resource):
    # Endpoint voor het toevoegen van een nieuwe subdomein.
    # Voorbeeld curl: http://192.168.1.158:5001/subdomain/new -H "Content-type: application/json" -d "{ \"subdomain\" : \"miro\", \"ip\" : \"1.1.1.1\" }" -X POST
    def post(self):
        args = parser.parse_args()
        if DEBUG:
            app.logger.warning(f"DEBUG: NewSubDomain.post() <- {args }")
        sub_domain = args['subdomain']
        ipv4 = args['ip']
        dns_zone.add_address(sub_domain, ipv4)
        return {'status': 'ok'}

class EditSubDomain(Resource):
    # Endpoint voor het verwijderen van een subdomein.
    # Voorbeeld curl: http://192.168.1.158:5001/subdomain/name/test1 -X DELETE
    def delete(self, fqdn):
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.delete(\"{fqdn}\")")
        dns_zone.clear_address(fqdn)
        return {'status': 'ok'}

    # Endpoint voor het bijwerken van een subdomein.
    # Voorbeeld curl: http://192.168.1.158:5001/subdomain/name/test1 -H "Content-type: application/json" -d "{ \"ip\" : \"1.1.1.1\" }" -X PUT
    def put(self, fqdn):
        args = parser.parse_args()
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.put(\"{fqdn}\") <- {args }")
        ipv4 = args['ip']
        update_result = dns_zone.update_address(fqdn, ipv4)
        return {'status': 'ok'}

    # Endpoint voor het ophalen van details van een subdomein.
    # Voorbeeld curl: http://192.168.1.158:5001/subdomain/name/test1
    def get(self, fqdn):
        if DEBUG:
            app.logger.warning(f"DEBUG: EditSubDomain.get(\"{fqdn}\")")
        domain_details = dns_zone.check_address(fqdn)
        return {domain_details}

# Definieer endpoints hieronder.
# Als een deel van de URL een variabele is, gebruik dan haakjes, bijvoorbeeld <fqdn>
api.add_resource(NewSubDomain, '/subdomain/new')
api.add_resource(EditSubDomain, '/subdomain/name/<fqdn>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
