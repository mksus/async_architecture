# Makefile
SHELL=/usr/bin/env bash -O extglob

create_task:
	curl -X POST 'http://localhost:8001/tracker/create_task/' -d '{"description": "some description"}'

reassign_tasks:
	curl -X POST 'http://localhost:8001/tracker/reassign_tasks/'

complete_task:
	curl -X POST 'http://localhost:8001/tracker/complete_task/' -d '{"task_id": 1}'