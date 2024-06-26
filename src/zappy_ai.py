#!/usr/bin/env python3

## @file zappy_ai.py
## @brief File containing every functions related to ai.

import socket
import argparse
import sys
import select
import random
import time

## Player class containing every player related information.
class Player:

    ## Class constructor of Player.
    #
    ##        Initializes a new player with default values for all attributes.
    def __init__(self):

        ## The level of the player.
        ## Go from 1 to 8.
        self.level = 1
        ## To know if the player is currently incanting.
        ## Can be True or False.
        self.incanting = False
        ## Indicates if the player is ready to evolve.
        ## Can be True or False.
        self.wants_incanting = False
        ## Indicates where the player needs to go.
        ## Go from 0 to 9.
        self.need_to_go = None
        ## Number of players of the same level ready to evolve.
        ## No maximum, but go back to 0 when the number of player ready to evolve reach the requisites.
        self.nb_r = 0
        ## Contains the information the player can see when they look.
        ## Gets more information scaling with level.
        self.view = []
        ## Indicates if the player asked the server what they see.
        ## True if he did else False
        self.look = False
        ## The queue of actions the player sent to the server.
        ## You have to take care not to fill it more than 10 because it doesn't allow queue bigger than 10.
        self.queue = []
        ## The number of linemates the player has.
        self.linemate = 0
        ## The number of deraumere the player has.
        self.deraumere = 0
        ## The number of sibur the player has.
        self.sibur = 0
        ## The number of mendiane the player has.
        self.mendiane = 0
        ## The number of phiras the player has.
        self.phiras = 0
        ## The number of thystame the player has.
        self.thystame = 0
        ## The number of linemate the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_linemate = 9
        ## The number of deraumer the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_deraumere = 8
        ## The number of sibur the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_sibur = 10
        ## The number of mendiane the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_mendiane = 5
        ## The number of phiras the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_phiras = 6
        ## The number of thystame the player needs to level up to 8.
        ## This maximum is modified when leveling up.
        self.max_thystame = 1
        ## The remaining food of the player.
        ## Set to a number after asking for Inventory to the server, reseted after used.
        self.starve = None
        ## Indicates if the player should stop broadcasting.
        ## None if no indication, 1 if should stop, 2 if should continue.
        self.should_stop = None
        ## The time since the person the player is following last gave news.
        ## Increment each time you execute a command in the server.
        self.follow = 0
        ## Indicates if the player was the originator of the incantation.
        self.just_inc = False
        ## Indicates if the player needs to plant an egg (perform a Fork on the server).
        self.plant = False
        ## Indicates if the player asked for an Inventory check at Level 8.
        ## False if he asked, True if not.
        self.inventory_b = True

## Splits the string received into a list.
## @param input_string String to split.
## @return List of strings created from the input string.
##
##        This function takes an input string, removes any square brackets,
## splits the string by commas, and returns a list of cleaned items.
def split_by_commas(input_string):
    input_string = input_string.replace('[', '').replace(']', '')
    items = input_string.split(',')
    cleaned_items = [item.strip() for item in items]
    return cleaned_items

## Finds the index of every keyword in the list.
## @param strings List of words.
## @param keyword Word to find in the list.
## @return A list of indexes where the keyword is found in the list.
##
##       This function searches through a list of strings and returns a list
##       of all the indices where the keyword appears.
def find_keyword_in_list(strings, keyword):
    indices = []
    for index, string in enumerate(strings):
        if keyword in string:
            indices.append(index)
    return indices

## Counts the number of words in a list at a certain index, excluding "egg" and "player".
## @param strings List of strings.
## @param index Index where to count the words in the list.
## @return Number of words in the list at the given index.
##
##        This function counts the number of words at a specified index in a list of strings,
##        excluding the words "egg" and "player". If the index is out of range, it returns 0.
def count_words_at_index(strings, index):
    if 0 <= index < len(strings):
        words = strings[index].split()
        words = [word for word in words if word != "egg" and word != "player"]
        return len(words)
    else:
        return 0

