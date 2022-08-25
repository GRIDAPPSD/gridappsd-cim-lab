from __future__ import annotations
from typing import List
from dataclasses import dataclass, field

import cim.data_profile as cim
from cim.loaders import ConnectionInterface
from cim.models import add_to_catalog, add_to_typed_catalog




@dataclass
class SecondaryArea:
    area_id: str
    connection: ConnectionInterface
    distribution_transformer: dict[str, object] = field(default_factory=dict)
    addressable_equipment: dict[str, object] = field(default_factory=dict)
    unaddressable_equipment: dict[str, object] = field(default_factory=dict)
    connectivity_nodes: dict[str, object] = field(default_factory=dict)
    secondary_areas: list[object] = field(default_factory=list)
    typed_catalog: dict[type, dict[str, object]] = field(default_factory=dict)

    # Initialize empty CIM objects for all equipment in secondary area
    def initialize_secondary_area(self, switch_msg: dict):
        self.feeder_mrid = self.area_id.split('.')[0]  # get feeder mRID from area id

        addr_equip = self.connection.create_default_instances(self.feeder_mrid, switch_msg['addressable_equipment'])
        for obj in addr_equip:
            add_to_catalog(obj, self.addressable_equipment)
            add_to_typed_catalog(obj, self.typed_catalog)
        unaddr_equip = self.connection.create_default_instances(self.feeder_mrid, switch_msg['unaddressable_equipment'])
        for obj in unaddr_equip:
            add_to_catalog(obj, self.unaddressable_equipment)
            add_to_typed_catalog(obj, self.typed_catalog)
        conn_nodes = self.connection.create_default_instances(self.feeder_mrid, switch_msg['connectivity_node'])
        for obj in conn_nodes:
            add_to_catalog(obj, self.connectivity_nodes)
            add_to_typed_catalog(obj, self.typed_catalog)
        xfmr = self.connection.create_default_instances(self.feeder_mrid, switch_msg['distribution_transformer'])
        for obj in xfmr:
            add_to_catalog(obj, self.distribution_transformer)
            add_to_typed_catalog(obj, self.typed_catalog)
            
    def get_all_attributes(self, cim_class):
        self.connection.get_all_attributes(self.feeder_mrid, self.typed_catalog, cim_class)