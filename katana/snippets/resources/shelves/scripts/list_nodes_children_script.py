"""
NAME: listNodesChildren_Script
ICON: icon.png
DROP_TYPES:
SCOPE:
Enter Description Here

"""

# The following symbols are added when run as shelf buttons:
# exit():      Allows 'error-free' early exit from the script.
# dropEvent:   If your script registers DROP_TYPES, this is a QDropEvent
#              upon a valid drop. Otherwise, it is None.
#              Example:  Registering for "nodegraph/nodes" DROP_TYPES
#                        allows the user to get dropped nodes using
#       nodes = [NodegraphAPI.GetNode(x) for x in
#               str(dropEvent.encodedData( 'nodegraph/nodes' )).split(',')]
# console_print(message, raisePanel = False):
#              If the Python Console exists, print the message to it.
#              Otherwise, print the message to the shell. If raisePanel
#              is passed as True, the panel will be raised to the front.

import sys

SNIPPETS_PATH = "/usr/people/thomas-ma/Developement/Snippets/katana"
not SNIPPETS_PATH in sys. path and sys.path.append(SNIPPETS_PATH)

import snippets.libraries.utilities

snippets.libraries.utilities.single_shot_script_node("/usr/people/thomas-ma/Developement/Snippets/katana/snippets/resources/recipes/listNodesChildren_Script_vLatest.katana", "listNodesChildren")
