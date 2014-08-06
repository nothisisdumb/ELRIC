# Main interface for ELRIC
# Import needed classes
import socket
import time
import aiml
import random

#import other ELRIC classes
import Helpers.irc_functions as irc_functions
import ELRIC_bir as bir

def main():# define class variables
    server = raw_input("What is the server you would like to connect to? (ex: irc.example.net) ")
    channel = raw_input("What is the channel you would like to connect to? (ex: #test_channel) ")
    bot_nick = raw_input("What is the nick you would like ELRIC to use? ")
    backup_bot_nick = bot_nick
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #set up the PyAIML Kernel
    k = aiml.Kernel()
    k.learn("AIML/std-brain.aiml")

    k.setBotPredicate("name", bot_nick)

    # connect to the server and register nick
    ircsock.connect((server, 6667))
    print ircsock.recv (4096)
    ircsock.send("USER "+ bot_nick +" "+ bot_nick +" "+ bot_nick +": 1234\n")
    ircsock.send("NICK "+ bot_nick +"\n")
    
    irc_msg = ""
    #this loops receives the messages from the server and analyzes them
    #TODO add parser when irc_msg contains PRIVMSG, this is where the AI aspect of ELRIC will come into play, move the "QUIT" to be part of this AI
    while (irc_msg.find("!die") == -1):
        irc_msg = ircsock.recv(2048) # receives messages from the server
        irc_msg = irc_msg.strip('\n\r') # strips the extra characters for readability
        print(irc_msg) # prints the server messages to the console
        if irc_msg.find('is now your displayed host') != -1: # this allows ELRIC to know when it has connected to the server and can join the channel
            irc_functions.join_channel(ircsock, channel) # join the channel
    
        elif irc_msg.find("PING :") != -1: # responds to server PINGs so ELRIC is not kicked
            irc_functions.ping(ircsock)
            
        elif irc_msg.find('PRIVMSG') != -1 and irc_msg.find(channel) != -1: # this is a user communicating
		
            if irc_msg.lower().find(bot_nick.lower()) != -1: # if the user has said Elric's name
                message = ':'.join(irc_msg.split (':')[2:]) #Split the command from the message
                print message
                if message.lower().find(channel) == -1: #ensuring it is from the correct channel
                    input_nick = irc_msg.split('!')[0]
                    input_nick = input_nick.replace(":", "")
                    user_input = message.lower()
                    print("%s said: %s" % (input_nick, user_input))
                    response = k.respond(user_input)
                    if response == "" or response == "huh?":
                        response = bir.information_retrieval(user_input, bot_nick)
                    if response.startswith('/me'):
                        response = response.replace('/me', '\001ACTION')
                        response += '\001'
                    print response
                    irc_functions.send_message(ircsock, channel, response)
    
    ircsock.send ( 'QUIT\r\n' )

def type_time(response):
    time.sleep(len(response) / 4)

if __name__ == '__main__':
    main()
