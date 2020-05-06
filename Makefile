
default: run

test:
	python3 -m unittest --locals exponentiation_test.py

run:
	python3 main.py