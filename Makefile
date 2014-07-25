BUILD_DIR:=build
VIRTUAL_ENV?=$(BUILD_DIR)/virtualenv
REMOTE_URL=$(shell git config remote.origin.url)
GIT_NAME?=$(shell git config user.name)
GIT_EMAIL?=$(shell git config user.email)

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

gh-pages: docs
	cd $(BUILD_DIR)/site ;\
		git init;\
		git remote add origin $(REMOTE_URL);\
		git remote set-branches --add origin gh-pages;\
		git config user.name "$(GIT_NAME)";\
		git config user.email "$(GIT_EMAIL)";\
		git checkout -b gh-pages ;\
		git add -A .;\
		git commit -m 'Updated docs';\
		git push -f origin gh-pages

clean:
	$(RM) -r $(BUILD_DIR)

.PHONY: clean test testenv docs gh-pages
