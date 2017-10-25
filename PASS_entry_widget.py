from tkinter import *
from tkinter import ttk
import time

def fn_search(*args):
    try:
        val_SSO.set(str(SSO.get()))
        val_SSO_password.set(str(SSO_password.get()))
        time.sleep(1)
        root.destroy()
        return (val_SSO, val_SSO_password)
    except ValueError:
        pass

#def exit_window(*args):
#    root.destroy()

root = Tk()
root.title("Enter credentials")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

SSO =  StringVar()
SSO_password = StringVar()
val_SSO = StringVar()
val_SSO_password = StringVar()


SSO_entry = ttk.Entry(mainframe, width=50, textvariable=SSO)
SSO_entry.grid(column=2, row=1, sticky=(W, E))
SSO_label = ttk.Label(mainframe, text = 'Enter SSO')
SSO_label.grid(column = 1, row = 1)

password_entry = ttk.Entry(mainframe, show = '*', width=50, textvariable=SSO_password)
password_entry.grid(column=2, row=2, sticky=(W, E))
password_label = ttk.Label(mainframe, text = 'Enter password')
password_label.grid(column = 1, row = 2)

button_title = "Submit"
ttk.Button(mainframe, text=button_title, command=fn_search).grid(column=3, row=3, sticky=W)

SSO_entry.focus()
root.bind('<Return>', fn_search)

root.mainloop()


SSO_string = val_SSO.get()
SSO_password_string = val_SSO_password.get()

print(SSO_string)
print(SSO_password_string)
