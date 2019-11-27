import tkinter as tk




def initWindow():
    root = tk.Tk()

    T = tk.Text(root)
    T.pack()
    T.insert(tk.END, "Just a text Widget\nin two lines\n")
    tk.mainloop()