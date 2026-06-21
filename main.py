from vedo import Mesh, Plotter
import customtkinter as ctk
from PIL import Image
import os
import sys

from components import ValuesTable
from utils import update_textbox


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
            x_values = tuple(x / 25.4 for x in self._model_.xbounds())
            y_values = tuple(y / 25.4 for y in self._model_.ybounds())
            z_values = tuple(z / 25.4 for z in self._model_.zbounds())
            self._values_table_.set_initial_values(
                x_values[1] - x_values[0],
                y_values[1] - y_values[0],
                z_values[1] - z_values[0],
            )

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

    def _visualize_(self):
        print(f"Before Scale{self._model_.zbounds()}")

        scale_factors = self._values_table_.get_set_percentages()
        self._model_.scale(scale_factors)
        print(f"After Scale{self._model_.zbounds()}")

        plotter = Plotter(axes=1)
        plotter.show(self._model_).close()

        scale_factors = [1 / x for x in scale_factors]
        self._model_.scale(scale_factors)

        print(f"Before Exit {self._model_.zbounds()}")


if __name__ == "__main__":
    vtk_path = os.path.join(sys.prefix, "Lib", "site-packages", "vtkmodules")

    if os.path.exists(vtk_path):
        os.add_dll_directory(vtk_path)

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
