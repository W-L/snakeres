from snakeres import utils, parsing, workflow_profile


def main():
    # get command line arguments
    args = utils.parse_args()
    # initialize the logger
    utils.init_logger(args)
    # parse the snakemake rules
    snake_rules = parsing.get_rules(args.input)
    # process the formatting of the directives
    for r in snake_rules.values():
        r.process_directives()
    # write certain directives to a workflow profile
    workflow_profile.write_profile(rules=snake_rules, output=args.output_profile)
    # rewrite the snakemake file to a version without these directives
    parsing.clean_snakefile(args.input, args.output_smk)


if __name__ == "__main__":
    main()