## Removes a word in a list at a given index.
## @param strings List of strings.
## @param index Index where to delete the word.
## @param element Word to delete in the list.
## 
##        This function removes the first occurrence of the specified element
##        from the string at the given index of the list. If the index is out of
##        range, it prints an error message.
def remove_element(strings, index, element):
    if 0 <= index < len(strings):
        strings[index] = strings[index].replace(element, "", 1)
    else:
        print("Index out of range (remove_element).")

## Sends a string to a socket and then calls remove_element, adds the send to the player.queue.
## @param client_socket The socket where to send the string.
## @param player The player class instance containing the information to delete.
## @param index The index where to delete a word.
## @param element A part of the message to send and the word to delete.
## 
##       This function sends a formatted string to the specified client socket, 
##       removes the element from the player's view at the given index using 
##       remove_element, and appends the sent data to the player's action queue.
def send_and_remove(client_socket, player, index, element):
    data_send = f"Take {element}\n"
    # print(f"Sending: {data_send}", end="")
    client_socket.send(data_send.encode())
    remove_element(player.view, index, element)
    player.queue.append(data_send)

## Sends the command "Forward" to the socket, resets player's look and view, and adds the command to the player's queue.
## 
## @param client_socket The socket to which the "Forward" command is sent.
## @param player The Player class instance containing player's state, including view, look, and queue.
## 
##       This function sends the "Forward" command to the specified client socket and appends the command to player.queue.
def going_forward(client_socket, player):
    data_send = "Forward\n"
    # print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

## Sends the command "Right" to the socket and adds the command to the player's queue.
## @param client_socket Socket to which the command is sent.
## @param player Player class instance containing queue.
##
##       This function sends the "Right" command to the specified client socket and appends the command to player.queue.
def turning_right(client_socket, player):
    data_send = "Right\n"
    # print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

## Sends the command "Left" to the socket and adds the command to the player's queue.
## @param client_socket Socket to which the command is sent.
## @param player Player class instance containing queue.
##
##        This function sends the "Left" command to the specified client socket and appends the command to player.queue.
def turning_left(client_socket, player):
    data_send = "Left\n"
    # print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

## @brief Sends the command "Look" to the socket, sets player.look to True, and adds the command to the player's queue.
## @param client_socket Socket to which the command is sent.
## @param player Player class instance containing queue and look.
##
##       This function sends the "Look" command to the specified client socket, sets player.look to True, and appends the command to player.queue.
def looking(client_socket, player):
    data_send = "Look\n"
    # print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.look = True
    player.queue.append(data_send)

## @brief Checks if there is a stone still needed by the player at a given index in player.view.
## @param player Player class instance containing view and stone-related attributes.
## @param index Index in the player's view to check for needed stones.
## @return The name of the needed stone if found, otherwise None.
##
##       This function checks the specified index in player.view for stones
##       that the player still needs. If a needed stone is found, its name 
##       is returned; otherwise, None is returned.
def check_stones(player, index):
    if 0 <= index < len(player.view):
        items = player.view[index].split()
        for item in items:
            if item == "food":
                return "food"
            if item == "linemate" and player.linemate < player.max_linemate:
                return "linemate"
            elif item == "deraumere" and player.deraumere < player.max_deraumere:
                return "deraumere"
            elif item == "sibur" and player.sibur < player.max_sibur:
                return "sibur"
            elif item == "mendiane" and player.mendiane < player.max_mendiane:
                return "mendiane"
            elif item == "phiras" and player.phiras < player.max_phiras:
                return "phiras"
            elif item == "thystame" and player.thystame < player.max_thystame:
                return "thystame"
    return None

## @brief Checks if the player can evolve to level three.
## @param player Player class instance containing view, linemate, deraumere, sibur, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level three, otherwise False.
## 
##       This function checks if the player has the necessary items to evolve to level three.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_two(player, client_socket) :
    if (not 0 in find_keyword_in_list(player.view, "linemate")) and player.linemate == 0 :
        return False
    if (not 0 in find_keyword_in_list(player.view, "deraumere")) and player.deraumere == 0 :
        return False
    if (not 0 in find_keyword_in_list(player.view, "sibur")) and player.sibur == 0 :
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 16 :
        player.just_inc = False
        player.starve = None
        return False

    if (not 0 in find_keyword_in_list(player.view, "sibur")) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    if (not 0 in find_keyword_in_list(player.view, "deraumere")) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    if (not 0 in find_keyword_in_list(player.view, "linemate")) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    return True

