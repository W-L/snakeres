import argparse
import pytest
from pathlib import Path
from snakeres import utils


def test_parse_args(monkeypatch):
    test_args = ["snakeres", "--input", "test.snakefile"]
    monkeypatch.setattr("sys.argv", test_args)
    args = utils.parse_args()
    assert args.input == Path("test.snakefile")
    assert args.output_profile == Path("profile.yaml")
    assert args.output_smk == Path("snakefile_cleaned")

def test_try_convert_to_int():
    assert utils.try_convert_to_int("123") == 123
    assert utils.try_convert_to_int("abc") == "abc"
    assert utils.try_convert_to_int(None) == None


