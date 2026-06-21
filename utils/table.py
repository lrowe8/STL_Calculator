import customtkinter as ctk


def create_table_value_textbox(
    parent: ctk.CTkFrame, initial_state: str
) -> ctk.CTkTextbox:
    textbox = ctk.CTkTextbox(
        master=parent, width=75, height=20, corner_radius=8, state=initial_state
    )

    return textbox


def create_table_label(parent: ctk.CTkFrame, text: str) -> ctk.CTkLabel:
    label = ctk.CTkLabel(
        master=parent, height=20, text=text, font=("Arial", 14, "bold")
    )

    return label
