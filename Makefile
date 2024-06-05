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

run-test:
	PYTHONPATH=src python -m unittest tests/unit-tests/test_zappy_ai.py
	@rm -rf tests/unit-tests/__pycache__
	@rm -rf src/__pycache__

clean:
	rm -rf zappy_ai

fclean: clean

re: clean all
