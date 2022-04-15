#!/usr/bin/env python

import argparse
import pathlib
import inspect
import yaml
import functools
import operator


this_file = pathlib.Path((inspect.getfile(inspect.currentframe())))
app_dir = this_file.joinpath('..', '..').resolve()
default_config_file = app_dir.joinpath('secrets', 'config.yml')


class Config(object):
    def __init__(self, key_chain, config_file=default_config_file, output_file=None):
        with open(config_file, 'r') as stream:
            data = yaml.safe_load(stream)

        keys = [str.strip() for str in key_chain.split()]

        deployments_dict = data['deployments']

        config = functools.reduce(operator.getitem, keys, deployments_dict)

        self.__output_file(output_file, config)

        self.data = config

    def __output_file(self, output_file, config):
        if not output_file:
            return

        ofp = pathlib.Path(output_file)

        suffix = ofp.suffix[1:]
        match suffix:
            case 'yml' | 'yaml':
                with open(output_file, 'w') as stream:
                    stream.write(yaml.dump(config))
            case _:
                raise RuntimeError(f"unsupported output file suffix '{suffix}'")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to interface with config file')

    parser.add_argument(
        '-k', '--key-chain',
        dest='key_chain',
        help="'key1 key2 key3': the list of keys separated by a space to dig into the YAML data",
        required=True
    )

    parser.add_argument(
        '-i', '--config-file',
        dest='config_file',
        default=default_config_file
    )

    parser.add_argument(
        '-o', '--output-file',
        dest='output_file'
    )

    args = parser.parse_args()

    config = Config(key_chain=args.key_chain, config_file=args.config_file, output_file=args.output_file)

    if not args.output_file:
        print(config.data)
