# GridAPPS-D CIM-Lab Library
Python library for parsing CIM power system models in distributed ADMS applications. It creates Python object instances in memory using a data profile exported from a specified CIM profile (e.g. GridAPPS-D CIM100 RC4_2021 profile).

The library is being expanded to cover centralized applications, transmission models, and real-time editing of CIM XML models natively.

## Requirements
The gridappsd-cim-lab requires a python version >=3.8 and <4. No testing has been done with other versions.

It also requires a connection to a Blazegraph TripleStore Database or the GridAPPS-D Platform. Support for other databases may be added in future releases.

The DistributedModel class also requires the output for GridAPPS-D Topology Processor, which may be obtained by importing the topology processor library or passing an API call to the `goss.gridappsd.request.data.topology` queue in the GridAPPS-D platform.

## Installation
The CIM-Lab library should be installed in same virtual environment as the ADMS application. 
```
pip install gridappsd-cim-lab
```
It is also included in the gridappsd-python library, which can be installed using
```
pip install gridappsd-python
```

## Specifying the CIM Profile
The CIM-Lab library supports multiple CIM profiles, which can be exported using CIMtool or Enterprise Architect Schema Composer as a .xsd data profile. The data profiles are ingested using the xsdata python library and saved in the cimlab/data_profile directory.

When importing the library, the CIM profile must be specified using the gridappsd-python constructor or directly as
```
import cimlab.data_profile.rc4_2021 as cim
```
or by using `importlib`:
```
import importlib
cim_profile = 'rc4_2021'
cim = importlib.import_module('cimlab.data_profile.' + cim_profile)
```


## Model Initialization

The CIM-Lab library creates object instances populated with the attributes of `name` and `mRID` for all addressable and unaddressable equipment in each distributed area. All other attributes are `None` or `[]` by default.

### Usage with GridAPPS-D Context Manager
If an application is built using the GridAPPS-D Context Manager and Field Interface in gridappsd-python, initialization of the `DistributedModel`, `SwitchArea`, and `SecondaryArea` classes is performed automatically.

### Standalone Usage
Initialization of the `DistributedModel`, `SwitchArea`, and `SecondaryArea` classes requires the distributed topology message from GridAPPS-D Topology Processor, which may be called through the GridAPPS-D API or by import the topology library:
```
topic = "goss.gridappsd.request.data.topology"

message = {
   "requestType": "GET_SWITCH_AREAS",
   "modelID":  "_FEEDER_MRID_1234_ABCD,
   "resultFormat": "JSON"
}

topology_response = gapps.get_response(topic, message, timeout=30)
```
```
from topology_processor import DistributedTopology
gapps = GridappsdConnection(feeder_mrid)
Topology = DistributedTopology(gapps, feeder_mrid)
topology_response = Topology.create_switch_areas(feeder_mrid)
topology_response = json.loads(topology_response)
```
The distributed network model can then be initialized using
```
feeder = cim.Feeder(mRID=feeder_mrid)
network = DistributedModel(connection=bg, feeder=feeder, topology=topology_response['feeders'])
```

## Core Library Methods
The CIM power system model can then be parsed by invoking the `.get_all_attributes(cim.ClassName)` method. The method populates all available attributes of the given attribute and creates default instances of all associated class object instances that are one association away in the CIM UML. Associated default instances are only populated with `mRID` attribute. The `.get_all_attributes` method must be invoked in sequential order following the inheritance hierarchy in the CIM UML, starting with the particular equiment class (e.g. ACLineSegment) and then each child class inheriting from the previous class. 

The Python object instances can be accessed using the `typed_catalog` dictionary of each distributed area class instance. The typed catalog is organized by the class type and then mRID of each object. The attributes of each class can be accessed directly or through any associated class. These two call are equivalent:
```
bus_name = switch_area.typed_catalog[cim.ConnectivityNode][node_mrid].name
```
```
bus_name = switch_area.typed_catalog[cim.ACLineSegment][line_mrid].Terminals[0].ConnectivityNode.name
```

Note that all classes and attributes are case sensitive and follow the CIM UML conventions for each class.

All instances of all given CIM class can also be exported as JSON text using the `.__dumps__(cim.ClassName)` method of the distributed area classes:
```
Lines = switch_area.__dumps__(cim.ACLineSegment)
```

Additional examples of usage for specified CIM classes are inlcuded in model_example.py
