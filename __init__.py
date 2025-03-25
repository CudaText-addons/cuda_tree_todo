TITLE_SEP = ':'
SYMBOLS = ['❍', '❑', '■', '□' , '☐', '▪' , '▫', '✓', '✔', '☑', '√', '✘']

def get_headers(filename, lines):
    res = []
    for i, line in enumerate(lines):
        if line.endswith(TITLE_SEP):
            line_ = line.split(TITLE_SEP)[0].strip()
            level_ = len(line.split('\t'))
            res.append(((level_-1, i, level_-1, i), level_, line_))
        for s in SYMBOLS:
            if s in line:
                line_ = s + ' ' + line.split(s)[1]
                level_ = len(line.split('\t'))
                res.append(((level_-1, i, level_-1, i), level_, line_))

    return res