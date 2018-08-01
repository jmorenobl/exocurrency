SETTINGS=exocurrency.settings.local
TEST_SETTINGS=exocurrency.settings.test
DEVELOPMENT_DB=db_exocurrency
LOCALPATH=$(PWD)
PYTHONPATH=$(LOCALPATH)/

# Execute target with arguments. e.g: make exec createsuperuser
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# target: all - Default target. Does nothing.
.PHONY: all
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
.PHONY: help
help:
	@egrep "^# target:" [Mm]akefile

# target: test - calls the "test" django command
.PHONY: test
test:
	DJANGO_READ_DOT_ENV_FILE=yes py.test

# target: clean - remove all ".pyc" files
.PHONY: clean
clean:
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py clean_pyc --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)
	-rm -rf htmlcov
	-rm -rf .coverage

# target: migrate - create or apply changes in the database
.PHONY: migrate
migrate:
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py migrate --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)

# target: rebuild - clean and rebuild all data
.PHONY: rebuild
rebuild: clean
	rm -rf exocurrency/media/*
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py reset_db --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH) --router=default --noinput
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py migrate --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)
	#django-admin.py loaddata --settings=$(SETTINGS) <your fixtures here>

# target: runserver - run development server
.PHONY: runserver
runserver:
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py runserver 0.0.0.0:8000 --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)

# target: createsuperuser - creates a superuser
.PHONY: createsuperuser
createsuperuser:
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py createsuperuser --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)

# target: run - runs any of the available django commands
.PHONY: run
run:
	DJANGO_READ_DOT_ENV_FILE=yes django-admin.py $(RUN_ARGS) --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)

# target: create_db - creates the development database
.PHONY: create_db
create_db:
	docker create --name $(DEVELOPMENT_DB) -p 5432:5432 -v /var/lib/postgresql/data postgres

# target: start_db - starts the development database
.PHONY: start_db
start_db:
	docker start $(DEVELOPMENT_DB)

# target: init_db - creates and starts the development database
.PHONY: init_db
init_db: create_db start_db
	sleep 2

# target: stop_db - stops the development database
.PHONY: stop_db
stop_db:
	docker stop $(DEVELOPMENT_DB)

# target: remove_db - removes the development database
.PHONY: remove_db
remove_db: stop_db
	docker rm -v $(DEVELOPMENT_DB)

# target: initapp - initializes the whole app: db, migrations and superuser
.PHONY: initapp
initapp: init_db migrate createsuperuser

# target: coverage - checks code coverage
.PHONY: coverage
coverage:
	DJANGO_READ_DOT_ENV_FILE=yes coverage run manage.py test --settings=$(SETTINGS) --pythonpath=$(PYTHONPATH)
	coverage html
	@echo "open htmlcov/index.html in a browser to see the results"
