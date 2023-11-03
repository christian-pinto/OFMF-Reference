# Copyright IBM Corp. 2023

# Resource implementation for - /redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}
# Program name - CXLLogicalDevice.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import check_authentication, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, create_collection
from .templates.CXLLogicalDevice import get_CXLLogicalDevice_instance
import api_emulator.agents_management as agents_management

members = []
member_ids = []
INTERNAL_ERROR = 500


# CXLLogicalDevice Collection API
class CXLLogicalDeviceCollectionAPI(Resource):
	def __init__(self, **kwargs):
		logging.info('CXLLogicalDevice Collection init called')
		self.root = PATHS['Root']
		self.auth = kwargs['auth']

	# HTTP GET
	def get(self, ChassisId, PCIeDeviceId):
		logging.info('CXLLogicalDevice Collection get called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = os.path.join(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices', 'index.json').format(ChassisId, PCIeDeviceId)
			return get_json_data(path)
		else:
			return msg, code

	# HTTP POST Collection
	def post(self, ChassisId, PCIeDeviceId):
		logging.info('CXLLogicalDevice Collection post called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			if request.data:
				config = json.loads(request.data)
				if "@odata.type" in config:
					if "Collection" in config["@odata.type"]:
						return "Invalid data in POST body", 400

			if PCIeDeviceId in members:
				resp = 404
				return resp
			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices').format(ChassisId, PCIeDeviceId)
			parent_path = os.path.dirname(path)
			if not os.path.exists(path):
				os.mkdir(path)
				create_collection(path, 'CXLLogicalDevice', parent_path)

			res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			if request.data:
				config = json.loads(request.data)
				if "@odata.id" in config:
					return CXLLogicalDeviceAPI.post(self, ChassisId, PCIeDeviceId, os.path.basename(config['@odata.id']))
				else:
					return CXLLogicalDeviceAPI.post(self, ChassisId, PCIeDeviceId, str(res))
			else:
				return CXLLogicalDeviceAPI.post(self, ChassisId, PCIeDeviceId, str(res))
		else:
			return msg, code

# CXLLogicalDevice API
class CXLLogicalDeviceAPI(Resource):
	def __init__(self, **kwargs):
		logging.info('CXLLogicalDevice init called')
		self.root = PATHS['Root']
		self.auth = kwargs['auth']

	# HTTP GET
	def get(self, ChassisId, PCIeDeviceId, CXLLogicalDeviceId):
		logging.info('CXLLogicalDevice get called')
		msg, code = check_authentication(self.auth)

		if code == 200:
			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices/{2}', 'index.json').format(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
			return get_json_data(path), 200
		else:
			return msg, code

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ChassisId, PCIeDeviceId, CXLLogicalDeviceId):
		logging.info('CXLLogicalDevice post called')
		msg, code = check_authentication(self.auth)
		full_id = f"/redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}"

		if code == 200:
			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices/{2}').format(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
			collection_path = os.path.join(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices', 'index.json').format(ChassisId, PCIeDeviceId)
			# Check if collection exists:
			if not os.path.exists(collection_path):
				CXLLogicalDeviceCollectionAPI.post(self, ChassisId, PCIeDeviceId)

			if full_id in member_ids:
				resp = "Element Id already existing", 404
				return resp
			try:
				logging.debug("ConnectionAPI POST - request payload")
				logging.debug(json.dumps(request.json, indent=2))
				if not request.data:
					return "Request payload missing", 400

				# This piece checking for the agent should really be in the collection class, because that is where one
				# would POST for creating an object. However, the actual resource is created in this method and this is
				# where we need the agent id.
				config = request.json
				agent, response = agents_management.forwardToAgentIfManaged("POST", request.path, config=config)
				if agent is not None and response[1] != 200:
					logging.debug("Agent returned an error")
					logging.debug(response)
					# This is the case where the object is agent managed and there was an error on the agent side
					# let's return the agent error code and message and stop here.
					return response

				logging.debug(f"Managing agent: {agent}")

				wildcards = {'ChassisId': ChassisId, 'PCIeDeviceId': PCIeDeviceId, 'CXLLogicalDeviceId': CXLLogicalDeviceId, 'rb': g.rest_base}
				config = get_CXLLogicalDevice_instance(wildcards)
				config = create_and_patch_object (config, members, member_ids, path, collection_path, agent)
				resp = config, 200

			except Exception:
				traceback.print_exc()
				resp = INTERNAL_ERROR
			logging.info('CXLLogicalDevice POST exit')
			return resp
		else:
			return msg, code

	# HTTP PUT
	def put(self, ChassisId, PCIeDeviceId, CXLLogicalDeviceId):
		logging.info('CXLLogicalDevice put called')
		msg, code = check_authentication(self.auth)
		full_id = f"/redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}"

		if code == 200:
			if full_id not in member_ids:
				return "Element not present.", 404

			agent, response = agents_management.forwardToAgentIfManaged("PUT", request.path, config=request.json)
			if agent is not None and response[1] != 200:
				logging.debug("Agent returned an error")
				logging.debug(response)
				# This is the case where the object is agent managed and there was an error on the agent side
				# let's return the agent error code and message and stop here.
				return response

			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices/{2}').format(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
			put_object(path, agent)
			return self.get(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
		else:
			return msg, code

	# HTTP PATCH
	def patch(self, ChassisId, PCIeDeviceId, CXLLogicalDeviceId):
		logging.info('CXLLogicalDevice patch called')
		msg, code = check_authentication(self.auth)
		full_id = f"/redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}"

		if code == 200:
			if full_id not in member_ids:
				return "Element not present.", 404

			agent, response = agents_management.forwardToAgentIfManaged("PATCH", request.path, config=request.json)
			if agent is not None and response[1] != 200:
				logging.debug("Agent returned an error")
				logging.debug(response)
				# This is the case where the object is agent managed and there was an error on the agent side
				# let's return the agent error code and message and stop here.
				return response

			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices/{2}').format(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
			patch_object(path)
			return self.get(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
		else:
			return msg, code

	# HTTP DELETE
	def delete(self, ChassisId, PCIeDeviceId, CXLLogicalDeviceId):
		logging.info('CXLLogicalDevice delete called')
		msg, code = check_authentication(self.auth)
		full_id = f"/redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}"

		if code == 200:
			if full_id not in member_ids:
				return "Element not present.", 404

			agent, response = agents_management.forwardToAgentIfManaged("DELETE", request.path)
			if agent is not None and response[1] != 200:
				logging.debug("Agent returned an error")
				logging.debug(response)
				# This is the case where the object is agent managed and there was an error on the agent side
				# let's return the agent error code and message and stop here.
				return response

			path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices/{2}').format(ChassisId, PCIeDeviceId, CXLLogicalDeviceId)
			base_path = create_path(self.root, 'Chassis/{0}/PCIeDevices/{1}/CXLLogicalDevices').format(ChassisId, PCIeDeviceId)
			return delete_object(path, base_path)
		else:
			return msg, code

