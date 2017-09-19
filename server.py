import socket
import sys
import select
from collections import defaultdict
import utils


class BasicServer(object):
    
    def __init__(self, port):
        self.socket = socket.socket()
        self.socket.bind(("", int(port)))
        self.socket.listen(5)
        self.socket_lst = [self.socket]
        self.channels = defaultdict(list)    # {channel: [list of sockets]}
        self.s_to_info = {}    # {socket: [name, channel]}
        self.s_to_msg = defaultdict(str)    # {socket: msg (buffering)}
        self.new_client = False   
    
    def start(self):
        while True:
            sockets_read, sockets_write, sockets_error = select.select(self.socket_lst, [], [], 0)
            for socket in sockets_read:
                # case 1: server socket
                if socket is self.socket:
                    (client_socket, address) = self.socket.accept()
                    self.socket_lst.append(client_socket)
                    self.new_client = True
                # case 2: client sockets
                else:
                    try:
                        self.s_to_msg[socket] += socket.recv(1024)
                        if len(self.s_to_msg[socket]) >= 200:
                            msg = (self.s_to_msg[socket][:200]).rstrip()
                            self.s_to_msg[socket] = self.s_to_msg[socket][200:]
                            # case 2.1: new client 1st msg ==  client name
                            if self.new_client:
                                self.s_to_info[socket] = [msg, None]
                                self.new_client = False
                            # case 2.2: control messages
                            elif msg[0] == '/':   
                                if msg[1:5] == "join":
                                    channel_name = msg[6:]
                                    socket_name = self.s_to_info[socket][0]
                                    if not channel_name:
                                        self.broadcast([socket], utils.SERVER_JOIN_REQUIRES_ARGUMENT)
                                        continue
                                    if not (channel_name in self.channels):
                                        self.broadcast([socket], utils.SERVER_NO_CHANNEL_EXISTS.format(channel_name))
                                        continue
                                    self.broadcast(self.channels[channel_name], utils.SERVER_CLIENT_JOINED_CHANNEL.format(socket_name))
                                    self.channels[channel_name].append(socket)
                                    prev_channel = self.s_to_info[socket][1]
                                    if prev_channel:
                                        self.channels[prev_channel].remove(socket)
                                        self.broadcast(self.channels[prev_channel], utils.SERVER_CLIENT_LEFT_CHANNEL.format(socket_name))
                                    self.s_to_info[socket][1] = channel_name
                                elif msg[1:7] == "create":
                                    channel_name = msg[8:]
                                    socket_name = self.s_to_info[socket][0]
                                    if not channel_name:
                                        self.broadcast([socket], utils.SERVER_CREATE_REQUIRES_ARGUMENT)
                                        continue
                                    if self.channels[channel_name]:
                                        self.broadcast([socket], utils.SERVER_CHANNEL_EXISTS.format(channel_name))
                                        continue
                                    self.channels[channel_name].append(socket)
                                    prev_channel = self.s_to_info[socket][1]
                                    if prev_channel:
                                        self.channels[prev_channel].remove(socket)
                                        self.broadcast(self.channels[prev_channel], utils.SERVER_CLIENT_LEFT_CHANNEL.format(socket_name))
                                    self.s_to_info[socket][1] = channel_name
                                elif msg[1:5] == "list":
                                    invalid_args = msg[5:]
                                    if invalid_args:
                                        self.broadcast([socket], utils.SERVER_INVALID_CONTROL_MESSAGE.format(msg))
                                        continue
                                    channels_lst = self.channels.keys()
                                    self.broadcast([socket], "\n".join(channels_lst))
                                else:
                                    self.broadcast([socket], utils.SERVER_INVALID_CONTROL_MESSAGE.format(msg))
                                    continue
                            # case 2.3: normal messages
                            else:
                                channel = self.s_to_info[socket][1]
                                if channel:
                                    self.broadcast(self.channels[channel], "[{0}] ".format(self.s_to_info[socket][0]) + msg)
                                else:
                                    self.broadcast([socket], utils.SERVER_CLIENT_NOT_IN_CHANNEL)
                                    continue
                        # client down
                        elif not self.s_to_msg[socket]:
                            self.socket_lst.remove(socket)
                            socket_name, socket_channel = self.s_to_info[socket]
                            if socket_channel:
                                self.channels[socket_channel].remove(socket)
                                self.broadcast(self.channels[socket_channel], utils.SERVER_CLIENT_LEFT_CHANNEL.format(socket_name))
                            del self.s_to_info[socket]
                            del self.s_to_msg[socket]
                    except Exception as e:
                        print(e)
                        raise(e)

    def broadcast(self, sockets, msg):
        msg = msg.ljust(utils.MESSAGE_LENGTH)
        for s in sockets:
            if s is not self.socket:
                s.sendall(msg)


# handle command line input
args = sys.argv
if len(args) != 2:
    print "Please supply a port."
    sys.exit()
server = BasicServer(args[1])
server.start()