from __future__ import division
from __future__ import print_function
from numpy import *

__all__ = ["naca4"]

def naca4(m, p, t, x):
    # Handle both percentage arguments and integer arguments
    if (m >= 1):
        m = m / 100
    if (p >= 1):
        p = p / 10
    if (t >= 1):
        t = t / 100
    # symmetric part
    yt = t/0.2 * (0.2969 * sqrt(x) -0.1260 * x -0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    if (p > 0):
        # camber, first half
        yc1 = m / p**2 * (2*p*x - x**2) * less(x, p);
        dyc1_dx = m / p**2 * (2*p - 2*x) * less(x, p)
        # camber, second half
        yc2 = m / (1-p)**2 * ((1-2*p) + 2*p*x - x**2) * greater_equal(x, p)
        dyc2_dx = m / (1-p)**2 * (2*p - 2*x) * greater_equal(x, p)
        dyc_dx = dyc1_dx + dyc2_dx
        theta = arctan(dyc_dx)
        yc = yc1 + yc2
        xu = x - yt * sin(theta)
        yu = yc + yt * cos(theta)
        xl = x + yt * sin(theta)
        yl = yc - yt * cos(theta)
    else:
        # symmetric airfoil
        xu = x
        yu = yt
        xl = x
        yl = -yt
    return (xu, yu, xl, yl, yc, yt)

def run():
    #~ from . import svg
    import svg
    svg_template = '''<?xml version="1.0" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg width="20cm" height="10cm" viewBox="0 0 1000 500" version="1.1"
         xmlns="http://www.w3.org/2000/svg">
      <desc>
      {desc}
      </desc>
      {contents}
    </svg>
    '''

    import argparse

    class IntRange(object):
        def __init__(self, lower, upper=None):
            if upper is None:
                lower, upper = 0, lower
            self.lower, self.upper = lower, upper

        def __call__(self, value):
            value = int(value)
            if value < self.lower or value >= self.upper:
                raise argparse.ArgumentTypeError('Number outside range')
            return value

    parser = argparse.ArgumentParser(description='Generate a SVG representation of a NACA 4-digit airfoil.')
    parser.add_argument('naca_number', metavar='number', type=IntRange(1000,10000),
                       help='NACA 4-digit airfoil number')
    parser.add_argument('-n', '--num-points', dest='num_points', metavar='N', type=int,
                       help='Number of control points per spline in the resulting file',
                       default=100)
    parser.add_argument('filename', help='Output filename (default: -, meaning standard output)', nargs='?', default='-')
    args = parser.parse_args()
    naca_number = args.naca_number
    filename = args.filename
    num_points = args.num_points

    t = naca_number % 100
    p = (naca_number // 100) % 10
    m = (naca_number // 1000);

    x = linspace(0, 1, num_points)
    (xu, yu, xl, yl, yc, yt) = naca4(m, p, t,x)
    upper = svg.spline(xu * 1000, 200-yu * 1000)
    lower = svg.spline(xl * 1000, 200-yl * 1000)
    camber = svg.spline(x * 1000, 200-yc * 1000, 'stroke: red; fill: none; stroke-width: 1')
    symmetric = svg.spline(x * 1000, 200-yt * 1000, 'stroke: blue; fill: none; stroke-width: 1')
    if filename == '-':
        print(svg_template.format(desc="NACA{num} Airfoil".format(num=naca_number), contents=upper+lower+camber+symmetric))
    else:
        with open(filename, 'w') as f:
            print(svg_template.format(desc="NACA{num} Airfoil".format(num=naca_number), contents=upper+lower+camber+symmetric), file=f)

if __name__ == '__main__':
    run()