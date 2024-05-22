#!/usr/bin/env python3

import socket
import argparse
import sys
import select

class Player:
    def __init__(self):
        self.view = []
        self.look = False

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
        # Diviser la chaîne en mots et retourner le nombre de mots
        return len(strings[index].split())
    else:
        raise IndexError("Index out of range")
    
def remove_element(strings, index, element):
    if 0 <= index < len(strings):
        strings[index] = strings[index].replace(element, "", 1)
    else:
        raise IndexError("Index out of range")

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
                if player.look == True and player.view == [] :
                    player.view = split_by_commas(data_rec.decode())

            if player.look == False : # actions
                data_send = "Look\n"
                print(f"Sending : {data_send}", end="")
                client_socket.send(data_send.encode())
                player.look = True

            if player.look == True and player.view != [] :
                if count_words_at_index(player.view, 0) > 1 and 0 in find_keyword_in_list(player.view, "food") :
                    #take food
                    data_send = "Take object\n"
                    print(f"Sending : {data_send}", end="")
                    client_socket.send(data_send.encode())
                    remove_element(player.view, 0, "food")
                else :
                    data_send = "Forward\n"
                    print(f"Sending : {data_send}", end="")
                    client_socket.send(data_send.encode())
                    player.look = False
                    player.view = []

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
