#!/bin/bash
## Description:
##  Performs a database transaction on the CAPS schema (postgresql) to delete
##  rows that have a recieved_timestamp value older than the offset from the
##  start of the day when the command is executed (based on psql's system time)

# formatted as an interval type
# https://www.postgresql.org/docs/9.2/datatype-datetime.html#DATATYPE-INTERVAL-INPUT
offset=${1:-$RETENTION_OFFSET}

echo 'BEGIN;DELETE FROM caps.client_calls WHERE received_timestamp <= (date_trunc($$day$$, now()) - interval $$'"${offset}"'$$);COMMIT;' | PGPASSWORD=${POSTGRESQL_PASSWORD} psql -h "${DATABASE_SERVICE_NAME}" -d "${POSTGRESQL_DATABASE}" -U "${POSTGRESQL_USER}"
