setup:
	pip3 install -r requirements.txt
	python3 setup.py install

test:
	python3 setup.py test