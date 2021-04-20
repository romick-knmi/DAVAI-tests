# Variables

all: clean

.PHONY: all clean

clean:
	find . -name "*.pyc"       -print0 | xargs -0r rm
	find . -name "__pycache__" -print0 | xargs -0r rm -r

# Usual target
clobber: clean
