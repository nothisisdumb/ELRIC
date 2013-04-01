# Main interface for ELRIC
# Import socket to enable IRC connections
import socket

#import other ELRIC classes
import Greet.greet as greet
import IRC_Functions.irc_functions as irc_functions

def main():
    # define class variables
    server = "irc.epic-chat.net" # the IRC server
    channel = "#LambdaTest" # the channel within that server
    bot_nick = "Elric" # the name (nick) that the bot will use within the server
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to the server and register nick
    ircsock.connect((server, 6667))
    print ircsock.recv (4096)
    ircsock.send("USER "+ bot_nick +" "+ bot_nick +" "+ bot_nick +": totally not a bot\n")
    ircsock.send("NICK "+ bot_nick +"\n")

    irc_msg = ""
    #this loops receives the messages from the server and analyzes them
    #TODO add parser when irc_msg contains PRIVMSG, this is where the AI aspect of ELRIC will come into play, move the "QUIT" to be part of this AI
    while (irc_msg.find("get outta here") == -1):
        irc_msg = ircsock.recv(2048) # receives messages from the server
        irc_msg = irc_msg.strip('\n\r') # strips the extra characters for readability
        print(irc_msg) # prints the server messages to the console
        if irc_msg.find('Welcome to the Epic-Chat IRC Network') != -1: # this allows ELRIC to know when it has connected to the server and can join the channel
            irc_functions.join_channel(ircsock, channel) # join the channel

        if irc_msg.find("PING :") != -1: # responds to server PINGs so ELRIC is not kicked
            irc_functions.ping(ircsock)

    ircsock.send ( 'QUIT\r\n' )

if __name__ == '__main__':
    main()
