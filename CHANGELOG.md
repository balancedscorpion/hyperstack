# Changelog
All notable changes to this project will be documented in this file. The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## 0.2.6 - 2024-08-01

### Added

* New CLI to allow deploying Ollama and Pytorch server with "hyperstack" command.

## 0.2.5 - 2024-07-31

### Added

* Removed hard-coded password argument from dockeruser for one-click deployments, improving security.

## 0.2.4 - 2024-07-29

### Added

* New function to poll the status of a vm until it's active
* One-click deployment of Ollama and Pytorch servers

### Removed

* _exec_with_backoff function. It wasn't working and not required.

## 0.2.4 - 2024-07-27

### Added

* Initial release of hyperstack-python
* Basic API wrapper functionality for Hyperstack API
* Support for most currently supported endpoints
* Project structure set up with Poetry for dependency management
* Basic test suite using pytest
* Documentation including README.md, CONTRIBUTING.md and this CHANGELOG.md
