default_style = "stroke: black; fill: none; stroke-width: 1"

__all__ = ["spline"]

def spline(x, y, style=None):
    spline_template = '<path style="{style}" d="{path}" />'
    if style is None:
        style = default_style
    path = 'M {x},{y} C {x},{y}'.format(x=x[0], y=y[0])
    path += ' {x},{y} {x},{y}'.format(x=x[1], y=y[1])
    for i in range(2, len(x)):
        path += ' S {x},{y} {x},{y}'.format(x=x[i], y=y[i])
    spline = spline_template.format(path=path, style=style)
    return spline

