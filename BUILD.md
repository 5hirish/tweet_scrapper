#### Release Build

1) Run all PyTest test cases
2) Update the version number
3) Build source and wheels packages
4) Upload to PyPi via Twine

```bash
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
$ pip install tweetscrape --upgrade
```

#### Edit Mode Install

```bash
$ pip install -e .
```