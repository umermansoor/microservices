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

launch: venv shutdown
	. venv/bin/activate; python  services/movies.py &
	. venv/bin/activate; python  services/showtimes.py &
	. venv/bin/activate; python  services/bookings.py &
	. venv/bin/activate; python  services/user.py &

shutdown:
	ps -ef | grep "services/movies.py" | grep -v grep | awk '{print $$2}' | xargs kill  
	ps -ef | grep "services/showtimes.py" | grep -v grep | awk '{print $$2}' | xargs kill  
	ps -ef | grep "services/bookings.py" | grep -v grep | awk '{print $$2}' | xargs kill  
	ps -ef | grep "services/user.py" | grep -v grep | awk '{print $$2}' | xargs kill  

