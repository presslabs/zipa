BUILD_DIR:=build
VIRTUAL_ENV?=$(BUILD_DIR)/virtualenv

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

testenv: $(VIRTUAL_ENV)/bin/py.test
devenv: $(VIRTUAL_ENV)/bin/mkdocs

test: testenv
	$(VIRTUAL_ENV)/bin/py.test tests

$(VIRTUAL_ENV)/bin/py.test: $(VIRTUAL_ENV)/bin/pip requirements-test.txt
	$(VIRTUAL_ENV)/bin/pip install -Ur requirements-test.txt
	touch $@

$(VIRTUAL_ENV)/bin/mkdocs: $(VIRTUAL_ENV)/bin/pip requirements-dev.txt
	$(VIRTUAL_ENV)/bin/pip install -Ur requirements-dev.txt
	touch $@

$(VIRTUAL_ENV)/bin/pip:
	virtualenv $(VIRTUAL_ENV)

docs: devenv $(BUILD_DIR)
	$(VIRTUAL_ENV)/bin/mkdocs build
	mv site $(BUILD_DIR)/site

clean:
	$(RM) -r $(BUILD_DIR)

.PHONY: clean test testenv docs
