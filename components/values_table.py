"""
Description: The values table is responsible for building a table and associated control logic
Author: Name email
"""

import customtkinter as ctk
from tkinter import Event
from typing import Any, Callable, Tuple
from PIL import Image

from utils import (
    create_table_label,
    create_table_value_textbox,
    get_textbox_value,
    update_textbox,
)

# TODO Add disable / enable
# TODO add callback for number validation and updates
# TODO update the header function so that it matches the style of the row calls

"""
This class handles the table in the form and the logic for control
"""


class ValuesTable(ctk.CTkFrame):
    def __init__(self, parent: ctk.Ctk) -> None:
        """
        This function initializes the clas

        Inputs:
            parent(ctk.Ctk): The application handle

        Returns:
            type: desc
        """
        super().__init__(master=parent, fg_color="transparent")

        # Load the images
        self._linked_operation_ = True
        self._linked_icon_ = ctk.CTkImage(
            Image.open("resources/link.jpg"), size=(20, 20)
        )
        self._unlinked_icon_ = ctk.CTkImage(
            Image.open("resources/broken.jpg"), size=(20, 20)
        )

        # Set up the form layout
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=1, pady=(20, 5))

        self._create_header_()

        # Create the table rows
        (
            self._x_label_,
            self._x_current_textbox_,
            _,
            self._x_updated_textbox_,
            self._x_percent_textbox_,
        ) = self._create_row_("X Distance:", 1)
        (
            self._y_label_,
            self._y_current_textbox_,
            self._toggle_button_,
            self._y_updated_textbox_,
            self._y_percent_textbox_,
        ) = self._create_row_(
            "Y Distance:", 2, self._linked_icon_, self._toggle_linked_operation_cb_
        )
        (
            self._z_label_,
            self._z_current_textbox_,
            _,
            self._z_updated_textbox_,
            self._z_percent_textbox_,
        ) = self._create_row_("Z Distance:", 3)
        (
            self._max_edge_height_label_,
            self._max_edge_height_current_textbox_,
            _,
            self._max_edge_height_updated_textbox_,
            self._max_edge_height_percent_textbox_,
        ) = self._create_row_("Thickest Edge Height:", 4)
        (
            self._min_edge_height_label_,
            self._min_edge_height_current_textbox_,
            _,
            self._min_edge_height_updated_textbox_,
            self._min_edge_height_percent_textbox_,
        ) = self._create_row_("Thinnest Edge Height:", 5)

        # Percentage callbacks
        self._x_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)
        self._y_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)
        self._z_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)

        # Value callbacks
        self._x_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)
        self._y_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)
        self._z_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)

    def _create_header_(self) -> None:
        """
        This function creates the header for the table

        Inputs:
            None

        Returns:
            None
        """
        self._original_label_ = create_table_label(self, "Original (in)")
        self._original_label_.grid(row=0, column=1, padx=10, pady=(0, 20), sticky="ns")
        self._updated_label_ = create_table_label(self, "Updated (in)")
        self._updated_label_.grid(row=0, column=3, padx=10, pady=(0, 20), sticky="ns")
        self._percentage_label_ = create_table_label(self, "Percentage")
        self._percentage_label_.grid(
            row=0, column=4, padx=10, pady=(0, 20), sticky="ns"
        )

    def _create_row_(
        self,
        label: str,
        row: int,
        toggle_initial_image: ctk.CTkImage = None,
        toggle_callback: Callable = None,
    ) -> Tuple[
        ctk.CTkLabel, ctk.CTkTextbox, ctk.CTkButton, ctk.CTkTextbox, ctk.CTkTextbox
    ]:
        """
        This function creates a row for the table

        Inputs:
            label(str): The label to be used for the row
            row(int): The row number
            toggle_initial_image(ctk.CTkImage): The image to be used for the initial state (Default: None)
            toggle_callback(Callable): The toggle callback function

        Returns:
            Tuple[ctk.CTkLabel, ctk.CTkTextbox, ctk.CtkButton, ctk.CTkTextbox, ctk.CTkTextbox]:
                The handle for the label of the row
                The handle for the textbox that contains the value read in from the file
                The handle for the toggle button
                The handle for the textbox that contains the updated value
                The handle for the textbox that contains the percent scaling
        """
        # Set up the label
        label = create_table_label(self, label)
        label.grid(row=row, column=0, padx=10, pady=(0, 20), sticky="ns")

        # Set up the default value box
        current_value = create_table_value_textbox(self, ctk.DISABLED)
        current_value.grid(row=row, column=1, padx=10, pady=(0, 20), sticky="ns")

        # If an image was passed in, create the button using the provided image
        if toggle_initial_image:
            button = ctk.CTkButton(
                master=self,
                text="",
                height=20,
                width=20,
                fg_color="transparent",
                bg_color="transparent",
                image=toggle_initial_image,
                command=toggle_callback,
            )
            button.grid(row=row, column=2, padx=10, pady=(0, 20), sticky="ns")
        else:
            button = None

        # Set up the update value textbox
        updated_value = create_table_value_textbox(self, ctk.NORMAL)
        updated_value.grid(row=row, column=3, padx=10, pady=(0, 20), sticky="ns")

        # Set up the scaling percentage textbox
        percentage_value = create_table_value_textbox(self, ctk.NORMAL)
        percentage_value.grid(row=row, column=4, padx=10, pady=(0, 20), sticky="ns")

        return label, current_value, button, updated_value, percentage_value

    def _toggle_linked_operation_cb_(self) -> None:
        """
        Handles the toggle logic for linked operations

        Inputs:
            None

        Returns:
            None
        """
        # Update the image
        if self._linked_operation_:
            self._toggle_button_.configure(image=self._unlinked_icon_)
        else:
            self._toggle_button_.configure(image=self._linked_icon_)

        # Toggle the value
        self._linked_operation_ = not self._linked_operation_

    def _percentage_based_update_(self, reference_field: ctk.CTkTextbox) -> None:
        """
        Controls the operation for a percentage based update

        Inputs:
            reference_field(ctk.CTkTextbox): The textbox that lost focus

        Returns:
            None
        """
        # Get the value from the textbox that lost focus
        updated_percentage = float(get_textbox_value(reference_field))

        # Get the default values from each of the rows
        x_current = float(get_textbox_value(self._x_current_textbox_))
        y_current = float(get_textbox_value(self._y_current_textbox_))
        z_current = float(get_textbox_value(self._z_current_textbox_))
        max_edge_depth_current = float(
            get_textbox_value(self._max_edge_height_current_textbox_)
        )
        min_edge_depth_current = float(
            get_textbox_value(self._min_edge_height_current_textbox_)
        )

        # Container that stores the elements that need updated
        elements_to_update = []

        # If this is a linked operation
        if self._linked_operation_:
            # Update percentage boxes
            update_textbox(self._x_percent_textbox_, f"{updated_percentage:.2f}")
            update_textbox(self._y_percent_textbox_, f"{updated_percentage:.2f}")
            update_textbox(self._z_percent_textbox_, f"{updated_percentage:.2f}")
            update_textbox(
                self._max_edge_height_percent_textbox_, f"{updated_percentage:.2f}"
            )
            update_textbox(
                self._min_edge_height_percent_textbox_, f"{updated_percentage:.2f}"
            )

            elements_to_update += [
                (self._x_updated_textbox_, x_current),
                (self._y_updated_textbox_, y_current),
                (self._z_updated_textbox_, z_current),
                (
                    self._max_edge_height_updated_textbox_,
                    max_edge_depth_current,
                ),
                (
                    self._min_edge_height_updated_textbox_,
                    min_edge_depth_current,
                ),
            ]
        # Else this is not a linked operation.  Condition on the row that lost focus
        elif reference_field is self._x_percent_textbox_:
            elements_to_update.append((self._x_updated_textbox_, x_current))
        elif reference_field is self._y_percent_textbox_:
            elements_to_update.append((self._y_updated_textbox_, y_current))
        # If that field was a Z field we need to scale the thicknesses as well
        elif reference_field is self._z_percent_textbox_:
            elements_to_update.append((self._z_updated_textbox_, z_current))
            elements_to_update.append(
                (
                    self._max_edge_height_updated_textbox_,
                    max_edge_depth_current,
                )
            )
            elements_to_update.append(
                (
                    self._min_edge_height_updated_textbox_,
                    min_edge_depth_current,
                )
            )

        # Update updated values
        for element, current in elements_to_update:
            update_textbox(
                element,
                f"{(current * (updated_percentage / 100)):.2f}",
            )

    def _percentage_update_cb_(self, event: Event) -> None:
        """
        The callback function for percentage based updates

        Inputs:
            event(Event): The tkinter event

        Returns:
            None
        """
        # Condition for the percentage update fields
        if event.widget.master in [
            self._x_percent_textbox_,
            self._y_percent_textbox_,
            self._z_percent_textbox_,
        ]:
            self._percentage_based_update_(event.widget.master)

    def _value_update_cb_(self, event: Event) -> None:
        """
        The callback for a value based update

        Inputs:
            event(Event): The tkinter triggering event

        Returns:
            None
        """
        # Get the updated value based on the event
        updated_value = float(get_textbox_value(event.widget.master))

        # Container for elements to update
        to_update = []

        # Contition for the element that triggered the event, then calculate the updated percentage
        if event.widget.master is self._x_updated_textbox_:
            to_update.append(
                (
                    f"{(updated_value / float(get_textbox_value(self._x_current_textbox_)) * 100):.2f}",
                    self._x_percent_textbox_,
                )
            )
        elif event.widget.master is self._y_updated_textbox_:
            to_update.append(
                (
                    f"{(updated_value / float(get_textbox_value(self._y_current_textbox_)) * 100):.2f}",
                    self._y_percent_textbox_,
                )
            )
        elif event.widget.master is self._z_updated_textbox_:
            z_percentage = updated_value / float(
                get_textbox_value(self._z_current_textbox_)
            )

            to_update.append(
                (
                    f"{z_percentage * 100:.2f}",
                    self._z_percent_textbox_,
                )
            )
            to_update.append(
                (
                    f"{z_percentage * 100:.2f}",
                    self._max_edge_height_percent_textbox_,
                )
            )
            to_update.append(
                (
                    f"{z_percentage * 100:.2f}",
                    self._min_edge_height_percent_textbox_,
                )
            )

        # Iterate through all of the elements that should be updated
        for updated_value, percentage_textbox in to_update:
            update_textbox(percentage_textbox, updated_value)
            self._percentage_based_update_(percentage_textbox)

    def set_initial_values(
        self,
        x_value: float,
        y_value: float,
        z_value: float,
        thickest_edge_thickness: float,
        thinnest_edge_thickness: float,
    ) -> None:
        """
        Responsible for setting the initial values in the form

        Inputs:
            x_value(float): The default value for the x axis
            y_value(float): The default value for the y axis
            z_value(float): The default value for the z axis
            thickest_edge_thickness(float): The thickness of the thickest edge
            thinnest_edge_thickness(float): The thickness of the thinnest edge

        Returns:
            None
        """
        # Set the initial / default values
        update_textbox(self._x_current_textbox_, f"{x_value:.2f}")
        update_textbox(self._y_current_textbox_, f"{y_value:.2f}")
        update_textbox(self._z_current_textbox_, f"{z_value:.2f}")
        update_textbox(
            self._max_edge_height_current_textbox_, f"{thickest_edge_thickness:.2f}"
        )
        update_textbox(
            self._min_edge_height_current_textbox_, f"{thinnest_edge_thickness:.2f}"
        )

        # Set the updated values
        update_textbox(self._x_updated_textbox_, f"{x_value:.2f}")
        update_textbox(self._y_updated_textbox_, f"{y_value:.2f}")
        update_textbox(self._z_updated_textbox_, f"{z_value:.2f}")
        update_textbox(
            self._max_edge_height_updated_textbox_, f"{thickest_edge_thickness:.2f}"
        )
        update_textbox(
            self._min_edge_height_updated_textbox_, f"{thinnest_edge_thickness:.2f}"
        )

        # Set the percentage fields
        update_textbox(self._x_percent_textbox_, "100.00")
        update_textbox(self._y_percent_textbox_, "100.00")
        update_textbox(self._z_percent_textbox_, "100.00")
        update_textbox(self._max_edge_height_percent_textbox_, "100.00")
        update_textbox(self._min_edge_height_percent_textbox_, "100.00")

    def get_percentages(self) -> Tuple[float, float, float]:
        """
        Returns the percentages for each of the axis

        Inputs:
            None

        Returns:
            Tuple[float, float, float]: x-axis, y-axis, z_axis
        """
        x_percentage = float(get_textbox_value(self._x_percent_textbox_)) / 100
        y_percentage = float(get_textbox_value(self._y_percent_textbox_)) / 100
        z_percentage = float(get_textbox_value(self._z_percent_textbox_)) / 100

        return x_percentage, y_percentage, z_percentage
