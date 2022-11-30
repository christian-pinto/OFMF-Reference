#
# Copyright (c) 2017-2021, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor
# the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.

# Resource implementation for - /redfish/v1/AccountService/ExternalAccountProviders/{ExternalAccountProviderId}/Certificates/{CertificateId}
# Program name - Certificate3_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Certificate3 import get_Certificate3_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Certificate3 Collection API
class Certificate3CollectionAPI(Resource):
	def __init__(self):
		logging.info('Certificate3 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ExternalAccountProviderId):
		logging.info('Certificate3 Collection get called')
		path = os.path.join(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates', 'index.json').format(ExternalAccountProviderId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ExternalAccountProviderId):
		logging.info('Certificate3 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if ExternalAccountProviderId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates').format(ExternalAccountProviderId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Certificate', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Certificate3API.post(self, ExternalAccountProviderId, os.path.basename(config['@odata.id']))
			else:
				return Certificate3API.post(self, ExternalAccountProviderId, str(res))
		else:
			return Certificate3API.post(self, ExternalAccountProviderId, str(res))

	# HTTP PUT Collection
	def put(self, ExternalAccountProviderId):
		logging.info('Certificate3 Collection put called')

		path = os.path.join(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates', 'index.json').format(ExternalAccountProviderId)
		put_object (path)
		return self.get(ExternalAccountProviderId)

# Certificate3 API
class Certificate3API(Resource):
	def __init__(self):
		logging.info('Certificate3 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ExternalAccountProviderId, CertificateId):
		logging.info('Certificate3 get called')
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates/{1}', 'index.json').format(ExternalAccountProviderId, CertificateId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ExternalAccountProviderId, CertificateId):
		logging.info('Certificate3 post called')
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates/{1}').format(ExternalAccountProviderId, CertificateId)
		collection_path = os.path.join(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates', 'index.json').format(ExternalAccountProviderId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Certificate3CollectionAPI.post(self, ExternalAccountProviderId)

		if CertificateId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ExternalAccountProviderId':ExternalAccountProviderId, 'CertificateId':CertificateId, 'rb':g.rest_base}
			config=get_Certificate3_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Certificate3API POST exit')
		return resp

	# HTTP PUT
	def put(self, ExternalAccountProviderId, CertificateId):
		logging.info('Certificate3 put called')
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates/{1}', 'index.json').format(ExternalAccountProviderId, CertificateId)
		put_object(path)
		return self.get(ExternalAccountProviderId, CertificateId)

	# HTTP PATCH
	def patch(self, ExternalAccountProviderId, CertificateId):
		logging.info('Certificate3 patch called')
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates/{1}', 'index.json').format(ExternalAccountProviderId, CertificateId)
		patch_object(path)
		return self.get(ExternalAccountProviderId, CertificateId)

	# HTTP DELETE
	def delete(self, ExternalAccountProviderId, CertificateId):
		logging.info('Certificate3 delete called')
		path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates/{1}').format(ExternalAccountProviderId, CertificateId)
		base_path = create_path(self.root, 'AccountService/ExternalAccountProviders/{0}/Certificates').format(ExternalAccountProviderId)
		return delete_object(path, base_path)

