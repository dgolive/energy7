# Contributing

Thank you for helping this project become a better tool for solar site assessment :)

- [Triage](#triage)
- [Reporting Bugs](#reporting-bugs)
- [Providing a feature request](#providing-a-feature-request)
- [Pull requests](#pull-requests)

## Triage

This is one of the easiest and most effective ways of helping out. If you see an open issue, try and reproduce the bug yourself, and comment with the result. If the issue is lacking any information to reproduce the bug, let the author know.

## Reporting Bugs

Open an issue, making sure to follow the bug report template.

## Providing a feature request

Open an issue, making sure to follow the Feature request template.

## Pull requests

### Getting started

- If there isn't one already, open an issue describing the bug or feature request that you are going to solve in your pull request.
- Fork the repository.
  - If you already have a fork, make sure it is up to date.
- Clone your fork and install dependencies:
  ```
  pip install -r requirements-dev.txt
  ```
- Copy `.env-sample` to `.env` and add your own Google Maps Platform API key.
- Create a branch from `master` to start working on your changes.

### Committing

- Run `pytest` to make sure the code you introduced doesn't cause any obvious regressions.
- Use present tense in commit messages: "add roof lookup caching" not "added roof lookup caching".
- Reference issues and pull requests before committing.

### Creating the pull request

- Keep the PR title short and describe the change, not the implementation detail.
- Describe what you tested manually (this is a Streamlit app, so most changes are best verified by running `streamlit run main.py` and exercising the UI).
