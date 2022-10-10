from ctypes import pointer
from tkinter import *
import os
from tkinter.filedialog import *
from tkinter import messagebox
import datetime

class Notepad:

    def run(self):
        self.window.mainloop()

    def new(self, event=None):
        self.x = messagebox.askyesno("Notepad", "Do you want to save ?")

        if self.x==True:
            self.save()
        else:
            pass

        self.window.title("Untitled - Notepad")
        self.cr_file = None
        self.text_box.delete(1.0, END)

    def open(self, event=None):
        self.x = messagebox.askyesno("Notepad", "Do you want to save ?")

        if self.x == True:
            self.save()
        else:
            pass

        self.cr_file = askopenfilename(defaultextension=".txt",
                                       filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.cr_file == "":
            self.cr_file = None

        else:
            self.window.title(os.path.basename(self.cr_file) + " - Notepad")
            self.text_box.delete(1.0, END)

            self.cr_file = open(self.cr_file, "r")

            self.text_box.insert(1.0,self.cr_file.read())

            self.cr_file.close()

    def save(self, event=None):
        try:
            f = open(self.cr_file, "w")
            f.write(self.text_box.get(1.0, END))
            f.close()

        except:
            self.save_as()

    def save_as(self):
        try:
            self.cr_file = asksaveasfilename(initialfile="Untitled.txt",
                                             defaultextension=".txt",
                                             filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

            f = open(self.cr_file, "w")
            f.write(self.text_box.get(1.0, END))
            f.close()

            self.window.title(os.path.basename(self.cr_file) + " - Notepad")
        except:
            pass

    def exit(self):
        self.x = messagebox.askyesno("Notepad", "Do you want to save ?")

        if self.x == True:
            self.save()
            self.window.destroy()
        else:
            self.window.destroy()

    def undo(self):
        self.text_box.event_generate("<<Undo>>")

    def redo(self):
        self.text_box.event_generate("<<Redo>>")

    def cut(self):
        self.text_box.event_generate("<<Cut>>")

    def copy(self):
        self.text_box.event_generate("<<Copy>>")

    def paste(self):
        self.text_box.event_generate("<<Paste>>")

    def find(self, event=None):
        #create find window
        self.window_2 = Tk()
        self.window_2.title("Find")
        self.window_2.resizable(False, False)
        self.window_2.geometry("300x50")
        self.window_2.bind('<Return>', self.find_word)

        self.label1 = Label(self.window_2, text="Find what:")
        self.label1.grid(row=1, column=1, padx=10, pady=8)

        self.entry1 = Entry(self.window_2)
        self.entry1.grid(row=1, column=2, padx=10, pady=8)

        self.button1 = Button(self.window_2, text="Find", command=self.find_word,width=6, activebackground="black", activeforeground="white")
        self.button1.grid(row=1, column=3, padx=10, pady=8)

    def find_word(self, event=None):
        self.text_box.tag_remove('found', '1.0', END)
        self.case = IntVar()
        self.case_sensitive = messagebox.askyesno("Information", "Case Sensitive ?")
        if self.case_sensitive:
            self.case = 0
        else:
            self.case = 1
            
        # take the word which we are searching
        self.searched_text = self.entry1.get()
        if self.searched_text:
            self.idx = '1.0'
            while 1:
                # searches for desired string from index 1
                #like idx = 1.10, idx = 2.12 etc
                self.idx = self.text_box.search(self.searched_text, self.idx, stopindex=END, nocase=self.case)

                if not self.idx:
                    break

                # it will take last character index of the upper searching word
                #like lastidx = 1.10+4c, 2.12+4c etc
                self.lastidx = '%s+%dc' % (self.idx, len(self.searched_text))

                # add all founded word in 'found' tag
                self.text_box.tag_add('found', self.idx, self.lastidx)
                self.idx = self.lastidx

            # mark located string as red
            self.text_box.tag_config('found', foreground='red', background="yellow")
        self.entry1.focus_set()

    def find_replace(self):
        # create find & replace window
        self.window_3 = Tk()
        self.window_3.title("Find")
        self.window_3.minsize(300, 80)
        self.window_3.geometry("300x80")
        self.window_3.columnconfigure([0,1], weight=3)
        self.entry1 = Entry(self.window_3, relief="sunken", borderwidth=2)
        self.entry1.grid(row=0, column=0, padx=10, pady=8, sticky="we")
        self.button1 = Button(self.window_3, text="Find", command=self.find_word)
        self.button1.grid(row=0, column=1, padx=10, sticky="we")
        self.entry2 = Entry(self.window_3, relief="sunken", borderwidth=2)
        self.entry2.grid(row=1, column=0, padx=10, pady=8,  sticky="we")
        self.button2 = Button(self.window_3, text="Replace", fg="green", command=self.replace)
        self.button2.grid(row=1, column=1, padx=10, sticky="we")

    def replace(self):
        self.text_box.tag_remove('found', '1.0', END)

        # take the word which we are searching & replacing
        self.searched_text = self.entry1.get()
        self.replaced_text = self.entry2.get()

        if (self.searched_text and self.replaced_text):
            self.idx = '1.0'
            while 1:
                # searches for desired string from index 1
                # like idx = 1.10, idx = 2.12 etc
                self.idx = self.text_box.search(self.searched_text, self.idx, stopindex=END, nocase=True)

                if not self.idx:
                    break

                # it will take last character index of the upper searching word
                # like lastidx = 1.10+4c, 2.12+4c etc
                self.lastidx = '%s+%dc' % (self.idx, len(self.searched_text))

                self.text_box.delete(self.idx, self.lastidx)
                self.text_box.insert(self.idx, self.replaced_text)

                self.lastidx = "%s+%dc" % (self.idx, len(self.replaced_text))

                # add all founded word in 'found' tag
                self.text_box.tag_add('found', self.idx, self.lastidx)

                # make previous first index as last index to search next foundable word
                self.idx = self.lastidx

            # mark located string as red
            self.text_box.tag_config('found', foreground='green', background="yellow")
        self.entry2.focus_set()

    def select_all(self, event=None):
        self.text_box.tag_add('sel', 1.0, END)

    def date_time(self, event=None):
        self.x = datetime.datetime.now()
        self.x = self.x.strftime("%d %B, %Y")
        self.current_index = self.text_box.index(INSERT)
        self.text_box.insert(self.current_index,self.x)

    def about(self):
        messagebox.showinfo("About Notepad", "This Notepad is made by Aashish Baisla")

    def line_column_info(self, event=None):
        self.line_no =  ''
        self.current_line, self.current_column = self.text_box.index("insert").split('.')
        self.information_bar.config(text='Line: %s | Column: %s' % (self.current_line, self.current_column))

    def show_info_bar(self):
        self.val = self.val_show_info.get()
        if self.val:
            self.information_bar.pack(side=BOTTOM, fill=X)
        elif not self.val:
            self.information_bar.pack_forget()

    def do_popup(self, event=None):
        try:
            self.m5.tk_popup(event.x, event.y, 0)
        finally:
            self.m5.grab_release()

    cr_file = None

    def __init__(self, **kwargs):
        self.layout_creation()
        self.icons()
        self.menu_button_creation()
        self.bindings()

    def layout_creation(self):
        self.window = Tk()
        self.window.title("Untitled - created by Aashish Baisla")
        self.window.geometry("400x400")
        self.window.wm_iconbitmap("icons/notepad.ico")

        # Creating Scroll Bar for text window
        self.scroll = Scrollbar(self.window)
        self.scroll.pack(side=RIGHT, fill=Y)
        # tell scroll bar to work for text_box
        self.text_box = Text(self.window, yscrollcommand=self.scroll.set)
        self.text_box.pack(side=LEFT, fill=BOTH, expand=True)
        # tell scroll bar to start motion in y direction
        self.scroll.config(command=self.text_box.yview)

        self.information_bar = Label(self.text_box, text='Line: 1 | Column: 0', padx=10)
        self.information_bar.pack(side=BOTTOM, fill=X)

    def menu_button_creation(self):
        self.main_menu = Menu(self.window)
        self.window.config(menu=self.main_menu)

        self.m1 = Menu(self.main_menu, tearoff=0)
        self.m1.add_command(label="New", command=self.new, accelerator='Ctrl+N',compound=LEFT, image=self.new_icon)
        self.m1.add_command(label="Open", command=self.open, accelerator='Ctrl+O',compound=LEFT, image=self.open_icon)
        self.m1.add_separator()
        self.m1.add_command(label="Save", command=self.save, accelerator='Ctrl+S',compound=LEFT, image=self.save_icon)
        self.m1.add_command(label="Save as", command=self.save_as,compound=LEFT, image=self.saveas_icon)
        self.m1.add_separator()
        self.m1.add_command(label="Exit", command=self.exit,compound=LEFT, image=self.exit_icon)
        self.main_menu.add_cascade(label="File", menu=self.m1)

        self.m2 = Menu(self.main_menu, tearoff=0)
        self.m2.add_command(label="Undo", accelerator='Ctrl+Z', command=self.undo, compound=LEFT, image=self.undo_icon)
        self.m2.add_command(label="Redo", accelerator='Ctrl+Y', command=self.redo, compound=LEFT, image=self.redo_icon)
        self.m2.add_separator()
        self.m2.add_command(label="Cut", command=self.cut, accelerator='Ctrl+X', compound=LEFT, image=self.cut_icon)
        self.m2.add_command(label="Copy", command=self.copy, accelerator='Ctrl+C', compound=LEFT, image=self.copy_icon)
        self.m2.add_command(label="Paste", command=self.paste, accelerator='Ctrl+V', compound=LEFT, image=self.paste_icon)
        self.m2.add_separator()
        self.m2.add_command(label="Find", command=self.find, accelerator='Ctrl+F',compound=LEFT, image=self.find_icon)
        self.m2.add_command(label="Replace", command=self.find_replace, compound=LEFT, image=self.replace_icon)
        self.m2.add_separator()
        self.m2.add_command(label="Select All", command=self.select_all, accelerator='Ctrl+A', compound=LEFT, image=self.selectall_icon)
        self.m2.add_command(label="Time/Date", command=self.date_time, accelerator='Ctrl+T', compound=LEFT, image=self.timedate_icon)
        self.main_menu.add_cascade(label="Edit", menu=self.m2)

        self.m3 = Menu(self.main_menu, tearoff=0)
        self.val_show_info = IntVar()
        self.val_show_info.set(1)
        self.m3.add_checkbutton(label="Show info bar", variable=self.val_show_info, command=self.show_info_bar, compound=LEFT, image=self.showinfobar_icon)
        self.main_menu.add_cascade(label="View", menu=self.m3)

        self.m4 = Menu(self.main_menu, tearoff=0)
        self.m4.add_command(label="About Notepad", command=self.about, compound=LEFT, image=self.help_icon)
        self.main_menu.add_cascade(label="Help", menu=self.m4)

        self.m5 = Menu(self.text_box, tearoff=0)
        self.m5.add_command(label="Cut", command=self.cut, compound=LEFT, image=self.cut_icon)
        self.m5.add_command(label="Copy", command=self.copy, compound=LEFT, image=self.copy_icon)
        self.m5.add_command(label="Paste", command=self.paste, compound=LEFT, image=self.paste_icon)
        self.m5.add_command(label="Select All", command=self.select_all, compound=LEFT, image=self.selectall_icon)

    def bindings(self):
        self.text_box.bind('<Control-S>', self.save)
        self.text_box.bind('<Control-s>', self.save)
        self.text_box.bind('<Control-A>', self.select_all)
        self.text_box.bind('<Control-a>', self.select_all)
        self.text_box.bind('<Control-N>', self.new)
        self.text_box.bind('<Control-n>', self.new)
        self.text_box.bind('<Control-O>', self.open)
        self.text_box.bind('<Control-o>', self.open)
        self.text_box.bind('<Control-F>', self.find)
        self.text_box.bind('<Control-f>', self.find)
        self.text_box.bind('<Control-T>', self.date_time)
        self.text_box.bind('<Control-t>', self.date_time)
        self.text_box.bind('<Any-KeyPress>', self.line_column_info)
        self.text_box.bind('<Button-3>', self.do_popup)

    def icons(self):
        self.new_icon = PhotoImage(file='icons/new_file.png')
        self.open_icon = PhotoImage(file='icons/open_file.png')
        self.save_icon = PhotoImage(file='icons/save_file.png')
        self.saveas_icon = PhotoImage(file='icons/save_as.png')
        self.exit_icon = PhotoImage(file='icons/Exit.png')

        self.undo_icon = PhotoImage(file='icons/undo.png')
        self.redo_icon = PhotoImage(file='icons/redo.png')
        self.cut_icon = PhotoImage(file='icons/cutting.png')
        self.copy_icon = PhotoImage(file='icons/copy.png')
        self.paste_icon = PhotoImage(file='icons/paste.png')
        self.find_icon = PhotoImage(file='icons/search.png')
        self.replace_icon = PhotoImage(file='icons/replace.png')
        self.selectall_icon = PhotoImage(file='icons/select_all.png')
        self.timedate_icon = PhotoImage(file='icons/time_date.png')

        self.showinfobar_icon = PhotoImage(file='icons/showinfobar.png')

        self.help_icon = PhotoImage(file='icons/help.png')



notepad = Notepad()
notepad.run()
