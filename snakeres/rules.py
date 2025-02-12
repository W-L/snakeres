from snakeres.utils import try_convert_to_int



class Rule:
    def __init__(self, name: str) -> None:
        '''
        Class to represent a rule in a snakefile
        :param name: name of the rule
        '''
        self.name = name
        self.directives = {}



    def process_directives(self) -> None:
        '''
        fix the parsed structure of the directives
        :return:
        '''
        for key, value in self.directives.items():
            value_lines = split_multiline_directives(value)
            value_names = split_named_values(value_lines)
            value_formatted = try_convert_to_int(value_names)
            self.directives[key] = value_formatted



def split_multiline_directives(value) -> list | str:
    '''
    Split a directive that spans multiple lines, separated by commas
    :param value: The parsed value of the directive
    :return: Either split value or original value
    '''
    if ',' in value:
        return value.split(',')
    else:
        return value


def split_named_values(value) -> dict | str:
    '''
    Split a directive that contains named values
    :param value: The parsed value of the directive
    :return: Either a dict of named values or the original value
    '''
    def split_named_value(value, dirdict):
        dirdict[value.split('=')[0]] = try_convert_to_int(value.split('=')[1])
        return dirdict

    directive_dict = {}
    if type(value) == str:
        if '=' in value:
            return split_named_value(value, directive_dict)
        else:
            return value

    for i in value:
        if '=' in i:
            directive_dict = split_named_value(i, directive_dict)

    if directive_dict:
        return directive_dict
    else:
        return value


