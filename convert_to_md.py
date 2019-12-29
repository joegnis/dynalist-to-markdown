#!/usr/bin/env python3
# Pass '-h' to command line to see help message
import re
import sys
import argparse
import itertools
import io


class ExportLine:

    indent_space = 4

    @classmethod
    def get_indent_string(cls, n=1):
        n = max(0, n)
        return " " * cls.indent_space * n

    def __init__(self, line, comments=None, indent=0):
        self.line = line
        if comments is None:
            comments = []
        self.comments = comments
        self.indent = indent

    def to_markdown_heading(self, heading_lvl):
        with io.StringIO() as ret:
            for _ in range(heading_lvl):
                ret.write("#")
            ret.write(' ' + self.line)
            ret.write("\n\n")

            if self.comments:
                if self.is_comment_code_block():
                    ret.write(self.get_comment_code_block())
                else:
                    ret.write("\n".join(self.comments))
                    ret.write("\n")
                ret.write("\n")

            return ret.getvalue()

    def to_markdown_paragraph(self):
        is_with_bullet_comment = False
        with io.StringIO() as ret:
            ret.write(self.line)
            ret.write("\n")

            if self.comments:
                if self.is_comment_code_block():
                    ret.write(self.get_comment_code_block())
                    ret.write('\n')
                else:
                    ret.write("* ")
                    ret.write(" ".join(self.comments))
                    ret.write("\n")
                    is_with_bullet_comment = True
            else:
                ret.write("\n")

            return ret.getvalue(), is_with_bullet_comment

    def to_list_item(self, indent_offset=0):
        with io.StringIO() as ret:
            ret.write(self.get_indent_string(self.indent + indent_offset))
            ret.write("* ")
            ret.write(self.line)
            ret.write("\n")

            if self.comments:
                if self.is_comment_code_block():
                    ret.write(self.get_comment_code_block(self.indent, 2))
                else:
                    ret.write(
                        self.get_indent_string(self.indent + indent_offset +
                                               1))
                    ret.write("* ")
                    ret.write(" ".join(self.comments))
                    ret.write("\n")

            return ret.getvalue()

    def is_comment_code_block(self):
        if not self.comments:
            return False
        if re.match(r"^`+", self.comments[0]) and re.match(
                r"`+$", self.comments[-1]):
            return True
        else:
            return False

    def get_comment_code_block(self, indent=0, extra_ws=0):
        ws = self.get_indent_string(indent) + " " * extra_ws
        with io.StringIO() as ret:
            ret.write(ws + "```\n")  # 1st line
            ret.write(ws + re.sub(r"^`+", "", self.comments[0]))
            ret.write("\n")  # 2nd line
            ret.write(ws)
            ret.write(("\n" + ws).join(self.comments[1:-1]))
            ret.write("\n")  # middle lines
            ret.write(ws + re.sub(r"`+$", "", self.comments[-1]))
            ret.write("\n")  # 2nd last line
            ret.write(ws + "```\n")  # last line
            return ret.getvalue()


def strip_line(line):
    return re.sub(r'^ *(\* )?', '', line)


def find_comment_lines(iter_exported, parent_line):
    comment_line_space = count_precede_space(parent_line) + 2
    comments = []
    while True:
        iter_exported, iter_peek = itertools.tee(iter_exported)
        line = next(iter_peek, None)
        if not line:  # Can be either None or ''
            break

        if re.match(r"^ *\* ", line) is None:
            comments.append(line[comment_line_space:])  # Strip whitespaces
        else:
            break

        iter_exported = iter_peek

    return comments, iter_exported


def count_precede_space(line):
    count = 0
    for c in line:
        if c == ' ':
            count += 1
        else:
            break
    return count


def count_indent(line):
    return count_precede_space(line) // ExportLine.indent_space


def convert_to_md(iter_exported, start_heading, heading_depth):
    first_line = next(iter_exported, None)

    if first_line is None or len(first_line) == 0:
        return 1, "Empty input"

    if first_line[0] != '*':
        return 1, "Invalid input"

    export_lines = []
    comments, iter_exported = find_comment_lines(iter_exported, first_line)
    export_lines.append(ExportLine(strip_line(first_line), comments))

    line = next(iter_exported, None)
    while line is not None:
        if re.match(r"^ *\* ", line):  # ignore empty lines
            # Comment area will be scanned and stored along with each item (line)
            comments, iter_exported = find_comment_lines(iter_exported, line)
            export_lines.append(
                ExportLine(strip_line(line), comments, count_indent(line)))
        line = next(iter_exported, None)

    with io.StringIO() as converted:
        is_prev_list = False
        is_prev_para_with_cmnt = False
        for exp_line in export_lines:
            if exp_line.indent <= heading_depth:
                if is_prev_list:
                    converted.write("\n")
                    is_prev_list = False
                if is_prev_para_with_cmnt:
                    converted.write("\n")
                    is_prev_para_with_cmnt = False

                converted.write(
                    exp_line.to_markdown_heading(start_heading +
                                                 exp_line.indent))
            elif exp_line.indent == heading_depth + 1:
                if is_prev_list:
                    converted.write("\n")
                    is_prev_list = False
                if is_prev_para_with_cmnt:
                    converted.write("\n")
                    is_prev_para_with_cmnt = False
                p, is_prev_para_with_cmnt = exp_line.to_markdown_paragraph()
                converted.write(p)
            else:
                if is_prev_para_with_cmnt:
                    is_prev_para_with_cmnt = False
                converted.write(exp_line.to_list_item(-2 - heading_depth))
                is_prev_list = True
        return 0, converted.getvalue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert text exported from Dynalist into Markdown format",
        epilog="""Must choose 'Asterisks' in Dynalist export panel. By default,
        lines of first level of indentation will be converted to heading 1,
        and lines of 2nd level will be converted to heading 2
        """)
    parser.add_argument('content', metavar='EXPORTED', narg='?')
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

    args = parser.parse_args()
    ret_val, ret_msg = convert_to_md(iter(args.content.split('\n')),
                                     args.start_heading, args.heading_depth)
    if ret_val != 0:
        print(ret_msg, file=sys.stderr)
        exit(ret_val)

    print(ret_msg)