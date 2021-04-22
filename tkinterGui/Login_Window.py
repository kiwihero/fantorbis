from tkinter import *
from tkinter import messagebox, Button
import tkinter as tk
import sys
import os
import sqlite3
import hashlib

WIDTH = 500
HEIGHT = 400
# USERNAME_LENGTH = 24
# PASSWORD_LENGTH = 128
title_bar_icon_path = os.path.join(os.path.dirname(sys.path[0])) + r'\fantorbis-old-backend\images\Fantorbis-Logo.ico'
logo_path = os.path.join(os.path.dirname(sys.path[0])) + r'\fantorbis-old-backend\images\Fantorbis-Logo.png'


# TODO: Add delete account button (with some "are you sure" prompt- tkinter.messagebox)
#       Show create account window on startup if no accounts found (not crucial)


class LoginWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        self.image_file = PhotoImage(file=logo_path)  # sets background image to logo
        self.image_label = Label(master, image=self.image_file)
        self.image_label.place(x=0, y=100)

        self.welcome_text = Label(master, text='Welcome! Enter your username and password\nor create an account below')
        self.welcome_text.grid(row=0)

        self.username_label = Label(master, text='Username')
        self.username_label.grid(row=1)

        self.password_label = Label(master, text='Password')
        self.password_label.grid(row=2)

        self.username_entry = Entry(master)
        self.password_entry = Entry(master, show='\u2022')  # \u2022: unicode for bullet character

        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)

        self.show_hide_pw_button = Button(master, text='Show password',
                                          command=lambda: show_hide_password(self, self.show_hide_pw_button))
        self.show_hide_pw_button.grid(row=3)

        self.create_acc_button = Button(master, text='Create Account', command=lambda: create_acc_window(self))
        self.create_acc_button.grid(row=4)

        self.login_button = Button(master, text='Login', command=lambda: login(self))
        self.login_button.grid(row=1, column=3)

        self.delete_acc_button = Button(master, text='Delete Account')
        self.delete_acc_button.grid(row=5)


def show_hide_password(self, password_status):
    if self.show_hide_pw_button.cget('text') == 'Hide password':
        password_status.config(text='Show password')
        self.password_entry.config(show='\u2022')

    else:
        password_status.config(text='Hide password')
        self.password_entry.config(show='')


def login(self):
    login_username = self.username_entry.get()
    login_password = self.password_entry.get()
    if login_username == '' or login_password == '':
        messagebox.showerror(
            'Error', 'Must provide both a username and a password')
        self.password_entry.delete(0, 'end')  # clears password field if both fields or just username are empty

    elif ' ' in login_username or ' ' in login_password:
        messagebox.showerror('Error', 'Username or password cannot contain spaces')

    else:
        connection = sqlite3.connect('creds.db')  # creates database if it doesn't exist
        cursor = connection.cursor()

        make_table_query = "CREATE TABLE IF NOT EXISTS accounts" \
                           "(user_id INTEGER UNIQUE, username TEXT UNIQUE NOT NULL, " \
                           "password TEXT NOT NULL, PRIMARY KEY(user_id AUTOINCREMENT));"
        cursor.execute(make_table_query)

        # check if username and password exist in database
        select_query = "SELECT username, password FROM accounts WHERE username = ? and password = ?"

        cursor.execute(select_query, (login_username, login_password))
        result = cursor.fetchone()
        if result is None:
            messagebox.showerror('Error', f'No account exists with username {login_username}')

        else:
            messagebox.showinfo('Logged in', f'Successfully logged in as user {login_username}')

            # self.root.destroy()
            return login_username

        connection.close()


#     validate_credential_length(self, login_username, login_password)
#
#
# def validate_credential_length(self, username, password):
#     if len(username) > USERNAME_LENGTH:
#         messagebox.showerror('Error', 'Username too long')
#         return False
#     if len(password) > PASSWORD_LENGTH:
#         messagebox.showerror('Error', 'Password too long')
#         return False


