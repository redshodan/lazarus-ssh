BUILD=../build
TBUILD=$(BUILD)/third_party

UNITTEST2_VER=0.5.1
UNITTEST2_TAR=unittest2-$(UNITTEST2_VER).tar.gz
UNITTEST2_SRC=$(TBUILD)/unittest2-$(UNITTEST2_VER)
UNITTEST2_BUILD=$(TBUILD)/unittest2
# UNITTEST2_EGG=$(UNITTEST2_BUILD)/lib/python/Unittest2-$(UNITTEST2_VER)-py$(PYVER)-*.egg
UNITTEST2_EGG=$(UNITTEST2_BUILD)/lib/python/site.py
UNITTEST2_INSTALL=$(BUILD)/python/unittest2
UNITTEST2_ABS_BUILD=$(shell python -c "import os.path; print os.path.abspath(\"$(UNITTEST2_BUILD)\");")

PKGS=unittest2
TINSTALL=$(UNITTEST2_INSTALL)
PYVER=$(shell python -c "import sys; print sys.version[:3]")
BDIRS=$(TBUILD) $(UNITTEST2_BUILD)/lib/python

all: $(BDIRS) $(PKGS)

$(BDIRS):
	mkdir -p $@

unittest2: $(UNITTEST2_INSTALL)

$(UNITTEST2_INSTALL): $(UNITTEST2_EGG)
	rm -rf $@
	cp -r $(UNITTEST2_BUILD)/lib/python/unittest2-*egg/unittest2 $@

$(UNITTEST2_EGG): $(UNITTEST2_SRC)
	(cd $(UNITTEST2_SRC); python setup.py build)
	(cd $(UNITTEST2_SRC); PYTHONPATH=$(UNITTEST2_ABS_BUILD)/lib/python python setup.py install --home $(UNITTEST2_ABS_BUILD))

$(UNITTEST2_SRC): $(UNITTEST2_TAR)
	rm -rf $(UNITTEST2_SRC)
	(cd $(TBUILD); tar -zxf ../../third_party/$(UNITTEST2_TAR))

clean:
	rm -rf $(TBUILD) $(TINSTALL) $(M2CRYPTO_SRC) $(UNITTEST2_SRC)
