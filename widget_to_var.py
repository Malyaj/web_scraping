from tkinter import *
from tkinter import ttk
import time

def fn_search(*args):
    try:
        val = str(query.get())
        #print(val)
        query_string.set(val)
        time.sleep(1)
        root.destroy()
        return val
    except ValueError:
        pass
    
#def exit_window(*args):
#    root.destroy()
    
root = Tk()
root.title("Amazon_POC")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

query = StringVar()
query_string = StringVar()

query_entry = ttk.Entry(mainframe, width=100, textvariable=query)
#query_entry = ttk.Entry(mainframe, show="*", width=100, textvariable=query)
query_entry.grid(column=2, row=1, sticky=(W, E))

button_title = "search and quit"
ttk.Button(mainframe, text=button_title, command=fn_search).grid(column=3, row=3, sticky=S)

query_entry.focus()
root.bind('<Return>', fn_search)

root.mainloop()


query_string_var = query_string.get()
print(query_string_var)
