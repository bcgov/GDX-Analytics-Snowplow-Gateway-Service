# Setup

## Update config.xml files

specify `repoOwner` and `repository` in `/docker/contrib/jenkins/configuration/jobs/_jenkins/config.xml` and `/docker/contrib/jenkins/configuration/jobs/app/config.xml`:

```
<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject ...
  <sources ...
    <data>
      <jenkins.branch.BranchSource>
        <source ...
          <id>generate a new giud</id>
            ...
          <repoOwner>bcgov</repoOwner>
          <repository>GDX-Analytics-OpenShift-Snowplow-Gateway-Service</repository>
```

## Update .jenkins/.pipeline/lib/config.js

to set the deployment phase namespaces according to the appropriate project namespaces

```
const phases = {
  build: {namespace:'8gsiqa-tools' ...
  dev:   {namespace:'8gsiqa-dev'   ...
  test:  {namespace:'8gsiqa-test'  ...
  prod:  {namespace:'8gsiqa-prod'  ...
```

```
oc -n 8gsiqa-tools process -f 'openshift/secrets.json' -p 'GH_USERNAME=<username>' -p 'GH_PASSWORD=<personal_access_token>' | oc  -n 8gsiqa-tools create -f -

oc run dev --image=docker-registry.default.svc:5000/bcgov/jenkins-basic:v2-latest -it --rm=true --restart=Never --command=true -- bash
#Wait for container to startuo and a shell to be available

```
## Getting Git
```
# branch may differ if it's being updated
git clone --single-branch --depth 1 'https://github.com/BCDevOps/openshift-components.git' -b jenkins-basic /tmp/jenkins
```
### From local working directory
```
oc rsync 
```

## oc login
```
#perform oc login (Copy command from web console)
```

### From Local Clone

## Create the Jenkins Configuration
- copy xxx job configuration file and modify
  - jenkins.branch.BranchSource.id
  - repoOwner
  - repository
  - scriptPath


## Create secrets
Use the provided `openshift/secrets.json` as follow:
```
oc -n csnr-devops-lab-tools create secret generic 'template.jenkins-slave-user' --from-literal=username=jenkins-slave

oc -n csnr-devops-lab-tools create secret generic 'template.jenkins-github' \
--from-literal=app-name=cvarjao-bot
--from-literal=app-id=17861
--from-file=app-private-key=cvarjao-bot.2019-02-21.private-key.pkcs8.pem



oc -n bcgov-tools process -f 'openshift/secrets.json' -p 'GH_USERNAME=' -p 'GH_PASSWORD=' | oc  -n bcgov-tools create -f -
```

## Grant Admin access to Jenkins Service account in each managed namespace
```
oc -n bcgov policy add-role-to-user 'admin' 'system:serviceaccounts:bcgov-tools:jenkins'
oc -n bcgov-tools policy add-role-to-group 'system:image-puller' 'system:serviceaccounts:bcgov'
```

# Build
```
( cd "$(git rev-parse --show-toplevel)" && .jenkins/pipeline-cli build --config=.jenkins/openshift/config.groovy --pr=19 )
```

# Deploy
```
( cd "$(git rev-parse --show-toplevel)" && .jenkins/pipeline-cli deploy --config=.jenkins/openshift/config.groovy --pr=19 --env=prod )
```
## Undeploy/Cleanup
```
oc -n bcgov-tools delete is/jenkins
```

## Cleanup
```
curl -sSL https://raw.githubusercontent.com/cvarjao-o/hello-world/WIP/.jenkins/docker/contrib/jenkins/configuration/scripts.groovy.d/clean.sh | bash -s - --namespaces=devhub-tools,devhub-dev --app=devhub --pr=1


-Dkeycloak.migration.action=export -Dkeycloak.migration.provider=dir -Dkeycloak.migration.usersExportStrategy=REALM_FILE -Dkeycloak.migration.dir=/tmp -Dkeycloak.migration.usersExportStrategy=SAME_FILE -Dkeycloak.profile=preview
```