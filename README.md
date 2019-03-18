# GDX-Analytics-Snowplow-Gateway-Service
A gateway service to the Snowplow analytics service for BCGov OpenShift projects

## Inital Project setup

### To Build Locally, and Deploy to OpenShift
This circumvents the Jenkins CI/CD pipeline in the **`TOOLS`** project on OpenShift. It is an alternative to the rsync/hot-deploy method described in the section below (and which is not yet an option).

#### Build
```
cd .pipeline
# Building
npm run build -- --pr=0 --dev-mode=true

```
#### Deploy
```
# Deploy to DEV
cd .pipeline
npm run deploy -- --pr=0 --env=dev
```
#### Clean
```
cd .pipeline

# Build environment
npm run clean -- --pr=0 --env=build

# DEV environment
npm run clean -- --pr=0 --env=dev

```

### Sync Working Directory to Pod

Currently we have no way to [hot-deploy](https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#python-hot-deploy) the app.py. The following steps are not recommended until hot deploy is set up, since while the contents of the [app.py](./app/app.py) can be updated on a given pod; it will not reload the Python process running that script from the one that is already loaded in memory.

You will need to set the autoscale to one pod to avoid the route sometimes calling a pod you aren't `rsync`ing to. In **`DEV`**, in the Application > Deployments > Actions > Edit Autoscaler section, set Min pods from 2 to 1, then save. The HPA will autoscale your pods down to one.

Locally, run:

```bash
cd "$(git rev-parse --show-toplevel)/app" # navigate to your working directory (./app)
oc rsync --no-perms=true ./ <pod_id>:/opt/app-root/src
oc rsh <pod_id>
cat /opt/app-root/src/app.py
```

### Postgres Schema Setup

#### Local Development

Configure your Postgres environment to include the role and schema necessary (see the commented lines in [./schema/caps_schema.sql](./schema/caps_schema.sql)). Build the tables and give the application user (`caps` is the example) ownership. Set the environment variables required for [./app/app.py](./app/app.py); `DB_HOSTNAME`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD` to access Postgres.

#### OpenShift Development

The DevOps recommendation is to port-forward to the local development workstation, run the PostgreSQL database locally, and connect remotely to that from an OpenShift Python pod from which you will be `rsync`ing (see above) your working directory (most likely [./app](./app)).

on *each* postgres pod in Dev, connect to the caps DB and create the schema, then create the tables

```bash
cd "$(git rev-parse --show-toplevel)/schema"
oc rsync --no-perms=true ./ <pod_id>:/home/postgres
oc rsh <pod_id>
psql caps -f caps_schema.sql
```

### Parsable POST JSON Example

The following snippet of JSON is an example of a POST body which will validate against the [`post_schema.json`](./app/post_schema.json).

```json
{
    "env": "test",
    "namespace": "TheQ_dev",
    "app_id": "theq",
    "dvce_created_tstamp": 1555802400000,
    "event_data_json": {
        "contexts": [
            {
                "data": {
                    "client_id": 283732,
                    "service_count": 2,
                    "quick_txn": false
                },
                "schema": "iglu:ca.bc.gov.cfmspoc/citizen/jsonschema/3-0-0"
            },
            {
                "data": {
                    "office_type": "reception",
                    "office_id": 14
                },
                "schema": "iglu:ca.bc.gov.cfmspoc/office/jsonschema/1-0-0"
            },
            {
                "data": {
                    "agent_id": 22,
                    "role": "CSR",
                    "quick_txn": false
                },
                "schema": "iglu:ca.bc.gov.cfmspoc/agent/jsonschema/2-0-0"
            }
        ],
        "data": {
            "inaccurate_time": false,
            "quantity": 2
        },
        "schema": "iglu:ca.bc.gov.cfmspoc/finish/jsonschema/2-0-0"
    }
}
```
