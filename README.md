# snakeres

This tool can be used to extract the resource specifications and job grouping from a snakemake workflow and create a workflow profile. 
It also writes a version of the workflow definition with the resource specifications and grouping information removed.



## Installation

snakeres needs python >=3.12 and pip. Then it can be installed with:

`pip install snakeres`

## Usage

```
usage: snakeres [-h] [--input INPUT] [--output-profile OUTPUT_PROFILE] [--output-smk OUTPUT_SMK]

Generate a workflow profile from a snakefile

options:
-h, --help                              show this help message and exit
--input INPUT                           Path to snakefile
--output-profile OUTPUT_PROFILE         Output profile file (default: profile.yaml)
--output-smk OUTPUT_SMK                 Output snakefile without the directives (default: snakefile_cleaned)
```


## Testing

The code is covered by pytests. To run these install: `pip install pytest pytest-cov`. Then run tests: `cd tests; pytest --cov --cov-report html`.
To test local builds: `hatch build && pip install dist/snakeres-V-py3-none-any.whl --force-reinstall --no-deps`



## Install development environment

```
conda env create -f dev.yaml -n snakeres_dev
conda activate snakeres_dev
pip install -e .
cd tests
pytest --cov --cov-report html
```

# New release

```
hatch build
pip install dist/snakeres-V-py3-none-any.whl --force-reinstall --no-deps
pytest --cov --cov-report html
hatch publish
```

