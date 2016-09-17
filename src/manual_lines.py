"""Computing the grid"""

import unittest
from math import sqrt, acos, copysign
from geometry import l2ad, line, intersection
from PIL import ImageDraw
import pygame
import debug_display

def lines(corners, screen, image):
    print "lines():"
    for c in corners:
        print "    c:", c

    draw = ImageDraw.Draw(image)
    line_width = 1

    # TODO Error on triangle 
    corners.sort() # TODO does this help?
    # TODO refactor this vvv
    cor_d = [(corners[0], (c[0] - corners[0][0], c[1] - corners[0][1]), c) for c in
             corners[1:]]
    cor_d = [(float(a[0] * b[0] + a[1] * b[1]) / (sqrt(a[0] ** 2 + a[1] ** 2) *
              sqrt(b[0] **2 + b[1] ** 2)), a[0] * b[1] - b[0] * a[1], c) for a, b, c in cor_d]
    cor_d = sorted([(copysign(acos(min(a, 1)), b), c) for a, b, c in cor_d])
    corners = [corners[0]] + [c for _, c in cor_d]
    print "manipulated corners:"
    for c in corners:
        print "    c:", c

    # inside horizontals
    l0 = _lines(corners, 0, image.copy())
    print "l0:", l0
    for l in l0:
        draw.line(l, fill=(255, 32, 32), width=line_width)

    # outside horizontals
    l1 = [(corners[0], corners[3]), (corners[1], corners[2])]
    print "l1:", l1
    for l in l1:
        draw.line(l, fill=(32, 255, 32), width=line_width)

    # inside verticals
    l2 = _lines(corners[1:4] + [corners[0]], 0, image.copy())
    print "l2:", l2
    for l in l2:
        draw.line(l, fill=(32, 32, 255), width=line_width)

    # outside verticals
    l3 = [(corners[0], corners[1]), (corners[2], corners[3])]
    print "l3:", l3
    for l in l3:
        draw.line(l, fill=(255, 255, 255), width=line_width)

    screen.display_picture(image)
    screen.wait_for_click_or_keypress()

    return (l0 + l1, l2 + l3)

def _lines(corners, n, image):
    orig_image = image.copy()
    print "_lines()"
    screen = debug_display.Screen(image.size, image=image)
    red = 120*n
    for c in corners:
        print "    c:", c
        screen.draw_cross(c, red, 40, 40, width=2)
    print "    n:", n

    # `mid_line` is a line that joins the midpoints of two oposite sides
    # of the quadrilateral defined by the four passed-in corners.
    mid_line = half_line(corners)

    # TODO what is this?
    if n == 0:
        screen.draw.line(mid_line, fill=(red, 40, 40), width=2)
        print "_lines(n=0) setup done"
        screen.display_picture(image)
        screen.wait_for_click_or_keypress()

        # This recurses to look at the part of the quadrilateral on
        # *one* side of `mid_line`.  Returns all lines on that side,
        # not including `mid_line` but including the other edge.
        recurse_image = image.copy()
        l0 = _lines([corners[0], mid_line[0], mid_line[1], corners[3]], 1, recurse_image)
        print "_lines(n=0) first recursion done"
        screen.display_picture(recurse_image)
        screen.wait_for_click_or_keypress()

        # This is just the mid-line.
        l1 = [mid_line]

        # This recurses to look at the part of the quadrilateral on the
        # *other* side of `mid_line`.  Returns all lines on that side,
        # not including `mid_line` but including the other edge.
        recurse_image = image.copy()
        l2 = _lines([mid_line[0], corners[1], corners[2], mid_line[1]], 1, recurse_image)
        print "_lines(n=0) second recursion done"
        screen.display_picture(recurse_image)
        screen.wait_for_click_or_keypress()

        for l in l0:
            screen.draw.line(l, fill=(255, 32, 32), width=1)
        for l in l1:
            screen.draw.line(l, fill=(32, 255, 32, 32), width=1)
        for l in l2:
            screen.draw.line(l, fill=(32, 32, 255), width=1)
        print "_lines(n=0) done"
        screen.display_picture(image)
        screen.wait_for_click_or_keypress()

        return (l0 + l1 + l2)

    else:
        c = intersection(line(mid_line[0], corners[2]), line(corners[1], corners[3]))
        d = intersection(line(corners[0], corners[3]), line(corners[1], corners[2]))
        if d:
            l = (intersection(line(corners[0], corners[1]), line(c, d)),
                 intersection(line(corners[2], corners[3]), line(c, d)))
        else:
            lx = line(c, (c[0] + corners[0][0] - corners[3][0], 
                      c[1] + corners[0][1] - corners[3][1]))
            l = (intersection(line(corners[0], corners[1]), lx),
                 intersection(line(corners[2], corners[3]), lx))
        l2 = half_line([corners[0], l[0], l[1], corners[3]])

        screen.draw.line(mid_line, fill=(0, 0, 255), width=1)
        screen.draw_cross(c, 0, 0, 255)
        if d: screen.draw_cross(d, 0, 0, 255)
        screen.draw.line(l, fill=(0, 0, 255), width=1)
        screen.draw.line(l2, fill=(0, 0, 255), width=1)

        print "_lines(n= 1 or 2) setup done"
        screen.display_picture(image)
        screen.wait_for_click_or_keypress()

        if n == 1:
            s0 = [l, l2]

            recurse_image = image.copy()
            s1 = _lines([l[0], l2[0], l2[1], l[1]], 2, recurse_image)
            print "_lines(n=1) first recursion done"
            screen.display_picture(recurse_image)
            screen.wait_for_click_or_keypress()

            recurse_image = image.copy()
            s2 = _lines([corners[0], l2[0], l2[1], corners[3]], 2, recurse_image)
            print "_lines(n=1) second recursion done"
            screen.display_picture(recurse_image)
            screen.wait_for_click_or_keypress()

            recurse_image = image.copy()
            s3 = _lines([l[0], corners[1], corners[2], l[1]], 2, recurse_image)
            print "_lines(n=1) third recursion done"
            screen.display_picture(recurse_image)
            screen.wait_for_click_or_keypress()

            for s in s0:
                screen.draw.line(s, fill=(255, 32, 32), width=1)
            for s in s1:
                screen.draw.line(s, fill=(32, 255, 32), width=1)
            for s in s2:
                screen.draw.line(s, fill=(32, 32, 255), width=1)
            for s in s3:
                screen.draw.line(s, fill=(255, 255, 255), width=1)
            print "_lines(n=1) done"
            print "    s0:", s0
            print "    s1:", s1
            print "    s2:", s2
            print "    s3:", s3
            screen.display_picture(image)
            screen.wait_for_click_or_keypress()
            return (s0 + s1 + s2 + s3)
        if n == 2:
            s0 = [l, l2]
            for s in s0:
                screen.draw.line(s, fill=(25, 255, 32), width=1)
            print "_lines(n=2) done"
            print "    s0:", s0
            screen.display_picture(image)
            screen.wait_for_click_or_keypress()
            return s0


