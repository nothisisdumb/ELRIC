import Helpers.text_functions as text_functions

PUNCTUATION = ".,!?:@;"

def main():
    #nicks = []
    #f1_path = "old_logs/log1.txt"
    #for i in range(1, 151):
        #f_path = "old_logs/log%d.txt" % i
        #nicks = get_nick_list(nicks, f_path)
    #for i in range(313, 829):
        #f_path = "old_logs/log%d.txt" % i
        #nicks = get_nick_list(nicks, f_path)

    #nick_file = open("nick_list.txt", "w")
    #for nick in nicks:
        #nick_file.write(nick + "\n")
    #nick_file.close()
    #raw_input("Enter any key to continue >> ")
    nicks = []
    nick_file = open("nick_list.txt")
    for line in nick_file:
        if line.rstrip().lower() not in nicks:
            nicks.append(line.rstrip().lower())
    print "Finished with making nick list. %d nicks listed." % len(nicks)

    for i in range(1, 151):
        f_path = "old_logs/log%d.txt" % i
        remove_nicks(nicks, f_path)
    for i in range(313, 829):
        f_path = "old_logs/log%d.txt" % i
        remove_nicks(nicks, f_path)
    print nicks

def get_nick_list(nick_list, f_path):
    f = open(f_path)
    for line in f:
        if line[0] != '*':
            second_nick_index = line.find('>')
            if(second_nick_index != -1):
                nick = line[1:second_nick_index]
                if nick not in nick_list:
                    nick_list.append(nick)
    return nick_list

def remove_nicks(nick_list, f_path):
    f = open(f_path)
    print "Now parsing: %s" % f_path
    f2 = open(f_path.replace("old_logs/", "logs/"), "w")
    for line in f:
        can_write = True
        new_line = ""
        if line[0] == '*':
            second_nick_index = line.find(' ')
            if(second_nick_index != -1):
                new_line = line.replace(line[0:(second_nick_index)], '/me')
        elif line[0] == '<':
            second_nick_index = line.find('>')
            if(second_nick_index != -1):
                new_line = line.replace(line[0:(second_nick_index+2)], '')
        new_line_list = text_functions.remove_items_from_string(new_line, PUNCTUATION).lower().split()
        for nick in nick_list:
            if nick in new_line_list:
                can_write = False
                break
        if can_write:
            f2.write(new_line)
    f2.close()
    print "Finished parsing: %s" % f_path

if __name__ == '__main__':
    main()
