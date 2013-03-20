all: dragon

dragon:
	python dragon.py

clean:
	rm -rf dragon.pyc
	rm -rf dragon_debug_*.log

