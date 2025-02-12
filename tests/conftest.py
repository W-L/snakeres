from pathlib import Path

import pytest

from snakeres import parsing


@pytest.fixture(scope="module")
def snakefile():
    return '''
rule all:
    input:
        expand('results/{sample}_counts.txt', sample=['SRR17913199_01', 'SRR17913199_02', 'SRR17913199_03'])


rule test_rule:
    input:
        'data/{sample}.fastq'
    output:
        'results/{sample}_motif.fastq'
    threads:
        2
    resources:
        mem_mb=2000,
        time=20,
        partition='basic'
    group:
        'jobgroup1'
    shell:
        'grep CTCTCT -A 2 -B 1 {input} > {output}'
        
rule test_rule_oneline:
    input: 'data/{sample}.fastq'
    output: 'results/{sample}_motif.fastq'
    threads: 2
    resources:
        mem_mb=2000,
        time=20,
        partition='basic'
    group: 'jobgroup1'
    shell: 'grep CTCTCT -A 2 -B 1 {input} > {output}'
    
    
rule test_rule_named:
    input:
        filtered_fastq=rules.find_motif.output
    output:
        counts='results/{sample}_counts.txt'
    threads:
        6
    resources:
        mem_mb=4000,
        time=60,
        cpus_per_task=6
    group:
        'jobgroup1'
    shell:
        'grep "^@" {input} | wc -l > {output}'    
    '''




@pytest.fixture(scope="module")
def output_profile():
    output = """group-components:
    jobgroup1: 1
groups:
    test_rule: jobgroup1
    test_rule_named: jobgroup1
    test_rule_oneline: jobgroup1
set-resources:
    test_rule:
        mem_mb: 2000
        partition: basic
        time: 20
    test_rule_named:
        cpus_per_task: 6
        mem_mb: 4000
        time: 60
    test_rule_oneline:
        mem_mb: 2000
        partition: basic
        time: 20
set-threads:
    test_rule: 2
    test_rule_named: 6
    test_rule_oneline: 2
"""


    with open('test.profile', 'w') as f:
        f.write(output)
    return 'test.profile'


@pytest.fixture(scope="module")
def standard_rules(snakefile):
    test_snake = Path("test.snakefile")
    with open(test_snake, "w") as f:
        f.write(snakefile)

    rules = parsing.get_rules(test_snake)
    return rules


@pytest.fixture(scope="module")
def standard_rules_processed(standard_rules):
    for r in standard_rules.values():
        r.process_directives()
    return standard_rules
