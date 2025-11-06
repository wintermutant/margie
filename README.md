# 🌹🦠️🍄 margie 🍄🦠️🌹
### Mostly Automated Rapid Genome Inference Environment

_*Purpose*_: To rapidly annotate genomes in a scalable and confident manner using all of the latest tools and technologies.  

_*Philosophy*_: Pass

## 🚀 Quick Start

### Installing Pixi
First, install pixi (a fast package manager for conda environments):

```bash
# macOS/Linux
curl -fsSL https://pixi.sh/install.sh | bash

# Or with Homebrew on macOS
brew install pixi

# Windows
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Setting Up the Environment
1. Clone this repository and navigate to the project directory
2. Clone the [GeneralTools repository](https://github.com/Diet-Microbiome-Interactions-Lab/GeneralTools)
   1. Make sure the margie/ folder is in the same parent folder as GeneralTools/. i.e. - /path/to/folders/margie and /path/to/folders/GeneralTools.
   2. This is important because in our pixi.toml, one of our dependencies is the development/editable version of GeneralTools -->`[pypi-dependencies]
bioinformatics_tools = { path = "../GeneralTools", editable = true }`
3. Install dependencies with pixi:
   ```bash
   pixi install
   ```
4. Activate the environment:
   ```bash
   pixi shell
   ```

### Testing our initial codebase is good
Test to determine bioinformatics_tools imports properly
```bash
# Basic usage
python tests/test.py
# Should see output: ✅ Tests passed successfully!
```

### Margie Usage:
```bash
cd margie-tool
python fasta.py -i raw-fastas/*.fasta
# Should see output: ✅ Margie pipeline completed successfully!
# This will also create: margie-tools/output/from-default2/example.db & example2.db
```

## TODO: 

pass

## Contributors:
- Dane Deemer: Lead developer