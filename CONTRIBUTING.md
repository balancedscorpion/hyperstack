## Contributing to Hyperstack Cloud

Thank you for your interest in contributing to Hyperstack Cloud! Before you begin writing code, please read through this document. 
First, it is important that you share your intention to contribute, based on the type of contribution.

Please first search through Hyperstack Cloud [issues](https://github.com/balancedscorpion/hyperstack/issues). If the feature is not listed, please create a new issue. 
If you would like to work on any existing issue, please comment and assign yourself to the issue and file a pull request.

This document covers some of the technical aspects of contributing to Babbab.

## Developing Hyperstack Cloud & Set-up

To develop Hyperstack Cloud on your machine, you can follow the set-up instructions. 

### Prerequisites

Python >= 3.8

Install poetry if you don't have it
```curl -sSL https://install.python-poetry.org | python3 -```

### Set-up

First clone the repo:

```git clone https://github.com/balancedscorpion/hyperstack.git```

Next open the repo and install dependencies:

```cd hyperstack && poetry install```

### Unit testing

Before you submit your pull request, please ensure you have written a unit test for your code and all unit tests are passing.
You can check this by visiting the babbab home directory and running pytest command:

```pytest```

### Linting

There is currently no linter.

### Writing documentation

Please make sure you add documentation to your functions. Please use [Google Style docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html).