all: CLEAN RELEASE

CLEAN: 
	rm -rf ./dist *.egg-info

RELEASE: BUILD UPLOAD

BUILD:
	python setup.py sdist bdist_wheel

UPLOAD:
	twine upload dist/*
