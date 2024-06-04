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
        raise IndexError("Index out of range")

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
        raise IndexError("Index out of range")

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

def can_evolve(client_socket, player):
    """
    @brief Checks if the conditions are met to evolve, if so set player.incanting to true and adds the request to evolve to player.queue.
    @param client_socket Socket where to send the string.
    @param player Player class containing queue and incanting.
    @return True if the player can evolve, else false.
    """
    if player.incanting == True :
        return False
    if player.view != [] :
        if player.level == 1:
            if check_stones(player, 0) == "linemate":
                data_send = "Incantation\n"
                print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.queue.append(data_send)
                player.incanting = True
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

def command_received(player, data_rec):
    """
    @brief Checks the received data to know what to do.
    @param player Player class containing queue.
    @param data_rec String containing ko or a potential instruction.
    """
    if data_rec.decode() == "Elevation underway\n":
        return
    if len(player.queue) > 0 :
        if player.look == True and player.view == [] and player.queue[0] == "Look\n":
            received_look(player, data_rec)
        elif player.queue[0] == "Incantation\n":
            if data_rec.decode() == f"Current level: {player.level + 1}\n" :
                player.level += 1   
            else :
                player.view = []
                player.look = False
            player.incanting = False
        player.queue.pop(0)

def moving_level_one(client_socket, player):
    """
    @brief Checks with the information in player.view where to move when level 1.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    if count_words_at_index(player.view, 2) > 0 :
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 1) > 0 :
        going_forward(client_socket, player)
        turning_left(client_socket, player)
        going_forward(client_socket, player)
    elif count_words_at_index(player.view, 3) > 0 :
        going_forward(client_socket, player)
        turning_right(client_socket, player)
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

def moving_player(client_socket, player):
    """
    @brief Checks the player level to know what move to do.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    if player.level == 1 :
        moving_level_one(client_socket, player)
    if player.level == 2 :
        moving_level_one(client_socket, player)

def command_send(client_socket, player):
    """
    @brief Checks informations in player class to know what command to do.
    @param client_socket Socket where to potentially send information.
    @param player Player class.
    """
    if player.look == False : 
        if len(player.queue) > 0 :
            return
        looking(client_socket, player)
    
    if can_evolve(client_socket, player) or player.incanting :
        return
    if player.look == True and player.view != [] :
        if count_words_at_index(player.view, 0) > 0 and 0 in find_keyword_in_list(player.view, "food") :
            send_and_remove(client_socket, player, 0, "food")
        elif count_words_at_index(player.view, 0) > 0 :
            stone = check_stones(player, 0)
            if stone != None :
                send_and_remove(client_socket, player, 0, stone)
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
        while True:

            ready_to_read, _, _ = select.select(sockets_to_read, [], [], 0.1)
            
            if client_socket in ready_to_read:
                data_rec = client_socket.recv(1024)
                print(f"Received: {data_rec.decode()}", end="")
                
                if data_rec.decode() == "dead\n": # receptions
                    break
                
                command_received(player, data_rec)
            command_send(client_socket, player)

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
