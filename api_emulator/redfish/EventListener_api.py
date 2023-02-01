from flask import request
from flask_restful import Resource
from .constants import *
import requests
import json

from api_emulator.utils import create_path, create_object

from api_emulator.redfish.Manager_api import ManagerCollectionAPI

import logging

config = {}

INTERNAL_ERROR = 500


# EventListener does not have a Collection API

class EventProcessor(Resource):
    def __init__(self):
        logging.info('Event Listener init called')
        self.root = PATHS['Root']

    def fetchResource(self, obj_id, obj_root, host, port):

        resource_endpoint = f"{host}:{port}/{obj_id}"
        logging.info(f"fetch: {resource_endpoint}")
        response = requests.get(resource_endpoint)

        if response.status_code == 200:
            redfish_obj = response.json()

            obj_path = "".join(redfish_obj['@odata.id'].split('/redfish/v1/'))
            file_path = create_path(self.root, obj_path)
            create_object(redfish_obj, [], [], file_path)

            if 'Collection' in redfish_obj['@odata.type']:
                logging.info(f"Found collection {redfish_obj['@odata.type']}")
                EventProcessor.recursiveFetch(self, {'Members': redfish_obj['Members']}, obj_root, host, port)

    def recursiveFetch(self, obj_dict, obj_root, host, port):
        logging.info(f"dict: {obj_dict}, obj_root:{obj_root}")
        if obj_root is None or not obj_root or type(obj_dict) is not dict:
            return

        for key, value in obj_dict.items():
            logging.info(f"checking k:{key}, v:{value}")
            if key == 'Links':  # Do not explore Links for now
                logging.info(f"returning k:{key}, v:{value}")
                continue
            elif key == '@odata.id' and obj_root in value and obj_root != value:
                logging.info(f"fetch k:{key}, v:{value}")
                EventProcessor.fetchResource(self, value, obj_root, host, port)

            if type(value) == dict:
                EventProcessor.recursiveFetch(self, value, obj_root, host, port)
            elif type(value) == list:
                for element in value:
                    EventProcessor.recursiveFetch(self, element, obj_root, host, port)

    def ManagerCreated(self):
        logging.info("ManagerCreated method called")
        config = json.loads(request.data)
        for event in config['Events']:
            host = event['MessageArgs'][0]
            port = event['MessageArgs'][1]
            response = requests.get(f"{host}:{port}/{event['OriginOfCondition']['@odata.id']}")
            if response.status_code == 200:
                redfish_obj = response.json()

                request.data = json.dumps(redfish_obj, indent=2).encode('utf-8')
                # Update ManagerCollection before fetching the resource subtree
                ManagerCollectionAPI.post(self)
                EventProcessor.recursiveFetch(self, redfish_obj, redfish_obj['@odata.id'], host, port)


def handle_events(res):
    config = json.loads(request.data)
    for event in config['Events']:
        ###
        # Each MessageId identifies the name of the handler that will be used to process the event
        # For instance an event json with MessageId as following will be handled by the function ConnectionCreated
        # {
        #   ...
        #   'MessageId': 'Manager.1.0.ManagerCreated'
        #   ...
        # }
        ###
        handlerfunc = getattr(EventProcessor, event['MessageId'].split(".")[-1])
        handlerfunc(res)


# EventListener API
class EventListenerAPI(Resource):
    def __init__(self, **kwargs):
        logging.info('Event Listener init called')
        self.root = PATHS['Root']
        self.auth = kwargs['auth']

    # HTTP GET
    def get(self):
        logging.info('Event Listener get called')
        return {}

    # HTTP POST Collection
    def post(self):
        logging.info('Event Listener post called')
        if request.data:
            config = json.loads(request.data)
            logging.info(f"Received request json: {config}")
            handle_events(self)

        return {}

    # HTTP PUT Collection
    def put(self):
        logging.info('Event Listener put called')
