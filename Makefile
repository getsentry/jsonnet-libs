VENV_PATH = .venv

.PHONY: all, venv-binding, venv-tester, setup-git

setup-git:
	pip install pre-commit==2.13.0
	pre-commit install --install-hooks


venv-binding: 
	sbin/make-venv binding

venv-tester: 
	sbin/make-venv tester
