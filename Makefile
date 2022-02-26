shfmt:
	shfmt -i 2 -l -w bin/*
pyfmt:
	black lib/
	black setup.py
req:
	pip install --upgrade pip
	pip install -r requirements/dev.txt