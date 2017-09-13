# ChatRoom
A chat server that connects multiple clients using non-blocking sockets and supports multi-channel messaging 
(inspired by UC Berkeley course CS168: Internet Architecture and Protocol)


## Functionalities
The application supports 3 types of control messages:
- `/join <channel>`: allows client to join an existing channel
- `/create <channel>`: client creates a new channel and automatically joins that channel
- `/list`: list out all currently existing channels

When a client first connects, s/he will need to join an existing channel or create a new channel to start chatting. Messages can only be seen by clients in the same channel.

Note: 
- the server currently can listen to up to 5 clients simultaneously (using non-blocking sockets)
- currently the default setting is any messages exchanged are within 200-character length
- all code written in Python 2


## Usage
- start server: in new terminal, type "python server.py <port_number>". 
- start client: in new terminal, type "python client.py <client_name> <client_address> <server_port_number>". 
If connection is successful, terminal will show "[Me]", and client can type in messages after that. (Note: "[Me]" = client's own messages,
"[another_name]" = messages from another client in the same channel)


