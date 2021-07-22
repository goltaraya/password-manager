# Password Manager
# Author >>> Yago Goltara

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

TEXT_FONT = ('arial', 12, 'normal')
WHITE = "#EEEBDD"
MAROON = "#630000"
BLACK = "#1B1717"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for char in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters
    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)

    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email_username = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email_username) == 0:
        messagebox.showinfo(title="Oops...", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data_passwords.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data_passwords.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data_passwords.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def find_website():
    website_name = website_entry.get()

    try:
        with open("data_passwords.json", "r") as data:
            dict_website = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="No Data File Found", message="There's no data file.")
    else:
        if website_name in dict_website:
            messagebox.showinfo(title=f"{website_name}", message=f"Email/Username: "
                                                                 f"{dict_website[website_name]['email']}\n"
                                                                 f"Password: {dict_website[website_name]['password']}")
        else:
            messagebox.showinfo(title="Website Not Found", message="No details for the website exists.")
    finally:
        website_entry.delete(0, END)


#  ---------------------------- UI SETUP ------------------------------- #
# Screen
root = Tk()
root.config(padx=50, pady=50, bg=BLACK)
root.minsize(height=300, width=450)
root.title("Password Manager")
root.resizable(False, False)

# Canvas
canvas = Canvas(height=200, width=200, bg=BLACK, highlightthickness=0)
padlock = PhotoImage(file='logo.png')
canvas.create_image(0, 0, image=padlock, anchor='nw')
canvas.grid(row=1, column=2)

# Website Label
website_label = Label(text="Website:", font=TEXT_FONT, bg=BLACK, fg=WHITE)
website_label.grid(row=2, column=1)

# Website Entry
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

# Email Label
email_label = Label(text="Email/Username:", font=TEXT_FONT, bg=BLACK, fg=WHITE)
email_label.grid(row=3, column=1)

# Email Entry
email_entry = Entry(width=35)
email_entry.grid(row=3, column=2, padx=5, pady=5, columnspan=2, sticky='nsew')

# Password Label
password_label = Label(text="Password:", font=TEXT_FONT, bg=BLACK, fg=WHITE)
password_label.grid(row=4, column=1)

# Password Entry
password_entry = Entry(width=21)
password_entry.grid(row=4, column=2, padx=5, pady=5, columnspan=1, sticky='nsew')

# Password Generator Button
password_generator_button = Button(text="Generate Password", command=generate_password, bg=MAROON, fg=WHITE)
password_generator_button.grid(row=4, column=3, sticky='nsew')

# Search Button
search_button = Button(text="Search", command=find_website, bg=MAROON, fg=WHITE)
search_button.grid(row=2, column=3, sticky='nsew')

# Add Button
add_button = Button(text="Add", width=36, command=save_password, bg=MAROON, fg=WHITE)
add_button.grid(row=5, column=2, padx=2, pady=5, columnspan=2, sticky='nsew')
mainloop()
