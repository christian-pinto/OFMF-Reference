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

# Resource implementation for - /redfish/v1/Systems/{SystemId}/FabricAdapters/{FabricAdapterId}/REQ-VCAT/{VCATEntryId}
# Program name - VCATEntry2_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import check_authentication, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, create_collection
from .templates.VCATEntry2 import get_VCATEntry2_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# VCATEntry2 Collection API
class VCATEntry2CollectionAPI(Resource):
	def __init__(self, **kwargs):
		logging.info('VCATEntry2 Collection init called')
		self.root = PATHS['Root']
		self.auth = kwargs['auth']

	# HTTP GET
	def get(self, SystemId, FabricAdapterId):
		logging.info('VCATEntry2 Collection get called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT', 'index.json').format(SystemId, FabricAdapterId)
			return get_json_data(path)
		else:
			return msg, code

	# HTTP POST Collection
	def post(self, SystemId, FabricAdapterId):
		logging.info('VCATEntry2 Collection post called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			if request.data:
				config = json.loads(request.data)
				if "@odata.type" in config:
					if "Collection" in config["@odata.type"]:
						return "Invalid data in POST body", 400

			if FabricAdapterId in members:
				resp = 404
				return resp
			path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT').format(SystemId, FabricAdapterId)
			parent_path = os.path.dirname(path)
			if not os.path.exists(path):
				os.mkdir(path)
				create_collection (path, 'VCATEntry', parent_path)

			res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			if request.data:
				config = json.loads(request.data)
				if "@odata.id" in config:
					return VCATEntry2API.post(self, SystemId, FabricAdapterId, os.path.basename(config['@odata.id']))
				else:
					return VCATEntry2API.post(self, SystemId, FabricAdapterId, str(res))
			else:
				return VCATEntry2API.post(self, SystemId, FabricAdapterId, str(res))
		else:
			return msg, code

# VCATEntry2 API
class VCATEntry2API(Resource):
	def __init__(self, **kwargs):
		logging.info('VCATEntry2 init called')
		self.root = PATHS['Root']
		self.auth = kwargs['auth']

	# HTTP GET
	def get(self, SystemId, FabricAdapterId, VCATEntryId):
		logging.info('VCATEntry2 get called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT/{2}', 'index.json').format(SystemId, FabricAdapterId, VCATEntryId)
			return get_json_data (path)
		else:
			return msg, code

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, SystemId, FabricAdapterId, VCATEntryId):
		logging.info('VCATEntry2 post called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT/{2}').format(SystemId, FabricAdapterId, VCATEntryId)
			collection_path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT', 'index.json').format(SystemId, FabricAdapterId)

			# Check if collection exists:
			if not os.path.exists(collection_path):
				VCATEntry2CollectionAPI.post(self, SystemId, FabricAdapterId)

			if VCATEntryId in members:
				resp = 404
				return resp
			try:
				global config
				wildcards = {'SystemId':SystemId, 'FabricAdapterId':FabricAdapterId, 'VCATEntryId':VCATEntryId, 'rb':g.rest_base}
				config=get_VCATEntry2_instance(wildcards)
				config = create_and_patch_object (config, members, member_ids, path, collection_path)
				resp = config, 200

			except Exception:
				traceback.print_exc()
				resp = INTERNAL_ERROR
			logging.info('VCATEntry2API POST exit')
			return resp
		else:
			return msg, code

	# HTTP PUT
	def put(self, SystemId, FabricAdapterId, VCATEntryId):
		logging.info('VCATEntry2 put called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT/{2}', 'index.json').format(SystemId, FabricAdapterId, VCATEntryId)
			put_object(path)
			return self.get(SystemId, FabricAdapterId, VCATEntryId)
		else:
			return msg, code

	# HTTP PATCH
	def patch(self, SystemId, FabricAdapterId, VCATEntryId):
		logging.info('VCATEntry2 patch called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT/{2}', 'index.json').format(SystemId, FabricAdapterId, VCATEntryId)
			patch_object(path)
			return self.get(SystemId, FabricAdapterId, VCATEntryId)
		else:
			return msg, code

	# HTTP DELETE
	def delete(self, SystemId, FabricAdapterId, VCATEntryId):
		logging.info('VCATEntry2 delete called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT/{2}').format(SystemId, FabricAdapterId, VCATEntryId)
			base_path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/REQ-VCAT').format(SystemId, FabricAdapterId)
			return delete_object(path, base_path, members=members, member_ids=member_ids)
		else:
			return msg, code

