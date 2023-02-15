from __future__ import annotations
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import cimlab.data_profile.rc4_2021 as cim

def get_class_objects_sparql(feeder_mrid: str, class_name:str) -> str: 
    """ Generates SPARQL query string for a given catalog of objects and feeder id
    Args:
        feeder_mrid (str | Feeder object): The mRID of the feeder or feeder object
        typed_catalog (dict[type, dict[str, object]]): The typed catalog of CIM objects organized by 
            class type and object mRID
    Returns:
        sparql_message: query string that can be used in blazegraph connection or STOMP client
    """

    
    query_message = """
        PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cim:  <http://iec.ch/TC57/CIM100#>
        SELECT ?mRID ?name 
        WHERE {          
          VALUES ?fdrid {"%s"}
          """%feeder_mrid
    
    query_message += """
        ?eq r:type cim:%s.
        ?eq cim:Equipment.EquipmentContainer ?fdr.
        ?fdr cim:IdentifiedObject.mRID ?fdrid.
        ?eq cim:IdentifiedObject.mRID ?mRID.
        ?eq cim:IdentifiedObject.name ?name.
        }
        ORDER by  ?name
        """%class_name
    
    return query_message