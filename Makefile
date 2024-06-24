##
## EPITECH PROJECT, 2024
## Zappy_AI
## File description:
## Makefile
##

MAKEFLAGS += -j

all:
	@sleep 0.2
	@cp src/zappy_ai.py .
	@mv zappy_ai.py zappy_ai
	@chmod 777 zappy_ai
	@echo -e "\033[1;33mBuilding zappy_ai...\033[0m"
	@sleep 0.1
	@echo -e "\033[1;32mZappy_ai built successfully!\033[0m"

run-test:
	PYTHONPATH=src python -m unittest tests/unit-tests/test_zappy_ai.py
	@rm -rf tests/unit-tests/__pycache__
	@rm -rf src/__pycache__

clean:
	@echo -e "\033[1;33mDeleting zappy_ai...\033[0m"
	@rm -rf zappy_ai
	@echo -e "\033[1;31mzappy_ai deleted successfully!\033[0m"
	@echo -e "\033[1;33mCleaning...\033[0m"
	@rm -rf *.txt
	@rm -rf vgcore.*
	@sleep 0.1
	@echo -e "\033[1;32mEverything is clean now!\033[0m"

fclean: clean

pull:
	@git pull

re: clean all
