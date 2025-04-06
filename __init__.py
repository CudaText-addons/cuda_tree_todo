from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)

TITLE_SEP = ':'
SYMBOLS = ['❍', '❑', '■', '□' , '☐', '▪' , '▫', '✓', '✔', '☑', '√', '✘']

def get_indent(filename, lines):
    try:
        import cuda_detect_indent
    except ImportError:
        msg_box(_('For the plugin to work properly, it is recommended to install the indentation detection plugin in Addons Manager: detect_indent'), MB_OK)
    bool_indent_spaces = False
    indent_spaces = ' '
    indent_tabs = '\t'
    for h in ed_handles():
        e = Editor(h)
        if (e.get_filename() == filename):
            bool_indent_spaces = e.get_prop(PROP_TAB_SPACES, '')
            ts_ = e.get_prop(PROP_TAB_SIZE, '')

            return ts_ * indent_spaces if bool_indent_spaces else indent_tabs

    return indent_tabs

def get_headers(filename, lines):
    indent_ = get_indent(filename, lines)
    res = []
    for i, line in enumerate(lines):
        if line.endswith(TITLE_SEP):
            line_ = line.split(TITLE_SEP)[0].strip()
            level_ = len(line.split(indent_))
            res.append(((level_-1, i, level_-1, i), level_, line_, 8))
        else:
            line_ = line.lstrip()
            for s in SYMBOLS:
                if line_.startswith(s):
                    level_ = len(line.split(indent_))
                    res.append(((level_-1, i, level_-1, i), level_, line_, 8))
                    break

    return res