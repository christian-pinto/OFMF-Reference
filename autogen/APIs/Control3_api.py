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

# Resource implementation for - /redfish/v1/PowerEquipment/Switchgear/{PowerDistributionId}/Controls/{ControlId}
# Program name - Control3_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Control3 import get_Control3_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Control3 Collection API
class Control3CollectionAPI(Resource):
	def __init__(self):
		logging.info('Control3 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, PowerDistributionId):
		logging.info('Control3 Collection get called')
		path = os.path.join(self.root, 'PowerEquipment/Switchgear/{0}/Controls', 'index.json').format(PowerDistributionId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, PowerDistributionId):
		logging.info('Control3 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if PowerDistributionId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls').format(PowerDistributionId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Control', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Control3API.post(self, PowerDistributionId, os.path.basename(config['@odata.id']))
			else:
				return Control3API.post(self, PowerDistributionId, str(res))
		else:
			return Control3API.post(self, PowerDistributionId, str(res))

	# HTTP PUT Collection
	def put(self, PowerDistributionId):
		logging.info('Control3 Collection put called')

		path = os.path.join(self.root, 'PowerEquipment/Switchgear/{0}/Controls', 'index.json').format(PowerDistributionId)
		put_object (path)
		return self.get(PowerDistributionId)

# Control3 API
class Control3API(Resource):
	def __init__(self):
		logging.info('Control3 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, PowerDistributionId, ControlId):
		logging.info('Control3 get called')
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls/{1}', 'index.json').format(PowerDistributionId, ControlId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, PowerDistributionId, ControlId):
		logging.info('Control3 post called')
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls/{1}').format(PowerDistributionId, ControlId)
		collection_path = os.path.join(self.root, 'PowerEquipment/Switchgear/{0}/Controls', 'index.json').format(PowerDistributionId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Control3CollectionAPI.post(self, PowerDistributionId)

		if ControlId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'PowerDistributionId':PowerDistributionId, 'ControlId':ControlId, 'rb':g.rest_base}
			config=get_Control3_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Control3API POST exit')
		return resp

	# HTTP PUT
	def put(self, PowerDistributionId, ControlId):
		logging.info('Control3 put called')
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls/{1}', 'index.json').format(PowerDistributionId, ControlId)
		put_object(path)
		return self.get(PowerDistributionId, ControlId)

	# HTTP PATCH
	def patch(self, PowerDistributionId, ControlId):
		logging.info('Control3 patch called')
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls/{1}', 'index.json').format(PowerDistributionId, ControlId)
		patch_object(path)
		return self.get(PowerDistributionId, ControlId)

	# HTTP DELETE
	def delete(self, PowerDistributionId, ControlId):
		logging.info('Control3 delete called')
		path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls/{1}').format(PowerDistributionId, ControlId)
		base_path = create_path(self.root, 'PowerEquipment/Switchgear/{0}/Controls').format(PowerDistributionId)
		return delete_object(path, base_path)

