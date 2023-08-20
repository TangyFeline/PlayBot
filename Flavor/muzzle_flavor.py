MUZZLE_FLAVORS = {
    "muzzle":{
        "defaults":["Woof", "Bark", "Arf"],
        "start":[
            "{muzzler} has muzzled {victim}."
        ],
        "talk":[
            "{victim} tried to say a disallowed word."
        ],
        "end":[
            "{muzzler} has released {victim}."
        ],
        "subtry":[
            "{muzzler} is a sub and cannot muzzle others."
        ],
        "struggle":[
            "{struggler} struggles helplessly against {struggler.his} muzzle."
        ],
        "escape":[
            "{struggler} breaks out of {struggler.his} muzzle!"
        ]
    }
}

STRUGGLING_ALLOWED_DIALOG = "{sub} will be allowed to struggle free from {sub.his} muzzle."
STRUGGLING_NOT_ALLOWED_DIALOG = "{sub} will not be allowed to struggle free from {sub.his} muzzle."
NO_FORCE_PRONOUNS_DIALOG = "{sub} will be called by {sub.his} normal pronouns."
FORCE_PRONOUNS_DIALOG = "{sub} will be referred to exclusively using **{pronouns}** pronouns."
CHOOSE_PRONOUNS_TEXT = "Choose which pronouns to refer to {sub} exclusively by."
NO_ALLOWED_WORDS = "No allowed words!" # Someone was muzzled with no words.