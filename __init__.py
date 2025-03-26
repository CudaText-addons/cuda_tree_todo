from cudatext import *

TITLE_SEP = ':'
SYMBOLS = ['❍', '❑', '■', '□' , '☐', '▪' , '▫', '✓', '✔', '☑', '√', '✘']

# cuda_detect_indent
def get_indent(lines):
    MIN_INDENTED_LINES = 5
    MAX_READ_LINES = 20
    INDENT_SPACES = True

    nlines = min(MAX_READ_LINES, sum(1 for line in lines))
    lines = lines[:nlines]

    starts_with_tab = 0
    spaces_list = []
    indented_lines = 0

    for line in lines:
        if not line: continue
        if line[0] == "\t":
            starts_with_tab += 1
            indented_lines += 1
        elif line.startswith(' '):
            spaces = 0
            for ch in line:
                if ch == ' ': spaces += 1
                else: break
            if spaces > 1 and spaces != len(line):
                indented_lines += 1
                spaces_list.append(spaces)

    evidence = [1.0, 1.0, 0.8, 0.9, 0.8, 0.9, 0.9, 0.95, 1.0]

    if indented_lines >= MIN_INDENTED_LINES:
        if len(spaces_list) > starts_with_tab:
            for indent in range(8, 1, -1):
                same_indent = list(filter(lambda x: x % indent == 0, spaces_list))
                if len(same_indent) >= evidence[indent] * len(spaces_list):
                    INDENT_SPACES = True

            for indent in range(8, 1, -2):
                same_indent = list(filter(lambda x: x % indent == 0 or x % indent == 1, spaces_list))
                if len(same_indent) >= evidence[indent] * len(spaces_list):
                    INDENT_SPACES = True

        elif starts_with_tab >= 0.8 * indented_lines:
            INDENT_SPACES = False

    return ed.get_prop(PROP_TAB_SIZE) * ' ' if INDENT_SPACES else '\t'

def get_headers(filename, lines):
    indent_ = get_indent(lines)
    res = []
    for i, line in enumerate(lines):
        if line.endswith(TITLE_SEP):
            line_ = line.split(TITLE_SEP)[0].strip()
            level_ = len(line.split(indent_))
            res.append(((level_-1, i, level_-1, i), level_, line_))
        else:
            line_ = line.lstrip()
            for s in SYMBOLS:
                if line_.startswith(s):
                    level_ = len(line.split(indent_))
                    res.append(((level_-1, i, level_-1, i), level_, line_))

    return res