## @brief Checks if the player can evolve to level four.
## @param player Player class instance containing view, linemate, deraumere, sibur, phiras, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level four, otherwise False.
##
##       This function checks if the player has the necessary items to evolve to level four.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_three(player, client_socket) :
    l = player.view[0].count("linemate")
    if (l + player.linemate) < 2:
        return False
    s = player.view[0].count("sibur")
    if (s + player.sibur) < 1 :
        return False
    p = player.view[0].count("phiras")
    if (p + player.phiras) < 2:
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 18 :
        player.just_inc = False
        player.starve = None
        return False

    while (l < 2) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        l += 1
    if (s < 1) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    while (p < 2) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        p += 1
    return True

## @brief Checks if the player can evolve to level five.
## @param player Player class instance containing view, linemate, deraumere, sibur, phiras, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level five, otherwise False.
##
##       This function checks if the player has the necessary items to evolve to level five.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_four(player, client_socket) :
    l = player.view[0].count("linemate")
    if (l + player.linemate) < 1:
        return False
    d = player.view[0].count("deraumere")
    if (d + player.deraumere) < 1:
        return False
    s = player.view[0].count("sibur")
    if (s + player.sibur) < 2 :
        return False
    p = player.view[0].count("phiras")
    if (p + player.phiras) < 1:
        return False
    if player.starve == None:
        data_send = "Inventory\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 25 :
        player.just_inc = False
        player.starve = None
        return False
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # l += 1
    if (d < 1) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    while (s < 2) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    if (p < 1) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # p += 1
    return True

## @brief Checks if the player can evolve to level six.
## @param player Player class instance containing view, linemate, deraumere, sibur, mendiane, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level six, otherwise False.
##
##       This function checks if the player has the necessary items to evolve to level six.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_five(player, client_socket) :
    l = player.view[0].count("linemate")
    if (l + player.linemate) < 1:
        return False
    d = player.view[0].count("deraumere")
    if (d + player.deraumere) < 2:
        return False
    s = player.view[0].count("sibur")
    if (s + player.sibur) < 1 :
        return False
    m = player.view[0].count("mendiane")
    if (m + player.mendiane) < 3:
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        # player.inventory_b = False
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 25 :
        player.just_inc = False
        player.starve = None
        return False
    
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    if (s < 1) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # s += 1
    while (m < 3) :
        player.mendiane -= 1
        data_send = "Set mendiane\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        m += 1
    return True

## @brief Checks if the player can evolve to level seven.
## @param player Player class instance containing view, linemate, deraumere, sibur, phiras, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level seven, otherwise False.
##
##       This function checks if the player has the necessary items to evolve to level seven.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_six(player, client_socket) :
    l = player.view[0].count("linemate")
    if (l + player.linemate) < 1:
        return False
    d = player.view[0].count("deraumere")
    if (d + player.deraumere) < 2:
        return False
    s = player.view[0].count("sibur")
    if (s + player.sibur) < 3 :
        return False
    p = player.view[0].count("phiras")
    if (p + player.phiras) < 1:
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 30 :
        player.just_inc = False
        player.starve = None
        return False
    
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # l += 1
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    while (s < 3) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    if (p < 1) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # p += 1
    return True

