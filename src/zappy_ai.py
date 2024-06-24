#!/usr/bin/env python3

"""
@file zappy_ai.py
@brief File containing every functions related to ai.
"""

import socket
import argparse
import sys
import select
import random
import time

class Player:
    """
    @class Player
    @brief Class containing every player related informations.
    """
    def __init__(self):
        """
        @brief Class constructor of Player.
        @param level Level of the player.
        @param incanting To know if the player is incanting or not.
        @param view Contains the informations the player is able to see when he looks.
        @param look To know if the player asked to server what he sees.
        @param queue The queue that the player sent to server.
        @param linemate The number of linemates the player has.
        @param deraumere The number of deraumere the player has.
        @param sibur The number of sibur the player has.
        @param mendiane The number of mendiane the player has.
        @param phiras The number of phiras the player has.
        @param thystame The number of thystame the player has.
        @param max_linemate The number of linemate the player needs to level up to 8.
        @param max_deraumere The number of deraumere the player needs to level up to 8.
        @param max_sibur The number of sibur the player needs to level up to 8.
        @param max_mendiane The number of mendiane the player needs to level up to 8.
        @param max_phiras The number of phiras the player needs to level up to 8.
        @param max_thystame The number of thystame the player needs to level up to 8.
        """
        self.level = 1
        self.incanting = False
        self.wants_incanting = False #
        self.need_to_go = None #
        self.nb_r = 0 #
        self.view = []
        self.look = False
        self.queue = []
        self.linemate = 0
        self.deraumere = 0
        self.sibur = 0
        self.mendiane = 0
        self.phiras = 0
        self.thystame = 0
        self.max_linemate = 9
        self.max_deraumere = 8
        self.max_sibur = 10
        self.max_mendiane = 5
        self.max_phiras = 6
        self.max_thystame = 1
        self.food = 10 #
        self.starve = None #
        self.should_stop = None
        self.follow = 0
        self.just_inc = False

def split_by_commas(input_string):
    """
    @brief Splits the string received into a list.
    @param input_string String to split.
    @return List created from the string.
    """
    input_string = input_string.replace('[', '').replace(']', '')
    items = input_string.split(',')
    cleaned_items = [item.strip() for item in items]
    return cleaned_items

def find_keyword_in_list(strings, keyword):
    """
    @brief Finds the index of every keyword in the list.
    @param strings List of words.
    @param keyword Word to find in the list.
    @return A list of every indexes where the keyword is in the list.
    """
    indices = []
    for index, string in enumerate(strings):
        if keyword in string:
            indices.append(index)
    return indices

def count_words_at_index(strings, index):
    """
    @brief Counts the number of words in a list at a certain index (excluding the words "egg" and "player").
    @param strings List of strings.
    @param index Index where to count in the list.
    @return Number of words in the list at the given index.
    """
    if 0 <= index < len(strings):
        words = strings[index].split()
        words = [word for word in words if word != "egg" and word != "player"]
        return len(words)
    else:
        return 0

def remove_element(strings, index, element):
    """
    @brief Removes a word in a list at a given index.
    @param strings List of strings.
    @param index Index where to delete the word.
    @param element Word to delete in the list.
    """
    if 0 <= index < len(strings):
        strings[index] = strings[index].replace(element, "", 1)
    else:
        print("Index out of range (remove_element).")

def send_and_remove(client_socket, player, index, element):
    """
    @brief Sends a string to a socket and then calls remove_element, adds the send to the player.queue.
    @param client_socket The socket where to send the string.
    @param player The player class where the information to delete are.
    @param index The index where to delete a word.
    @param element A part of the message to send and the word to delete.
    """
    data_send = f"Take {element}\n"
    print(f"Sending: {data_send}", end="")
    client_socket.send(data_send.encode())
    remove_element(player.view, index, element)
    player.queue.append(data_send)

def going_forward(client_socket, player):
    """
    @brief Sends Forward to the socket and put back player.look to false and player.view to [], adds the send to the player.queue.
    @param client_socket Socket where to send the string.
    @param player Player class containing view, look and queue.
    """
    data_send = "Forward\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.look = False
    player.view = []
    player.queue.append(data_send)

def turning_right(client_socket, player):
    """
    @brief Sends Right to the socket, adds the send to the player.queue.
    @param client_socket Socket where to send the string.
    @param player Player class containing queue.
    """
    data_send = "Right\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

def turning_left(client_socket, player):
    """
    @brief Sends Left to the socket, adds the send to the player.queue.
    @param client_socket Socket where to send the string.
    @param player Player class containing queue.
    """
    data_send = "Left\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.queue.append(data_send)

def looking(client_socket, player):
    """
    @brief Sends Look to the socket, adds the send to the player.queue and set player.look to true.
    @param client_socket Socket where to send the string.
    @param player Player class containing queue.
    """
    data_send = "Look\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.look = True
    player.queue.append(data_send)

