import test_templates
import json
import pytest
from api_emulator.resource_manager import ResourceManager
from api_emulator.redfish.constants import PATHS

import g

REST_BASE = '/redfish/v1/'
g.rest_base = REST_BASE

request_headers = {
    'Content-Type': 'application/json'
}

test_objs_agent_fwd_post = [{"url": f"{REST_BASE}Fabrics/CXL/Connections",
                             "payload": test_templates.fabric_connection},
                            {"url": f"{REST_BASE}Systems/CXL-System/MemoryDomains/CXL/MemoryChunks",
                             "payload": test_templates.memory_chunk},
                            {"url": f"{REST_BASE}Chassis/CXL3/MemoryDomains/1/MemoryChunks",
                             "payload": test_templates.memory_chunk},
                            {"url": f"{REST_BASE}Fabrics/CXL/Zones",
                             "payload": test_templates.zone},
                            {"url": f"{REST_BASE}Chassis/CXL3/PCIeDevices/1/CXLLogicalDevices",
                             "payload": test_templates.cxl_logical_device}
                            ]


test_objs_agent_fwd_put = [{"url": f"{REST_BASE}Fabrics/CXL/Connections/14",
                            "payload": test_templates.fabric_connection},
                           {"url": f"{REST_BASE}Systems/CXL-System/MemoryDomains/CXL/MemoryChunks/2",
                            "payload": test_templates.memory_chunk},
                           {"url": f"{REST_BASE}Chassis/CXL3/MemoryDomains/1/MemoryChunks/2",
                            "payload": test_templates.memory_chunk},
                           {"url": f"{REST_BASE}Fabrics/CXL/Zones/4",
                            "payload": test_templates.zone},
                            {"url": f"{REST_BASE}Chassis/CXL3/PCIeDevices/1/CXLLogicalDevices/4",
                             "payload": test_templates.cxl_logical_device}]

test_objs_agent_fwd_patch = [{"url": f"{REST_BASE}Fabrics/CXL/Connections/14",
                             "payload": test_templates.fabric_connection_patch},
                             {"url": f"{REST_BASE}Systems/CXL-System/MemoryDomains/CXL/MemoryChunks/2",
                             "payload": test_templates.memory_chunk_patch},
                             {"url": f"{REST_BASE}Chassis/CXL3/MemoryDomains/1/MemoryChunks/2",
                              "payload": test_templates.memory_chunk_patch},
                             {"url": f"{REST_BASE}Fabrics/CXL/Zones/4",
                              "payload": test_templates.zone_patch},
                            {"url": f"{REST_BASE}Chassis/CXL3/PCIeDevices/1/CXLLogicalDevices/4",
                             "payload": test_templates.cxl_logical_device_patch}]

test_objs_agent_fwd_del = [{"url": f"{REST_BASE}Fabrics/CXL/Connections/14"},
                           {"url": f"{REST_BASE}Systems/CXL-System/MemoryDomains/CXL/MemoryChunks/2"},
                           {"url": f"{REST_BASE}Chassis/CXL3/MemoryDomains/1/MemoryChunks/2"},
                           {"url": f"{REST_BASE}Fabrics/CXL/Zones/4"},
                           {"url": f"{REST_BASE}Chassis/CXL3/PCIeDevices/1/CXLLogicalDevices/4"}]


class TestOFMF:
    @classmethod
    def setup_class(cls):
        global resource_manager
        global REST_BASE
        global TRAYS
        global SPEC

        PATHS['Root'] = 'Resources/Sunfish'
        resource_manager = ResourceManager(None, None, None, "Disable", None)
        g.app.testing = True
        cls.client = g.app.test_client()

    def test_create_computer_system(self):
        system_url = f"{REST_BASE}Systems"
        response = self.client.post(system_url, json=test_templates.test_system)
        status_code = response.status_code

        assert status_code == 200

    def test_create_chassis(self):
        chassis_url = f"{REST_BASE}Chassis"
        response = self.client.post(chassis_url, json=test_templates.test_chassis)
        status_code = response.status_code

        assert status_code == 200

    def test_agent_registration(self):
        events_url = f"/EventListener"
        response = self.client.post(events_url, json=test_templates.test_aggregation_source_event)
        status_code = response.status_code

        assert status_code == 200

        manager_name = \
        test_templates.test_aggregation_source_event["Events"][0]["OriginOfCondition"]["@odata.id"].split('/')[-1]
        conn_method = test_templates.test_aggregation_source_event["Events"][0]["OriginOfCondition"]
        aggr_source_url = f"{REST_BASE}AggregationService/AggregationSources"
        response = self.client.get(aggr_source_url)

        # validate the generation of a new AggregationSource related to the new Agent
        aggr_source_collection = json.loads(response.data)
        aggr_source_found = False
        for aggr_source in aggr_source_collection['Members']:
            aggr_source_endpoint = self.client.get(aggr_source['@odata.id'])
            aggr_source_data = json.loads(aggr_source_endpoint.data)
            if conn_method == aggr_source_data['Links']['ConnectionMethod']:
                aggr_source_found = True

        assert aggr_source_found

    @pytest.mark.order(after="test_agent_registration")
    def test_agent_registration_create_fabric(self):
        events_url = f"/EventListener"
        response = self.client.post(events_url, json=test_templates.test_fabric_event)
        status_code = response.status_code
        assert status_code == 200

    @pytest.mark.order(after="test_agent_registration_create_fabric")
    def test_agent_forward_post(self):
        for item in test_objs_agent_fwd_post:
            print(f"Testing POST for {item['url']}")
            print(item['payload'])
            item["payload"]["@odata.id"] = f"{item['url']}/{item['payload']['Id']}"
            r = self.client.post(item["url"], headers=request_headers, data=json.dumps(item["payload"]))
            assert r.status_code == 200

    @pytest.mark.order(after="test_agent_forward_post")
    def test_agent_forward_patch(self):
        for item in test_objs_agent_fwd_patch:
            print(f"Testing PATCH for {item['url']}")
            r = self.client.patch(item["url"], headers=request_headers, data=json.dumps(item["payload"]))

            print(r)
            assert r.status_code == 200

    @pytest.mark.order(after="test_agent_forward_patch")
    def test_agent_forward_put(self):
        for item in test_objs_agent_fwd_put:
            print(f"Testing PUT for {item['url']}")
            item["payload"]["@odata.id"] = item['url']
            r = self.client.put(item["url"], headers=request_headers, data=json.dumps(item["payload"]))
            assert r.status_code == 200

    @pytest.mark.order(after="test_agent_forward_put")
    def test_agent_forward_delete(self):
        for item in test_objs_agent_fwd_del:
            print(f"Testing DELETE for {item['url']}")
            r = self.client.delete(item["url"])
            assert r.status_code == 200
