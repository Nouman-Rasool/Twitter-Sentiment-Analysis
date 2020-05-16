from tkinter import *
import tkinter.messagebox as tm


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_login = Label(self, text="Login", fg="black", font=('times', 20, ' bold'), bg="#42ddd4")

        self.label_username = Label(self, text="Username:", height=2, fg="black", bg="#42ddd4",
                                    font=('times', 12))

        self.label_password = Label(self, text="Password:", height=2, fg="black", bg="#42ddd4",
                                    font=('times', 12))

        self.entry_username = Entry(self, width="40")
        self.entry_password = Entry(self, show="*", width="40")

        self.label_login.grid(row=16, column=2)
        self.label_username.grid(row=20, column=2)
        self.label_password.grid(row=24, column=2)
        self.entry_username.grid(row=20, column=4)
        self.entry_password.grid(row=24, column=4)

        self.checkbox = Checkbutton(self, font=('times', 10, ' bold'), text="Keep me logged in", bg="#42ddd4")
        self.checkbox.grid(columnspan=5)

        self.logbtn = Button(self, text="Login", width="10", fg="#42ddd4", bg="#A8A7AE", font=('times', 16, ' bold'),
                             command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=5)

        self.pack(padx=30, pady=120)

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)

        if username == "admin" and password == "Pakistan":
            tm.showinfo("Login info", "Welcome admin")
        else:
            tm.showerror("Login error", "Incorrect username")


root = Tk()
root.config(bg="#42ddd4")
root.geometry("610x500+120+120")

fr=LoginFrame(root)
fr.config(bg="#42ddd4")
root.mainloop()

