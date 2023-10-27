# Copyright (c) 2023 International Business Machines, Inc. All rights reserved.

import json
import api_emulator.utils as utils
import requests

request_headers = {
    'Content-Type': 'application/json'
}

# This function checks if an object is managed by a Sunfish agent and returns
# the Agent @odata.id or None if the object is not managed by an Agent
# We are assuming that the resource_path we receive is always that of a collection because according to the RedFish
# specification (v1.18.0 at the time of writing this comment): "To create a resource, services shall support the POST
# method on resource collections."
def isAgentManaged(resource_path):
    resource = utils.get_object(resource_path)
    if "Oem" in resource and "Sunfish_RM" in resource["Oem"] and "ManagingAgent" in resource["Oem"]["Sunfish_RM"]:
        return resource["Oem"]["Sunfish_RM"]["ManagingAgent"]["@odata.id"]

    return None

def requestToAgent(method, agent_id, resource_path, payload):
    if agent_id is None or agent_id == "":
        raise Exception("Error: Missing Agent id")
    if resource_path is None or resource_path == "":
        raise Exception("Error: Missing resource_path")

    agent = utils.get_object(agent_id)
    agent_hostname = agent["HostName"]
    resource_uri = agent_hostname + "/" + resource_path
    if method == "POST":
        if payload is None:
            # we only check if there is a payload and we assume that is correct
            raise Exception("Error: Missing payload")
        r = requests.post(resource_uri, headers=request_headers, data=json.dumps(payload))
    elif method == "PATCH":
        if payload is None:
            # we only check if there is a payload and we assume that is correct
            raise Exception("Error: Missing payload")
        r = requests.patch(resource_uri, headers=request_headers, data=json.dumps(payload))
    elif method == "DELETE":
        r = requests.delete(resource_uri)
    elif method == "PUT":
        if payload is None:
            # we only check if there is a payload and we assume that is correct
            raise Exception("Error: Missing payload")
        r = requests.put(resource_uri, headers=request_headers, data=json.dumps(payload))
    else:
        raise Exception("Invalid method for requestToAgent")

    return r

# This method forwards the request to the agent specified in the arguments and returns an object config dict
# updated with the OEM field pointing to the management server.
# The function returns:
#   - (None, None) if the resource is not managed by an agent
#   - (agent id, (reason, status code)) if agent managed and returning the message from the agent
def forwardToAgentIfManaged(method, resource_path, config=None):
    agent = isAgentManaged(resource_path)
    if agent:
        # This collection is managed by an agent, let's forward the request
        # We just return whatever the agent returns to us
        r = requestToAgent(method, agent, resource_path, config)
        return agent, (r.reason, r.status_code)

    return None, None
