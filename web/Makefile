all: CLEAN BUILD

CLEAN: 
	rm -rf /dist *.egg-info

BUILD: PACKAGE UPLOAD

PACKAGE:
	python setup.py sdist bdist_wheel

UPLOAD:
	twine upload dist/*
