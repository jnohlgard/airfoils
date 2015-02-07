default_style = "stroke: black; fill: none; stroke-width: 0.2"

__all__ = ["spline", "polyline"]
spline_template = '<path style="{style}" d="{path}"{stroke} />'
polyline_template = '<polyline style="{style}" points="{points}"{stroke} />'

def polyline(x, y, style=None, stroke=None):
    if style is None:
        style = default_style

    if stroke is not None:
        stroke = ' stroke="{stroke}"'.format(stroke=stroke)
    else:
        stroke = ''

    points = '{x},{y}'.format(x=x[0], y=y[0])
    for i in range(1, len(x)):
        points += ' {x},{y}'.format(x=x[i], y=y[i])
    polyline = polyline_template.format(points=points, style=style, stroke=stroke)
    return polyline

# See http://stackoverflow.com/questions/1257168/how-do-i-create-a-bezier-curve-to-represent-a-smoothed-polyline
def smooth_spline(x, y, tension, style=None, stroke=None):
    n = len(x);
    dx = list();
    dy = list();
    dx.append((x[1] - x[0]) * tension)
    dy.append((y[1] - y[0]) * tension)
    for i in range(1, n-1):
        dx.append((x[i+1] - x[i-1]) * tension)
        dy.append((y[i+1] - y[i-1]) * tension)
    dx.append((x[n-1] - x[n-2]) * tension)
    dy.append((y[n-1] - y[n-2]) * tension)

    if style is None:
        style = default_style

    if stroke is not None:
        stroke = ' stroke="{stroke}"'.format(stroke=stroke)
    else:
        stroke = ''

    path = 'M {x},{y} C {bx},{by}'.format(x=x[0], y=y[0], bx=x[0]+dx[0], by=y[0]+dy[0])
    path += ' {bx},{by} {x},{y}'.format(x=x[1], y=y[1], bx=x[1]-dx[1], by=y[1]-dy[1])
    for i in range(2, len(x)):
        path += ' S {bx},{by} {x},{y}'.format(x=x[i], y=y[i], bx=x[i]-dx[i], by=y[i]-dy[i])
    spline = spline_template.format(path=path, style=style, stroke=stroke)
    return spline
