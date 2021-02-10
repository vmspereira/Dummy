[![Build Status](https://travis-ci.org/vmspereira/Dummy.svg?branch=travis)](https://travis-ci.org/vmspereira/Dummy)
[![codecov](https://codecov.io/gh/vmspereira/Dummy/branch/workflow/graph/badge.svg?token=ugFx13qISc)](https://codecov.io/gh/vmspereira/Dummy)

# Dummy CI-CD with Travis CI and Codecov

A great way to test your code on several Python versions is to use the [Travis CI](https://travis-ci.org) service, which offers (among other features) cloud-based, continuous testing, **free** for open source (i.e. public) GitHub projects. Let me briefly introduce you to basic Python testing with Travis.

To use [Travis](https://travis-ci.org) simply follow these three steps:

1. Sign up to Travis with GitHub, allowing Travis some access to you projects. You may use travis-ci.com instead of travis-ci.org.
2. Enable Travis for the repository you want to test in [your repositories page](https://travis-ci.org/account/repositories).
3. Place a `.travis.yml` file in the root of your repository; this file will tell Travis how this specific project should be built and tested.


Lets begin with a simple example:

```yaml
language: python

python: "3.7"

install:
  - pip install -r requirements.txt
  - pip install .

script:
  - pytest
```

Testing with pytest works both with unittests and py.tests. By default test files are defined on the `tests` folder of your repository.

#### Code coverage

We also want to perform structural coverage analysis (also referred to as code coverage) which is an important component of critical systems development for measuring completeness of testing.

- Log into [codecov.com]() with your github account
- If you are planning on using codecov outside an official CI or git repository, add the provided codecov token key to your travis environment (CODECOV_TOKEN)

Now let us add the necessary instructions to the `.travis.yml` file, and add a few more testing Python environments in the process:

```yaml
language: python
python:
  - "3.6"
  - "3.7"
  - "3.8"

install:
  - pip install pytest-cov
  - pip install -r requirements.txt
  - pip install .

script:
  - pytest --cov=dummy

after_success:
  - bash <(curl -s https://codecov.io/bash)
```

We need to install the `pytest-cov` plugin to enable pytest to perform code coverage, and identify the name of the package, `--cov=dummy`

Commit and push the modifications, and grab your badges.
