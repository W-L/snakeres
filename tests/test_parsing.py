from pathlib import Path

from snakeres import parsing



def test_get_rules(standard_rules_processed):
    rules = standard_rules_processed

    assert "test_rule" in rules
    r = rules["test_rule"]
    assert r.directives["input"] == 'data/{sample}.fastq'
    assert r.directives["output"] == 'results/{sample}_motif.fastq'
    assert r.directives["threads"] == 2
    assert r.directives["resources"] == {'mem_mb': 2000, 'time': 20, "partition": 'basic'}
    assert r.directives["group"] == 'jobgroup1'


    assert "test_rule_oneline" in rules
    r = rules["test_rule_oneline"]
    assert r.directives["input"] == 'data/{sample}.fastq'
    assert r.directives["output"] == 'results/{sample}_motif.fastq'
    assert r.directives["threads"] == 2
    assert r.directives["resources"] == {'mem_mb': 2000, 'time': 20, "partition": 'basic'}
    assert r.directives["group"] == 'jobgroup1'


    assert "test_rule_named" in rules
    r = rules["test_rule_named"]
    assert r.directives["input"]['filtered_fastq'] == 'rules.find_motif.output'
    assert r.directives["output"]['counts'] == 'results/{sample}_counts.txt'
    assert r.directives["threads"] == 6
    assert r.directives["resources"] == {'mem_mb': 4000, 'time': 60, "cpus_per_task": 6}
    assert r.directives["group"] == 'jobgroup1'



def test_clean_snakefile(snakefile):
    test_snake = Path("test.snakefile")
    with open(test_snake, "w") as f:
        f.write(snakefile)

    parsing.clean_snakefile(test_snake, test_snake.with_suffix('.clean'))

    with open(test_snake.with_suffix('.clean'), "r") as f:
        cleaned_content = f.read()

    assert "threads" not in cleaned_content
    assert "resources" not in cleaned_content
    assert "group" not in cleaned_content