## @brief Checks if the player can evolve to level eight.
## @param player Player class instance containing view, linemate, deraumere, sibur, mendiane, phiras, thystame, starve, and queue.
## @param client_socket Socket to which the commands are sent.
## @return True if the player can evolve to level eight, otherwise False.
##
##       This function checks if the player has the necessary items to evolve to level eight.
##       If the required items are not in the player's view or inventory, it sends an 
##       inventory request. If the player has insufficient food, the evolution is halted.
def check_level_seven(player, client_socket) :
    l = player.view[0].count("linemate")
    if (l + player.linemate) < 2:
        return False
    d = player.view[0].count("deraumere")
    if (d + player.deraumere) < 2:
        return False
    s = player.view[0].count("sibur")
    if (s + player.sibur) < 2 :
        return False
    p = player.view[0].count("phiras")
    if (p + player.phiras) < 2:
        return False
    m = player.view[0].count("mendiane")
    if (m + player.mendiane) < 2 :
        return False
    t = player.view[0].count("thystame")
    if (t + player.thystame) < 1:
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        player.inventory_b = False
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 30:
        player.starve = None
        player.just_inc = False
        return False

    while (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        l += 1
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    while (s < 2) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    while (p < 2) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        p += 1
    while (m < 2) :
        player.mendiane -= 1
        data_send = "Set mendiane\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        m += 1
    if (t < 1) :
        player.thystame -= 1
        data_send = "Set thystame\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    return True

## @brief Checks if the conditions are met to evolve, if so set player.incanting to true and adds the request to evolve to player.queue.
## @param client_socket Socket where to send the string.
## @param player Player class containing queue and incanting.
## @return True if the player can evolve, else false.
##
##       This function determines whether the player can evolve to the next level by checking 
##       the necessary conditions. If the conditions are met, it sends an incantation request 
##       and sets the player's incanting state to True.
def can_evolve(client_socket, player):
    if player.incanting == True or player.need_to_go != None or player.should_stop == 1 :
        return False
    if player.view != [] :
        if player.level == 1:
            if player.view[0].count("player") >= 2:
                return False
            if player.view[0].count("linemate") >= 1:
                data_send = "Incantation\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                player.incanting = True
                return True
            else :
                return False
        elif player.level == 2 :
            if player.view[0].count("player") >= 2:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_two(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        elif player.level == 3 :
            if player.view[0].count("player") >= 2:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_three(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        elif player.level == 4 :
            if player.view[0].count("player") >= 2:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_four(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        elif player.level == 5 :
            if player.view[0].count("player") >= 2 and player.just_inc == False:
                return False
            # player.just_inc = False
            if player.wants_incanting == True :
                return True
            if check_level_five(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        elif player.level == 6 :
            if player.view[0].count("player") >= 2 and player.just_inc == False:
                return False
            # player.just_inc = False
            if player.wants_incanting == True :
                return True
            if check_level_six(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        elif player.level == 7 :
            if player.wants_incanting == True :
                return True
            if check_level_seven(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                return True
            else :
                return False
        else :
            return False
    else :
        return False

## @brief Based on the data received after using the looking function.
## @param player Player class containing look and view.
## @param data_rec String containing 'ko' or a long string.
##
##       Sets player.look to False if data is 'ko', otherwise updates player.view with the result of split_by_commas.
def received_look(player, data_rec):
    if data_rec.decode() == "ko\n" :
        player.look = False
    else :
        player.view = split_by_commas(data_rec.decode())

## @brief Reduces the maximum number of resources required for the player to evolve to the max level based on their current level.
## @param player Player class containing max_* attributes.
def reduce_max(player):
    if player.level == 2:
        player.max_linemate -= 1
    elif player.level == 3:
        player.max_linemate -= 1
        player.max_deraumere -= 1
        player.max_sibur -= 1
    elif player.level == 4:
        player.max_linemate -= 2
        player.max_sibur -= 1
        player.max_phiras -= 2
    elif player.level == 5:
        player.max_linemate -= 1
        player.max_deraumere -= 1
        player.max_sibur -= 2
        player.max_phiras -= 1
    elif player.level == 6:
        player.max_linemate -= 1
        player.max_deraumere -= 2
        player.max_sibur -= 1
        player.max_mendiane -= 3
    elif player.level == 7:
        player.max_linemate -= 1
        player.max_deraumere -= 2
        player.max_sibur -= 3
        player.max_phiras -= 1
    elif player.level == 8:
        player.max_linemate -= 2
        player.max_deraumere -= 2
        player.max_sibur -= 2
        player.max_mendiane -= 2
        player.max_phiras -= 2
        player.max_thystame -= 1

## @brief Updates the player's food quantity based on the received inventory data.
## @param player Player class containing starve attribute.
## @param data_rec String containing inventory data.
def inventory(player, data_rec):
    data = split_by_commas(data_rec)
    for item in data:
        if item.startswith("food"):
            _, quantity = item.split()
            player.starve = int(quantity)
            # print(f"I have {player.starve} food at level {player.level}.")
            return

## @brief Checks the received data to determine the appropriate action.
## @param player Player class containing various attributes related to the game state.
## @param data_rec String containing the received data which could be 'ko', 'dead', 'Elevation underway', 'Current level', or other instructions.
## @return -1 if the player is dead, otherwise 0.
def command_received(player, data_rec):
    # print(f"Received: {data_rec.decode()}", end="")

    if data_rec.decode() == "end\n" :
        return -10
    if data_rec.decode() == "dead\n" :
        return -1
    if data_rec.decode() == "Elevation underway\n":
        return 0

    if "message" in data_rec.decode() :
        words = data_rec.decode().replace('"', '').replace(',', '').split()
        if len(words) > 4 and words[0] == "message" and words[2] == "Level" :
            player_num = words[1]
            player_level = words[3]
            if int(player_level) == int(player.level):
                if words[4] == "c" :
                    player.nb_r += 1
                    if incant_nb(player) and (player.need_to_go != 0 and player.wants_incanting == False) :
                        player.need_to_go = None 
                        player.nb_r = 0
                        player.should_stop = None
                        return 0
                elif words[4] == "r" :
                    player.follow = 0
                    if player.should_stop == None and player.wants_incanting == False :
                        player.should_stop = 1
                    player.need_to_go = int(player_num)
                if player.nb_r == 0 :
                    player.nb_r = 1
        return 0
    
    if data_rec.decode() == f"Current level: {player.level + 1}\n" :
        player.level += 1   
        player.view = []
        player.look = False
        player.nb_r = 0
        player.wants_incanting = False
        player.incanting = False
        player.need_to_go = None
        player.starve = None
        reduce_max(player)
        if len(player.queue) > 0 :
            if player.queue[0] == "Incantation\n":
                player.just_inc = True
                player.queue.pop(0)
            else :
                player.just_inc = False
        else :
            player.just_inc = False
        # print(f"Player got level : {player.level}", file=sys.stderr)
        player.should_stop = None
        player.plant = True
        return 0

    if player.follow > 5 and player.should_stop == 1 and player.need_to_go == None :
        player.nb_r = 0
        player.wants_incanting = False
        player.incanting = False
        player.should_stop = None

    if len(player.queue) > 0 :
        player.follow += 1
        if "Inventory" in player.queue[0] :
            inventory(player, data_rec.decode())
            player.inventory_b = True
        if "Broadcast" in player.queue[0] :
            if player.should_stop == None :
                player.should_stop = 2
            player.queue.pop(0)
            return 0
        if "Take" in player.queue[0]:
            item = player.queue[0].split()[1]
            if hasattr(player, item):
                setattr(player, item, getattr(player, item) + 1)
            player.queue.pop(0)
            return 0
        if player.look == True and player.view == [] and player.queue[0] == "Look\n":
            received_look(player, data_rec)
        if player.queue[0] == "Incantation\n" and data_rec.decode() == "ko\n":
            player.view = []
            player.look = False
            player.nb_r = 0
            player.wants_incanting = False
            player.starve = None
            player.incanting = False
            player.need_to_go = None
            player.should_stop = None
        player.queue.pop(0)
    
## @brief Sends a command to plant an egg.
## @param client_socket Socket used to send the command.
## @param player Player class containing queue.
def plant_egg(client_socket, player):
    data_send = "Fork\n"
    # print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

## @brief Make a random move to avoid clustering of players.
## @param client_socket The socket used to communicate with the server.
## @param player The player object containing the state and attributes of the player.
##
##       This function selects a random move from a predefined set of movements, including
##       the possibility of not moving at all. It executes two random moves consecutively 
##       to maximize the randomness and avoid clustering of players in the same spot.
def make_random_move(client_socket, player):
    moves = [
        going_forward,
        turning_left,
        turning_right,
        lambda s, p: (going_forward(s, p), turning_left(s, p)),
        lambda s, p: (going_forward(s, p), turning_right(s, p)),
        lambda s, p: (turning_left(s, p), going_forward(s, p)),
        lambda s, p: (turning_right(s, p), going_forward(s, p)),
        lambda s, p: None  # No move
    ]

    for _ in range(2):
        move = random.choice(moves)
        if move is not None:
            move(client_socket, player)

## @brief Checks with the information in player.view where to move.
## @param client_socket The socket used to communicate with the server.
## @param player The player object containing the state and attributes of the player.
## 
##       This function decides the next move for the player based on the player's level and the
##       objects in their view. It includes checks to avoid clustering by making a random move
##       when there are too many players in the same position. It also handles special logic
##       for players at level 8 to either check their inventory or make strategic moves based
##       on their starvation level.
def moving_level(client_socket, player):
    indices = find_keyword_in_list(player.view, "food")

    if player.level == 8 :
        if player.starve == None:
            data_send = "Inventory\n"
            player.inventory_b = False
            # print(f"Sending : {data_send}", end="")
            client_socket.send(data_send.encode())
            player.queue.append(data_send)
            return
        elif player.starve > 30 :
            player.starve = None
            r = random.random()
            if r > 0.4 :
                make_random_move(client_socket, player)
            else :
                plant_egg(client_socket, player)
            return
        player.starve = None
    if player.view[0].count("player") > 1 :
        make_random_move(client_socket, player)
    elif count_words_at_index(player.view, 2) > 0 and (check_stones(player, 2) != None or 2 in indices):
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 6) > 0 and (check_stones(player, 6) != None or 6 in indices) and player.level >= 2 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 12) > 0 and (check_stones(player, 12) != None or 12 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 1) > 0 and (check_stones(player, 1) != None or 1 in indices):
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 3) > 0 and (check_stones(player, 3) != None or 3 in indices):
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 5) > 0 and (check_stones(player, 5) != None or 5 in indices) and player.level >= 2 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 7) > 0 and (check_stones(player, 7) != None or 7 in indices) and player.level >= 2 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 4) > 0 and (check_stones(player, 4) != None or 4 in indices) and player.level >= 2 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 8) > 0 and (check_stones(player, 8) != None or 8 in indices) and player.level >= 2 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 11) > 0 and (check_stones(player, 11) != None or 11 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 13) > 0 and (check_stones(player, 13) != None or 13 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 10) > 0 and (check_stones(player, 10) != None or 10 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 14) > 0 and (check_stones(player, 14) != None or 14 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 10) > 0 and (check_stones(player, 10) != None or 10 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 14) > 0 and (check_stones(player, 14) != None or 14 in indices) and player.level >= 3 :
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
        going_forward(client_socket, player)
    else :
        make_random_move(client_socket, player)
    player.look = False
    player.view = []

