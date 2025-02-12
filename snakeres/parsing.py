import pathlib
import re
import logging
from collections import defaultdict

from snakeres.rules import Rule



def get_rules(snakefile: pathlib.Path) -> dict:
    '''
    Parse the snakefile and return a dictionary of rules with directives
    :param snakefile: Input snakemake file
    :return: Dictionary of rules
    '''
    rules = {}
    current_rule = None
    current_directive = None

    with open(snakefile, 'r') as f:
        for line in f:
            line = line.strip()

            # Detect rule and checkpoint names
            rule_match = re.match(r'^(rule|checkpoint)\s+(\w+):', line)
            if rule_match:
                rule_name = rule_match.group(2)
                # skip the rule all since it does not have directives other than input
                if rule_name == 'all':
                    continue
                current_rule = Rule(rule_name)
                # store the rule in the output dictionary
                rules[rule_name] = current_rule
                current_directive = None
                continue

            # Detect and store directives
            if current_rule:
                directive_match = re.match(r'(\w+):\s*(.*)', line)
                if directive_match:
                    directive_key = directive_match.group(1)
                    directive_value = directive_match.group(2)
                    # remove spaces and quotes from the directive value
                    directive_value_clean = directive_value.strip().replace('"', '').replace("'", '')
                    current_directive = directive_key
                    if current_directive == 'shell':
                        continue
                    current_rule.directives[directive_key] = directive_value_clean
                elif current_directive:
                    if current_directive == 'shell':
                        continue
                    # Append to the current directive value
                    line_clean = line.strip().replace('"', '').replace("'", '')
                    current_rule.directives[current_directive] += line_clean

    logging.info(f'Parsed {len(rules)} rules')
    logging.info(f'')
    return rules




def clean_snakefile(input_file: pathlib.Path, output_file: pathlib.Path) -> None:
    '''
    Clean the snakefile by removing only certain directives
    :param input_file:
    :param output_file:
    :return:
    '''
    to_remove = {'resources', 'threads', 'group'}
    n_removed = defaultdict(int)
    # read the entire snakefile into memory
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # write a new file by iterating the input lines
    with open(output_file, 'w') as f:
        current_directive = None
        for line in lines:
            stripped_line = line.strip()

            # Detect and skip resources, threads, and group directives
            directive_match = re.match(r'(\w+):\s*(.*)', stripped_line)
            if directive_match:
                directive_key = directive_match.group(1)
                # only skip writing these directives
                if directive_key in to_remove:
                    n_removed[directive_key] += 1
                    current_directive = directive_key
                    continue
                else:
                    # other directives that we don't want to omit
                    current_directive = None
            elif current_directive:
                # skip lines belonging to the current directive
                continue
            f.write(line)

    # write some info about removed directives
    logging.info(f'Writing new snakefile to {output_file}')
    for k, v in n_removed.items():
        logging.info(f'Omitted {v} {k} directives')
    logging.info('')
