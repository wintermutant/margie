# margie Documentation

This directory contains the Sphinx documentation for margie, using the Alabaster theme to match the bioinformatics-tools documentation.

## Building Documentation Locally

### Using Pixi (Recommended)

If you have the margie environment set up with pixi:

```bash
# Build the documentation
pixi run docs

# Clean build artifacts
pixi run docs-clean

# Build and serve locally (view at http://localhost:8000)
pixi run docs
pixi run docs-serve
```

### Using Make

If you prefer using Make:

```bash
cd docs

# Build HTML documentation
make html

# View the built documentation
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
start _build/html/index.html  # Windows

# Clean build artifacts
make clean
```

### Manual Build

```bash
cd docs
sphinx-build -b html . _build/html
```

## Documentation Structure

- `index.rst` - Main documentation page with project overview
- `usage.rst` - Usage guide and installation instructions
- `technical.rst` - Technical documentation and API reference
- `philosophy.rst` - Project philosophy and design principles
- `todo.rst` - Project roadmap and TODO items
- `conf.py` - Sphinx configuration (using Alabaster theme)
- `requirements.txt` - Documentation build dependencies

## ReadTheDocs

The documentation is configured to be built automatically on ReadTheDocs. The configuration is in `.readthedocs.yaml` in the project root.

To set up ReadTheDocs:

1. Go to https://readthedocs.org/
2. Sign in with your GitHub account
3. Import the margie repository
4. The documentation will be built automatically on each commit

## Adding New Pages

1. Create a new `.rst` file in this directory
2. Add it to the `toctree` in `index.rst`
3. Build the documentation to verify

## Editing Documentation

The documentation uses reStructuredText (.rst) format, matching the bioinformatics-tools documentation style.

### reStructuredText Resources

- [Sphinx reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [reStructuredText Quick Reference](https://docutils.sourceforge.io/docs/user/rst/quickref.html)

## Theme

The documentation uses the **Alabaster** theme, which is the same as the bioinformatics-tools documentation for consistency across projects.
