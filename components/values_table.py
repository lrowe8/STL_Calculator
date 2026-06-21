import customtkinter as ctk
from typing import Any, Callable, Tuple
from PIL import Image

from utils import create_table_label, create_table_value_textbox


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
            "Y Distance:", 2, self._linked_icon_, self._toggle_linked_operation_
        )
        (
            self._z_label_,
            self._z_current_textbox_,
            _,
            self._z_updated_textbox_,
            self._z_percent_textbox_,
        ) = self._create_row_("Z Distance:", 3)

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

    def _toggle_linked_operation_(self):
        if self._linked_operation_:
            self._toggle_button_.configure(image=self._unlinked_icon_)
        else:
            self._toggle_button_.configure(image=self._linked_icon_)

        self._linked_operation_ = not self._linked_operation_
