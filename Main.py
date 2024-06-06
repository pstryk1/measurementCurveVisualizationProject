import functions as f
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
import re
import dataVar as dV

#-------------------------------------------------------plot-------------------------------------------------------#
def calculation():
    env_data = [dV.resistance_1, dV.resistance_2, dV.current]
    ############################
    measurement = f.measurement(dV.mes_system)
    dV.app_res_values = measurement.measure(dV.mes_system, dV.m, env_data)# 4 env data = lista: opornosc1, opor2, natezenie
    dV.x = measurement.x_values



    #------------------plot
    figure = plt.figure()
    ax = figure.add_subplot()
    ax.set_xticks([i for i in range(0,100) if i%2 == 0])
    #plt.plot(measurement.x_values, y)
    plt.scatter(dV.x, dV.app_res_values)
    plt.yscale('log')
    plt.grid()
    plt.show()
    #------------------plot


def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    with open(file_path, 'w') as file:
                file.write("x   y\n")
    for i in range(len(dV.x)):
        
        if file_path:
            with open(file_path, 'a') as file:
                file.write(f"{dV.x[i]}\t{dV.app_res_values[i]}\n")


def save_plot():






    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("png files", "*.png")])
    plt.savefig(file_path)
    pass

#-------------------------------------------------------plot-------------------------------------------------------#



ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("green")
ctk.deactivate_automatic_dpi_awareness()

app = ctk.CTk()
app.title("Hydrogeofizyka - Wyznaczanie krzywej profilowania elektrooporowego")
app.iconbitmap('images/app-icon.ico')
app.geometry("750x750")
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
    
    try:
        if (selection == "Wybierz"):
            raise ValueError

        if selection == "Układ Trójelektrodowy":
            forward_backward_combobox.place(relx=0.15, rely=0.58, anchor=tk.CENTER)
            forward_backward_label.place(relx=0.16, rely=0.53, anchor=tk.CENTER)
            distance_label_1.place(relx=0.15, rely=0.63, anchor=tk.CENTER)
            distance_entry_1.place(relx=0.15, rely=0.68, anchor=tk.CENTER)
            distance_label_2.place(relx=0.42, rely=0.63, anchor=tk.CENTER)
            distance_entry_2.place(relx=0.42, rely=0.68, anchor=tk.CENTER)
        elif selection == "Układ Wennera":
            forward_backward_combobox.place_forget()
            forward_backward_label.place_forget()
            distance_label_1.place(relx=0.15, rely=0.53, anchor=tk.CENTER)
            distance_entry_1.place(relx=0.15, rely=0.58, anchor=tk.CENTER)
            distance_label_2.place_forget()
            distance_entry_2.place_forget()
        elif selection == "Układ Schlumbergera":
            forward_backward_combobox.place_forget()
            forward_backward_label.place_forget()
            distance_label_1.place(relx=0.15, rely=0.53, anchor=tk.CENTER)
            distance_entry_1.place(relx=0.15, rely=0.58, anchor=tk.CENTER)
            distance_label_2.place(relx=0.42, rely=0.53, anchor=tk.CENTER)
            distance_entry_2.place(relx=0.42, rely=0.58, anchor=tk.CENTER)
    except ValueError:
        warning_label = ctk.CTkLabel(frame, font=("Arial", 18), text_color="red")
        warning_label.configure(text="NIE podano wszystkich wartości lub są one nieprawidłowe! ")
        warning_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        app.after(2000, lambda: warning_label.destroy())
        return



    # Funkcja do zatwierdzania pod przyciskiem 
