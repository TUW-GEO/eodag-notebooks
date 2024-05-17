# Description
'''
ROI - Regions of Interest
=========================

This Script shall be used as a tool for the exercise 'applied remote sensing'.
It allows the user to define Regions of Interest and export them as geojson file
aswell as an png Image. The usage of QGIS in this exercies is therefore unnecessary.
'''

# Variables
__name__ = 'roi'
__version__ = '04-Aug-2023_v01'

# Modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.image as mpimg
import ipywidgets as widgets
from IPython.display import display
from shapely.geometry import Point, Polygon
import json
import rasterio


# Functions
def roi(image, dc, row, col, row_size, col_size, title='ROI', figsize=(8, 8), button_1="Woodland", button_2="Artificial-land", button_3="Water", button_4="Cropland",
        button_5="Bare-land", button_6="Grassland", button_7="Wetland", button_8="Shrubland", c1="g", c2="r", c3="b", c4="y", c5="m", c6="lightgreen", c7="c", c8="orange",
        alpha=0.2):
    """
    |
    |Interactive Plot in which you can create Polygons in different colors and with different labels of land usage.
    |The following buttons are available:
    |
    |   Button 1 - Button 8:
    |       By clicking, the land usage type and color of the next drawn polygon is selected.
    |
    |   Clear all button:
    |       Starts the process fresh-over: Clears the plot of all finished and started polygons.
    |       Also clears the list of polygons from any data.
    |
    |   Clear most recent button:
    |       Clears the most recent drawn polygon out of the list and the plot, if the polygon
    |       is not finished it clears the last clicked point (similar to ctrl+z button).
    |   Clear polygon button:
    |       After clicking the button it is possible to clear an individual, finished polygon
    |       by clicking inside of it.
    |   Export Geojson button:
    |       Creates geojson files of the drawn polygons, for each land usage type a seperate
    |       geojson file is created.
    |   Export png button:
    |       Creates a png image of the plot.
    |
    |
    |Parameters:
    |===========
    |   image: the image to be plotted
    |   dc: datacube of the filepaths used to create the image and containing the image geometry
    |   (row, col): the upper-left origin of the pixel window
    |   (row_size, col_size): the shape of the pixel window
    |   figsize: tuple with the figsize (default: (8,8))
    |   button_1 - button_8: string of the label for the land usage class (default: labels from eurostat land coverage statistics)
    |   c1 - c8: string of the color for each label
    |   alpha: transparency value for the filling of the polygons (default: 0.2)
    |
    |
    |Returns:
    |========
    | Has no return value, but plots the image and lets user draw polygons, which can be exported as geojson and png
    """

    def export_geojson(polygons):
        """
            Exports geojson files out of a dictionary containing coordinates of polygons and their respective labels and id's

            Parameters:
                polygons: dictionary containing polygons and information about the label and the id of the polygon
        """

        # Create a seperate dictionary for each label and define the basic layout of the geojson file
        button_1_dict = {"type": "FeatureCollection", "name": button_1, "features": []}
        button_2_dict = {"type": "FeatureCollection", "name": button_2, "features": []}
        button_3_dict = {"type": "FeatureCollection", "name": button_3, "features": []}
        button_4_dict = {"type": "FeatureCollection", "name": button_4, "features": []}
        button_5_dict = {"type": "FeatureCollection", "name": button_5, "features": []}
        button_6_dict = {"type": "FeatureCollection", "name": button_6, "features": []}
        button_7_dict = {"type": "FeatureCollection", "name": button_7, "features": []}
        button_8_dict = {"type": "FeatureCollection", "name": button_8, "features": []}

        # Add respective values to the feature- and id-key of each dictionary
        for polygon in polygons:
            if polygon["label"] == button_1:
                button_1_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_2:
                button_2_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_3:
                button_3_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_4:
                button_4_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_5:
                button_5_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_6:
                button_6_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_7:
                button_7_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})
            elif polygon["label"] == button_8:
                button_8_dict["features"].append({"type": "Feature", "properties": {"id": polygon["id"]}, "geometry": {"type": "Polygon", "coordinates": [polygon["coordinates"]]}})

        # Combine the dictionaries in a list and create an empty list for the filtered dictionaries
        dict_list_raw = [button_1_dict, button_2_dict, button_3_dict, button_4_dict, button_5_dict, button_6_dict, button_7_dict, button_8_dict]
        dict_list_filtered = []

        # Append non-empty dictionaries to the filtered dictionaries list
        for dictionary in dict_list_raw:
            if len(dictionary["features"]) > 0:
                dict_list_filtered.append(dictionary)

        # Export the geojson files
        for dictionary in dict_list_filtered:
            name = dictionary["name"].lower()
            with open(f"{name}.geojson", "w") as geojson_file:
                json.dump(dictionary, geojson_file)

    def redraw(polygons):
        """
            Draws polygons out of a dictionary containing the label of the polygon and the shapely polygon object.

            Parameters:
                polygons: dictionary containing polygons as shapely objects and the label of the polygon.
        """

        # The axes is cleared and the empty image is shown
        ax.clear()
        ax.imshow(image, extent=(xyext))

        # The polygons get drawn
        for polygon in polygons:
            if polygon["label"] == button_1:
                ax.plot(*polygon["polygon"].exterior.xy, c=c1)
                ax.fill(*polygon["polygon"].exterior.xy, c=c1, alpha=alpha)
            elif polygon["label"] == button_2:
                ax.plot(*polygon["polygon"].exterior.xy, c=c2)
                ax.fill(*polygon["polygon"].exterior.xy, c=c2, alpha=alpha)
            elif polygon["label"] == button_3:
                ax.plot(*polygon["polygon"].exterior.xy, c=c3)
                ax.fill(*polygon["polygon"].exterior.xy, c=c3, alpha=alpha)
            elif polygon["label"] == button_4:
                ax.plot(*polygon["polygon"].exterior.xy, c=c4)
                ax.fill(*polygon["polygon"].exterior.xy, c=c4, alpha=alpha)
            elif polygon["label"] == button_5:
                ax.plot(*polygon["polygon"].exterior.xy, c=c5)
                ax.fill(*polygon["polygon"].exterior.xy, c=c5, alpha=alpha)
            elif polygon["label"] == button_6:
                ax.plot(*polygon["polygon"].exterior.xy, c=c6)
                ax.fill(*polygon["polygon"].exterior.xy, c=c6, alpha=alpha)
            elif polygon["label"] == button_7:
                ax.plot(*polygon["polygon"].exterior.xy, c=c7)
                ax.fill(*polygon["polygon"].exterior.xy, c=c7, alpha=alpha)
            elif polygon["label"] == button_8:
                ax.plot(*polygon["polygon"].exterior.xy, c=c8)
                ax.fill(*polygon["polygon"].exterior.xy, c=c8, alpha=alpha)

    def on_image_click(event):
        """
            Defines what happens when the image is clicked
        """

        # Assert the error text and id list
        global error_text

        if event.inaxes is not None:

            ### Left mouseclick is defined to add points to a polygon and clear individual polygons ###
            if event.button == 1:

                # The x- and y-coordinate of the clicked point get saved
                clicked_point = [event.xdata, event.ydata]

                # If one of the label buttons is active one of the following statements is carried out
                if button1.value or button2.value or button3.value or button4.value or button5.value or button6.value or button7.value or button8.value:

                    # If an error text is shown it gets cleared of the plot
                    # if error_text is not None:
                    #     error_text.remove()
                    #     error_text = None

                    # The clicked point gets appended to the clicked points list
                    clicked_points.append(clicked_point)

                    ### The following eight statements treat the left mouseclick when one of the label buttons is acitve ###

                    # firstly the non active label buttons are disabled so it is not possible to change the label while still having an open polygon
                    # secondly a plot is drawn with the respective color of the label with regards to which coordinates the mouseclick has
                    # thirdly the drawn lines are saved into a line_segments list

                    if button1.value:
                        button2.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c1, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c1, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button2.value:
                        button1.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c2, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c2, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button3.value:
                        button1.disabled = True
                        button2.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c3, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c3, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button4.value:
                        button1.disabled = True
                        button2.disabled = True
                        button3.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c4, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c4, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button5.value:
                        button1.disabled = True
                        button2.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button6.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c5, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c5, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button6.value:
                        button1.disabled = True
                        button2.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button7.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c6, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c6, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button7.value:
                        button1.disabled = True
                        button2.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button8.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c7, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c7, ls="-", lw=1)
                        line_segments.append(line[0])

                    elif button8.value:
                        button1.disabled = True
                        button2.disabled = True
                        button3.disabled = True
                        button4.disabled = True
                        button5.disabled = True
                        button6.disabled = True
                        button7.disabled = True

                        plt.plot(clicked_point[0], clicked_point[1], c=c8, ls="-", lw=10, marker="x")
                        last_point = clicked_points[-2]
                        current_point = clicked_points[-1]
                        line = plt.plot([last_point[0], current_point[0]], [last_point[1], current_point[1]], c=c8, ls="-", lw=1)
                        line_segments.append(line[0])

                # If the clear polygon button is active one of the following statements is carried out
                elif clear_polygon_button.value:

                    # If the clicked points list is not empty an error text shows to make sure the polygon is finished before it is possible to delete a different polygon
                    if len(clicked_points) != 0:
                        ax.text(xyext[1] - (xyext[1] - xyext[0]) / 2 - 0.16 * (xyext[1] - xyext[0]), xyext[3] - (xyext[3] - xyext[2]) / 2, "Finish drawing previous polygon",
                                color='r', bbox={'facecolor': 'white', 'edgecolor': 'r', 'pad': 3})

                    # If the clicked points list is empty it is possible to delete a finished polygon by clicking inside of it
                    else:
                        clicked_polygon = None
                        point = Point(clicked_point)  # A shapely point object is created out of the clicked point

                        # If a finished polygon contains the point which is clicked it is removed out of the dictionary
                        for polygon in polygons:
                            if polygon['polygon'].contains(point):
                                polygons.remove(polygon)

                        # The plot gets redrawn
                        redraw(polygons)

                # If no button is active an error text is shown
                elif error_text is None:
                    error_text = ax.text(xyext[1] - (xyext[1] - xyext[0]) / 2 - 0.16 * (xyext[1] - xyext[0]), xyext[3] - (xyext[3] - xyext[2]) / 2,
                                         "Choose a label for the Polygon", color='r', bbox={'facecolor': 'white', 'edgecolor': 'r', 'pad': 3})

                else:
                    pass

            ### Right mouseclick is defined to close the polygon and save its data ###
            elif event.button == 3:

                # Making sure that at least three point have been clicked before closing the polygon
                if len(clicked_points) > 2:

                    ### Depending on the active label button the polygon is closed and the id of the polygon, a list of the coordinates of the vertices, a shapely polygon object
                    ### and the label of the polygon are saved into a dictionary and this dictionary is appended to a list containing the dictionary of each created polygon
                    if button1.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c1, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_1
                        polygons.append(polygon_dict.copy())


                    elif button2.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c2, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_2
                        polygons.append(polygon_dict.copy())

                    elif button3.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c3, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_3
                        polygons.append(polygon_dict.copy())

                    elif button4.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c4, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_4
                        polygons.append(polygon_dict.copy())

                    elif button5.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c5, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_5
                        polygons.append(polygon_dict.copy())

                    elif button6.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c6, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_6
                        polygons.append(polygon_dict.copy())

                    elif button7.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c7, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_7
                        polygons.append(polygon_dict.copy())

                    elif button8.value:
                        first_point = clicked_points[0]
                        last_point = clicked_points[-1]
                        clicked_points.append(first_point)

                        plt.plot([last_point[0], first_point[0]], [last_point[1], first_point[1]], c=c8, ls="-", lw=1)

                        polygon_dict["id"] = max(index) + 1
                        polygon_dict["coordinates"] = clicked_points.copy()
                        polygon_dict["polygon"] = Polygon(clicked_points.copy())
                        polygon_dict["label"] = button_8
                        polygons.append(polygon_dict.copy())

                    # To make sure no id is used twice the used ids are saved into a list
                    index.append(max(index) + 1)

                    # The polygons are redrawn
                    redraw(polygons)

                    # All the buttons are enabled and the clicked points list is cleared so a new polygon can be drawn
                    clicked_points.clear()

                    button1.disabled = False
                    button2.disabled = False
                    button3.disabled = False
                    button4.disabled = False
                    button5.disabled = False
                    button6.disabled = False
                    button7.disabled = False
                    button8.disabled = False

    ### The following nine deffinitions make sure only one button can be active at a time by deactivating all buttons except the button clicked ###
    def button1_clicked(change):
        if change.new:
            button2.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button2_clicked(change):
        if change.new:
            button1.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button3_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button4_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button5_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button4.value = False
            button6.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button6_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button7.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button7_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button8.value = False
            clear_polygon_button.value = False

    def button8_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            clear_polygon_button.value = False

    def clear_polygon_button_clicked(change):
        if change.new:
            button1.value = False
            button2.value = False
            button3.value = False
            button4.value = False
            button5.value = False
            button6.value = False
            button7.value = False
            button8.value = False

    ### The clear all button restores the original settings by clearing the plot, all the lists and dictionaries and enabling and deactivating all buttons ###
    def clear_all_button_clicked(button):
        polygons.clear()
        polygon_dict.clear()
        clicked_points.clear()
        line_segments.clear()

        ax.clear()
        ax.imshow(image, extent=(xyext))

        button1.disabled = False
        button2.disabled = False
        button3.disabled = False
        button4.disabled = False
        button5.disabled = False
        button6.disabled = False
        button7.disabled = False
        button8.disabled = False

        button1.value = False
        button2.value = False
        button3.value = False
        button4.value = False
        button5.value = False
        button6.value = False
        button7.value = False
        button8.value = False

    ### The clear most recent button clears the most recent drawn line and deletes the most recent coordinates out of the clicked points list if the clicked points list is not empty
    ### If the clicked points list is empty the most recent drawn polygon gets deleted as a whole
    def clear_most_recent_button_clicked(button):
        if len(clicked_points) > 0:
            if len(clicked_points) == 1:
                clicked_points.clear()
                line_segments.clear()
                plt.gca().lines[-1].remove()

                button1.disabled = False
                button2.disabled = False
                button3.disabled = False
                button4.disabled = False
                button5.disabled = False
                button6.disabled = False
                button7.disabled = False
                button8.disabled = False
            else:
                clicked_points.pop()
                line_segments[-1].remove()
                line_segments.pop()
                plt.gca().lines[-1].remove()
        else:
            polygons.pop()
            redraw(polygons)

    ### The export geojson button exports the polygons as a geojson file ###
    def export_geojson_button_clicked(button):
        export_geojson(polygons)

    ### The export png buttons exports a png of the figure ###
    def export_png_button_clicked(button):
        plt.savefig("ROI.png")

    ### The starting settings are defined ###
    polygons = []
    polygon_dict = {}
    clicked_points = []
    line_segments = []
    index = [0]
    error_text = None

    ### The label-buttons and the clear polygon-button are defined as togglebuttons and they are connected with the button_clicked function ###
    button1 = widgets.ToggleButton(value=False, description=button_1)
    button1.observe(button1_clicked, 'value')

    button2 = widgets.ToggleButton(value=False, description=button_2)
    button2.observe(button2_clicked, 'value')

    button3 = widgets.ToggleButton(value=False, description=button_3)
    button3.observe(button3_clicked, 'value')

    button4 = widgets.ToggleButton(value=False, description=button_4)
    button4.observe(button4_clicked, 'value')

    button5 = widgets.ToggleButton(value=False, description=button_5)
    button5.observe(button5_clicked, 'value')

    button6 = widgets.ToggleButton(value=False, description=button_6)
    button6.observe(button6_clicked, 'value')

    button7 = widgets.ToggleButton(value=False, description=button_7)
    button7.observe(button7_clicked, 'value')

    button8 = widgets.ToggleButton(value=False, description=button_8)
    button8.observe(button8_clicked, 'value')

    clear_polygon_button = widgets.ToggleButton(value=False, description="Clear polygon", button_style="warning")
    clear_polygon_button.observe(clear_polygon_button_clicked, 'value')

    ### The clear all-, clear most recent-, export geojson- and export png-button are defined as buttons and connected with the button_clicked function ###
    clear_all_button = widgets.Button(description='Clear all', button_style="danger")
    clear_all_button.on_click(clear_all_button_clicked)

    clear_most_recent_button = widgets.Button(description='Clear most recent', button_style="warning")
    clear_most_recent_button.on_click(clear_most_recent_button_clicked)

    export_geojson_button = widgets.Button(description='Export Geojson', button_style="success")
    export_geojson_button.on_click(export_geojson_button_clicked)

    export_png_button = widgets.Button(description='Export png', button_style="success")
    export_png_button.on_click(export_png_button_clicked)

    ### The buttons are stored in boxes ###
    buttons_box1 = widgets.HBox([button1, button2, button3, button4])
    buttons_box2 = widgets.HBox([button5, button6, button7, button8])
    buttons_box3 = widgets.HBox([clear_most_recent_button, clear_polygon_button])
    buttons_box4 = widgets.VBox([clear_all_button, export_geojson_button, export_png_button])
    buttons_box5 = widgets.VBox([buttons_box1, buttons_box2, buttons_box3])

    ### The image is plotted with the correct x- and y-axis ###
    coord_extent = dc.raster_geometry.slice_by_rc(col, row, col_size, row_size).coord_extent
    xyext = (coord_extent[0], coord_extent[2], coord_extent[1], coord_extent[3])
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image, extent=(xyext))
    ax.set_title(title)

    ### If there is a mouseclick on the image it is connected with the on image click function, also the buttons boxes are displayed ###
    cid = fig.canvas.mpl_connect('button_press_event', on_image_click)
    box = widgets.HBox([buttons_box5, buttons_box4])
    display(box)


def remove_empty_polygons(poly_dict):
    """
    Removes all entries (ids and values) from your polygon dictionary where the `ogr.Geometry` object is empty.

    Parameters
    ----------
    poly_dict : dict
        Dictionary containing a map between polygon IDs and `ogr.Geometry` polygons.

    Notes
    -----
    Modifies object in place.

    """
    polygons_to_remove = []
    for poly_id, poly in poly_dict.items():
        if poly.IsEmpty():
            polygons_to_remove.append(poly_id)

    for key in polygons_to_remove:
        del poly_dict[key]