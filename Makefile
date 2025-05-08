all: test

#: interpreter version (ex.: 3.12) or use all current available
PYTHON ?= __all_available__

# -- Installs -----------------------------------------------------------------

.PHONY: install
install:
	pip install --upgrade .

.PHONY: install_dev
install_dev:
	pip install --upgrade --editable .[develop,testing,dist]

# -- Cleans -------------------------------------------------------------------

.PHONY: clean_images
clean_images:
	- docker ps -a | grep lottery | awk '{print $$1}' | \
	 xargs --no-run-if-empty docker rm
	- docker images | grep lottery | awk '{print $$1":"$$2}' | \
	 xargs --no-run-if-empty docker rmi
