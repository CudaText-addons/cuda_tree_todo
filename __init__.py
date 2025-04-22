import os
from cudatext import *

from cudax_lib import get_translation
_ = get_translation(__file__)

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
ini_section = os.path.basename(os.path.dirname(os.path.abspath(__file__))).replace('cuda_', '')
opts_def = dict(
    title_sep = ':',
    spec_symbols = '❍❑■□☐▪▫✓✔☑√✘+',
)

def load_opts():
    data = dict()
    for key in opts_def:
        data[key] = ini_read(fn_config, ini_section, key, opts_def[key])

    return data

opts = load_opts()

def save_opts():
    global opts
    for key in opts:
        ini_write(fn_config, ini_section, key, opts[key])

def get_indent(filename, lines):
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
    global opts
    for i, line in enumerate(lines):
        if line.endswith(opts['title_sep']):
            line_ = line.split(opts['title_sep'])[0].strip()
            level_ = len(line.split(indent_))
            res.append((((level_-1) * len(indent_), i, level_-1, i), level_, line_, -1))
        else:
            line_ = line.lstrip()
            for s in opts['spec_symbols']:
                if line_.startswith(s):
                    level_ = len(line.split(indent_))
                    res.append((((level_-1) * len(indent_), i, level_-1, i), level_, line_, -1))
                    break

    return res

class Command:
    def config(self):
        save_opts()
        file_open(fn_config)
        lines = [ed.get_text_line(i) for i in range(ed.get_line_count())]
        try:
            index = lines.index('[' + ini_section + ']')
            ed.set_caret(0, index)
        except:
            pass