from Bump.components import *
from Bump.constants import *

SUB_BUMP_MESSAGES = {
    "default": BumpFlavor(thumbnail="")
                .add("Thanks for bumping the server, Sub {bumper}!"),
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The above displays when a sub bumps but we have no flavor text for any kinks they have.   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    "Spanking": BumpFlavor(thumbnail="")
                .add("Over my knee, {bumper}. I think your bottom needs some special attention.")
                .add("Bend over, {bumper}, I'm about to redden that bottom of yours.")
                .add("Time for your maintenance spanking, {bumper}. Tell your friends goodbye, unless you'd like to invite them to watch.")
                .add("Remember to regularly spank {bumper}, {bumper.heis} much more compliant after a session over someone's lap.")
                ,
    "Dumbification": BumpFlavor(thumbnail="")
                .add("It's a good thing {bumper} is cute, because there's not much going on in {bumper.his} head.")
                .add("Everyone congratulate {bumper} on learning how to spell 'bump'.")
                ,
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