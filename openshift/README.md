# Generating Build Configs
```
oc new-build registry.access.redhat.com/rhscl/python-36-rhel7:1~https://github.com/bcgov/GDX-Analytics-Snowplow-Gateway-Service.git --strategy=source --dry-run -o yaml '--name=${NAME}${SUFFIX}' '--context-dir=${GIT_DIR'

```

# Generating Deployment Config
```
oc new-app registry.access.redhat.com/rhscl/python-36-rhel7:1 --dry-run -o yaml '--name=${NAME}${SUFFIX}'
```