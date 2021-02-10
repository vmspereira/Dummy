[![Build Status](https://travis-ci.org/vmspereira/Dummy.svg?branch=TOX)](https://travis-ci.org/vmspereira/Dummy)[![codecov](https://codecov.io/gh/vmspereira/Dummy/branch/TOX/graph/badge.svg?token=ugFx13qISc)](https://codecov.io/gh/vmspereira/Dummy)



# Dummy CI-CD with TOX

## Tox[¶](https://docs.python-guide.org/scenarios/ci/#tox)

[tox](https://tox.readthedocs.io/en/latest/) is an automation tool providing packaging, testing, and deployment of Python software right from the console or CI server. It is a generic virtualenv management and test command line tool which provides the following features:

- Checking that packages install correctly with different Python versions and interpreters
- Running tests in each of the environments, configuring your test tool of choice
- Acting as a front-end to Continuous Integration servers, reducing boilerplate and merging CI and shell-based testing

- tox is a generic virtualenv management and test command line tool;
- It acts as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging CI and shell-based testing;
- Test against different versions of Python and dependency versions;
- Isolate environment variables;
- Do all the above across Windows / macOS / Linux;
- tox-travis is a plugin for tox that simplifies the setup between tox and Travis.



Place a `tox.ini` file in the root of your repository:

```ini
[tox]
envlist = py3{6,7,8}

[travis]
python = 
       3.6: py36
       3.7: py37
       3.8: py38

[testenv]
passenv = CI TRAVIS TRAVIS_*
setenv =
       PYTHONPATH = {toxinidir}
deps = 
       codecov
       pytest
       pytest-cov

commands =
       pytest  --cov=dummy
       codecov
```

We will use the GitHub Travis plugin to call tox, so we need to place a `.travis.yml` file in the root of the repository:

```yaml
language: python
python:
  - "3.6"
  - "3.7"
  - "3.8"

install:
  - pip install tox-travis

script:
  - tox
```

We need to install `tox-travis` , a plugin for [tox](https://pypi.org/project/tox/) that simplifies the setup between tox and Travis.

Env detection is the primary feature of Tox-Travis. Based on the matrix created in `.travis.yml`, it decides which Tox envs need to be run for each Travis job.



```ini
[tox]
envlist = py3{6,7,8},flake8,pylint

[travis]
python = 
       3.6: py36
       3.7: py37,flake8,pylint
       3.8: py38

[testenv]
passenv = CI TRAVIS TRAVIS_*
setenv =
       PYTHONPATH = {toxinidir}
deps = 
       codecov
       pytest
       pytest-cov

commands =
       pytest  --cov=dummy
       codecov

[flake8]
ignore = E501
max-complexity = 10

[testenv:flake8]
basepython = python3
skip_install = true
deps =
      flake8
      flake8-bugbear
      flake8-docstrings>=1.3.1
      flake8-import-order>=0.9
      flake8-typing-imports>=1.1
      pep8-naming
commands = flake8 src tests setup.py

[testenv:pylint]
basepython = python3
skip_install = true
deps =
       pyflakes
       pylint!=2.5.0
commands = pylint src
```

