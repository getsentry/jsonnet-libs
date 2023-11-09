- [ ] fix the tests in CI.

  Specifically sentry_jsonnet tests cannot find sentry_jsonish. It was not a
  separate lib. We did not publish successfully a version of the package yet
  though for sentry_jsonnet to import from pypi. Other way is to make
  sentry_jsonnet tests rely on the local unpublished sentry_jsonish.

- high priority: (this week)
  - [ ] shared precommit hook (for other repos to use)
    - [ ] lint
    - [ ] format
    - [ ] (optionally) generate
  - [ ] github action (for other repos to use)
    - [ ] lint
    - [ ] format
    - [ ] (optionally) generate
  - [ ] The test harness. Basically that is a third package to build from the
        ground up
  - [ ] a new jsonnet package: ops/region_configs
    - [ ] testing: needs test-harness
    - [ ] precommit
    - [ ] GHA
- medium priority: (not this week)
  - [ ] The go-jsonnet issue: getsetry/pypi lacks a go compiler?
    - blocked by: a working sentry-pypi release process
    - "the go-jsonnet issue" being getsentry/pypi seemingly lacked a go
      compiler?
    - Yeah, the error was something like Command not found: go
- lower priority: (perhaps never)
  - [ ] add monorepo support to craft (i.e. tags of the form $PACKAGE/vX.Y)
  - [ ] fix craft: initial `craft prepare` changelog fails end-of-file fixer
    - AI: edit the initial changelog string to not have extra trailing newlines
    - check if that is the expected behavior in craft, may actually be a bug,
      craft should be able to create the first commit to a CHANGELOG file with a
      proper new line at the end.
    - Otherwise we can just turn the check off for the first release and
      re-enable afterwards.
    - Once that is fixed hopefully there are no more blockers to publish the two
      libraries.

# TODO

Fixing types. pyright was complaining when I ran it two weeks ago and it is
disabled in pre-commit. Cannot remember which errors we had and whether it was a
config issues or there were actually broken types.

Maybe reuse the release and build GH workflows instead of copy pasting them.
Just as you did for CI.

This is what I know on top of my head now, you may have others as well. So
basically I think you can pick whatever you want there. I'll start working on
this around my 2 pm. I can pick what you did not pick.

---

- [ ] goal: allow sentaurs to use jsonnet in a fully-tested manner
  - [ ] submit ops/jsonnet integration:
        https://github.com/getsentry/ops/pull/7245/files
  - [ ] test getsentry deployment
        https://github.com/getsentry/getsentry/blob/master/gocd/templates/backend.jsonnet
  - [ ] rework tests of application to gocd
        https://github.com/getsentry/gocd-jsonnet
  - [ ] DRY pyproject.toml, in this repo
- [ ] we're creating three new python libraries
  - [ ] sentry-jsonish -- mostly just typing
    - [x] pypi packaging exists
    - [x] unit testing
    - [ ] readme
  - [ ] sentry-jsonnet
    - [x] pypi packaging exists
    - [ ] update to gojsonnet
      - [ ] blocked by: figure out why our pypi GHA has no `go`
    - [ ] depends on sentry-jsonish
    - [ ] readme
  - [ ] test harness: jsonnet-tester
    - [ ] refactor pytest to a library
      - [ ] extract three functions from jsonnet-private-libs make_port_test.py
      - [ ] some unit testing of those three functions
      - [ ] later: use those three functions in a pytest extension
    - [ ] readme
    - [ ] depends on sentry-jsonnet
  - sentry-jsonnet-lib
    - [ ] add it to this repo
- [ ] repo scope:
  - [ ] set up autoreleasing
    - [ ] GHA "release" action -- prepares assets and creates an issue in
          github.com/getsentry/publish
    - [ ] blocked by: add all three packages to this repo
- [ ] delete the old getsentry/private-jsonnet-libs

# TODONE

- [x] a working sentry-pypi release process

# out of scope

    * private shared jsonnet functions: getsentry/getsentry-jsonnet-lib.private
        * don't need it, for the forseeable future
        * anything private can be modeled as parmeters' values in private repos (e.g. ops)
        * would need to be a new repo, since this one's public
