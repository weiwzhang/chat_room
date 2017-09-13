# default setting: all messages exchanged between servers are within 200 characters
MESSAGE_LENGTH = 200    

#### Client util messages ####

# Error message printed when a client can't connect to the server host and port that were passed in.
CLIENT_CANNOT_CONNECT = "Unable to connect to {0}:{1}"

# Error message printed before exiting, if the server disconnected.
CLIENT_SERVER_DISCONNECTED = "Server at {0}:{1} has disconnected"

# Printed at the beginning of new lines in the client.
CLIENT_MESSAGE_PREFIX = "[Me] "

# Wipe out "[Me]" in client terminal and print out received message at the right indentation.
CLIENT_WIPE_ME = "\r    "


#### Server messages ####

# The client sent a control message (a message starting with "/") that doesn't fit standard format 
# of any of the valid messages
SERVER_INVALID_CONTROL_MESSAGE = \
  "{0} is not a valid control message. Valid messages are /create, /list, and /join."

# Error message returned when a client attempts to join a channel that doesn't exist.
SERVER_NO_CHANNEL_EXISTS = "No channel named {0} exists. Try '/create {0}'?"

# Error message sent to a client that uses the "/join" command without a channel name.
SERVER_JOIN_REQUIRES_ARGUMENT = "/join command must be followed by the name of a channel to join."

# Message sent to all clients in a channel when a new client joins.
SERVER_CLIENT_JOINED_CHANNEL = "{0} has joined"

# Message sent to all clients in a channel when a client leaves.
SERVER_CLIENT_LEFT_CHANNEL = "{0} has left"

# Error message sent to a client that tries to create a channel that doesn't exist.
SERVER_CHANNEL_EXISTS = "Room {0} already exists, so cannot be created."

# Error message sent to a client that uses the "/create" command without a channel name.
SERVER_CREATE_REQUIRES_ARGUMENT = \
  "/create command must be followed by the name of a channel to create"

# Error message sent to a client that sends a regular message before joining any channels.
SERVER_CLIENT_NOT_IN_CHANNEL = \
  "Not currently in any channel. Must join a channel before sending messages."
