import customtkinter as ctk
from typing import Any, Callable, Tuple
from PIL import Image

from utils import (
    create_table_label,
    create_table_value_textbox,
    get_textbox_value,
    update_textbox,
)

# TODO Add disable / enable


class ValuesTable(ctk.CTkFrame):
    def __init__(self, parent: Any) -> None:
        super().__init__(master=parent, fg_color="transparent")

        self._linked_operation_ = True
        self._linked_icon_ = ctk.CTkImage(
            Image.open("resources/link.jpg"), size=(20, 20)
        )
        self._unlinked_icon_ = ctk.CTkImage(
            Image.open("resources/broken.jpg"), size=(20, 20)
        )

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=1, pady=(20, 5))
        self._create_header_()
        # TODO add callback for number validation and updates
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

        # Percentage callbacks
        self._x_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)
        self._y_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)
        self._z_percent_textbox_.bind("<FocusOut>", self._percentage_update_cb_)

        # Value callbacks
        self._x_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)
        self._y_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)
        self._z_updated_textbox_.bind("<FocusOut>", self._value_update_cb_)

    def _create_header_(self):
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
        # Set up X row
        label = create_table_label(self, label)
        label.grid(row=row, column=0, padx=10, pady=(0, 20), sticky="ns")

        current_value = create_table_value_textbox(self, ctk.DISABLED)
        current_value.grid(row=row, column=1, padx=10, pady=(0, 20), sticky="ns")

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

        updated_value = create_table_value_textbox(self, ctk.NORMAL)
        updated_value.grid(row=row, column=3, padx=10, pady=(0, 20), sticky="ns")
        percentage_value = create_table_value_textbox(self, ctk.NORMAL)
        percentage_value.grid(row=row, column=4, padx=10, pady=(0, 20), sticky="ns")

        return label, current_value, button, updated_value, percentage_value

    def _toggle_linked_operation_cb_(self):
        if self._linked_operation_:
            self._toggle_button_.configure(image=self._unlinked_icon_)
        else:
            self._toggle_button_.configure(image=self._linked_icon_)

        self._linked_operation_ = not self._linked_operation_

    def _percentage_based_update_(self, reference_field):
        updated_percentage = float(get_textbox_value(reference_field))
        x_current = float(get_textbox_value(self._x_current_textbox_))
        y_current = float(get_textbox_value(self._y_current_textbox_))
        z_current = float(get_textbox_value(self._z_current_textbox_))
        elements_to_update = []

        if self._linked_operation_:
            # Update percentage boxes
            update_textbox(self._x_percent_textbox_, f"{updated_percentage:.2f}")
            update_textbox(self._y_percent_textbox_, f"{updated_percentage:.2f}")
            update_textbox(self._z_percent_textbox_, f"{updated_percentage:.2f}")

            elements_to_update += [
                (self._x_updated_textbox_, x_current),
                (self._y_updated_textbox_, y_current),
                (self._z_updated_textbox_, z_current),
            ]
        elif reference_field is self._x_percent_textbox_:
            elements_to_update.append((self._x_updated_textbox_, x_current))
        elif reference_field is self._y_percent_textbox_:
            elements_to_update.append((self._y_updated_textbox_, y_current))
        elif reference_field is self._z_percent_textbox_:
            elements_to_update.append((self._z_updated_textbox_, z_current))

        # Update updated values
        for element, current in elements_to_update:
            update_textbox(
                element,
                f"{(current * (updated_percentage / 100)):.2f}",
            )

    def _percentage_update_cb_(self, event) -> None:
        if event.widget.master in [
            self._x_percent_textbox_,
            self._y_percent_textbox_,
            self._z_percent_textbox_,
        ]:
            self._percentage_based_update_(event.widget.master)

    def _value_update_cb_(self, event) -> None:
        new_value = float(get_textbox_value(event.widget.master))
        percentage_textbox = None

        if event.widget.master is self._x_updated_textbox_:
            default_value = float(get_textbox_value(self._x_current_textbox_))
            percentage_textbox = self._x_percent_textbox_
        elif event.widget.master is self._y_updated_textbox_:
            default_value = float(get_textbox_value(self._y_current_textbox_))
            percentage_textbox = self._y_percent_textbox_
        elif event.widget.master is self._z_current_textbox_:
            default_value = float(get_textbox_value(self._z_current_textbox_))
            percentage_textbox = self._z_percent_textbox_

        if percentage_textbox:
            update_textbox(
                percentage_textbox, f"{(new_value / default_value * 100):.2f}"
            )
            self._percentage_based_update_(percentage_textbox)

    def set_initial_values(
        self, x_value: float, y_value: float, z_value: float
    ) -> None:
        update_textbox(self._x_current_textbox_, f"{x_value:.2f}")
        update_textbox(self._y_current_textbox_, f"{y_value:.2f}")
        update_textbox(self._z_current_textbox_, f"{z_value:.2f}")
        update_textbox(self._x_updated_textbox_, f"{x_value:.2f}")
        update_textbox(self._y_updated_textbox_, f"{y_value:.2f}")
        update_textbox(self._z_updated_textbox_, f"{z_value:.2f}")
        update_textbox(self._x_percent_textbox_, "100.00")
        update_textbox(self._y_percent_textbox_, "100.00")
        update_textbox(self._z_percent_textbox_, "100.00")

    def get_set_percentages(self) -> Tuple[float, float, float]:
        x_percentage = float(get_textbox_value(self._x_percent_textbox_)) / 100
        y_percentage = float(get_textbox_value(self._y_percent_textbox_)) / 100
        z_percentage = float(get_textbox_value(self._z_percent_textbox_)) / 100

        return x_percentage, y_percentage, z_percentage
