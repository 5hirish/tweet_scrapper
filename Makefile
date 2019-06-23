SHELL := /bin/bash
sha = $(shell "git" "rev-parse" "--short" "HEAD")

dist/tweetscrape.pex : tweetscrape/*.py* tweetscrape/*/*.py*
	python3.6 -m venv env
	source env/bin/activate
	env/bin/pip install wheel
	env/bin/pip install -r requirements.txt --no-cache-dir
	env/bin/python setup.py build_ext --inplace
	env/bin/python setup.py sdist
	env/bin/python setup.py bdist_wheel
	env/bin/python -m pip install pex==1.6.7
	env/bin/pex pytest dist/*.whl -e tweetscrape -o dist/tweetscrape-$(sha).pex
	cp dist/tweetscrape-$(sha).pex dist/tweetscrape.pex
	chmod a+rx dist/tweetscrape.pex

.PHONY : clean

clean : setup.py
	source env/bin/activate
	rm -rf dist/*
	python setup.py clean --all