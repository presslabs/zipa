BUILD_DIR:=build
VENV:=$(BUILD_DIR)/virtualenv

testenv: $(VENV)/bin/py.test

test: testenv
	$(VENV)/bin/py.test tests

$(VENV)/bin/py.test: $(VENV)/bin/pip requirements-test.txt
	$(VENV)/bin/pip install -Ur requirements-test.txt
	touch $@

$(VENV)/bin/pip:
	virtualenv $(VENV)

clean:
	$(RM) -r $(BUILD_DIR)

.PHONY: clean test testenv
