# Microservices Project Make File
# author: umer mansoor

VIRTUALENV = $(shell which virtualenv)

clean: shutdown
	rm -fr microservices.egg-info
	rm -fr venv

venv:
	$(VIRTUALENV) venv

install: clean venv
	. venv/bin/activate; python setup.py install
	. venv/bin/activate; python setup.py develop

# TODO
shutdown:
	ps -ef | grep python  

launch: venv shutdown
	. venv/bin/activate; python microservices/services/movies.py &
	. venv/bin/activate; python microservices/services/showtimes.py &
	. venv/bin/activate; python microservices/services/bookings.py &
	. venv/bin/activate; python microservices/services/user.py &