"""Manual grid selection module"""

from math import sqrt, acos, copysign
from PIL import ImageDraw
import pygame

from geometry import l2ad, line, intersection
from manual_lines import *
import debug_display
import traceback

class UserQuitError(Exception):
    pass

def find_lines(im_orig):
    # TODO rename, refactor, comment

    im = im_orig.copy()

    screen = debug_display.Screen((620, 350))

    font = pygame.font.Font(None, 25)
    instructions = ["Imago manual mode", "",   
    "To set the grid position, click on the corners of the grid. Once you mark",
    "all four corners, the grid will appear. To adjust it, just click on the new",
    "position and the nearest corner will move there. Once you are content",
    "with the alignment, press any key on your keyboard or close the window.",
    "", "", "",
    "Press any key to continue."]
    y = 10
    for i in instructions:
        text1 = font.render(i, True, [128, 255, 128])
        screen._screen.blit(text1, [10, y])
        y += 25

    pygame.display.flip()

    screen.wait_for_click_or_keypress()

    pygame.display.set_mode(im.size)

    clock = pygame.time.Clock()
    draw = ImageDraw.Draw(im)
    hoshi = lambda c: draw.ellipse((c[0] - 1, c[1] - 1, c[0] + 1, c[1] + 1),
                 fill=(255, 64, 64))
    corners = []
    color = (32, 255, 32)
    line_width = 1
    lines_r = []

    def dst((x1, y1), (x2, y2)):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                if len(corners) == 4:
                    return lines_r
                else:
                    raise UserQuitError 
            if event.type == pygame.MOUSEBUTTONDOWN:
                np = pygame.mouse.get_pos()
                if len(corners) >= 4: 
                    corners.sort(key=lambda p: dst(p, np))
                    corners = corners[1:]
                corners.append(np)
                (x, y) = corners[-1]
                draw.line((x-2, y, x + 2, y), fill=color)
                draw.line((x, y+2, x, y-2), fill=color)
                if len(corners) == 4:
                    im = im_orig.copy()
                    draw = ImageDraw.Draw(im)
                    try:
                        l_vert, l_hor = lines(corners, screen, im_orig.copy())
                        print "l_vert:", l_vert
                        print "l_hor:", l_hor
                    except Exception as e:
                        print "exception!", e
                        traceback.print_exc()
                        corners = corners[:-1]
                        continue
                    for l in l_vert:
                        draw.line(l, fill=color, width=line_width)
                    for l in l_hor:
                        draw.line(l, fill=color, width=line_width)
                    # TODO sort by distance
                    #l_vert.sort()
                    #l_hor.sort()
                    #for i in [3, 9, 15]:
                    #    for j in [3, 9, 15]:
                    #        hoshi(intersection(line(l_vert[i][0], l_vert[i][1]),
                    #                           line(l_hor[j][0], l_hor[j][1])))
                    lines_r = [[l2ad(l, im.size) for l in l_vert], 
                               [l2ad(l, im.size) for l in l_hor]]

        screen.display_picture(im)
        clock.tick(15)


