#!/usr/bin/env python3
import jinja2
import sys
import argparse
from pathlib import Path


def main(argv=None):
    if argv is None:
        argv = sys.argv

    dest_choices = ['clipboard',
                    'new_record_cur_group']  # first item is default

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--start-heading',
                        type=int,
                        default=1,
                        metavar="LEVEL")
    parser.add_argument('--heading-depth',
                        type=int,
                        default=1,
                        metavar="DEPTH")
    parser.add_argument('--dest',
                        choices=dest_choices,
                        default=dest_choices[0])

    args = parser.parse_args(argv[1:])

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        str(Path(__file__).parent)),
                             trim_blocks=True,
                             lstrip_blocks=True)
    template = env.get_template('template.jxa.jinja')
    script_basename = "ClipboardTo{0}-{1}-{2}.jxa".format(
        ''.join(c.capitalize() for c in args.dest.split('_')),
        args.start_heading, args.heading_depth)
    script_path = Path(__file__).parent.joinpath(script_basename)

    with script_path.open('w') as f:
        f.write(template.render(vars(args)))


if __name__ == "__main__":
    main(sys.argv)
