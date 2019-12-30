import sys
import argparse
from .convert_to_md import convert_to_md


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Convert text exported from Dynalist into Markdown format",
        epilog="""Must choose 'Asterisks' in Dynalist export panel. By default,
        lines of first level of indentation will be converted to heading 1,
        and lines of 2nd level will be converted to heading 2
        """)
    parser.add_argument('content', metavar='EXPORTED', nargs='?')
    parser.add_argument(
        '--start-heading',
        type=int,
        default=1,
        metavar="LVL",
        help="Starting Markdown heading level, e.g. 1 means heading 1 (#).")
    parser.add_argument(
        '--heading-depth',
        type=int,
        default=1,
        metavar="DEPTH",
        help="Depth of sub-headings, e.g. 1 means at most heading 2 (##)")

    args = parser.parse_args(argv[1:])
    ret_val, ret_msg = convert_to_md(iter(args.content.split('\n')),
                                     args.start_heading, args.heading_depth)
    if ret_val != 0:
        print(ret_msg, file=sys.stderr)
        exit(ret_val)

    print(ret_msg)


if __name__ == "__main__":
    main(sys.argv)
