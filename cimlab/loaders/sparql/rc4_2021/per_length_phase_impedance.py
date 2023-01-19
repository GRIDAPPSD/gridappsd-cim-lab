from typing import List
from dataclasses import dataclass, field

def get_all_attributes(feeder_id: str, mrid_list: List[str]):
    query_message = """
        PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cim:  <http://iec.ch/TC57/CIM100#>
        SELECT ?mRID ?name ?conductorCount
        (group_concat(distinct ?PhaseImpedance_Data; separator=";") as ?PhaseImpedanceData) 
        (group_concat(distinct ?ACLineSegment; separator=';') as ?ACLineSegments)  
        WHERE {          
          ?eq r:type cim:PerLengthPhaseImpedance.
          VALUES ?fdrid {"%s"}
          VALUES ?mRID {"""%feeder_id
    # add all equipment mRID
    for mrid in mrid_list:
        query_message += ' "%s" \n'%mrid
    # add all attributes
    query_message += """               } 
        ?line cim:ACLineSegment.PerLengthImpedance ?eq.
        ?line cim:IdentifiedObject.mRID ?ACLineSegment.
        ?line cim:Equipment.EquipmentContainer ?fdr.
        ?fdr cim:IdentifiedObject.mRID ?fdrid.
        ?eq cim:IdentifiedObject.mRID ?mRID.
        ?eq cim:IdentifiedObject.name ?name.
        
        OPTIONAL {?eq cim:PerLengthPhaseImpedance.conductorCount ?conductorCount.}
        OPTIONAL {?pi cim:PhaseImpedanceData.PhaseImpedance ?eq.
                  #?pi cim:IdentifiedObject.mRID ?PhaseImpedance_Data. #missing from xml
                  bind(strafter(str(?pi),"sparql#") as ?PhaseImpedance_Data).}

        }
        GROUP by ?mRID ?name ?conductorCount 
        ORDER by  ?name
        """
    return query_message