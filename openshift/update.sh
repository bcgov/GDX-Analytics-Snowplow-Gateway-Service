#!/bin/bash
set -Eeu
#set -o pipefail

# Latest known commit id of the working template
PATRONI_SOURCE_REF=581eb6eb39f97fb59f92eb617a8913efa3f40cb5

PATRONI_BASE_URL="https://raw.githubusercontent.com/BCDevOps/platform-services/${PATRONI_SOURCE_REF}/apps/pgsql/patroni"

cd "$( dirname "${BASH_SOURCE[0]}" )"

curl -sSk -o postgresql-secrets.yaml "${PATRONI_BASE_URL}/openshift/deployment-prereq.yaml"
curl -sSk -o postgresql.yaml "${PATRONI_BASE_URL}/openshift/deployment.yaml"