def check_stones(player, index):
    """
    @brief Checks if there is a stone still needed by the player at an index of player.view.
    @param player Player class containing view and all stone related informations.
    @param index Index to look at for stones still needed.
    @return Returns the name of the stone if there is one needed, else return None.
    """
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

def check_level_two(player, client_socket) :
    if (not 0 in find_keyword_in_list(player.view, "linemate")) and player.linemate == 0 :
        return False
    if (not 0 in find_keyword_in_list(player.view, "deraumere")) and player.deraumere == 0 :
        return False
    if (not 0 in find_keyword_in_list(player.view, "sibur")) and player.sibur == 0 :
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 16 :
        player.starve = None
        return False

    if (not 0 in find_keyword_in_list(player.view, "sibur")) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    if (not 0 in find_keyword_in_list(player.view, "deraumere")) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    if (not 0 in find_keyword_in_list(player.view, "linemate")) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    return True

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
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 18 :
        player.starve = None
        return False

    while (l < 2) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        l += 1
    if (s < 1) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    while (p < 2) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        p += 1
    return True

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
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 25 :
        player.starve = None
        return False
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # l += 1
    if (d < 1) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    while (s < 2) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    if (p < 1) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # p += 1
    return True

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
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 25 :
        player.starve = None
        return False
    
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # l += 1
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    if (s < 1) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # s += 1
    while (m < 3) :
        player.mendiane -= 1
        data_send = "Set mendiane\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        m += 1
    return True

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
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 30 :
        player.starve = None
        return False
    
    if (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # l += 1
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    while (s < 3) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    if (p < 1) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        # p += 1
    return True

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
    m = player.view[0].count("mendiane")
    if (m + player.mendiane) < 2 :
        return False
    p = player.view[0].count("phiras")
    if (p + player.phiras) < 2:
        return False
    t = player.view[0].count("thystame")
    if (t + player.thystame) < 1:
        return False
    
    if player.starve == None:
        data_send = "Inventory\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        return False
    elif player.starve < 30 :
        player.starve = None
        return False
    
    while (l < 1) :
        player.linemate -= 1
        data_send = "Set linemate\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        l += 1
    while (d < 2) :
        player.deraumere -= 1
        data_send = "Set deraumere\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        d += 1
    while (s < 2) :
        player.sibur -= 1
        data_send = "Set sibur\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        s += 1
    while (p < 2) :
        player.phiras -= 1
        data_send = "Set phiras\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        p += 1
    while (m < 2) :
        player.mendiane -= 1
        data_send = "Set mendiane\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
        m += 1
    if (t < 1) :
        player.thystame -= 1
        data_send = "Set thystame\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        player.queue.append(data_send)
    return True

def can_evolve(client_socket, player):
    """
    @brief Checks if the conditions are met to evolve, if so set player.incanting to true and adds the request to evolve to player.queue.
    @param client_socket Socket where to send the string.
    @param player Player class containing queue and incanting.
    @return True if the player can evolve, else false.
    """
    if player.incanting == True or player.need_to_go != None or player.should_stop == 1 :
        return False
    if player.view != [] :
        if player.level == 1:
            if player.view[0].count("player") >= 2:
                return False
            if player.view[0].count("linemate") >= 1:
                data_send = "Incantation\n"
                print(f"Sending : {data_send}", end="")
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
                return True
            else :
                return False
        elif player.level == 5 :
            if player.view[0].count("player") >= 2:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_five(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                return True
            else :
                return False
        elif player.level == 6 :
            if player.view[0].count("player") >= 2:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_six(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                return True
            else :
                return False
        elif player.level == 7 :
            if player.view[0].count("player") >= 2 and player.just_inc == False:
                return False
            if player.wants_incanting == True :
                return True
            if check_level_seven(player, client_socket) :
                player.wants_incanting = True
                player.nb_r = 1
                return True
            else :
                return False
        else :
            return False
    else :
        return False

def received_look(player, data_rec):
    """
    @brief Based on the data received after using looking function, if the date is ko, player.look is set to false, else, player.view gets the result of the received data sent to split_by_commas function.
    @param player Player class containing look and view.
    @param data_rec String containing ko or a long string.
    """
    if data_rec.decode() == "ko\n" :
        player.look = False
    else :
        player.view = split_by_commas(data_rec.decode())

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

def inventory(player, data_rec):
    data = split_by_commas(data_rec)
    for item in data:
        if item.startswith("food"):
            _, quantity = item.split()
            player.starve = int(quantity)
            print(f"I have {player.starve} food", file=sys.stderr)
            return

def command_received(player, data_rec):
    """
    @brief Checks the received data to know what to do.
    @param player Player class containing queue.
    @param data_rec String containing ko or a potential instruction.
    """
    print(f"Received: {data_rec.decode()}", end="")

    if data_rec.decode() == "dead\n" :
        return -1
    if data_rec.decode() == "Elevation underway\n":
        return 0

    if "message" in data_rec.decode() :
        words = data_rec.decode().replace('"', '').replace(',', '').split()
        if len(words) > 4 and words[0] == "message" and words[2] == "Level" :
            # if player.should_stop == 2 :
            #     return 0
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
        reduce_max(player)
        if len(player.queue) > 0 :
            if player.queue[0] == "Incantation\n":
                player.just_inc = True
                player.queue.pop(0)
        print(f"Player got level : {player.level}", file=sys.stderr)
        player.should_stop = None
        return 0

    if player.follow > 3 and player.should_stop == 1 and player.need_to_go == None :
        player.nb_r = 0
        player.wants_incanting = False
        player.incanting = False
        player.should_stop = None

    if len(player.queue) > 0 :
        player.follow += 1
        if "Inventory" in player.queue[0] :
            inventory(player, data_rec.decode())
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
            player.incanting = False
            player.need_to_go = None
        player.queue.pop(0)
    

def moving_level(client_socket, player):
    """
    @brief Checks with the information in player.view where to move.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    indices = find_keyword_in_list(player.view, "food")

    if count_words_at_index(player.view, 2) > 0 and (check_stones(player, 2) != None or 2 in indices):
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
        r = random.random()
        if r > 0.4 :
            going_forward(client_socket, player)
        elif r > 0.2 :
            going_forward(client_socket, player)
            turning_left(client_socket, player)
            going_forward(client_socket, player)
        else :
            going_forward(client_socket, player)
            turning_right(client_socket, player)
            going_forward(client_socket, player)

def go_to_need(client_socket, player):
    if player.need_to_go == 0 :
        data_send = f"Broadcast \"Level {player.level} c\"\n"
        player.nb_r += 1
        print(f"Sending : {data_send}", end="")
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
    player.need_to_go = None

def moving_player(client_socket, player):
    """
    @brief Checks the player level to know what move to do.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    if player.need_to_go != None :
        if incant_nb(player) and player.need_to_go == 0 :
            # player.incanting = True
            # player.nb_r = 0
            player.need_to_go = 0
            return
        go_to_need(client_socket, player)
        return
    moving_level(client_socket, player)

def incant_nb(player):
    if (player.level == 2 or player.level == 3) and player.nb_r >= 2 :
        return True
    if (player.level == 4 or player.level == 5) and player.nb_r >= 4 :
        return True
    if (player.level == 6 or player.level == 7) and player.nb_r >= 6 :
        return True
    return False

def command_send(client_socket, player):
    """
    @brief Checks informations in player class to know what command to do.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    if player.wants_incanting == True :
        if player.should_stop == 1 :
            player.wants_incanting = False

            return
        if len(player.queue) >= 1 :
            return
        else :
            if incant_nb(player) :
                data_send = "Incantation\n"
                print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                player.incanting = True
                player.nb_r = 0
                player.wants_incanting = False
                return #evolve
            data_send = f"Broadcast \"Level {player.level} r\"\n"
            print(f"Sending : {data_send}", end="")
            client_socket.send(data_send.encode())
            player.queue.append(data_send)
    if player.look == False : 
        if len(player.queue) > 0 :
            return
        looking(client_socket, player)
    
    if can_evolve(client_socket, player) or player.incanting or player.wants_incanting :
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

def netcat_client(host, port, name):
    """
    @brief What i should have called "Main", creates the socket, the player class, use select and has the main loop.
    @param host IP address of the host.
    @param port Port of the host.
    @param name Name of the team to join.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    player = Player()

    sockets_to_read = [client_socket]
    print(f"Received: {client_socket.recv(1024).decode()}", end="")
    try:
        data_send = name + "\n"
        print(f"Sending : {data_send}", end="")
        client_socket.send(data_send.encode())
        while 1 :
            data_rec = client_socket.recv(1024)
            if data_rec.decode() == "ko\n":
                time.sleep(0.5)
                data_send = name + "\n"
                print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
            elif data_rec.decode() == "This team is full, please wait\n" :
                print(f"{data_rec.decode()}")
                data_rec = client_socket.recv(1024)
                break
            elif data_rec.decode() == "Wrong team name, please try again\n" :
                print("Wrong team name. Closing...")
                exit(0)
            else:
                break

        d = 0
        print(data_rec.decode, end="")
        while True:

            ready_to_read, _, _ = select.select(sockets_to_read, [], [], 0.1)
            
            if client_socket in ready_to_read:
                data_rec = client_socket.recv(1024)
                # print(f"Received: {data_rec.decode()}", end="")
                
                # if data_rec.decode() == "dead\n": # receptions
                #     break
                commands = data_rec.decode().splitlines(keepends=True)
                for command in commands:
                    d = command_received(player, command.encode())
                    if d == -1 :
                        break
                if d == -1 :
                    break
            # print(f"N : {player.need_to_go}")
            command_send(client_socket, player)

        print("Player session ended", file=sys.stderr)
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
