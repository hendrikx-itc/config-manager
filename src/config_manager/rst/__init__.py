def render_rst_head(title, underline_char='='):
    yield '{}\n'.format(title)
    yield '{}\n'.format(len(title) * underline_char)
