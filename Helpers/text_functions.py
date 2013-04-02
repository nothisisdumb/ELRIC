def remove_items_from_string(message, PUNCTUATION):
    new_message = ""
    for letter in message:
        if letter.lower() not in PUNCTUATION:
            new_message += letter
    return new_message

def remove_items_from_list(old_list, REMOVEABLES):
    new_list = []
    for item in old_list:
        if item.lower() not in REMOVEABLES:
            new_list.append(item)
    return new_list
