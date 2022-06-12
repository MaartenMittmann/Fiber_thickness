"""
This program can be used to determine the distance of a black area between
two points. A file-name has to be written into the console after starting
the program (png-files only) and a maximum value for the RGB data has to
be set manually in the main function. Clicking twice in the loaded image
calculates the distance of the black area between the clicked points.
"""

import numpy as np
from matplotlib import pyplot as plt
import functools
import math


class ClickSaver:
    def __init__(self):
        self.clicked = True
        self.check_color = True
        self.points = np.zeros((2, 2))

    def get_clicked(self):
        return self.clicked

    def update(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True

    def update_color(self):
        if self.check_color:
            self.check_color = False
        else:
            self.check_color = True

    def flush(self):
        self.points = np.zeros((2, 2))


def picture(name):
    """Returns the RGB data for any given image"""
    img = plt.imread(name)
    plt.imshow(img)
    return img


def is_black(pix, max_val):
    """Checks whether a pixel is considered black."""
    if pix[0] < max_val and pix[1] < max_val and pix[2] < max_val:
        return True
    else:
        return False


def mouse_clicked(event, ax, img, steps, conversion, click_saver, max_val):
    """Calculates the distance between two clicked points."""
    mode = event.canvas.toolbar.mode

    if click_saver.get_clicked():
        if event.button == 1 and mode == '' and event.inaxes == ax:
            # Saving the clicked points in the first line of the created array
            click_saver.points[0, 0] = event.xdata
            click_saver.points[0, 1] = event.ydata

            # Setting first_click to false after the mouse has been clicked
            click_saver.update()

    else:
        if event.button == 1 and mode == '' and event.inaxes == ax:
            # Saving the clicked points in the second line of the created array
            click_saver.points[1, 0] = event.xdata
            click_saver.points[1, 1] = event.ydata

            # Updating the status for the next set of two clicked points
            click_saver.update()

            # Creating x-Array between two clicked points
            x = np.linspace(click_saver.points[0][0], click_saver.points[1][0], steps)
            # Computing parameters for linear function through both points
            a = (click_saver.points[0][1] - click_saver.points[1][1]) / (click_saver.points[0][0]
                                                                         - click_saver.points[1][0] + 0.0000001)
            b = click_saver.points[0][1] - a * click_saver.points[0][0]
            # Saving values of y-Array
            y = a * x + b

            # Creating an array, which later saves booleans for black pixels
            black = np.zeros(len(x), dtype=object)

            for i in range(0, len(x)):
                # Check whether that pixel is black and save boolean values
                black[i] = is_black(img[math.floor(y[i])][math.floor(x[i])], max_val=max_val)

            # Creating an array to later save the start and end points of black areas
            line_points = np.empty((0, 2), dtype=object)

            # Check for black pixels to save the start and end point of the black area
            for i in range(0, len(x)):
                if black[i]:
                    if click_saver.check_color:
                        line_points = np.append(line_points, np.array([[x[i], y[i]]]), axis=0)
                        click_saver.update_color()
                else:
                    if not click_saver.check_color:
                        line_points = np.append(line_points, np.array([[x[i], y[i]]]), axis=0)
                        click_saver.update_color()

            # Print the calculated lengths depending on the number of start and end points in the array
            if len(line_points) == 2:
                length = np.sqrt((line_points[1][0] - line_points[0][0])**2
                                 + (line_points[1][1] - line_points[0][1])**2)

                print("The measured thickness in pixels is: {}".format(length))

                length *= conversion

                print("The measured thickness in micrometers is: {}".format(length))
            elif len(line_points) == 0:
                print("No black area has been found.")
            else:
                print("More than one black area has been found. Their thicknesses are:")

                ind = 0

                while ind < len(line_points):

                    length = np.sqrt((line_points[ind+1][0] - line_points[ind][0])**2 +
                                     (line_points[ind+1][1] - line_points[ind][1])**2)

                    print("{} pixels or {} micrometers".format(length, conversion*length))

                    ind += 2

            click_saver.flush()


def main():

    print(__doc__)

    # The maximum value for the RGB data has to be set manually
    max_rgb = 0.35

    name = input(str("Please insert the name of the file:"))

    steps = 10000
    conversion = 1.714

    # Creating a plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Saving the RGB data of the picture
    img = picture(name)

    click_saver = ClickSaver()

    click_function = functools.partial(mouse_clicked, ax=ax, img=img, steps=steps,
                                       conversion=conversion, click_saver=click_saver,
                                       max_val=max_rgb)
    fig.canvas.mpl_connect('button_press_event', click_function)

    plt.show()


if __name__ == "__main__":
    main()
