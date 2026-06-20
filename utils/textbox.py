import customtkinter as ctk


def update_textbox(textbox: ctk.CTkTextbox, text: str):
    current_state = textbox._textbox.cget("state")

    textbox.configure(state=ctk.NORMAL)
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)
    textbox.configure(state=current_state)


def get_textbox_value(textbox: ctk.CTkTextbox):
    return textbox.get("1.0", "end-1c")
