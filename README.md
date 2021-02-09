![CI-CD](https://github.com/vmspereira/Dummy/workflows/CI-CD/badge.svg?branch=workflow)
[![codecov](https://codecov.io/gh/vmspereira/Dummy/branch/workflow/graph/badge.svg?token=ugFx13qISc)](https://codecov.io/gh/vmspereira/Dummy)

# Dummy CI-CD with GitHub Actions

GitHub Actions help you automate tasks within your software development life cycle. GitHub Actions are event-driven, meaning that you can run a series of commands after a specified event has occurred. For example, every time someone creates a pull request for a repository, you can automatically run a command that executes a software testing script.

You can create a continuous integration (CI) workflow to build and test your Python project by defining a GitHub action directly on your project or using the GitHub web interface.

#### Configuration file

Create a workflow YAML file on your repository `.github/workflows/main.yml` and insert the workflow configuration, in the example, wich uses TOX:

```yaml
name: CI-CD

on:
  push:
    branches:
      - workflow
    tags:
      - "[0-9]+.[0-9]+.[0-9]+"
      - "[0-9]+.[0-9]+.[0-9]+a[0-9]+"
  pull_request:
    branches:
      - workflow

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: [3.6, 3.7, 3.8]

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install tox tox-gh-actions
      - name: Test with tox
        run: tox -e py
      - name: Report coverage
        shell: bash
        run: bash <(curl -s https://codecov.io/bash)
```

The configuration will only be applied to the 'workflow' branch. You may specify additional branches or use the wildcard '\*'. The same is valid when it comes to tags. You may choose to simplify and consider the action to be triggered on all pushes and pull request:

```yaml
on: [push, pull_request]
```

Now lets define the jobs.

#### Using multiple Python versions/OS

We want to build and test the package on different OS and Python versions, so we define a build matrix. The fail-fast strategy is set to false so that GitHub does not cancels all in-progress jobs if any `matrix` job fails. The default is set to true.

We wan to test the Python code on distinct OS and Python versions. We might want, howerver, to exclude a particular Python version on a specific OS, such as Python 3.6 on macOS:

```yaml
python-version: [3.6, 3.7, 3.8]
exclude:
  - os: macos-latest
    python-version: 3.6
```

#### Steps

A job contains a sequence of tasks called `steps`. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps.

To provide access to our repository we define the uses `actions/checkout@v2`.

We now define the name of the step to display on GitHub. It is possible to add conditions to steps:

```yaml
- name: My first step
   if: ${{ github.event_name == 'pull_request' && github.event.action == 'unassigned' }}
```

#### Installing dependencies

GitHub-hosted runners have the pip package manager installed. You can use pip to install dependencies from the PyPI package registry before building and testing your code. We need to setup the Python versions and, in our particular case, we will settle to upgrade our environment and install `tox` and `tox-gh-actions`. The last is a plugin that enables to run tox on github actions.

If we didn't use tox, we would require to install the dependencies and eventually ou package:

```yaml
steps:
  - uses: actions/checkout@v2
  - name: Set up Python
    uses: actions/setup-python@v2
    with:
      python-version: ${{ matrix.python-version }}
  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip intall .
```

#### Testing

As we are using tox to run the tests, we only need to invoke tox to get the job done.

```yaml
- name: Test with tox
  run: tox -e py
```

The `-e py` ensures that tox uses the version of Python in `PATH`.

Without tox:

```yaml
steps:
  - uses: actions/checkout@v2
  - name: Set up Python
    uses: actions/setup-python@v2
    with:
      python-version: ${{ matrix.python-version }}
  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip intall .
  - name: Test with pytest
    run: |
      pip install pytest
      pip install pytest-cov
      pytest --cov=com --cov-report=xml --cov-report=term
```

Finally, we only need to submit the code coverage data.

```yaml
- name: Report coverage
      shell: bash
      run: bash <(curl -s https://codecov.io/bash)
```

### Publishing to package registries

You can configure your workflow to publish your Python package to any package registry you'd like when your CI tests pass.

You can store any access tokens or credentials needed to publish your package using secrets. The following example creates and publishes a package to PyPI using `twine` and `dist`. For more information, see "[Creating and using encrypted secrets](https://docs.github.com/en/github/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets)."

```yaml
- name: Build and publish
  env:
    TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
    TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
  run: |
    python setup.py sdist bdist_wheel
    twine upload dist/*
```



### TOX Configuration

We need to update the tox.ini file to work with GitHub action workflows:

```ini
[tox]
envlist = py3{6,7,8}

[gh-actions]
python = 
    3.6: py36
    3.7: py37
    3.8: py38

[testenv]
setenv =
        PYTHONPATH = {toxinidir}

deps =
       pytest
       pytest-cov
       
commands =
     pytest --cov=dummy --cov-report=term --cov-report=xml
   
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
commands =
    flake8 src tests setup.py
```

