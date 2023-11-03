# Copyright IBM Corp. 2023

# Template for - CXLLogicalDevice
# Program name - CXLLogicalDevice.py

import copy
from flask import json

_TEMPLATE = \
	{
		"@odata.id": "{rb}Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/CXLLogicalDevices/{CXLLogicalDeviceId}",
		"@odata.type": "#CXLLogicalDevice.v1_0_0.CXLLogicalDevice",
		"Id": "{CXLLogicalDeviceId}",
		"Name": "CXL Logical Device",
	}


def get_CXLLogicalDevice_instance(wildcards):
		"""
		Instantiates and formats the template
		Arguments:
			wildcard - A dictionary of wildcards strings and their repalcement values
		"""
		c = copy.deepcopy(_TEMPLATE)
		d = json.dumps(c)
		g = d.replace('{ChassisId}', '0')
		g = g.replace('{PCIeDeviceId}', '1')
		g = g.replace('{CXLLogicalDeviceId}', '2')
		g = g.replace('{rb}', 'NUb')
		g = g.replace('}}', '!!~')
		g = g.replace('{{', '~~!')
		g = g.replace('{', '~!')
		g = g.replace('}', '!~')
		g = g.replace('0', '{ChassisId}')
		g = g.replace('1', '{PCIeDeviceId}')
		g = g.replace('2', '{CXLLogicalDeviceId}')
		g = g.replace('NUb', '{rb}')
		g = g.format(**wildcards)
		g = g.replace('~~!', '{{')
		g = g.replace('!!~', '}}')
		g = g.replace('~!', '{')
		g = g.replace('!~', '}')
		return json.loads(g)