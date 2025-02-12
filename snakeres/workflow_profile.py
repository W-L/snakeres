import logging
from pathlib import Path

import yaml




def write_profile(rules: dict, output: Path, default_groupsize: int = 1) -> None:
    '''
    Write the values of certain directives to a profile according to snakemake profile structure
    :param rules: dictionary of rules
    :param output: path for output profile
    :param default_groupsize: default size for job groups
    :return:
    '''
    # iterate over rules to get the values of the directives
    direc = ['threads', 'resources', 'group']
    direc_dict = {}
    for d in direc:
        direc_dict[d] = _get_directives(rules, d)

    # create mock group components for output
    group_components = {g: default_groupsize for g in set(direc_dict['group'].values())}
    # print some information
    logging.info(f'Writing profile to {output}')
    logging.info(f'Number of threads directives: {len(direc_dict["threads"])}')
    logging.info(f'Number of resources directives: {len(direc_dict["resources"])}')
    logging.info(f'Number of group directives: {len(direc_dict["group"])}')
    logging.info('')

    # create the profile dictionary
    profile = {
        'set-threads': direc_dict['threads'],
        'set-resources': direc_dict['resources'],
        'groups': direc_dict['group'],
        'group-components': group_components
    }
    # dump the profile to a yaml file
    with open(output, 'w') as f:
        yaml.dump(profile, f, default_flow_style=False, indent=4)




def _get_directives(rules: dict, directive: str) -> dict:
    '''
    Get the values of a specific directive from all rules
    :param rules: dictionary of rules
    :param directive: names of the directive
    :return: dictionary of the directive values for each rule
    '''
    d = dict()
    for rule in rules.values():
        if directive in rule.directives:
            d[rule.name] = rule.directives[directive]
    return d





