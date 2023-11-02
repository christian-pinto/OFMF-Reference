aggregation_source = {
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
            "MessageArgs": ["Redfish", "http://sunfish.ofa.org:5000"],
            "OriginOfCondition": {
                "@odata.id": "/redfish/v1/AggregationService/ConnectionMethods/CXL"
            }
        }
        ]
}

fabric = {
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
    ]}

headers = {
    "Content-Type": "application/json"
}
