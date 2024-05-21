##
## EPITECH PROJECT, 2024
## Zappy_AI
## File description:
## Makefile
##

all:
	cp src/zappy_ai.py .
	mv zappy_ai.py zappy_ai
	chmod 777 zappy_ai

clean:
	rm -rf zappy_ai

fclean: clean

re: clean all
