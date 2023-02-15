from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json
import logging

import cimlab.data_profile as cim
from cimlab.loaders import ConnectionInterface, QueryResponse
from cimlab.models.model_parsers import add_to_catalog, add_to_typed_catalog, cim_dump
from cimlab.models.switch_area import SwitchArea
_log = logging.getLogger(__name__)

@dataclass
class CentralizedModel:
    feeder: cim.Feeder
    connection: ConnectionInterface
    typed_catalog: dict[type, dict[str, object]] = field(default_factory=dict)
    

    def __post_init__(self):
        self.__initialize_network__()
        
        
    # Initialize all CIM objects in feeder model
    def __initialize_network__(self):
        
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'ACLineSegment')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'TransformerTank')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'PowerTransformer')       
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'PowerElectronicsConnection')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'Breaker')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'Fuse')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'LoadBreakSwitch')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'Recloser')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'Sectionaliser')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'SynchronousMachine')
        self.connection.create_default_objects(self.feeder.mRID, self.typed_catalog, 'LinearShuntCompensator')
        
    def get_all_attributes(self, cim_class):
        if cim_class in self.typed_catalog:
            self.connection.get_all_attributes(self.feeder.mRID, self.typed_catalog, cim_class)
        else:
            _log.info('no instances of '+str(cim_class.__name__)+' found in catalog.')


    def get_attributes_query(self, cim_class):
        if cim_class in self.typed_catalog:
            sparql_message = self.connection.get_attributes_query(self.feeder.mRID, self.typed_catalog, cim_class, False)
        else:
            _log.info('no instances of '+str(cim_class.__name__)+' found in catalog.')
            sparql_message = ''
        return sparql_message

    def __dumps__(self, cim_class):
        if cim_class in self.typed_catalog:
            json_dump = cim_dump(self.typed_catalog, cim_class)
        else:
            json_dump = {}
            _log.info('no instances of '+str(cim_class.__name__)+' found in catalog.')

        return json_dump