def submit_data():
    try:
        dV.resistance_1 = float(input_entry_1.get())
        if (dV.resistance_1<=0 or dV.resistance_1>1000000):
            input_entry_1.configure(text_color="red")
            raise ValueError   
        else:
            input_entry_1.configure(text_color="white")     

        dV.resistance_2 = float(input_entry_2.get())
        if (dV.resistance_2<=0 or dV.resistance_2>1000000):
            input_entry_2.configure(text_color="red")
            raise ValueError    
        else:
            input_entry_2.configure(text_color="white")   
        dV.current = float(input_entry_3.get())
        if (dV.current<=0 or dV.current>1000):
            input_entry_3.configure(text_color="red")
            raise ValueError    
        else:
            input_entry_3.configure(text_color="white") 
        dV.m = float(input_entry_4.get())
        if (dV.m<=0 or dV.m>10):
            input_entry_4.configure(text_color="red")
            raise ValueError 
        else:
            input_entry_4.configure(text_color="white") 


        # Sprawdzenie dodatkowych pól w zależności od wyboru układu pomiarowego
        dV.mes_system = measurement_setup_combobox.get()
        if (dV.mes_system == "Wybierz"):
            raise ValueError
        if dV.mes_system == "Układ Trójelektrodowy":
            dV.variant = forward_backward_combobox.get()
            if (dV.variant == "Wybierz"):
                forward_backward_combobox.configure(background="red")
                raise ValueError
            else:
                forward_backward_combobox.configure(background="white") 

            dV.distance1 = float(distance_entry_1.get())
            if (dV.distance1<=0 or dV.distance1>10):
                distance_entry_1.configure(text_color="red")
                raise ValueError
            else:
                distance_entry_1.configure(text_color="white") 
            dV.distance2 = float(distance_entry_2.get())
            if (dV.distance2<=0 or dV.distance2>10):
                distance_entry_2.configure(text_color="red")
                raise ValueError
            else:
                distance_entry_2.configure(text_color="white")
        elif dV.mes_system == "Układ Wennera":
            dV.distance1 = float(distance_entry_1.get())
            if (dV.distance1<=0 or dV.distance1>10):
                distance_entry_1.configure(text_color="red")
                raise ValueError
            else:
                distance_entry_1.configure(text_color="white") 
            dV.distance2 = None
        elif dV.mes_system == "Układ Schlumbergera":
            dV.distance1 = float(distance_entry_1.get())
            if (dV.distance1<=0 or dV.distance1>10):
                distance_entry_1.configure(text_color="red")
                raise ValueError
            else:
                distance_entry_1.configure(text_color="white")  
            dV.distance2 = float(distance_entry_2.get())
            if (dV.distance2<=0 or dV.distance2>10):
                distance_entry_2.configure(text_color="red")
                raise ValueError
            else:
                distance_entry_2.configure(text_color="white")

        if dV.mes_system == "Układ Trójelektrodowy":
            if not dV.variant:
                warning_label = ctk.CTkLabel(frame, font=("Arial", 18), text_color="red")
                warning_label.configure(text="NIE podano wszystkich wartości ! ")
                warning_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
                app.after(2000, lambda: warning_label.destroy())
        calculation()

    except ValueError:
        warning_label = ctk.CTkLabel(frame, font=("Arial", 18), text_color="red")
        warning_label.configure(text="NIE podano wszystkich wartości lub są one nieprawidłowe! ")
        warning_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        app.after(2000, lambda: warning_label.destroy())
        return

        # Sprawdzenie 
    """
    print(f"Oporność warstwy pierwszej: {r1} Ωm")
    print(f"Oporność warstwy drugiej: {r2} Ωm")
    print(f"Natężenie prądu: {i} A")
    print(f"Odległość pomiędzy punktami pomiarowymi {m} m")
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
    """
    
        

frame = ctk.CTkFrame(master=app, width=700, height=700)
frame.pack(pady=25)

# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania oporności warstwy pierwszej
title_label_1 = ctk.CTkLabel(master=frame, text="Oporność elektryczna warstwy pierwszej", height=5, width=5)
title_label_1.place(relx=0.18, rely=0.03, anchor=tk.CENTER)

input_entry_1 = CustomEntry(master=frame, width=170, height=40)
input_entry_1.place(relx=0.15, rely=0.08, anchor=tk.CENTER)

