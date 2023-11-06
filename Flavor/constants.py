from Flavor.muzzle_flavor import *
from Flavor.rename_flavor import *
from Flavor.soap_flavor import *
from constants_helper import *

# =~=~=~=~=~=~=~==~=~ Role Names =~=~=~=~=~=~=~=~=~=~ #

# Pronouns
SHE_HER_ROLE = "She/Her" # Can be referred to as she/her
HE_HIM_ROLE = "He/Him" # Can be referred to as he/him
THEY_THEM_ROLE = "They/Them" # Can be referred to as they/them
IT_ITS_ROLE = "It/Its" # Can be referred to as it/its

# Renaming
RENAMER_ROLE = "Renamer" # Can rename others
RENAME_ME_ROLE = "Rename Me" # Can be renamed
RENAME_ME_CONSENT_ROLE = "Rename Me Maybe?" # Can be renamed, with a consent check

# Muzzling
MUZZLE_ME_ROLE = "Muzzle Me" # Can be muzzled
MUZZLE_CONSENT_ROLE = "Muzzle Me Maybe?" # Can be muzzled, with a consent check
SUB_ROLE = "Active Sub" # Role that cannot muzzle, and is teased for trying.
CAN_MUZZLE_ROLES = ["Active Dom", "Active Switch"] # Roles that can muzzle.
CAN_RELEASE_ROLES = ["Active Dom", "Active Switch"] # Roles that can release from muzzles.

# Transforming
TRANSFORM_ME_ROLE = "Transform Me" # Can be transformed
TRANSFORM_CONSENT_ROLE = "Transform Me Maybe" # Can be transformed, with a consent check
TRANSFORM_SUB_ROLE = "Active Sub" # Role that cannot transform, and is teased for trying.
CAN_TRANSFORM_ROLES = ["Active Dom", "Active Switch"] # Roles that can transform.
CAN_RELEASE_TRANSFORM_ROLES = ["Active Dom", "Active Switch"] # Roles that can release from transforms.

# Swearing
SOAP_ROLE = "Soapy" # People with this role will be scolded if swearing is detected.

# =~=~=~=~=~=~=~==~ Constant Values =~=~=~=~=~=~=~=~=~ #
STRUGGLE_CHANCE =  0.1 # Percentile chance to struggle out of a muzzle. 1 in 10.
STRUGGLE_TIMEOUT = 10 # How long before you can struggle again. In seconds.
SOAPY_APOLOGY_MIN_LENGTH = 100
SOAPY_APOLOGY_MAX_LENGTH = 2000
SAFEWORDS = [
    ":red_safeword:",
    ":yellow_safeword:",
    ":green_safeword:"
]

# =~=~=~=~=~=~=~==~ Static Messages =~=~=~=~=~=~=~=~=~ #
# Error Messages
ERROR_NOT_RENAMER = f"You do not have the {RENAMER_ROLE} role and cannot rename!" # Someone tried to rename without Renamer.
ERROR_NOT_RENAME_ME = f"That person does not have the {RENAME_ME_ROLE} or {RENAME_ME_CONSENT_ROLE} roles and cannot be renamed." # A Renamer tried to rename someone without Rename Me.

ERROR_CANT_MUZZLE = f"You do not have the {pretty_list(CAN_MUZZLE_ROLES)} role and cannot muzzle others." # Someone tried to muzzle someone without any muzzler roles or sub roles.
ERROR_CANT_BE_MUZZLED = f"That person does not have the {MUZZLE_ME_ROLE} or {MUZZLE_CONSENT_ROLE} roles and cannot be muzzled."
ERROR_CANT_RELEASE = f"You do not have the {pretty_list(CAN_RELEASE_ROLES)} role and cannot release from a muzzle."
ERROR_CANNOT_RELEASE_SELF = "You can't release yourself from a muzzle." # Someone tried to /release themselves.
ERROR_STRUGGLE_NOT_MUZZLED = "Struggle against what? You aren't muzzled!" # Someone tried to /struggle without being in a muzzle. Ephemeral.
ERROR_STRUGGLE_NOT_ALLOWED = "You can't struggle out of this muzzle." # Someone tried to /struggle but struggling was disabled for this muzzle.

ERROR_CANT_TRANSFORM = f"You do not have the {pretty_list(CAN_TRANSFORM_ROLES)} role and cannot transform others." # Someone tried to transform someone without any roles or sub roles.
ERROR_CANT_BE_TRANSFORMED = f"That person does not have the {TRANSFORM_ME_ROLE} or {TRANSFORM_CONSENT_ROLE} roles and cannot be transformed."
ERROR_CANT_RELEASE_TRANSFORM = f"You do not have the {pretty_list(CAN_RELEASE_TRANSFORM_ROLES)} role and cannot release someone from a transformation."
ERROR_CANNOT_RELEASE_SELF_TRANSFORM = "You can't release yourself from a transformation." # Someone tried to /release themselves while transformed.

ERROR_NOT_RESTRICTING = "You are not restricting anyone." # Someone tried to /release without having anyone muzzled/transformed. Ephemeral.
ERROR_NOT_RESTRICTING_TARGET = "That person does not seem to be restricted." # Someone tried to /release @target and their target that was not in a muzzle or transformation. Ephemeral.

# =~=~=~=~=~=~=~= Variable Messages =~=~=~=~=~=~=~=~=~ #
# Feedback to a Muzzler after choosing to muzzle a Muzzle Me Maybe user.
# victim: A mention of the person being muzzled
MUZZLER_WAITING_CONSENT = ["You have sent a request to muzzle {victim}."]
# Example: You have sent a request to muzzle @SallyTheSub. (This message is only visible to you.)

# DM to ask the user if they consent to being muzzled.
# muzzler: A mention of the person trying to muzzle
# channel: The id of the channel that the request was sent from.
MUZZLE_CONSENT_DM = ["{muzzler} is trying to muzzle you in <#{channel}>!\n\nDo you consent?"]
TRANSFORM_CONSENT_DM = ["{muzzler} is trying to transform you in <#{channel}>!\n\nDo you consent?"]
# Example: @DonnaTheDom is trying to muzzle you in [PlayRoom->#blush-chat]! Do you consent?

# Feedback to a user consenting to being muzzled.
# muzzler: A mention of the person trying to muzzle
# channel: The id of the channel that the request was sent from.
MUZZLING_CONSENT_ACCEPTED = ["You're muzzled now! Head to <#{channel}> and tell {muzzler} how you feel about it."] # DM - User consented to muzzling.
TRANSFORM_CONSENT_ACCEPTED = ["You're transformed now! Head to <#{channel}> and tell {muzzler} how you feel about it."] # DM - User consented to transforming.

ERROR_CANT_STRUGGLE_YET = "You can't struggle yet." # Someone tried to struggle, but has struggled recently. Ephemeral.


# =~=~=~=~=~=~=~= Technical Errors =~=~=~=~=~=~=~=~=~=~ #
TECHNICAL_ERROR_PERMISSION_DENIED = "🔧 Permission denied! You either tried to rename the server owner, or the bot's permissions are misconfigured. 🔧"
