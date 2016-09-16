# Imago Theory of Operation

This document gives a brief overview of the image processing that imago
does to recognize Go board positions.

The complete description is available in Tomáš Musil's paper "Optical
Game Position Recognition in the Board Game of Go" (2014), available at:
http://tomasm.cz/imago


# Phases

Imago processes each input image using the following steps:

1. Detect the grid lines of the board.

2. Compute the intersections of the grid lines.

3. Detect the stones at the intersections.


# Detecting the grid

This is the hardest step - the most time consuming and error prone.

Though automatic grid detection is the default behavior, to save time
and improve correctness the grid lines can be supplied manually, or from
a cache saved by an earlier invocation of imago.

Manual grid line detection is done interactively by the user, by clicking
on the corners of the board in the input image.

Imago can read grid information from cache files.  These cache files can
be saved by Imago after it learns the grid lines (by either detecting
them automatically, or by a user identifying them manually).  A later
invocation can read these cache files and avoid detection or manual
selection.  This only works if the board and camera did not move between
when the images were captured.


## Automatic grid line detection

Grid line detection is done in two steps:

1. Identify straight lines in the image

2. Identify the grid from all the straight lines.

```
lines, l1, l2, bounds, hough = linef.find_lines(image, do_something, logger)
grid, lines = gridf.find(lines, image.size, l1, l2, bounds, hough,
```

### Straight line detection

Straight line detection is done in `linef.find_lines()`.  This function
takes an image as input and returns the lines detected.

The image is in PIL Image format, and is processed with the PIL image
processing functions and with custom code that's part of Imago.

The image processing follows these steps:

```
    prepare():

        convert image to black and white (ITU-R 601-2 luma transform)

        perform edge detection on luma image (ie, identify regions of
        high spatial rate-of-change of luminance)

        perform high-pass filter on edge-detected image (FIXME: this doesn't
        seem to do much)

    create a Hough filter for the high-pass image

    transform():

        compute Hough transform of the high-pass image

        perform high-pass filter on Hough image

        find 'component centers' in hp-filtered Hough image (this seems
        to compress each blob of white to a single pixel at the "center"
        of the blob)

    run_ransac():
    
        runs RANSAC on the simplified hough image (This identifies straight
        lines in hough-space.  Why not run hough again?)

        Returns a list of two lists of points in the simplified hough
        image.  Each point is specified by its (x, y) coordinates, and
        identifies a line in the original input image.  Every such line
        within each list is roughly parallel to all the other lines in its
        list, and roughly perpendicular to the lines in the other list.

    convert these hough image coordinates to lines in (angle, distance) format

    return mapped lines
```


### Grid detection

Grid detection is done in `gridf.find()`
