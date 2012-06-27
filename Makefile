all: build

build:
	python setup.py build

install:
	python setup.py install

sdist:
	python setup.py sdist

clean:
	python setup.py clean
	rm -rf build/ dist/ lssh.log

.PHONY: build install
