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