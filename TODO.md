# TODO

 * [ ] goal: allow sentaurs to use jsonnet in a fully-tested manner
    * [ ] submit ops/jsonnet integration:
      https://github.com/getsentry/ops/pull/7245/files
    * [ ] test getsentry deployment
      https://github.com/getsentry/getsentry/blob/master/gocd/templates/backend.jsonnet
    * [ ] rework tests of application to gocd
      https://github.com/getsentry/gocd-jsonnet
    * [ ] DRY pyproject.toml, in this repo
 * [ ] we're creating three new python libraries
     * [ ] sentry-jsonish -- mostly just typing
        * [x] pypi packaging exists
        * [x] unit testing
        * [ ] readme
     * [ ] sentry-jsonnet
        * [x] pypi packaging exists
        * [ ] update to gojsonnet
            * [ ] blocked by: figure out why our pypi GHA has no `go` 
        * [ ] depends on sentry-jsonish
        * [ ] readme
     * [ ] test harness: jsonnet-tester
        * [ ] refactor pytest to a library
            * [ ] extract three functions from jsonnet-private-libs make_port_test.py
            * [ ] some unit testing of those three functions
            * [ ] later: use those three functions in a pytest extension
        * [ ] readme
        * [ ] depends on sentry-jsonnet
    * sentry-jsonnet-lib
        * [ ] add it to this repo
 * [ ] repo scope:
    * [ ] set up autoreleasing
        * [ ] GHA "release" action -- prepares assets and creates an issue in github.com/getsentry/publish
        * [ ] blocked by: add all three packages to this repo
 * [ ] delete the old getsentry/private-jsonnet-libs

# out of scope

    * private shared jsonnet functions: getsentry/getsentry-jsonnet-lib.private
        * don't need it, for the forseeable future
        * anything private can be modeled as parmeters' values in private repos (e.g. ops)
        * would need to be a new repo, since this one's public
