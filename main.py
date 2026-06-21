from vedo import Mesh, Plotter
import customtkinter as ctk
from PIL import Image
import os
import sys

from components import ValuesTable
from utils import (
    # create_table_value_textbox,
    # create_table_label,
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

        self._values_table_ = ValuesTable(self)

        viz_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        viz_frame.grid(row=2, pady=(20, 5))
        self._set_viz_controls_(viz_frame)

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

    def _set_viz_controls_(self, frame: ctk.CTkFrame):
        self._viz_button_ = ctk.CTkButton(
            frame, text="Visualize", command=self._visualize_, state=ctk.DISABLED
        )
        self._viz_button_.grid(row=0, column=0, padx=10, pady=(0, 20))

    # def _setup_calc_table_(self, frame: ctk.CTkFrame):

    #     # TODO add callback for number validation and updates
    #     # Setup Y row
    #     self._y_label = create_table_label(frame, "Y Distance:")
    #     self._y_label.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ns")

    #     self._y_textbox_current_value_ = create_table_value_textbox(frame, ctk.DISABLED)
    #     self._y_textbox_current_value_.grid(
    #         row=2, column=1, padx=10, pady=(0, 20), sticky="ns"
    #     )

    #     self._linked_operation_ = True
    #     self._linked_button_ = ctk.CTkButton(
    #         master=frame,
    #         text="",
    #         height=20,
    #         width=20,
    #         fg_color="transparent",
    #         bg_color="transparent",
    #         image=self._linked_icon_,
    #         command=self._toggle_linked_operation_,
    #     )
    #     self._linked_button_.grid(row=2, column=2, padx=10, pady=(0, 20), sticky="ns")

    #     self._y_textbox_updated_value_ = create_table_value_textbox(frame, ctk.NORMAL)
    #     self._y_textbox_updated_value_.grid(
    #         row=2, column=3, padx=10, pady=(0, 20), sticky="ns"
    #     )
    #     self._y_textbox_percentage_value_ = create_table_value_textbox(
    #         frame, ctk.NORMAL
    #     )
    #     self._y_textbox_percentage_value_.grid(
    #         row=2, column=4, padx=10, pady=(0, 20), sticky="ns"
    #     )

    #     # Set up Z row
    #     self._z_label = create_table_label(frame, "Z Distance:")
    #     self._z_label.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="ns")

    #     # Create textbox
    #     self._z_textbox_current_value_ = create_table_value_textbox(frame, ctk.DISABLED)
    #     self._z_textbox_current_value_.grid(
    #         row=3, column=1, padx=10, pady=(0, 20), sticky="ns"
    #     )
    #     self._z_textbox_updated_value_ = create_table_value_textbox(frame, ctk.NORMAL)
    #     self._z_textbox_updated_value_.grid(
    #         row=3, column=3, padx=10, pady=(0, 20), sticky="ns"
    #     )
    #     self._z_textbox_percentage_value_ = create_table_value_textbox(
    #         frame, ctk.NORMAL
    #     )
    #     self._z_textbox_percentage_value_.grid(
    #         row=3, column=4, padx=10, pady=(0, 20), sticky="ns"
    #     )

    def _setup_calc_callbacks_(self):
        self._x_textbox_updated_value_.bind("<FocusOut>", self._x_values_update_)
        self._y_textbox_updated_value_.bind("<FocusOut>", self._y_values_update_)
        self._z_textbox_updated_value_.bind("<FocusOut>", self._z_values_update_)
        self._x_textbox_percentage_value_.bind("<FocusOut>", self._x_values_update_)
        self._y_textbox_percentage_value_.bind("<FocusOut>", self._y_values_update_)
        self._z_textbox_percentage_value_.bind("<FocusOut>", self._z_values_update_)

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

    def _toggle_linked_operation_(self):
        if self._linked_operation_:
            self._linked_button_.configure(image=self._unlinked_icon_)
        else:
            self._linked_button_.configure(image=self._linked_icon_)

        self._linked_operation_ = not self._linked_operation_

    def _visualize_(self):
        print(f"Before Scale{self._model_.zbounds()}")
        x_percentage = float(get_textbox_value(self._x_textbox_percentage_value_))
        y_percentage = float(get_textbox_value(self._y_textbox_percentage_value_))
        z_percentage = float(get_textbox_value(self._z_textbox_percentage_value_))

        scale_factors = [x_percentage / 100, y_percentage / 100, z_percentage / 100]
        self._model_.scale(scale_factors)
        print(f"After Scale{self._model_.zbounds()}")

        plotter = Plotter(axes=1)
        plotter.show(self._model_).close()

        scale_factors = [1 / x for x in scale_factors]
        self._model_.scale(scale_factors)

        print(f"Before Exit {self._model_.zbounds()}")

    def _percentage_updated_(self, event):
        updated_percentage = float(get_textbox_value(event.widget.master))

        if self._linked_operation_:
            # Update all percentages
            pass
        else:
            pass

    def _x_values_update_(self, event):
        # TODO bounds check for zero
        updated_val = float(get_textbox_value(event.widget.master))
        default_value = float(get_textbox_value(self._x_textbox_current_value_))

        if self._linked_operation_:
            if event.widget.master is self._x_textbox_updated_value_:
                percentage = updated_val / default_value
                update_textbox(
                    self._x_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
            elif event.widget.master is self._x_textbox_percentage_value_:
                percentage = float(get_textbox_value(event.widget.master)) / 100
                update_textbox(
                    self._x_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._x_textbox_current_value_)) * percentage):.2f}",
                )

            if event.widget.master in [
                self._x_textbox_updated_value_,
                self._x_textbox_percentage_value_,
            ]:
                update_textbox(
                    self._y_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._z_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._y_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._y_textbox_current_value_)) * percentage):.2f}",
                )
                update_textbox(
                    self._z_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._z_textbox_current_value_)) * percentage):.2f}",
                )
        else:
            if event.widget.master is self._x_textbox_updated_value_:
                textbox_to_update = self._x_textbox_percentage_value_
                updated_val = updated_val / default_value * 100
            elif event.widget.master is self._x_textbox_percentage_value_:
                textbox_to_update = self._x_textbox_updated_value_
                updated_val = (updated_val / 100) * default_value

            if event.widget.master in [
                self._x_textbox_updated_value_,
                self._x_textbox_percentage_value_,
            ]:
                update_textbox(textbox_to_update, f"{updated_val:.2f}")

    def _y_values_update_(self, event):
        # TODO bounds check for zero
        updated_val = float(get_textbox_value(event.widget.master))
        default_value = float(get_textbox_value(self._y_textbox_current_value_))

        if self._linked_operation_:
            if event.widget.master is self._y_textbox_updated_value_:
                percentage = updated_val / default_value
                update_textbox(
                    self._y_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
            elif event.widget.master is self._y_textbox_percentage_value_:
                percentage = float(get_textbox_value(event.widget.master)) / 100
                update_textbox(
                    self._y_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._y_textbox_current_value_)) * percentage):.2f}",
                )

            if event.widget.master in [
                self._y_textbox_updated_value_,
                self._y_textbox_percentage_value_,
            ]:
                update_textbox(
                    self._x_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._z_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._x_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._x_textbox_current_value_)) * percentage):.2f}",
                )
                update_textbox(
                    self._z_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._z_textbox_current_value_)) * percentage):.2f}",
                )
        else:
            if event.widget.master is self._y_textbox_updated_value_:
                textbox_to_update = self._y_textbox_percentage_value_
                updated_val = updated_val / default_value * 100
            elif event.widget.master is self._y_textbox_percentage_value_:
                textbox_to_update = self._y_textbox_updated_value_
                updated_val = (updated_val / 100) * default_value

            if event.widget.master in [
                self._y_textbox_updated_value_,
                self._y_textbox_percentage_value_,
            ]:
                update_textbox(textbox_to_update, f"{updated_val:.2f}")

    def _z_values_update_(self, event):
        # TODO bounds check for zero
        updated_val = float(get_textbox_value(event.widget.master))
        default_value = float(get_textbox_value(self._z_textbox_current_value_))

        if self._linked_operation_:
            if event.widget.master is self._z_textbox_updated_value_:
                percentage = updated_val / default_value
                update_textbox(
                    self._z_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
            elif event.widget.master is self._z_textbox_percentage_value_:
                percentage = float(get_textbox_value(event.widget.master)) / 100
                update_textbox(
                    self._z_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._z_textbox_current_value_)) * percentage):.2f}",
                )

            if event.widget.master in [
                self._z_textbox_updated_value_,
                self._z_textbox_percentage_value_,
            ]:
                update_textbox(
                    self._y_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._x_textbox_percentage_value_, f"{(percentage * 100):.2f}"
                )
                update_textbox(
                    self._y_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._y_textbox_current_value_)) * percentage):.2f}",
                )
                update_textbox(
                    self._x_textbox_updated_value_,
                    f"{(float(get_textbox_value(self._x_textbox_current_value_)) * percentage):.2f}",
                )
        else:
            if event.widget.master is self._z_textbox_updated_value_:
                textbox_to_update = self._z_textbox_percentage_value_
                updated_val = updated_val / default_value * 100
            elif event.widget.master is self._z_textbox_percentage_value_:
                textbox_to_update = self._z_textbox_updated_value_
                updated_val = (updated_val / 100) * default_value

            if event.widget.master in [
                self._z_textbox_updated_value_,
                self._z_textbox_percentage_value_,
            ]:
                update_textbox(textbox_to_update, f"{updated_val:.2f}")


if __name__ == "__main__":
    vtk_path = os.path.join(sys.prefix, "Lib", "site-packages", "vtkmodules")

    if os.path.exists(vtk_path):
        os.add_dll_directory(vtk_path)

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
