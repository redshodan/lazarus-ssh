TSRC=$(shell find tests -name '*.py')
TOBJS=$(patsubst %, build/%c, $(TSRC))
DIRS=$(shell find tests -type d) python
BDIRS=$(patsubst %, build/%, $(DIRS)) build/runs


all: build

build:
	python setup.py build

install:
	python setup.py install

sdist:
	python setup.py sdist

$(BDIRS):
	mkdir -p $@

clean-run:
	rm -rf build/runs/*

third_party: $(BDIRS)
	make -C third_party

tests: $(BDIRS) clean-run third_party $(TOBJS)
	(cd build/runs; python ../tests/run.pyc $(ARGS))

third_party-clean:
	make -C third_party clean

clean: third_party-clean
	python setup.py clean
	rm -rf build/ dist/ lssh.log

build/tests/%.pyc: tests/%.py
	python -c "import sys, py_compile; py_compile.compile(sys.argv[1], sys.argv[2], doraise=True)" $< $@

.PHONY: build install tests third_party
