# GDX-Analytics-Snowplow-Gateway-Service
A gateway service to the Snowplow analytics service for BCGov OpenShift projects

## Inital Project setup
TODO: 
review other readme.

## For local development purposes

### Build
```
cd .pipeline
# Building
npm run build -- --pr=0 --dev-mode=true

```
### Deploy
```
# Deploy to DEV
cd .pipeline
npm run deploy -- --pr=0 --env=dev
```
### Clean
```
cd .pipeline

# Build environment
npm run clean -- --pr=0 --env=build

# DEV environment
npm run clean -- --pr=0 --env=dev

```

## Sync working directory to pod.

Currently we have no way to [hot-deploy](https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#python-hot-deploy) the app.py. The following steps are not recommended until then, since while app.py can be updated on a given pod; it will not reload Python.

In **`DEV`**, in the Application > Deployments > Actions > Edit Autoscaler section, set Min pods from 2 to 1, then save. The HPA will autoscale your pods down to one.

Locally, run:

```
cd app # navigate to your working directory
oc rsync --no-perms=true ./ <pod_id>:/opt/app-root/src
oc rsh <pod_id>
cat /opt/app-root/src/app.py
```

## PSQL to create the schema

DevOps recommendation is to port-forward to the local development workstation, run the PostgreSQL database locally, and connect remotely from the Python pod.

on *each* postgres pod in Dev, connect to the caps DB and create the schema, then create the tables
```
cd "$(git rev-parse --show-toplevel)/schema"
oc rsync --no-perms=true ./ <pod_id>:/home/postgres
oc rsh <pod_id>
psql caps -f caps_schema.sql
```
