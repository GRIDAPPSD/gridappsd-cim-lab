from typing import Dict, List



def query_string_parser(obj_dict:Dict, mRID:str, query:List, key:str):
    try:
        setattr(obj_dict[mRID], key, query[key]['value'])
    except:
        []
        
def query_class_parser(obj_dict:Dict, mRID:str, query:List, class_name:str):
    try: 
        cls = class_name
        setattr(obj_dict[mRID], class_name, eval(f"{cls}(mRID='{query[class_name]['value']}')"))
    except:
        []
        
def query_list_parser(obj_dict:Dict, mRID:str, query:List, key, separator):
    #print(query[key]['value'].split(separator))
    try: 
        setattr(obj_dict[mRID], key, query[key]['value'].split(separator))
    except:
        []