def half_line(corners):
    """Divides a quadrilateral in half.

    The argument `corners` is a list of four points (tuples of (x, y)),
    representing the corners of a quadrilateral.  The list may start
    on any of the four corners, but must go around the quadrilateral in
    clockwise or counter-clockwise order; skipping around is not allowed.

    The function returns a line (a list of two points) that joins the
    midpoints of two oposite sides of the quadrilateral defined by the
    four passed-in corners.  Arbitrarily, the bisected sides are the
    one joining corner 0 and corner 1, and the one joining corner 2 and
    corner 3."""

    c = center(corners)

    # `d` is the perspective vanishing point for the two sides that
    # we're *not* bisecting.
    d = intersection(line(corners[0], corners[3]), line(corners[1], corners[2]))
    if not d:
        # No vanishing point found: the two sides must be parallel.
        # So just use one of the sides as the direction.  This adds
        # the vector from corner[3] to corner[0] to the center point we
        # computed above.
        d = (c[0] + corners[0][0] - corners[3][0], c[1] + corners[0][1] - corners[3][1])

    l = line(c, d)
    p1 = intersection(l, line(corners[0], corners[1]))
    p2 = intersection(l, line(corners[2], corners[3]))
    r = (p1, p2)
    return r

def center(corners):
    """Given a list of four corner points, return the center of the square."""
    print "center():"
    for c in corners:
        print "    c:", c
    return intersection(line(corners[0], corners[2]), 
                        line(corners[1], corners[3]))


#
# Just tests below here.
#

class test_manual_lines(unittest.TestCase):
    def test_half_line(self):

        """This function tests the half_line() function.  It passes
        in corner-tuples for a bunch of different quadrilaterals and
        verifies that the returned half-line is the expected one."""

        # square
        corners = (
            (0, 0),
            (10, 0),
            (10, 10),
            (0, 10)
        )
        r = half_line(corners)
        assert(r == ((5, 0), (5, 10)))

        # parallelogram leaning right
        corners = (
            (0, 0),
            (10, 0),
            (20, 10),
            (10, 10)
        )
        r = half_line(corners)
        assert(r == ((5, 0), (15, 10)))

        # parallelogram leaning up
        corners = (
            (0, 0),
            (10, 10),
            (10, 20),
            (0, 10)
        )
        r = half_line(corners)
        assert(r == ((5, 5), (5, 15)))

        # isosceles trapezoid, pinched at top
        corners = (
            (0, 0),
            (10, 0),
            (8, 10),
            (2, 10)
        )
        r = half_line(corners)
        assert(r == ((5, 0), (5, 10)))

        # isosceles trapezoid, pinched at bottom
        corners = (
            (2, 0),
            (8, 0),
            (10, 10),
            (0, 10)
        )
        r = half_line(corners)
        assert(r == ((5, 0), (5, 10)))

        # isosceles trapezoid, pinched at right
        corners = (
            (0, 0),
            (10, 2),
            (10, 8),
            (0, 10)
        )
        r = half_line(corners)
        assert(r == ((6, 1), (6, 9)))

        # isosceles trapezoid, pinched at left
        corners = (
            (0, 2),
            (10, 0),
            (10, 10),
            (0, 8)
        )
        r = half_line(corners)
        assert(r == ((4, 1), (4, 9)))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_manual_lines)
    unittest.TextTestRunner(verbosity=2).run(suite)
