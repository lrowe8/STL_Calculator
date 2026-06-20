import customtkinter as ctk

from utils import create_table_label, create_table_value_textbox


class ValuesTable(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _create_header_(self):
        self._original_label_ = create_table_label(self, "Original (in)")
        self._original_label_.grid(row=0, column=1, padx=10, pady=(0, 20), sticky="ns")
        self._updated_label_ = create_table_label(self, "Updated (in)")
        self._updated_label_.grid(row=0, column=3, padx=10, pady=(0, 20), sticky="ns")
        self._percentage_label_ = create_table_label(self, "Percentage")
        self._percentage_label_.grid(
            row=0, column=4, padx=10, pady=(0, 20), sticky="ns"
        )

    def _create_row_(self, label: str, row: int):
        # Set up X row
        label = create_table_label(self, label)
        label.grid(row=row, column=0, padx=10, pady=(0, 20), sticky="ns")

        current_value = create_table_value_textbox(self, ctk.DISABLED)
        current_value.grid(row=row, column=1, padx=10, pady=(0, 20), sticky="ns")

        button = ctk.CTkButton(
            master=self,
            text="",
            height=20,
            width=20,
            fg_color="transparent",
            bg_color="transparent",
            image=self._linked_icon_,
            command=self._toggle_linked_operation_,
        )
        self._linked_button_.grid(row=2, column=2, padx=10, pady=(0, 20), sticky="ns")

        updated_value = create_table_value_textbox(self, ctk.NORMAL)
        updated_value.grid(row=row, column=3, padx=10, pady=(0, 20), sticky="ns")
        percentage_value = create_table_value_textbox(self, ctk.NORMAL)
        percentage_value.grid(row=row, column=4, padx=10, pady=(0, 20), sticky="ns")
