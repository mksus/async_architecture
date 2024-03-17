# Makefile
SHELL=/usr/bin/env bash -O extglob

AUTH_URL=http://localhost:8000
TRACKER_URL=http://localhost:8001

TRACKER_TOKEN=nYo4QnDyIZaZQ5zezMjeQQ85iPJUMx


### TRACKER ###
auth_in_tracker_url:
	echo "${TRACKER_URL}/auth_client/auth_via_provider/"

create_task:
	curl -X POST ${TRACKER_URL}/tracker/create/ --header "Authorization: Bearer ${TRACKER_TOKEN}" --form description="test 1" --form is_open="True"

my_tasks:
	curl --location ${TRACKER_URL}/tracker/my_tasks/ --header "Authorization: Bearer ${TRACKER_TOKEN}"

reassign:
	curl -X POST ${TRACKER_URL}/tracker/reassign/ --header "Authorization: Bearer ${TRACKER_TOKEN}"

complete:
	curl -X POST ${TRACKER_URL}/tracker/complete/ --header "Authorization: Bearer ${TRACKER_TOKEN}" --form public_id="953a45a8-96ab-45db-902a-62c619610f10"


### BILLING ###
auth_in_billing_url:
	echo "${TRACKER_URL}/auth_client/auth_via_provider/"


