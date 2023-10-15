# $(venv): a short path to $VIRTUAL_ENV, just for better output readability
venv := $(shell realpath $(VIRTUAL_ENV) $(CURDIR))

.PHONY: all
all: env

.PHONY: env
env: $(venv)

.PHONY: lint
lint: env
	pre-commit run --all

.PHONY: test
test: env
	pytest

.PHONY: typecheck
typecheck:
	@set -x; PYTHONPATH=$(CURDIR)/src pyright --verifytypes sentry_jsonnet --outputjson


# conventions:
#   1. for improved logging and failure modes, each recipe is wrapped by `makerule`
#      * first arg to "makerule" is the rule target (AKA $@)
#      * further "makerule" args are the command to run
#   1. first requirement (AKA $<) must be a script containing the rule's recipe
#   1. ensure that any/all relevant configuration files appear in dependency list
$(venv)/bin/pip-sync: $(venv)/bin/pip-compile
$(venv)/bin/pip-compile: $(shell which venv-init) $(shell which makerule)
	@ makerule "$@" "$<" "$(venv)"/

requirements-dev.txt: $(venv)/bin/pip-compile requirements-dev.in pyproject.toml
	@ makerule "$@" "$<" requirements-dev.in --strip-extras --output-file="$@"

$(venv): $(venv)/bin/pip-sync requirements-dev.txt pyproject.toml
	@ makerule "$@"/ "$<" requirements-dev.txt


# this cleans up `make -d` output:
.SUFFIXES:
MAKEFLAGS += --no-builtin-rules
