from tkinter import *
from tkinter import messagebox
import random
from string import ascii_letters, digits, punctuation
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    nr_letters = random.randint(8, 10)
    nr_digits = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    password_list = []

    draw_letters = [password_list.append(random.choice(ascii_letters)) for letter in range(nr_letters)]
    draw_digits = [password_list.append(random.choice(digits)) for digit in range(nr_digits)]
    draw_symbols = [password_list.append(random.choice(punctuation)) for symbol in range(nr_symbols)]

    random.shuffle(password_list)
    new_pass = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, new_pass)
    password_entry.focus()
    password_entry.clipboard_clear()
    password_entry.clipboard_append(new_pass)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def valid_website(website):
    if len(website) > 0:
        return True
    else:
        return False


def valid_password(password):
    if len(password) > 0:
        return True
    else:
        return False


def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password,}}


    if not valid_website(website):
        messagebox.showerror(title="Invalid website", message="Please enter a valid webiste")
        website_entry.focus()
        return 0
    if not valid_password(password):
        messagebox.showerror(title="Invalid password", message="Please enter a valid password")
        password_entry.focus()
        return 0

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\nPassword: {password}\nIs it ok to save?")

    if is_ok:
        try:
            with open("data_pass.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data_pass.json", 'w') as file:
                json.dump(new_data, file, indent=4)
        except json.decoder.JSONDecodeError:
            with open("data_pass.json", 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data_pass.json", 'w') as file:
                json.dump(data, file, indent=4)



        website_entry.delete(0, END)
        website_entry.focus()
        password_entry.delete(0, END)
        messagebox.showinfo(title="Operation successful", message="You have successfully saved the data.")

# ---------------------------- SEARCH MECHANISMS ------------------------------- #

def search():
    website = website_entry.get()
    if not valid_website(website):
        messagebox.showerror(title="Incorrect website", message="Please enter a valid webiste")
        return 0

    try:
        with open("data_pass.json", 'r') as file:
            data = json.load(file)
            print(data)
            found_email = data[website]["email"]
            found_password = data[website]["password"]
            print(f"Website: {website}, Password: {data[website]['password']}")
    except FileNotFoundError:
        with open("data_pass.json", 'w') as file:
            json.dump(new_data, file, indent=4)
        messagebox.showerror(title="No data", message="You must save some data first to search it.")
    except json.decoder.JSONDecodeError:
        messagebox.showerror(title="No data", message="You must save some data first to search it.")
    except KeyError as error_key:
        messagebox.showwarning(title="No match", message="No match found. Please add website first or check spelling.")
    else:
        messagebox.showinfo(title="Operation successful", message=f"Data found."
                                                                  f"\nWebsite: {website}"
                                                                  f"\nEmail: {found_email}"
                                                                  f"\nPassword: {found_password}")




# ---------------------------- UI SETUP ------------------------------- #
window_title = "MyPassword"
window_pad_left = 20
window_pad_right = 20

window = Tk()
window.title(window_title)
window.geometry("600x400+400+200")


canvas = Canvas(height=250, width=300)
logo_img = PhotoImage(file="logo.png")
canvas.create_image((175, 100), image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

website_label.grid(column=0, row=1, pady=5, padx=25)
email_label.grid(column=0, row=2, pady=5, padx=25)
password_label.grid(column=0, row=3, pady=5, padx=25)

# Entries
website_entry = Entry(width=48)
website_entry.focus()
email_entry = Entry()
email_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=48)

website_entry.grid(column=1, row=1, sticky='W')
email_entry.grid(column=1, row=2, sticky='WE', columnspan=2)
password_entry.grid(column=1, row=3, sticky='W')

# Buttons
website_search_button = Button(text="Search", width=15, command=search)
generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
add_button = Button(text="Add", command=save_data)

website_search_button.grid(column=2, row=1, sticky='E')
generate_password_button.grid(column=2, row=3, sticky='E')
add_button.grid(column=1, row=4, sticky='WE', columnspan=2)





window.mainloop()


