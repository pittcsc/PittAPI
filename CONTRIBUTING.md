# Contributing Guidelines

To get started with contributing to the Pitt API, please read these guidelines in their entirety to set up your development environment and learn our tooling.

## Initial Setup

### Setting Up Your Virtual Environment

PittAPI uses [uv](https://docs.astral.sh/uv/) to manage Python 3.13 and its dependencies.

After installing uv and cloning the repository, create the virtual environment and install the exact locked dependencies:

```sh
uv sync --locked
```

Use `uv run <command>` to run commands in the project environment. You do not need to activate the `.venv` manually.

### Pre-Commit

As a contributor, you should add [pre-commit](https://pre-commit.com/) to your development workflow in order to help us maintain a high-quality codebase.
We've included several pre-commit hooks in [`.pre-commit-config.yaml`](/.pre-commit-config.yaml) that we consider to be essential for our purposes.

pre-commit is installed as a development dependency by `uv sync`.
To add pre-commit to your workflow, run
```sh
uv run pre-commit install
```
From this point on, pre-commit should run whenever you make a commit.
If it catches any errors (trailing whitespace, questionable code formatting, etc.), it'll try to fix them automatically or ask you to fix them if it can't.
Make sure to fix all pre-commit errors before you commit.

By default, pre-commit checks all modified files staged in your commit.
If you want to run pre-commit on the entire repo, including files that you haven't modified, run
```sh
uv run pre-commit run --all-files
```

## Contributing to the API

To make a contribution to the Pitt API, simply open a PR from your local fork of the Pitt API repo.

Naturally, you should ensure that contributions work and are of high quality before you make a PR.
This includes making sure that your code compiles, passes all unit tests, and adhere to common style guidelines.

### Unit Testing

PittAPI uses `pytest` for unit testing.
The suite requires 100% statement and branch coverage. To run it:
```sh
uv run pytest --cov=pittapi --cov-branch --cov-fail-under=100 tests/
```

### Code Quality

To ensure consistent and readable code, we use the `flake8` linter and `black` formatter to help our code adhere to [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
`flake8` and `black` are installed by `uv sync`, and they're also included in our pre-commit hooks.
This means that if you have pre-commit set up correctly, pre-commit should run `flake8` and `black` automatically when you make a commit.

However, if you wish to run the linter and formatter yourself, simply run these commands:
```sh
uv run flake8 --max-line-length=127 .
uv run black --line-length=127 .
```

PittAPI should remain understandable to developers who are still learning Python. Prefer explicit control flow,
descriptive intermediate variables, and early returns over dense expressions. Add a helper only when it names a
meaningful domain operation, removes real duplication, or substantially reduces nesting. Do not add pass-through
wrappers or speculative defensive checks.

Ordinary helper functions, methods, and classes do not begin with `_`; modules use `__all__` to document their
supported exports. Comments should explain non-obvious provider behavior rather than narrating ordinary Python.

In terms of writing style, we expect you to write in a professional manner and follow proper commenting etiquette—pretend that this is a work environment and your comments are being reviewed by your manager and coworkers.

### GitHub Workflows

Note that we use automated GitHub workflows to check incoming PRs.
For you as a contributor, this means that GitHub will run `flake8`, `black`, and `pytest` on your PR.
For more information on the commands that we run as part of our workflows, please see our [workflows directory](/.github/workflows).
Make sure your code pass all workflows before requesting a review.
