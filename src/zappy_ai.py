#!/usr/bin/env python3

import socket
import argparse
import sys
import select

class Player:
    def __init__(self):
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
    # Supprimer les crochets
    input_string = input_string.replace('[', '').replace(']', '')
    # Utilisation de split pour diviser la chaîne par des virgules
    items = input_string.split(',')
    # Utilisation de strip pour enlever les espaces
    cleaned_items = [item.strip() for item in items]
    return cleaned_items

def find_keyword_in_list(strings, keyword):
    indices = []
    for index, string in enumerate(strings):
        if keyword in string:
            indices.append(index)
    return indices

def count_words_at_index(strings, index):
    if 0 <= index < len(strings):
        # Diviser la chaîne en mots, filtrer les "egg" et retourner le nombre de mots restants
        words = strings[index].split()
        words = [word for word in words if word != "egg"]
        return len(words)
    else:
        raise IndexError("Index out of range")
    
def remove_element(strings, index, element):
    if 0 <= index < len(strings):
        strings[index] = strings[index].replace(element, "", 1)
    else:
        raise IndexError("Index out of range")

def send_and_remove(client_socket, player, index, element):
    data_send = f"Take {element}\n"
    print(f"Sending: {data_send}", end="")
    client_socket.send(data_send.encode())
    remove_element(player.view, index, element)
    player.queue.append(data_send)

def going_forward(client_socket, player):
    data_send = "Forward\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.look = False
    player.view = []
    player.queue.append(data_send)

def looking(client_socket, player):
    data_send = "Look\n"
    print(f"Sending : {data_send}", end="")
    client_socket.send(data_send.encode())
    player.look = True
    player.queue.append(data_send)

def check_stones(player, index):
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
    else :
        return False

def netcat_client(host, port, name):
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
                if data_rec.decode() == "Elevation underway\n":
                    continue
                if player.look == True and player.view == [] :
                    player.view = split_by_commas(data_rec.decode())
                if len(player.queue) > 0 :
                    if data_rec.decode() == f"Current level: {player.level + 1}\n" and player.queue[0] == "Incantation\n":
                        player.incanting = False
                        player.level += 1
                    player.queue.pop(0)

            if player.look == False : # actions
                if len(player.queue) > 0 :
                    continue
                looking(client_socket, player)
            
            if can_evolve(client_socket, player) or player.incanting :
                continue

            if player.look == True and player.view != [] :
                if count_words_at_index(player.view, 0) > 1 and 0 in find_keyword_in_list(player.view, "food") :
                    #take food
                    send_and_remove(client_socket, player, 0, "food")
                elif count_words_at_index(player.view, 0) > 1 :
                    stone = check_stones(player, 0)
                    if stone != None :
                        send_and_remove(client_socket, player, 0, stone)
                else :
                    going_forward(client_socket, player)

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
