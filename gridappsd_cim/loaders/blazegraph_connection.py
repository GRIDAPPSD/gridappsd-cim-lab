from dataclasses import dataclass
from typing import List, Dict

from SPARQLWrapper import SPARQLWrapper, JSON

from gridappsd_cim.loaders.connection import Connection
import gridappsd_cim as cim
from gridappsd_cim.loaders.blazegraph_loaders import query_class_parser, query_list_parser, query_string_parser

@dataclass
class BlazeGraphConnection(Connection):
    url: str
    feeder_mrid: str = None
    sparql: SPARQLWrapper = None

#     def load_attributes(self, obj: object):
#         if isinstance(obj, LinearShuntCompensator):
#             # load all attributes onto obj from a custom query for specific compensator
#             setattr(obj, "b0PerSection", 5)
    
    def create_default_instances(self,feeder_mrid, mrid_list):
        """ Creates an empty CIM object with the correct class type with mRID and name fields populated
        
        @param: feeder_id: str: 
        
        """
        """Example function with types documented in the docstring.

        `PEP 484`_ type annotations are supported. If attribute, parameter, and
        return types are annotated according to `PEP 484`_, they do not need to be
        included in the docstring:

        Args:
            param1 (int): The first parameter.
            param2 (str): The second parameter.

        Returns:
            bool: The return value. True for success, False otherwise.

        .. _PEP 484:
            https://www.python.org/dev/peps/pep-0484/

        """
        
        query_message = """
            PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX c:  <http://iec.ch/TC57/CIM100#>
            SELECT ?eqid ?eqname ?class
            {
              VALUES ?fdrid {"%s"}
              VALUES ?eqid {"""%feeder_mrid
        for mrid in mrid_list:
            query_message += ' "%s" \n'%mrid

        query_message += """               } 
              ?fdr c:IdentifiedObject.mRID ?fdrid.
              ?eq c:IdentifiedObject.name ?eqname.
              ?eq c:IdentifiedObject.mRID ?eqid.
              ?eq a ?classraw.
              bind(strafter(str(?classraw),"CIM100#") as ?class)
            }
            GROUP BY  ?eqid ?eqname ?class
            ORDER by  ?fdrid
            """
        #print(query_message)
#         results = gapps.query_data(query = query_message, timeout = 60)
#         output = results['data']['results']['bindings']

        if self.sparql is None:
            self.sparql = SPARQLWrapper(self.url)
            self.sparql.setReturnFormat(JSON)
        self.sparql.setQuery(query_message)

        output = self.sparql.query().convert()
#         print(output)
        
        objects = []
        for result in output['results']['bindings']:
            print(result)
            cls = result['class']['value']
            mrid = result['eqid']['value']
            try:
                objects.append(eval(f"cim.{cls}(mRID='{mrid}')"))
                print(cls)
            except:
                print('warning: object class missing:', cls)
        return objects