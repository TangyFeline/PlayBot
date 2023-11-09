from Transform.transform_types import *

TRANSFORM_FLAVORS = {
    "dronify":{
        "start":[
            "{transformer} has dronified {victim}."
        ],        
        "end":[
            "{transformer} has reverted {victim}."
        ],
        "subtry":[
            "{transformer} is a sub and cannot transform others."
        ],

        "classtouse": DroneTransformation,
        "args":['dronify']
    },
    "plushify":{
        "start":[
            "{transformer} has plushified {victim}."
        ],        
        "end":[
            "{transformer} has reverted {victim}."
        ],
        "subtry":[
            "{transformer} is a sub and cannot transform others."
        ],

        "classtouse": PlushTransformation,
        "args":['plushify']
    },
    "pettify":{
        "start":[
            "{transformer} has pettified {victim}."
        ],        
        "end":[
            "{transformer} has reverted {victim}."
        ],
        "subtry":[
            "{transformer} is a sub and cannot transform others."
        ],

        "classtouse": PetTransformation,
        "args":['pettify']
    }
}
