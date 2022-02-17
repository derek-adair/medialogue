all: CLEAN BUILD

CLEAN: 
	rm -rf /dist *.egg-info

BUILD: 
	python setup.py sdist bdist_wheel
	twine upload dist/*
