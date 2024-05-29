import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import re

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("green")
ctk.deactivate_automatic_dpi_awareness()

app = ctk.CTk()
app.title("Hydrogeofizyka - Wyznaczanie krzywej profilowania elektrooporowego")
app.iconbitmap('images/app-icon.ico')
app.geometry("750x600")
style = ttk.Style(app)
app.tk.call("source", "Theme/forest-dark.tcl")
style.theme_use("forest-dark")
app.resizable(False, False)


class CustomEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):  
        super().__init__(master, **kwargs)
        self.configure(validate="key")
        self.configure(validatecommand=(self.register(self.validate_input), '%P'))
        
    def validate_input(self, new_text):
            # Dozwolone są cyfry i kropki w Entryboxie
        return re.match(r'^[0-9.]*$', new_text) is not None
    

        # Combobox do wyboru układu pomiarowego
def update_measurement_setup_options(event):
    selection = measurement_setup_combobox.get()
    if selection == "Układ Trójelektrodowy":
        forward_backward_combobox.place(relx=0.15, rely=0.68, anchor=tk.CENTER)
        forward_backward_label.place(relx=0.16, rely=0.62, anchor=tk.CENTER)
        distance_label_1.place(relx=0.15, rely=0.74, anchor=tk.CENTER)
        distance_entry_1.place(relx=0.15, rely=0.80, anchor=tk.CENTER)
        distance_label_2.place(relx=0.42, rely=0.74, anchor=tk.CENTER)
        distance_entry_2.place(relx=0.42, rely=0.80, anchor=tk.CENTER)
    elif selection == "Układ Wennera":
        forward_backward_combobox.place_forget()
        forward_backward_label.place_forget()
        distance_label_1.place(relx=0.15, rely=0.62, anchor=tk.CENTER)
        distance_entry_1.place(relx=0.15, rely=0.68, anchor=tk.CENTER)
        distance_label_2.place_forget()
        distance_entry_2.place_forget()
    elif selection == "Układ Schlumbergera":
        forward_backward_combobox.place_forget()
        forward_backward_label.place_forget()
        distance_label_1.place(relx=0.15, rely=0.62, anchor=tk.CENTER)
        distance_entry_1.place(relx=0.15, rely=0.68, anchor=tk.CENTER)
        distance_label_2.place(relx=0.42, rely=0.62, anchor=tk.CENTER)
        distance_entry_2.place(relx=0.42, rely=0.68, anchor=tk.CENTER)


    # Funkcja do zatwierdzania pod przyciskiem 
def submit_data():
    try:
        r1 = float(input_entry_1.get())
        r2 = float(input_entry_2.get())
        i = float(input_entry_3.get())

        # Sprawdzenie dodatkowych pól w zależności od wyboru układu pomiarowego
        setup = measurement_setup_combobox.get()
        if setup == "Układ Trójelektrodowy":
            variant = forward_backward_combobox.get()
            distance1 = float(distance_entry_1.get())
            distance2 = float(distance_entry_2.get())
        elif setup == "Układ Wennera":
            distance1 = float(distance_entry_1.get())
            distance2 = None
        elif setup == "Układ Schlumbergera":
            distance1 = float(distance_entry_1.get())
            distance2 = float(distance_entry_2.get())
        if setup == "Układ Trójelektrodowy":
            if not variant:
                warning_label = ctk.CTkLabel(frame, font=("Arial", 18), text_color="red")
                warning_label.configure(text="NIE podano wszystkich wartości ! ")
                warning_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
                app.after(2000, lambda: warning_label.destroy())

    except ValueError:
        warning_label = ctk.CTkLabel(frame, font=("Arial", 18), text_color="red")
        warning_label.configure(text="NIE podano wszystkich wartości ! ")
        warning_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        app.after(2000, lambda: warning_label.destroy())
        return

        # Sprawdzenie 
    print(f"Oporność warstwy pierwszej: {r1} Ωm")
    print(f"Oporność warstwy drugiej: {r2} Ωm")
    print(f"Natężenie prądu: {i} A")
    print(f"Układ pomiarowy: {setup}")
    if setup == "Układ Trójelektrodowy":
        print(f"Wariant układu trójelektrodowego: {variant}")
        print(f"Odległość AM: {distance1}")
        print(f"Odległość MN: {distance2}")
    elif setup == "Układ Wennera":
        print(f"Odległość AM: {distance1}")
    elif setup == "Układ Schlumbergera":
        print(f"Odległość AM: {distance1}")
        print(f"Odległość MN: {distance2}")

        

