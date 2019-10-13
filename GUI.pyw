from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import *
from PIL import ImageTk, Image

import denmap
import socket
import threading


# Class to redirect stdout to GUI window
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert(END, string)
        self.text_space.see(END)

    def flush(self):
        pass


# Start the main application as thread
def StartMain():
    global thread
    thread = threading.Thread(target=Analyze)
    thread.daemon = True
    ProgressBar.start()
    thread.start()

    # Check if thread is alive
    def CheckThread():
        if thread.is_alive():
            window.after(50, CheckThread)
        else:
            ProgressBar.stop()
            messagebox.showinfo("DenMap", "Program stopped")

    window.after(50, CheckThread)


# Helper function to call main
def Analyze():
    try:
        # Clean the window from previous logs
        Console_Text.delete(1.0, "end")
        # Print text to window on red
        Console_Text.insert(END, "DenMap Active...\n")
        Console_Text.tag_add("red", "1.0", "1.16")
        Console_Text.tag_configure("red", foreground="red")
        # Call the application
        denmap.main()
    except Exception as e:
        messagebox.showerror("DenMap", e)


# Terminate the application
def Stop():
    exit(0)


# Popup whitelist window
def Whitelist():
    # Set up the popup window
    popup = Toplevel(window)
    popup.title('Whitelist')
    popup.geometry("+550+350")
    popup.tkraise(window)

    # Set up widgets
    Label = ttk.Label(popup, text="Enter IP")
    Label.grid(row=0, column=0, sticky=W + E, padx=(6, 0))
    Entry = ttk.Entry(popup, justify='right')
    Entry.grid(row=0, column=1, sticky=W + E, padx=(5, 5))

    # Add function
    def Add():
        if Entry.get() != "":
            try:
                socket.inet_aton(Entry.get())
                # Append to whitelist
                denmap.whitelist.append(Entry.get())
                messagebox.showinfo("DenMap", "IP added to whitelist")
                Entry.delete(0, 'end')
            except socket.error:
                messagebox.showerror("DenMap", "IP address is not valid")
                Entry.delete(0, 'end')
        else:
            messagebox.showerror("DenMap", "IP address cannot be empty")
            Entry.delete(0, 'end')

    # Remove function
    def Remove():
        if Entry.get() != "":
            try:
                socket.inet_aton(Entry.get())
                # Remove from whitelist
                try:
                    denmap.whitelist.remove(Entry.get())
                except:
                    pass
                messagebox.showinfo("DenMap", "IP removed from whitelist")
                Entry.delete(0, 'end')
            except socket.error:
                messagebox.showerror("DenMap", "IP address is not valid")
                Entry.delete(0, 'end')
        else:
            messagebox.showerror("DenMap", "IP address cannot be empty")
            Entry.delete(0, 'end')

    Add_Butoon = ttk.Button(popup, text="Add", command=Add)
    Add_Butoon.grid(row=0, column=2, sticky=W + E)
    Remove_Button = ttk.Button(popup, text="Remove", command=Remove)
    Remove_Button.grid(row=0, column=3, sticky=W + E)


# Popup blacklist window
def Blacklist():
    # Set up the popup window
    popup = Toplevel(window)
    popup.title('Blacklist')
    popup.geometry("+550+350")
    popup.tkraise(window)

    # Set up widgets
    Label = ttk.Label(popup, text="Enter IP")
    Label.grid(row=0, column=0, sticky=W + E, padx=(6, 0))
    Entry = ttk.Entry(popup, justify='right')
    Entry.grid(row=0, column=1, sticky=W + E, padx=(5, 5))

    # Add function
    def Add():
        if Entry.get() != "":
            try:
                socket.inet_aton(Entry.get())
                # Append to blacklist
                denmap.blacklist.append(Entry.get())
                messagebox.showinfo("DenMap", "IP added to blacklist")
                Entry.delete(0, 'end')
            except socket.error:
                messagebox.showerror("DenMap", "IP address is not valid")
                Entry.delete(0, 'end')
        else:
            messagebox.showerror("DenMap", "IP address cannot be empty")
            Entry.delete(0, 'end')

    # Remove function
    def Remove():
        if Entry.get() != "":
            try:
                socket.inet_aton(Entry.get())
                # Remove from blacklist
                try:
                    denmap.blacklist.remove(Entry.get())
                except:
                    pass
                messagebox.showinfo("DenMap", "IP removed from blacklist")
                Entry.delete(0, 'end')
            except socket.error:
                messagebox.showerror("DenMap", "IP address is not valid")
                Entry.delete(0, 'end')
        else:
            messagebox.showerror("DenMap", "IP address cannot be empty")
            Entry.delete(0, 'end')

    Add_Butoon = ttk.Button(popup, text="Add", command=Add)
    Add_Butoon.grid(row=0, column=2, sticky=W + E)
    Remove_Button = ttk.Button(popup, text="Remove", command=Remove)
    Remove_Button.grid(row=0, column=3, sticky=W + E)


# Set up tkinter
window = Tk()
window.wm_title("DenMap")
window.geometry("+550+100")
window.resizable(False, False)

# Row 0 - Logo
img = ImageTk.PhotoImage(Image.open("denmap.png"))
Logo = ttk.Label(window, image=img)
Logo.grid(row=0, column=0, columnspan=2)

# Row 0 - Start / Stop
Start_Button = ttk.Button(window, text="Start analysis", command=StartMain)
Start_Button.grid(row=1, column=0, sticky=W + E)
Stop_Button = ttk.Button(window, text="Stop analysis", command=Stop)
Stop_Button.grid(row=1, column=1, sticky=W + E)

# Row 1 - Whitelist/Blacklist
Whitelist_Button = ttk.Button(window, text="Whitelist IP", command=Whitelist)
Whitelist_Button.grid(row=2, column=0, sticky=W + E)
Blacklist_Button = ttk.Button(window, text="Blacklist IP", command=Blacklist)
Blacklist_Button.grid(row=2, column=1, sticky=W + E)

# Row 2 - Console
Console_Text = ScrolledText(window, height=20, width=80)
Console_Text.grid(row=3, column=0, columnspan=2, sticky=W + E)
sys.stdout = StdoutRedirector(Console_Text)

# Row 3 - ProgressBar
ProgressBar = ttk.Progressbar(window, orient='horizontal', mode='indeterminate')
ProgressBar.grid(row=4, column=0, columnspan=2, sticky=W + E)

# Initialize the widgets
window.mainloop()
