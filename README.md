# HiPEAC Vision printing press

[![github-tests-py-badge]][github-tests-py]
[![codecov-badge]][codecov]
[![license-badge]](LICENSE)


## Builder

The HiPEAC Vision printing press is a parser for the [hipeac.net/vision][hipeac-vision] document.
It takes all Word documents that the editorial board has written and converts them into a collection
of Python objects that can be used to generate different outputs.

### Application dependencies

The application uses [Poetry][poetry] to manage application dependencies.

```bash
poetry lock && poetry update && poetry sync
```

### Run the builder

This will generate a `.build` folder with all Word documents converted to Markdown and PDF files,
and a folder structure and Frontmatter fields that can be used by Vitepress to generate the website.

```bash
python build.py
```

### Run the tests

```bash
pytest --cov=hipeac_press --cov-report=term
```

### Style guide

Tab size is 4 spaces. Max line length is 120. You should run `ruff` before committing any change.

```bash
ruff format . && ruff check hipeac_press
```

## Frontend

The generated documents can be accessed as a [Vitepress][vitepress] website.

```bash
yarn
yarn build && yarn dev
```


[github-tests]: https://github.com/hipeac/hipeac-press/actions?query=workflow%3Atests-py
[github-tests-badge]: https://github.com/hipeac/hipeac-press/actions/workflows/tests_py.yml/badge.svg?branch=main
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg

[hipeac-vision]: https://www.hipeac.net/vision/

[vitepress]: https://vitepress.vuejs.org/
