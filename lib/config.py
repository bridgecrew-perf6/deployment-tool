#!/usr/bin/env python

import argparse
import pathlib
import inspect
import yaml
import functools
import sys


this_file = pathlib.Path((inspect.getfile(inspect.currentframe())))
app_dir = this_file.joinpath('..', '..').resolve()
secrets_dir = app_dir.joinpath('secrets')
default_config_file = secrets_dir.joinpath('config.yml')


class Config(object):
    def __init__(
        self,
        deployment_name,
        section,
        config_file=default_config_file, output_file=None, key_chain=None
    ):
        with open(config_file, 'r') as stream:
            data = yaml.safe_load(stream)

        config = data['deployments'][deployment_name][section]

        self.__resolve_paths(config)

        self.data = config
        if output_file:
            self.__output_file(output_file, config)
            return

        if key_chain:
            self.value = self.__key_chain(config, key_chain)

    def print_ips(self):
        print("\n".join(self.data['ips']))

    def __resolve_paths(self, config):
        ptr_key = 'paths_to_resolve'
        if ptr_key not in config:
            return

        ptr = config[ptr_key]

        for path_key in ptr:
            if path_key not in config:
                continue

            config[path_key] = secrets_dir.joinpath(config[path_key]).as_posix()

        return config

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

    def __key_chain(self, config, key_chain):
        keys = [str.strip() for str in key_chain.split()]
        return functools.reduce(dict.get, keys, config)

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to interface with config file')

    parser.add_argument(
        '-d', '--deployment-name',
        dest='deployment_name',
        required=True
    )

    section_choices = ['cm', 'infra']
    parser.add_argument(
        '-s', '--section',
        dest='section',
        choices=section_choices,
        help=f'{section_choices}',
        required=True
    )

    parser.add_argument(
        '-k', '--key-chain',
        dest='key_chain',
        help="'key1 key2 key3': the list of keys separated by a space to dig into the YAML data",
    )

    parser.add_argument(
        '-c', '--config-file',
        dest='config_file',
        default=default_config_file
    )

    parser.add_argument(
        '-o', '--output-file',
        dest='output_file'
    )

    parser.add_argument(
        '-i', '--ips',
        dest='ips',
        action=argparse.BooleanOptionalAction
    )

    args = parser.parse_args()

    config = Config(
        args.deployment_name,
        args.section,
        key_chain=args.key_chain, config_file=args.config_file, output_file=args.output_file
    )

    if args.ips:
        config.print_ips()
        sys.exit()

    if args.key_chain:
        if config.value:
            print(config.value)

        sys.exit()
