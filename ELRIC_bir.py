# Main interface for ELRIC
# Import socket to enable IRC connections
import socket
import time
import random

#import other ELRIC classes
import Helpers.irc_functions as irc_functions
import Helpers.text_functions as text_functions


COMMON_WORDS = ["a", "and", "the", "some", "if", "of", "or", "to", "is", "it", "it's", "its", "he", "she", "they", "we", "you", "us", "his", "hers", "theirs", "ours", "yours", "her", "their", "our", "your", "he's", "he'll", "she's", "she'll", "they're", "they'll", "they've", "we're", "we'll", "we've", "you're", "you'll", "you've", "was", "were", "am", "are", "seem", "be", "will", "been", "has", "have", "had", "so", "there", "who", "what", "why", "who", "where", "when", "on", "i", "my", "in", "used", "could", "at", "get", "k", "y", "u", "do", "what's", "what're", "this"] 
PUNCTUATION = ".,/:;-!?*&"

def information_retrieval(message, bot_nick):
    COMMON_WORDS.append(bot_nick.lower())
    message = text_functions.remove_items_from_string(message, PUNCTUATION)
    original_keywords = message.lower().split() #there is a difference between keywords and original keywords because all the original keywords are used to narrow down the matches to get a single response
    keywords = text_functions.remove_items_from_list(original_keywords, COMMON_WORDS)
    if len(keywords) == 0:
        return get_random_confused_response()[0][random.randint(0,1)]
    
    keyword_matches = get_random_confused_response()
    loop_count = 0
    while len(keyword_matches) == 1 and loop_count < 50:
        keyword = get_keyword(keywords)
        keyword_matches = get_initial_keyword_matches(keyword)
        loop_count += 1
    final_keyword_matches = get_final_keyword_matches(keyword_matches, original_keywords)
    match = final_keyword_matches[random.randint(0, len(final_keyword_matches) - 1)][random.randint(0, 1)]
    #return "The keyword ~%s~ found the match ~%s~ with %d matching words" % (keyword, match, matching_words_max)
    return match

def get_initial_keyword_matches(keyword):
    keyword_matches = get_random_confused_response()
    loop_count = 0
    while len(keyword_matches) == 1 and loop_count < 100: #will look through 100 random files for the randomly selected keyword before giving up
        log_file_index = random.randint(1, 666) #chooses between the log files
        if log_file_index > 150:
            log_file_index += 162
        f_path = "logs/log%d.txt" % log_file_index
        log_file = open(f_path)
        previous_line = ""
        for line in log_file: # making a 2D array of all lines with matches to the keyword and responses to those matches
            line = line.replace('\n','')
            line = line.replace('\r','')
            if previous_line != "": #if the previous line had a match, add the match and its response to the 2D array of matches
                keyword_matches.append([previous_line, line])
            temp_line = text_functions.remove_items_from_string(line.lower(), PUNCTUATION) # remove the punctuation from the string
            temp_line_list = temp_line.split()
            if keyword in temp_line_list:
                #keyword_matches.append([previous_line, line])
                previous_line = line
            else:
                previous_line = ""
        loop_count += 1
    return keyword_matches

def get_final_keyword_matches(keyword_matches, original_keywords):
    matching_words_max = 0
    final_keyword_matches = []
    for lines in keyword_matches: #making a list of the matches with the highest number of matching words
        matching_words = 0
        temp_line = lines[0].lower()
        temp_line_list = temp_line.split()
        for original_keyword in original_keywords: #checking each keyword against each line in the list and counting occurances of this
            if original_keyword in temp_line_list:
                matching_words += 1
        if matching_words > matching_words_max: #replacing the old list of matches if there are a higher number of matches on the current string
            matching_words_max = matching_words
            final_keyword_matches = [lines]
        elif matching_words == matching_words_max: #otherwise adding to the list of matches
            final_keyword_matches.append(lines)
    return final_keyword_matches

def get_keyword(keywords):
    keyword = keywords[random.randint(0, (len(keywords) - 1))]
    return keyword

def get_random_confused_response():
    decision = random.randint(0, 10)
    if decision == 1:
        response = [["o.o", "O.o"]]
    elif decision == 2:
        response = [["hm", ":|"]]
    elif decision == 3:
        response = [["?", ":3"]]
    elif decision == 4:
        response = [["huh", "wtf"]]
    elif decision == 5:
        response = [["heh", "huh?"]]
    elif decision == 6:
        response = [["oh my...", "wut"]]
    elif decision == 7:
        response = [["ok", "sorry"]]
    elif decision == 8:
        response = [["fuck", "damn"]]
    elif decision == 9:
        response = [["whatever", "I'm confused"]]
    else:
        response = [["blech", "/me twiddles thumbs"]]
    return response
