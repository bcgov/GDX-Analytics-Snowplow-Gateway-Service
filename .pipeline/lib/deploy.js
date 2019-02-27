'use strict';
const {OpenShiftClientX} = require('pipeline-cli')
const path = require('path');

module.exports = (settings)=>{
  const phases = settings.phases
  const options= settings.options
  const phase=options.env
  const changeId = phases[phase].changeId
  const oc=new OpenShiftClientX({'namespace':phases[phase].namespace});
  const templatesLocalBaseUrl =oc.toFileUrl(path.resolve(__dirname, '../../openshift'))
  var objects = []

  
  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/sso72-x509.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'DB_SECRET_NAME':`${phases[phase].name}-pgsql${phases[phase].suffix}`,
      'DB_SECRET_DATABASE_KEY':'app-db-name',
      'DB_SECRET_USERNAME_KEY':'app-db-username',
      'DB_SECRET_PASSWORD_KEY':'app-db-password',
      'DB_SERVICE_HOST': `${phases[phase].name}-pgsql-master${phases[phase].suffix}`
    }
  }))

  oc.applyRecommendedLabels(objects, phases[phase].name, phase, `${changeId}`, phases[phase].instance)
  
  oc.importImageStreams(objects, phases[phase].tag, phases.build.namespace, phases.build.tag)
  oc.applyAndDeploy(objects, phases[phase].instance)

}