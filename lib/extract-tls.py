#!/usr/bin/env python

import argparse
import pathlib
import inspect
import os
import subprocess

from config import Config

this_file = pathlib.Path((inspect.getfile(inspect.currentframe())))
app_dir = this_file.joinpath('..', '..').resolve()


class ExtractTLS(object):
    def __init__(self, config):
        md_key = 'main_domain'
        if md_key not in config:
            return

        secrets_dir = pathlib.Path(config['secrets_dir'])
        archive_fp = secrets_dir.joinpath('.'.join([config[md_key], 'tar', 'xz']))

        if archive_fp.is_file():
            os.chdir(pathlib.Path(config['cert_files_dir']).parent)

            subprocess.run(['tar', 'xJvf', archive_fp], check=True)

            archive_fp.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract TLS files')

    parser.add_argument(
        '-d', '--deployment-name',
        dest='deployment_name',
        required=True
    )

    args = parser.parse_args()

    config = Config(
        args.deployment_name,
        'cm'
    )

    ExtractTLS(config)
