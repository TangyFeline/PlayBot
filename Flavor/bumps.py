from Bump.components import *
from Bump.constants import *

SUB_BUMP_MESSAGES = {
    "default": BumpFlavor(thumbnail="")
                .add("Thanks for bumping the server, Sub {bumper}!"),
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The above displays when a sub bumps but we have no flavor text for any kinks they have.   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    "ExampleKink": BumpFlavor(thumbnail="")
                .add("{bumper} bumped the server! {bumper.He} is a good sub. Or switch."),
}

DOM_BUMP_MESSAGES = {
    "default": BumpFlavor(thumbnail="")
            .add("Thanks for bumping the server, Dom {bumper}!"),
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The above displays when a dom bumps but we have no flavor text for any kinks they have.   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    "ExampleKink": BumpFlavor(thumbnail="")
                .add("{bumper} bumped the server! {bumper.He} is a good dom. Or switch."),
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# These messages show if the person bumping is missing any sub/switch/dom roles at all.     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
DEFAULT_BUMP_MESSAGES = {
    "default": BumpFlavor(thumbnail="")
            .add("Thanks for bumping the server, {bumper}!"),
}