'use strict'
const options = require('pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const version = '1'
const name = 'caps'

const phases = {
  build: {
    namespace: '8gsiqa-tools',
    name: `${name}`,
    phase: 'build',
    changeId: changeId,
    suffix: `-build-${changeId}`,
    instance: `${name}-build-${changeId}`,
    version: `${version}-${changeId}`,
    tag: `build-${version}-${changeId}`,
  },
  dev: {
    namespace: '8gsiqa-dev',
    name: `${name}`,
    phase: 'dev',
    changeId: changeId,
    suffix: `-dev-${changeId}`,
    instance: `${name}-dev-${changeId}`,
    version: `${version}-${changeId}`,
    tag: `dev-${version}-${changeId}`,
    host: 'dev-caps.analytics.gov.bc.ca',
    pvc_size: '2Gi',
  },
  test: {
    namespace: '8gsiqa-test',
    name: `${name}`,
    phase: 'test',
    changeId: changeId,
    suffix: `-test-${changeId}`,
    instance: `${name}-test-${changeId}`,
    version: `${version}-${changeId}`,
    tag: `test-${version}`,
    host: 'test-caps.analytics.gov.bc.ca',
    pvc_size: '2Gi',
  },
  prod: {
    namespace: '8gsiqa-prod',
    name: `${name}`,
    phase: 'prod',
    changeId: changeId,
    suffix: '',
    instance: `${name}-prod`,
    version: `${version}-${changeId}`,
    tag: `prod-${version}`,
    host: 'caps.analytics.gov.bc.ca',
    pvc_size: '10Gi',
  },
}

module.exports = exports = { phases, options }
