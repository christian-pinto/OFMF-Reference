

test_chassis = {
    "@odata.type": "#Chassis.v1_21_0.Chassis",
    "Id": "1",
    "Name": "Test Chassis",
    "PowerState": "On",
    "ChassisType": "Drawer",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK"
    },
    "Action": {
        "#Chassis.Reset": {
            "target": "/redfish/v1/Chassis/1/Actions/Chassis.Reset/",
            "ResetType@Redfish.AllowableValues": [
                "On",
                "ForceOff",
                "PushPowerButton",
                "PowerCycle"
            ]
        }
    },
    "@odata.id": "/redfish/v1/Chassis/1",
    "@Redfish.Copyright": "Copyright 2022 OpenFabrics Alliance. All rights reserved."
}

test_system = {
    "@odata.id": "/redfish/v1/Systems/1",
    "@odata.type": "#ComputerSystem.1.00.0.ComputerSystem",
    "Id": "1",
    "Name": "Compute Node 1",
    "SystemType": "Physical",
    "Manufacturer": "Manufacturer Name",
    "Model": "Model Name",
    "SKU": "",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollUp": "OK"
    },
    "IndicatorLED": "Off",
    "Power": "On",
    "Boot": {
        "BootSourceOverrideEnabled": "Once",
        "BootSourceOverrideTarget": "Pxe",
        "BootSourceOverrideSupported": [
            "None",
            "Pxe",
            "Floppy",
            "Cd",
            "Usb",
            "Hdd",
            "BiosSetup",
            "Utilities",
            "Diags",
            "UefiTarget"
        ],
        "UefiTargetBootSourceOverride": "uefi device path"
    },
    "Processors": {
        "Count": 8,
        "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollUp": "OK"
        }
    },
    "Memory": {
        "TotalSystemMemoryGB": 16,
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollUp": "OK"
        }
    },
    "FabricAdapters": [
        { "@odata.id": "/redfish/1/Systems/1/FabricAdapters" }
    ],
    "Links": {
        "Chassis": [
            {
                "@odata.id": "/redfish/v1/Chassis/1"
            }
        ],
    }

}

test_aggregation_source_event = {
"@odata.type": "#Event.v1_7_0.Event",
"Id": "1",
"Name": "AggregationSourceDiscovered",
"Context": "",
"Events": [ {
  "EventType": "Other",
  "EventId": "4594",
  "Severity": "Ok",
  "Message": "A aggregation source of connection method Redfish located at http://cxl01.ofa.org:5002 has been discovered.",
  "MessageId": "Foo.1.0.AggregationSourceDiscovered",
  "MessageArgs": [ "Redfish", "http://127.0.0.1:5002" ],
  "OriginOfCondition": {
   "@odata.id": "/redfish/v1/AggregationService/ConnectionMethods/CXL"
  }
}
]}

test_fabric_event = {
    "@odata.type": "#Event.v1_7_0.Event",
    "Id": "1",
    "Name": "Fabric Created",
    "Context": "",
    "Events": [ {
        "EventType": "Other",
        "EventId": "4595",
        "Severity": "Ok",
        "Message": "New Fabric Created ",
        "MessageId": "Resource.1.0.ResourceCreated",
        "MessageArgs": [],
        "OriginOfCondition": {
            "@odata.id": "/redfish/v1/Fabrics/CXL"
        }
    }
    ]
}

fabric_connection = {
    "@odata.id": "/redfish/v1/Fabrics/CXL/Connections/14",
    "@odata.type": "#Connection.v1_1_0.Connection",
    "ConnectionType": "Memory",
    "Description": "CXL Connection 14 Information",
    "Id": "14",
    "Name": "Connection 14",
    "Status": {
        "Health": "OK",
        "HealthRollup": "OK",
        "State": "Enabled"
    }
}

fabric_connection_patch = {
    "Links": {
        "InitiatorEndpoints": [
            {
                "@odata.id": "/redfish/v1/Fabrics/CXL/Endpoints/I2"
            }
        ],
        "TargetEndpoints": [
            {
                "@odata.id": "/redfish/v1/Fabrics/CXL/Endpoints/T2"
            }
        ]
    }
}

memory_chunk = {
    "@odata.type": "#MemoryChunks.v1_5_0.MemoryChunks",
    "@odata.id": "/redfish/v1/Chassis/CXL3/MemoryDomains/1/MemoryChunks/2",
    "Id": "2",
    "Name": "Memory Chunk 2",
    "Description": "Memory chunk accessible through CXL",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "MemoryChunkSizeMiB": 1024,
    "AddressRangeType": "PMEM",
    "AddressRangeOffsetMiB": 2048,
    "MediaLocation": "Local",
    "OperationalState": "Online",
    "Oem": {},
    "@Redfish.Copyright": "Copyright 2014-2021 DMTF. For the full DMTF copyright policy, see http://www.dmtf.org/about/policies/copyright."
}

memory_chunk_patch = {
    "Links": {
        "CXLLogicalDevices": [
            {
                "@odata.id": "/redfish/v1/Chassis/CXL3/PCIeDevices/1/CXLLogicalDevices/1"
            }
        ]
    }
}

zone = {
    "@odata.type": "#Zone.v1_6_1.Zone",
    "Id": "4",
    "Name": "CXL Zone 4",
    "Description": "CXL Zone 4",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "ZoneType": "ZoneOfEndpoints",
    "Oem": {},
    "@odata.id": "/redfish/v1/Fabrics/CXL/Zones/4",
    "@Redfish.Copyright": "Copyright 2014-2021 DMTF. For the full DMTF copyright policy, see http://www.dmtf.org/about/policies/copyright."
}

zone_patch = {
    "Links": {
        "Endpoints": [
            {
                "@odata.id": "/redfish/v1/Fabrics/CXL/Endpoints/I1"
            },
            {
                "@odata.id": "/redfish/v1/Fabrics/CXL/Endpoints/T1"
            },
            {
                "@odata.id": "/redfish/v1/Fabrics/CXL/Endpoints/1"
            }
        ]
    }
}
