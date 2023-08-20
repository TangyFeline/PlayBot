# Static
RENAMING_CONSENT_ACCEPTED = "Enjoy your new name!" # DM - User clicked the consent button.

# Variable

# Alert in a channel that a user has been renamed.
# renamer: A mention of the person renaming
# target: A mention of the user being renamed
SUCCESSFULLY_RENAMED = [
    "{renamer} has given {target} a new name.",
    "{target} has been renamed by {renamer}."
]
# Example: @DonnaTheDom has given @SallyTheSub a new name.

# A Renamer with Rename Me tried to rename themselves.
# renamer: A mention of the person renaming
ERROR_SELF_RENAME = [
    "You cannot rename yourself, {renamer}. You goof. Feel humiliated. Shame.",
    "Bad {renamer}, no renaming yourself, rawr.",
    "{renamer}! No self-renaming. Shaaaaame.",
    "For shame, {renamer}, you can't rename yourself."
]
# Example: You cannot rename yourself, @SammyTheSwitch. You goof. Feel humiliated. Shame.

# DM to ask the user if they consent to a rename.
# renamer: A mention of the person renaming
RENAME_CONSENT_DM = "{renamer} would like to rename you! Do you consent?"
# Example: @DonnaTheDom would like to rename you! Do you consent? 

# Feedback to a Renamer after choosing a name for a Rename Me Maybe user.
# target: A mention of the person renaming
RENAMER_WAITING_CONSENT = "You have sent a request to rename {target}."
# Example: You have sent a request to rename @SallyTheSub. (This message is only visible to you.)