def create_acc_window(self):
    new_acc_window = Toplevel(self)
    new_acc_window.wm_title('Create Account')
    new_acc_window.iconbitmap(title_bar_icon_path)
    new_acc_window.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    new_acc_window.attributes('-topmost', 'true')

    bg_image = self.image_file
    image_label = Label(new_acc_window, image=bg_image)
    image_label.place(x=0, y=100)

    username_label_new_acc = Label(new_acc_window, text='Username')
    username_label_new_acc.grid(row=1)

    password_label_new_acc = Label(new_acc_window, text='Password')
    password_label_new_acc.grid(row=2)

    username_entry_new_acc = Entry(new_acc_window)
    password_entry_new_acc = Entry(new_acc_window, show='\u2022')

    username_entry_new_acc.grid(row=1, column=1)
    password_entry_new_acc.grid(row=2, column=1)

    new_user_button = Button(new_acc_window, text='Create Account',
                             command=lambda: User(username_entry_new_acc, password_entry_new_acc)
                             .add_user_to_account_list(username_entry_new_acc, password_entry_new_acc))

    new_user_button.grid(row=4)

    # close_win = Label(self, text='Account created\nYou may now close this window')
    # close_win.grid(row=4)

    # self.create_acc_button.config(state=DISABLED)
    # self.create_acc_button.grid_forget()
    # accounts.append([username, password])
    # print(accounts)


class User:
    def __init__(self, username, password):
        super().__init__()
        self.username = username.get()
        self.password = password.get()

    # TODO:
    #  Add casing rules to username to prevent making two accounts where once is uppercase and one is lowercase

    def add_user_to_account_list(self, username, password):
        if self.username == '' or self.password == '':
            messagebox.showerror(
                'Error', 'Must provide both a username and a password')
            password.delete(0, 'end')  # clears password field if both fields or just username are empty

        elif ' ' in self.username or ' ' in self.password:
            messagebox.showerror('Error', 'Username or password cannot contain spaces')

        else:
            #  create folder for accounts if it doesn't exist
            if not os.path.exists(os.path.join(os.path.dirname(sys.path[0]) +
                                               fr'\fantorbis-old-backend\accounts')):
                os.mkdir(os.path.join(os.path.dirname(sys.path[0])) + fr'\fantorbis-old-backend\accounts')

            #  create folder called the current username if it doesn't exist
            if not os.path.exists(os.path.join(os.path.dirname(sys.path[0]) +
                                               fr'\fantorbis-old-backend\accounts\{self.username}')):
                os.mkdir(
                    os.path.join(os.path.dirname(sys.path[0])) + fr'\fantorbis-old-backend\accounts\{self.username}')

            connection = sqlite3.connect('creds.db')  # creates database if it doesn't exist
            cursor = connection.cursor()

            make_table_query = "CREATE TABLE IF NOT EXISTS accounts" \
                               "(user_id INTEGER UNIQUE, username TEXT UNIQUE NOT NULL, " \
                               "password TEXT NOT NULL, PRIMARY KEY(user_id AUTOINCREMENT));"

            cursor.execute(make_table_query)

            # questions marks- placeholders for passed tuple at execute()
            insert_query = "INSERT INTO accounts(username, password) VALUES(?,?);"

            try:
                cursor.execute(insert_query, (self.username, self.password))
                messagebox.showinfo('Account created', f'Account {self.username} created')

            except sqlite3.Error as error:

                if 'no such table' in str(error):
                    messagebox.showerror("Error (this shouldn't happen)", "accounts table not found")

                if 'UNIQUE' in str(error):
                    messagebox.showerror("Username already taken",
                                         "This username has already been taken. \n Error: " + "\n" + str(error))

            connection.commit()
            connection.close()


def main():
    root = Tk()
    login_window = LoginWindow(root)
    root.wm_title('Login')
    root.iconbitmap(title_bar_icon_path)
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    root.mainloop()


if __name__ == "__main__":
    main()