frame = ctk.CTkFrame(master=app, width=700, height=600)
frame.pack(pady=25)

# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania oporności warstwy pierwszej
title_label_1 = ctk.CTkLabel(master=frame, text="Oporność elektryczna warstwy pierwszej", height=5, width=5)
title_label_1.place(relx=0.18, rely=0.03, anchor=tk.CENTER)

input_entry_1 = CustomEntry(master=frame, width=170, height=40)
input_entry_1.place(relx=0.15, rely=0.1, anchor=tk.CENTER)

output_label_1 = ctk.CTkLabel(master=frame, text="[Ωm]", height=7, width=7)
output_label_1.place(relx=0.32, rely=0.1, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania oporności warstwy drugiej
title_label_2 = ctk.CTkLabel(master=frame, text="Oporność elektryczna warstwy drugiej", height=5, width=5)
title_label_2.place(relx=0.17, rely=0.18, anchor=tk.CENTER)

input_entry_2 = CustomEntry(master=frame, placeholder_text="", width=170, height=40)
input_entry_2.place(relx=0.15, rely=0.25, anchor=tk.CENTER)

output_label_2 = ctk.CTkLabel(master=frame, text="[Ωm]", height=5, width=5)
output_label_2.place(relx=0.32, rely=0.25, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania natężenia prądu
title_label_3 = ctk.CTkLabel(master=frame, text="Natężenie prądu w obwodzie", height=5, width=5)
title_label_3.place(relx=0.15, rely=0.33, anchor=tk.CENTER)

input_entry_3 = CustomEntry(master=frame, placeholder_text="", width=170, height=40)
input_entry_3.place(relx=0.15, rely=0.4, anchor=tk.CENTER)

output_label_2 = ctk.CTkLabel(master=frame, text="[A]", height=5, width=5)
output_label_2.place(relx=0.31, rely=0.4, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
title_label_4 = ctk.CTkLabel(master=frame, text="Wybierz układ pomiarowy", height=5, width=5)
title_label_4.place(relx=0.15, rely=0.48, anchor=tk.CENTER)

measurement_setup_combobox = ttk.Combobox(frame, values=["Układ Wennera", "Układ Schlumbergera", "Układ Trójelektrodowy"], state="readonly")
measurement_setup_combobox.place(relx=0.15, rely=0.54, anchor=tk.CENTER)
measurement_setup_combobox.bind("<<ComboboxSelected>>", update_measurement_setup_options)

    # Dodatkowy combobox do wyboru wariantu układu trójelektrodowego
forward_backward_combobox = ttk.Combobox(frame, values=["Forward", "Backward"], state="readonly")
forward_backward_label = ctk.CTkLabel(frame, text="Wariant do układu trójelektrodowego", height=5, width=5)
# forward_backward_combobox.place_forget()
# forward_backward_label.place_forget()

distance_label_1 = ctk.CTkLabel(master=frame, text="Odległość AM", height=5, width=5)
distance_entry_1 = CustomEntry(master=frame, width=170, height=40)

distance_label_2 = ctk.CTkLabel(master=frame, text="Odległość MN", height=5, width=5)
distance_entry_2 = CustomEntry(master=frame, width=170, height=40)

submit_button = ctk.CTkButton(master=frame, text="Zatwierdź", command=submit_data)
submit_button.place(relx=0.15, rely=0.90, anchor=tk.CENTER)

app.mainloop()