output_label_1 = ctk.CTkLabel(master=frame, text="[Ωm]", height=7, width=7)
output_label_1.place(relx=0.32, rely=0.08, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania oporności warstwy drugiej
title_label_2 = ctk.CTkLabel(master=frame, text="Oporność elektryczna warstwy drugiej", height=5, width=5)
title_label_2.place(relx=0.17, rely=0.13, anchor=tk.CENTER)

input_entry_2 = CustomEntry(master=frame, placeholder_text="", width=170, height=40)
input_entry_2.place(relx=0.15, rely=0.18, anchor=tk.CENTER)

output_label_2 = ctk.CTkLabel(master=frame, text="[Ωm]", height=5, width=5)
output_label_2.place(relx=0.32, rely=0.18, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania natężenia prądu
title_label_3 = ctk.CTkLabel(master=frame, text="Natężenie prądu w obwodzie", height=5, width=5)
title_label_3.place(relx=0.135, rely=0.23, anchor=tk.CENTER)

input_entry_3 = CustomEntry(master=frame, placeholder_text="", width=170, height=40)
input_entry_3.place(relx=0.15, rely=0.28, anchor=tk.CENTER)

output_label_2 = ctk.CTkLabel(master=frame, text="[A]", height=5, width=5)
output_label_2.place(relx=0.31, rely=0.28, anchor=tk.CENTER)

# ------------------------------------------------------------------------------------------------------------------------------
        # Pole do wprowadzania odległosci pomiaru
title_label_4 = ctk.CTkLabel(master=frame, text="Odległość pomiędzy punktami pomiarowymi", height=5, width=5)
title_label_4.place(relx=0.2, rely=0.33, anchor=tk.CENTER)

input_entry_4 = CustomEntry(master=frame, placeholder_text="", width=170, height=40)
input_entry_4.place(relx=0.15, rely=0.38, anchor=tk.CENTER)

output_label_2 = ctk.CTkLabel(master=frame, text="[m]", height=5, width=5)
output_label_2.place(relx=0.31, rely=0.38, anchor=tk.CENTER)


# ------------------------------------------------------------------------------------------------------------------------------
title_label_4 = ctk.CTkLabel(master=frame, text="Wybierz układ pomiarowy", height=5, width=5)
title_label_4.place(relx=0.15, rely=0.43, anchor=tk.CENTER)

measurement_setup_combobox = ttk.Combobox(frame, values=["Układ Wennera", "Układ Schlumbergera", "Układ Trójelektrodowy"], text="Układ Wennera", state="readonly")
measurement_setup_combobox.set("Wybierz")
measurement_setup_combobox.place(relx=0.15, rely=0.48, anchor=tk.CENTER)
measurement_setup_combobox.bind("<<ComboboxSelected>>", update_measurement_setup_options)

    # Dodatkowy combobox do wyboru wariantu układu trójelektrodowego
forward_backward_combobox = ttk.Combobox(frame, values=["Forward", "Backward"], state="readonly")
forward_backward_combobox.set("Wybierz")
forward_backward_label = ctk.CTkLabel(frame, text="Wariant do układu trójelektrodowego", height=5, width=5)
# forward_backward_combobox.place_forget()
# forward_backward_label.place_forget()

distance_label_1 = ctk.CTkLabel(master=frame, text="Odległość AM", height=5, width=5)
distance_entry_1 = CustomEntry(master=frame, width=170, height=40)

distance_label_2 = ctk.CTkLabel(master=frame, text="Odległość MN", height=5, width=5)
distance_entry_2 = CustomEntry(master=frame, width=170, height=40)

submit_button = ctk.CTkButton(master=frame, text="Zatwierdź", command=submit_data)
submit_button.place(relx=0.15, rely=0.8, anchor=tk.CENTER)

save_button = ctk.CTkButton(master=frame, text="Zapisz dane", command=save_text)
save_button.place(relx=0.15, rely=0.89, anchor=tk.CENTER)

save_button = ctk.CTkButton(master=frame, text="Zapisz wykres", command=save_plot)
save_button.place(relx=0.40, rely=0.89, anchor=tk.CENTER)

submit_button = ctk.CTkLabel(master=frame, text="Created by Mateusz Kalisz & Jakub Kłosiński & Bartłomiej Stachurski & Patryk Kusper", height=5, width=5)
submit_button.place(relx=0.38, rely=0.98, anchor=tk.CENTER)
app.mainloop()



#-------------------------------------------------------UI END-------------------------------------------------------#