## @brief Directs the player to the required location based on the value of player.need_to_go.
## @param client_socket Socket used to send commands.
## @param player Player class containing attributes like need_to_go, level, etc.
def go_to_need(client_socket, player):
    if player.need_to_go == 0 :
        data_send = f"Broadcast \"Level {player.level} c\"\n"
        player.nb_r += 1
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        player.wants_incanting = True
        player.should_stop = None
    elif player.need_to_go == 1 :
        going_forward(client_socket, player)
    elif player.need_to_go == 2 :
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 3 :
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 4 :
        turning_left(client_socket, player)
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 5 :
        turning_left(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 6 :
        turning_right(client_socket, player)
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 7 :
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    elif player.need_to_go == 8 :
        going_forward(client_socket, player)
        turning_right(client_socket, player)
        going_forward(client_socket, player)
    player.look = False
    player.view = []
    player.need_to_go = None

## @brief Determines the movement of the player based on their level and state.
## @param client_socket Socket where to potentially send information.
## @param player Player class containing attributes like need_to_go, level, etc.
def moving_player(client_socket, player):
    if player.need_to_go != None :
        if incant_nb(player) and player.need_to_go == 0 :
            return
        go_to_need(client_socket, player)
        return
    moving_level(client_socket, player)

## @brief Checks if the player has reached the required number of players for an incantation.
## @param player Player class containing the level and nb_r (number of players ready for incantation).
## @return True if the required number of players is met, otherwise False.
def incant_nb(player):
    if (player.level == 2 or player.level == 3) and player.nb_r >= 2 :
        return True
    if (player.level == 4 or player.level == 5) and player.nb_r >= 4 :
        return True
    if (player.level == 6 or player.level == 7) and player.nb_r >= 6 :
        return True
    return False

## @brief Checks information in the player class to determine the appropriate command to execute.
## @param client_socket Socket used to send commands.
## @param player Player class containing various attributes indicating the player's state and actions.
def command_send(client_socket, player):
    if player.plant == True :
        plant_egg(client_socket, player)
        player.plant = False

    if player.wants_incanting == True :
        if player.should_stop == 1 :
            return
        if len(player.queue) >= 1 :
            return
        else :
            if incant_nb(player) :
                data_send = "Incantation\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                player.incanting = True
                player.nb_r = 0
                player.wants_incanting = False
                return #evolve
            elif player.should_stop == 2 :
                data_send = f"Broadcast \"Level {player.level} r\"\n"
                # print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)

    if player.look == False : 
        if len(player.queue) > 0 :
            return
        looking(client_socket, player)
    if can_evolve(client_socket, player) or player.incanting or player.wants_incanting :
        return
    if player.inventory_b == False :
        return
    if player.look == True and player.view != [] :
        if count_words_at_index(player.view, 0) > 0 and 0 in find_keyword_in_list(player.view, "food") :
            send_and_remove(client_socket, player, 0, "food")
        elif count_words_at_index(player.view, 0) > 0 :
            stone = check_stones(player, 0)
            if stone != None and player.view[0].count("player") < 2 :
                send_and_remove(client_socket, player, 0, stone)
            else :
                moving_player(client_socket, player)
        else :
            moving_player(client_socket, player)

## @brief Main function that creates the socket, initializes the player class, uses select for I/O multiplexing, and contains the main loop.
## @param host IP address of the host.
## @param port Port of the host.
## @param name Name of the team to join.
def netcat_client(host, port, name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    player = Player()

    sockets_to_read = [client_socket]
    # print(f"Received: {client_socket.recv(1024).decode()}", end="")
    try:
        data_send = name + "\n"
        # print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        while 1 :
            data_rec = client_socket.recv(1024)
            if data_rec.decode() == "ko\n":
                time.sleep(0.5)
                data_send = name + "\n"
                print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
            elif data_rec.decode() == "This team is full, please wait\n" :
                # print(f"{data_rec.decode()}")
                data_rec = client_socket.recv(1024)
                break
            elif data_rec.decode() == "Wrong team name, please try again\n" :
                # print("Wrong team name. Closing...")
                exit(0)
            else:
                break

        d = 0
        # print(data_rec.decode, end="")
        while True:

            ready_to_read, _, _ = select.select(sockets_to_read, [], [], 0.1)
            data_rec = ""
            if client_socket in ready_to_read:
                data_rec = client_socket.recv(2048)
                commands = data_rec.decode().splitlines(keepends=True)
                for command in commands:
                    d = command_received(player, command.encode())
                    if d == -1 or d == -10 :
                        break
                if d == -1 or d == -10 :
                    break
            command_send(client_socket, player)
        if d == -1 :
            print("Player session ended", file=sys.stderr)
        else :
            print("End of the game !", file=sys.stderr)
        return 0
    except KeyboardInterrupt:
        print("Closing...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) == 1 :
        print("usage: zappy_ai.py -p PORT -n NAME [-h MACHINE] [--help]")
        exit(0)
    
    required_args = ['-p', '--port', '-n', '--name']
    missing_args = [arg for arg in required_args if arg not in sys.argv]
    if '-p' not in sys.argv and '--port' not in sys.argv or '-n' not in sys.argv and '--name' not in sys.argv:
        print("usage: zappy_ai.py -p PORT -n NAME [-h MACHINE] [--help]")
        exit(0)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    parser.add_argument("-n", "--name", type=str, required=True, help="Name of the team")
    parser.add_argument("-h", "--machine", type=str, default="localhost", help="Server IP address")
    parser.add_argument("--help", action="help", help="Show this help message and exit")

    try:
        args = parser.parse_args()
        print(args)
        netcat_client(args.machine, args.port, args.name)
    except ValueError:
        print("usage: zappy_ai.py -p PORT -n NAME [-h MACHINE] [--help]")
        exit(0)
