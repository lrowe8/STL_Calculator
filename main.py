from vedo import Mesh, show, Plotter
import customtkinter as ctk
from PIL import Image
import os
import sys

from shared_utils import (
    create_table_value_textbox,
    create_table_label,
    update_textbox,
    get_textbox_value,
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Class variable initialization
        self._model_ = None
        self._linked_operation_ = True
        self._plot_ = None
        self._linked_icon_ = ctk.CTkImage(
            Image.open("resources/link.jpg"), size=(20, 20)
        )
        self._unlinked_icon_ = ctk.CTkImage(
            Image.open("resources/broken.jpg"), size=(20, 20)
        )

        # Configure application window dimensions
        self.title("CNC Router STL Application")
        self.geometry("800x800")

        # self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Set up load controls
        load_control_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        load_control_frame.grid_rowconfigure(0, weight=1)
        load_control_frame.grid_columnconfigure(2, weight=1)
        load_control_frame.grid(row=0, pady=(20, 5))
        self._set_load_controls_(load_control_frame)

        # Set up modification controls
        calc_control_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        calc_control_frame.grid_rowconfigure(2, weight=1)
        calc_control_frame.grid_columnconfigure(1, weight=1)
        calc_control_frame.grid(row=1, pady=(20, 5))
        self._setup_calc_table_(calc_control_frame)
        self._setup_calc_callbacks_()

        viz_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        viz_frame.grid(row=2, pady=(20, 5))
        self._set_viz_controls_(viz_frame)

    def _set_load_controls_(self, frame: ctk.CTkFrame):
        # Create label for load box
        self.my_label = ctk.CTkLabel(
            master=frame,
            height=20,
            text="Current File:",
            font=("Arial", 14, "bold"),
        )
        self.my_label.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="ns")

        # Create textbox
        self.my_textbox = ctk.CTkTextbox(
            master=frame, width=400, height=20, corner_radius=8, state=ctk.DISABLED
        )
        self.my_textbox.grid(row=0, column=1, padx=10, pady=(0, 20), sticky="ns")

        # Create load button
        self.button = ctk.CTkButton(
            frame, text="Load file", command=self._open_file_prompt_
        )
        self.button.grid(row=0, column=2, padx=10, pady=(0, 20))

    def _setup_calc_table_(self, frame: ctk.CTkFrame):
        # Set up header
        self._original_label_ = create_table_label(frame, "Original (in)")
        self._original_label_.grid(row=0, column=1, padx=10, pady=(0, 20), sticky="ns")
        self._updated_label_ = create_table_label(frame, "Updated (in)")
        self._updated_label_.grid(row=0, column=3, padx=10, pady=(0, 20), sticky="ns")
        self._percentage_label_ = create_table_label(frame, "Percentage")
        self._percentage_label_.grid(
            row=0, column=4, padx=10, pady=(0, 20), sticky="ns"
        )

        # Set up X row
        self._x_label = create_table_label(frame, "X Distance:")
        self._x_label.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ns")

        self._x_textbox_current_value_ = create_table_value_textbox(frame, ctk.DISABLED)
        self._x_textbox_current_value_.grid(
            row=1, column=1, padx=10, pady=(0, 20), sticky="ns"
        )

        self._x_textbox_updated_value_ = create_table_value_textbox(frame, ctk.NORMAL)
        self._x_textbox_updated_value_.grid(
            row=1, column=3, padx=10, pady=(0, 20), sticky="ns"
        )
        self._x_textbox_percentage_value_ = create_table_value_textbox(
            frame, ctk.NORMAL
        )
        self._x_textbox_percentage_value_.grid(
            row=1, column=4, padx=10, pady=(0, 20), sticky="ns"
        )
        # TODO add callback for number validation and updates
        # Setup Y row
        self._y_label = create_table_label(frame, "Y Distance:")
        self._y_label.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ns")

        self._y_textbox_current_value_ = create_table_value_textbox(frame, ctk.DISABLED)
        self._y_textbox_current_value_.grid(
            row=2, column=1, padx=10, pady=(0, 20), sticky="ns"
        )

        self._linked_operation_ = True
        self._linked_button_ = ctk.CTkButton(
            master=frame,
            text="",
            height=20,
            width=20,
            fg_color="transparent",
            bg_color="transparent",
            image=self._linked_icon_,
            command=self._toggle_linked_operation_,
        )
        self._linked_button_.grid(row=2, column=2, padx=10, pady=(0, 20), sticky="ns")

        self._y_textbox_updated_value_ = create_table_value_textbox(frame, ctk.NORMAL)
        self._y_textbox_updated_value_.grid(
            row=2, column=3, padx=10, pady=(0, 20), sticky="ns"
        )
        self._y_textbox_percentage_value_ = create_table_value_textbox(
            frame, ctk.NORMAL
        )
        self._y_textbox_percentage_value_.grid(
            row=2, column=4, padx=10, pady=(0, 20), sticky="ns"
        )

        # Set up Z row
        self._z_label = create_table_label(frame, "Z Distance:")
        self._z_label.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ns")

        # Create textbox
        self._z_textbox_current_value_ = create_table_value_textbox(frame, ctk.DISABLED)
        self._z_textbox_current_value_.grid(
            row=3, column=1, padx=10, pady=(0, 20), sticky="ns"
        )
        self._z_textbox_updated_value_ = create_table_value_textbox(frame, ctk.NORMAL)
        self._z_textbox_updated_value_.grid(
            row=3, column=3, padx=10, pady=(0, 20), sticky="ns"
        )
        self._z_textbox_percentage_value_ = create_table_value_textbox(
            frame, ctk.NORMAL
        )
        self._z_textbox_percentage_value_.grid(
            row=3, column=4, padx=10, pady=(0, 20), sticky="ns"
        )

    def _setup_calc_callbacks_(self):
        self._x_textbox_updated_value_.bind("<FocusOut>", self._values_update_)
        self._y_textbox_updated_value_.bind("<FocusOut>", self._values_update_)
        self._z_textbox_updated_value_.bind("<FocusOut>", self._values_update_)
        self._x_textbox_percentage_value_.bind("<FocusOut>", self._values_update_)
        self._y_textbox_percentage_value_.bind("<FocusOut>", self._values_update_)
        self._z_textbox_percentage_value_.bind("<FocusOut>", self._values_update_)

    def _set_viz_controls_(self, frame: ctk.CTkFrame):
        self._viz_button_ = ctk.CTkButton(
            frame, text="Visualize", command=self._visualize_, state=ctk.DISABLED
        )
        self._viz_button_.grid(row=0, column=0, padx=10, pady=(0, 20))

    def _update_size_values_(self):
        x_values = tuple(x / 25.4 for x in self._model_.xbounds())
        y_values = tuple(y / 25.4 for y in self._model_.ybounds())
        z_values = tuple(z / 25.4 for z in self._model_.zbounds())

        # Update original textboxes
        update_textbox(
            self._x_textbox_current_value_, f"{(x_values[1] - x_values[0]):.2f}"
        )
        update_textbox(
            self._y_textbox_current_value_, f"{(y_values[1] - y_values[0]):.2f}"
        )
        update_textbox(
            self._z_textbox_current_value_, f"{(z_values[1] - z_values[0]):.2f}"
        )

        # Update updated textboxes
        update_textbox(
            self._x_textbox_updated_value_, f"{(x_values[1] - x_values[0]):.2f}"
        )
        update_textbox(
            self._y_textbox_updated_value_, f"{(y_values[1] - y_values[0]):.2f}"
        )
        update_textbox(
            self._z_textbox_updated_value_, f"{(z_values[1] - z_values[0]):.2f}"
        )

        # Update percentage textboxes
        update_textbox(self._x_textbox_percentage_value_, f"{(100):.2f}")
        update_textbox(self._y_textbox_percentage_value_, f"{(100):.2f}")
        update_textbox(self._z_textbox_percentage_value_, f"{(100):.2f}")

    def _open_file_prompt_(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select a File", initialdir="/", filetypes=[("STL Files", "*.stl")]
        )

        if file_path:
            self._model_ = Mesh(file_path)

            # Update the file path
            update_textbox(self.my_textbox, file_path)

            # Update the size values
            self._update_size_values_()

            # Enable visualize button
            self._viz_button_.configure(state=ctk.NORMAL)

    def _toggle_linked_operation_(self):
        if self._linked_operation_:
            self._linked_button_.configure(image=self._unlinked_icon_)
        else:
            self._linked_button_.configure(image=self._linked_icon_)

        self._linked_operation_ = not self._linked_operation_

    def _visualize_(self):
        self._model_.show(axes=1)

    def _values_update_(self, event):
        if not self._linked_operation_:
            textbox_to_update = None
            val = float(get_textbox_value(event.widget.master))
            if event.widget.master is self._x_textbox_updated_value_:
                textbox_to_update = self._x_textbox_percentage_value_
                val /= float(get_textbox_value(self._x_textbox_current_value_))
            elif event.widget.master is self._y_textbox_updated_value_:
                textbox_to_update = self._y_textbox_percentage_value_
                val /= float(get_textbox_value(self._y_textbox_current_value_))
            elif event.widget.master is self._z_textbox_updated_value_:
                textbox_to_update = self._z_textbox_percentage_value_
                val /= float(get_textbox_value(self._y_textbox_current_value_))

            if textbox_to_update in (
                self._x_textbox_percentage_value_,
                self._y_textbox_percentage_value_,
                self._z_textbox_percentage_value_,
            ):
                val *= 100

            update_textbox(textbox_to_update, f"{val:.2f}")

        if event.widget.master in (
            self._x_textbox_updated_value_,
            self._y_textbox_updated_value_,
            self._z_textbox_updated_value_,
        ):
            print("Updated value")
        elif event.widget.master in (
            self._x_textbox_percentage_value_,
            self._y_textbox_percentage_value_,
            self._z_textbox_percentage_value_,
        ):
            print("Percentage update")
        else:
            print("Missed")
        pass


if __name__ == "__main__":
    vtk_path = os.path.join(sys.prefix, "Lib", "site-packages", "vtkmodules")

    if os.path.exists(vtk_path):
        os.add_dll_directory(vtk_path)

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
