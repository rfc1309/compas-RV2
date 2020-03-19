# .rv2 File Format Specification

```python
{
    # session stores info about the user session,
    # includes file location, creation time, system and version etc
    "session":{

    }

    # stores metadata of scene and metadata of each contained nodes
    "scene":{

        # global settings for scene TODO: consider to move to session
        "settings": {
            "visualisation.color.vertices": (255,0,0),
            "visualisation.color.edges": (0,255,0),
            #...
        },

        # metadata for each scene nodes
        "nodes": {

            "{node_uuid1}":{
                "name": "FormDiagram", # user specified name for the node
                "type": "RhinoFormDiagram", # the object wrapper class name
                "data_type": "FormDiagram", # the data class name
                
                "matrix": [], # 4x4 transformation matrix
                "visible": True,
                "children": ["node_uuids"]
            },
            # "{node_uuid2}":{}...
        }
    }

    # serialised data for each nodes
    "data":{
        
         "{node_uuid1}": {},
         # "{node_uuid2}":{}...
    
    }

}
```