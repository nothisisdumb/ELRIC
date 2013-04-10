import socket

#ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# function to respond to server PINGs
def ping(ircsock):
    ircsock.send("PONG :Pong\n")

# function to send messages to the channel
def send_message(ircsock, chan , message):
    ircsock.send("PRIVMSG "+ chan +" "+ message +"\n") 

# function used to join a channel
def join_channel(ircsock, chan):
    ircsock.send("JOIN "+ chan +"\n")
