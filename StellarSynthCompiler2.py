import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
import Syntax, Lexer, Semantic
import customtkinter
import datetime
import subprocess
import Transpiler

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()

        self.geometry('%dx%d+0+0' % (width,height))
        self.iconbitmap("Astronaut.ico")
        self.title("StellarSynth Compiler")
        self.configure(background="white")
        self.mainframe = None

        # Main Frame
        self.CreateMainFrame()

        # Text Editor
        self.TextEditor = CreateTextEditor(self)

        # Lexeme Token Table
        self.LexemeTable = CreateTable(self)
        
        # Logs & Console
        self.Console = CreateConsole(self)

        # Logo
        self.StellarLogo = CreateLogo(self)

        # Buttons
        self.Buttons = CreateButtons(self, self.LexemeTable, self.TextEditor, self.Console)

        # Date
        self.TimeDate = CreateTimer(self)

        # Main Menu
        self.Menu = CreateMenu(self, self.LexemeTable, self.TextEditor, self.Console)

    def ConfigureRowColumn(self, Name, n):
        for i in range (0,n):
            Name.grid_rowconfigure(i, weight=1)
            Name.grid_columnconfigure(i, weight=1)

    def CreateMainFrame(self):
        self.mainframe = customtkinter.CTkFrame(self, bg_color='gray10')
        self.mainframe.pack(anchor='n',fill=tk.BOTH,expand=True)
        self.mainframe.grid_rowconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(2, weight=1)
        self.mainframe.grid_rowconfigure(3, weight=1)
        self.mainframe.grid_rowconfigure(4, weight=1)
        self.mainframe.grid_rowconfigure(5, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_columnconfigure(2, weight=1)
        self.mainframe.grid_columnconfigure(3, weight=1)
        self.mainframe.grid_columnconfigure(4, weight=1)
        self.mainframe.grid_columnconfigure(5, weight=1)

    def scrollwheel(self, event):
        return 'break'

    """def populateLineNum(self,linenumber):
        for i in range (1, 50):
            linenumber.insert(tk.END, f"{i}\n")"""

class CreateTextEditor(customtkinter.CTkTextbox):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.textframe = customtkinter.CTkFrame(master.mainframe, fg_color='transparent', corner_radius=0,border_width=1, border_color="gray20")
        self.textframe.grid(row=1,column=0, columnspan=5, rowspan=4, sticky='nsew', padx=(5,0),pady=(5,0))
        self.textframe.grid_rowconfigure(0,weight=1)
        self.textframe.grid_rowconfigure(1,weight=1)
        self.textframe.grid_rowconfigure(2,weight=1)
        self.textframe.grid_columnconfigure(1,weight=1)
        self.textframe.grid_columnconfigure(2,weight=1)

        self.texteditor = customtkinter.CTkTextbox(self.textframe, font=("Courier", 15), activate_scrollbars = False, undo = True, wrap='none'
                                              ,border_width=1, border_color="gray20", corner_radius=0)
        self.texteditor.grid(row=0,column=1, columnspan=3,rowspan=3, sticky='nsew')

        self.linenumber = customtkinter.CTkTextbox(self.textframe, font=("Courier", 15), activate_scrollbars = False, wrap='none'
                                              ,border_width=1, border_color="gray20", corner_radius=0, width=30)
        self.linenumber.grid(row=0,column=0,rowspan=3, sticky='nsw')

        self.scrollbar1 = customtkinter.CTkScrollbar(self.texteditor, button_color="gray18",button_hover_color="gray30", command=lambda *args: (self.texteditor.yview(*args), self.linenumber.yview(*args)))
        self.scrollbar1.grid(row=0, column=1, sticky="ns",padx=(0,5),pady=(5,0))
        self.scrollbar2 = customtkinter.CTkScrollbar(self.texteditor, command=self.texteditor.xview,orientation="horizontal", button_color="gray18",button_hover_color="gray30")
        self.scrollbar2.grid(row=1, column=0, sticky="ew", padx=(5, 0), pady=(0, 5))

        self.texteditor.configure(yscrollcommand=self.scrollbar1.set, xscrollcommand = self.scrollbar2.set, tabs='0.5i')
        self.linenumber.bind('<MouseWheel>', master.scrollwheel) # Overrides so that scrolling no longer works in linenumbers text widget.
        self.texteditor.bind('<MouseWheel>', master.scrollwheel) # I Overrode scrolling for texteditor too, since scrolling with mousewheel is currently clunky

        self.addlineNumbers()
        self.linenumber.configure(state='disabled')
        master.after(10, self.addlineNumbers) # Updates every 0.010 seconds.


    """def HandleBackSpace(self):
        # This solution is very improvised, does not work properly when moving back a line while still having characters on current line.
        # end-2c It is so that on backspace, instead of calculating the position of cursor. It calculates the position of the last printable character (Not including newline)
        numofline = int(float(self.texteditor.index("end-2c")))

        self.linenumber.configure(state='normal')
        self.linenumber.delete("1.0", tk.END)
        if numofline < 9:
            for i in range(1, 11):
                self.linenumber.insert(tk.END, f"{i}\n")
        else:
            for i in range(1, numofline + 2):
                self.linenumber.insert(tk.END, f"{i}\n")
        self.linenumber.configure(state='disabled')"""


    def addlineNumbers(self):
        numofline = int(float(self.texteditor.index("end")))

        self.linenumber.configure(state='normal')
        self.linenumber.delete("1.0", tk.END)
        if numofline < 9:
            for i in range(1, 11):
                self.linenumber.insert(tk.END, f"{i}\n")
        else:
            for i in range(1, numofline + 2):
                self.linenumber.insert(tk.END, f"{i}\n")
        self.linenumber.configure(state='disabled')
        self.master.after(10, self.addlineNumbers)



class CreateTable(ttk.Treeview):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.tableframe = customtkinter.CTkFrame(master.mainframe, height=400, fg_color='transparent')
        self.tableframe.grid(row=1, column=5, columnspan=2, rowspan=5, padx=(0, 5), pady=(5, 5), sticky='nsew')
        master.ConfigureRowColumn(self.tableframe, 3)
        self.Lexeme_Token_Table = ttk.Treeview(self.tableframe, columns=("Number", "Lexeme", "Token"), show="headings")
        self.Lexeme_Token_Table.heading("Number", text="Number")
        self.Lexeme_Token_Table.heading("Lexeme", text="Lexeme")
        self.Lexeme_Token_Table.heading("Token", text="Token")
        self.Lexeme_Token_Table.column("Number", width=125)
        self.Lexeme_Token_Table.column("Lexeme", width=125)
        self.Lexeme_Token_Table.column("Token", width=125)

        self.Lexeme_Token_Table_scrollbar = tk.Scrollbar(self.tableframe, orient="vertical",
                                                         command=self.Lexeme_Token_Table.yview)
        self.Lexeme_Token_Table.configure(yscrollcommand=self.Lexeme_Token_Table_scrollbar.set)
        self.Lexeme_Token_Table.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="nsew")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="gray14",
                        fieldbackground="gray14", foreground="gray84", lightcolor="transparent", bordercolor="transparent",
                        darkcolor="#ffc61e")
        self.style.configure("Treeview.Heading", borderwidth=0, background="gray30", foreground="gray84")


    def tag_rows(self, tree):
        for i, item in enumerate(tree.get_children()):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.tag_configure(tag, background='gray20' if tag == 'even' else 'gray14')
            for col in tree['columns']:
                tree.item(item, tags=(tag,))

class CreateConsole(customtkinter.CTkTextbox):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.consoleframe = customtkinter.CTkFrame(master.mainframe, fg_color='transparent')
        self.consoleframe.grid(row=5, column=0, columnspan=5, rowspan=2, padx=(5, 0), pady=(0, 5), sticky='nsew')
        self.consoleframe.grid_rowconfigure(0, weight=1)
        self.consoleframe.grid_rowconfigure(1, weight=1)
        self.consoleframe.grid_rowconfigure(2, weight=1)
        self.consoleframe.grid_columnconfigure(1, weight=1)
        self.consoleframe.grid_columnconfigure(2, weight=1)

        self.console = customtkinter.CTkTextbox(self.consoleframe, font=("Courier", 14), activate_scrollbars=True,
                                           state='disabled',
                                           wrap='none', border_width=1, border_color="gray20", corner_radius=0,
                                           fg_color="black", border_spacing=8)
        self.console.grid(row=0, column=0, columnspan=3, rowspan=3, sticky='nsew')



class CreateLogo(customtkinter.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.namelogo = customtkinter.CTkFrame(master.mainframe, fg_color="transparent")
        self.namelogo.grid(row=0, column=0, padx=(5, 10), pady=(5, 0))
        master.ConfigureRowColumn(self.namelogo, 3)
        self.stellar_synth_name = customtkinter.CTkLabel(self.namelogo, text="StellarSynth Compiler", fg_color="transparent",
                                                         text_color="#dbdbff", font=("Impact", 35))
        self.stellar_synth_name.grid(row=1, column=0,ipadx=10)

        self.astronaut1 = customtkinter.CTkImage(
            dark_image=Image.open("Astronaut.ico"),
            size=(70, 70))
        self.astronaut = customtkinter.CTkLabel(self.namelogo, image=self.astronaut1, text="")
        self.astronaut.grid(row=1, column=1, sticky='nsew')

class CreateMenu(tk.Menu):
    def __init__(self, master: any, lexeme_table: CreateTable, text_editor: CreateTextEditor, console : CreateConsole, **kwargs):
        super().__init__(master, **kwargs)

        self.mainmenu = tk.Menu(master)
        self.lexeme_table = lexeme_table
        self.text_editor = text_editor
        self.console1 = console

        filemenu = tk.Menu(self.mainmenu, tearoff=0, foreground='gray14', activeforeground= "gray84", activebackground="gray20")
        self.mainmenu.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="New")
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)

        clear = tk.Menu(self.mainmenu, tearoff=0, foreground='gray14', activeforeground="gray84",
                        activebackground="gray20")
        self.mainmenu.add_command(label="Clear All Windows", command=self.clear)

        master.config(menu=self.mainmenu)

    def new_file(self):
        pass
    def open_file(self):
        try:
            self.text_editor.texteditor.delete('1.0', tk.END)
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
            if file_path:
                with open(f'{file_path}', 'r') as f:
                    input_text = f.read()
                    self.text_editor.texteditor.insert(tk.END, input_text)
                f.close()
        except:
            messagebox.showerror("Error!", "Unable to open File.")

    def save_file(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(self.text_editor.texteditor.get("1.0", "end-1c"))
                f.close()
        except:
            messagebox.showerror("Error!", "Unable to save file.")

    def clear(self):
        try:
            if self.text_editor.texteditor:
                self.text_editor.texteditor.delete('1.0', tk.END)
            if self.console1.console:
                self.console1.console.configure(state="normal")
                self.console1.console.delete('1.0', tk.END)
                self.console1.console.configure(state="disabled")
            if self.lexeme_table.Lexeme_Token_Table:
                self.lexeme_table.Lexeme_Token_Table.delete(*self.lexeme_table.Lexeme_Token_Table.get_children())
            messagebox.showinfo("Success", "Clearing Successful.")
        except:
            messagebox.showerror("Error!", "Clearing Unsuccessful.")


class CreateButtons(customtkinter.CTkButton):
    def __init__(self, master: any, lexeme_table: CreateTable, text_editor: CreateTextEditor, console: CreateConsole,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.lexeme_table = lexeme_table
        self.text_editor = text_editor
        self.console1 = console
        self.LexSynSemPass = False

        self.ButtonFrame = customtkinter.CTkFrame(master.mainframe, fg_color='transparent')
        self.ButtonFrame.grid(row=0, column=2, columnspan=3, padx=(5,0), pady=(10,0))
        master.ConfigureRowColumn(self.ButtonFrame, 4)
        self.createbutton("Lexer",0, self.run_lexical)
        self.createbutton("Syntax", 1, self.run_syntax)
        self.createbutton("Semantic", 2, self.run_semantic)
        self.createbutton("Run", 3, self.run_Compile)

    def createbutton(self, text, column, command):
        button = customtkinter.CTkButton(self.ButtonFrame, text=text, font=("terminal", 17), fg_color='#381456', hover_color="#4b1a73", border_width=1, border_color="#1a1631", height=40,width=200, command=command)
        button.grid(row=1, column=column, sticky='nsew', padx=(5, 0))

    def run_lexical(self):
        self.console1.console.configure(state="normal")
        tok_count = 0
        self.console1.console.tag_config("Error", foreground="#d50000")
        self.console1.console.tag_config("Complete", foreground="green")
        try:
            contents=self.text_editor.texteditor.get("1.0", "end-1c")
            errors, tokens = Lexer.read_text(contents)
            self.console1.console.delete("1.0", tk.END)

            if not errors and tokens:
                self.console1.console.insert(tk.END, "StellarSynth -> No errors found during lexical analysis.\n", tags="Complete")
            else:
                for error in errors:
                    self.console1.console.insert(tk.END, f"StellarSynth -> {error}\n", tags="Error")

            self.lexeme_table.Lexeme_Token_Table.delete(*self.lexeme_table.Lexeme_Token_Table.get_children())
            if not tokens:
                self.console1.console.insert(tk.END, "StellarSynth -> Tokens list is empty.\n")
            else:
                tok_count = 0
                for lexeme, token in tokens:
                    if token == "\n" or token == "\t":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tempval2 = repr(token)
                        tempval2 = tempval2[1:-1]
                        tok_count += 1
                        self.lexeme_table.Lexeme_Token_Table.insert("", tk.END, values=(tok_count, tempval1, tempval2))
                    elif token == "StarsysLiteral":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tok_count += 1
                        self.lexeme_table.Lexeme_Token_Table.insert("", tk.END, values=(tok_count,tempval1, token))
                    else:
                        tok_count += 1
                        self.lexeme_table.Lexeme_Token_Table.insert("", tk.END, values=(tok_count,lexeme, token))

            self.lexeme_table.tag_rows(self.lexeme_table.Lexeme_Token_Table)
            self.console1.console.insert(tk.END, "\nStellarSynth -> Lexical Analysis Complete.")
            self.console1.console.insert(tk.END, f"\nStellarSynth -> Generated a total of {tok_count} tokens. ")

        except Exception as e:
            print(f"Error: {e}")

        self.console1.console.configure(state='disabled')

    def run_syntax(self):
        self.console1.console.configure(state="normal")

        self.console1.console.tag_config("Error", foreground="#d50000")
        self.console1.console.tag_config("Complete", foreground="green")
        contents = self.text_editor.texteditor.get("1.0", "end-1c")
        try:
            self.console1.console.delete("1.0", tk.END)
            errors, tokens = Lexer.read_text(contents)
            if errors:
                self.console1.console.insert(tk.END,
                                             "StellarSynth -> Lexical Analysis Error. Cannot proceed with Syntax Analysis.\n",
                                             tags="Error")
                return
            if not tokens:
                self.console1.console.insert(tk.END, "StellarSynth -> Tokens list is empty.\n")
            else:
                syntax_analyzer = Syntax.SyntaxAnalyzer(tokens)
                syntax_analyzer.parse_top_program()

                if syntax_analyzer.errors:
                    for error in syntax_analyzer.errors:
                        self.console1.console.insert(tk.END, f"StellarSynth -> {error}\n", tags="Error")
                else:
                    self.console1.console.insert(tk.END, "StellarSynth -> Syntax is correct. No Errors Found.\n", tags="Complete")

            self.console1.console.insert(tk.END, "\nStellarSynth -> Syntax Analysis Complete.")
        except Exception as e:
            print(f"Error: {e}")

        self.console1.console.configure(state="disabled")

    def run_semantic(self):
        self.console1.console.configure(state="normal")

        self.console1.console.tag_config("Error", foreground="#d50000")
        self.console1.console.tag_config("Complete", foreground="green")
        contents = self.text_editor.texteditor.get("1.0", "end-1c")
        try:
            self.console1.console.delete("1.0", tk.END)
            errors, tokens = Lexer.read_text(contents)
            if errors:
                self.console1.console.insert(tk.END,
                                             "StellarSynth -> Lexical Analysis Error. Cannot proceed with Syntax Analysis.\n",
                                             tags="Error")
                return
            if not tokens:
                self.console1.console.insert(tk.END, "StellarSynth -> Tokens list is empty.\n")
            else:
                syntax_analyzer = Syntax.SyntaxAnalyzer(tokens)
                syntax_analyzer.parse_top_program()

                if syntax_analyzer.errors:
                    self.console1.console.insert(tk.END, f"StellarSynth -> Syntax Analysis Error. Cannot proceed with Semantic Analysis.\n", tags="Error")
                else:
                    semantic_analyzer = Semantic.SemanticAnalyzer(tokens)
                    semantic_analyzer.parse_top_program()

                    if semantic_analyzer.errors:
                        for error in semantic_analyzer.errors:
                            self.console1.console.insert(tk.END, f"StellarSynth -> {error}\n", tags="Error")
                    else:
                        self.console1.console.insert(tk.END, "StellarSynth -> Syntax is Semantically Correct. No Semantic Errors Found.\n",
                                                     tags="Complete")

            self.console1.console.insert(tk.END, "\nStellarSynth -> Semantic Analysis Complete.")
        except Exception as e:
            print(f"Error: {e}")

        self.console1.console.configure(state="disabled")
        
    def run_Compile(self):
        self.console1.console.configure(state="normal")
        self.console1.console.tag_config("Error", foreground="#d50000")
        self.console1.console.tag_config("Complete", foreground="green")
        contents = self.text_editor.texteditor.get("1.0", "end-1c")
        try:
            self.console1.console.delete("1.0", tk.END)
            errors, tokens = Lexer.read_text(contents)
            if errors:
                self.console1.console.insert(tk.END,
                                             "StellarSynth -> Lexical Analysis Error. Cannot proceed with Syntax Analysis.\n",
                                             tags="Error")
                return
            if not tokens:
                self.console1.console.insert(tk.END, "StellarSynth -> Tokens list is empty.\n")
            else:
                syntax_analyzer = Syntax.SyntaxAnalyzer(tokens)
                syntax_analyzer.parse_top_program()

                if syntax_analyzer.errors:
                    self.console1.console.insert(tk.END, f"StellarSynth -> Syntax Analysis Error. Cannot proceed with Semantic Analysis.\n", tags="Error")
                else:
                    semantic_analyzer = Semantic.SemanticAnalyzer(tokens)
                    semantic_analyzer.parse_top_program()

                    if semantic_analyzer.errors:
                        self.console1.console.insert(tk.END, f"StellarSynth -> Semantic Analysis Error. Cannot proceed with compilation.\n", tags="Error")
                    else:
                        transpilerInstance = Transpiler.Transpiler(tokens)
                        transpilerInstance.stellarTranslator()
                        transerrors, transoutput = transpilerInstance.writetoCPPFile()
                        if errors:
                            self.console1.console.insert(tk.END, f"StellarSynth -> {transerrors}\n", tags="Error")
                        else:
                            self.console1.console.insert(tk.END, f"\n{transoutput}\n")
                    self.console1.console.insert(tk.END, "\nStellarSynth -> Compilation Complete.")
            
        except Exception as e:
            print(f"Error: {e}")
            
        self.console1.console.configure(state="disabled")


class CreateTimer(customtkinter.CTkFrame):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)

        self.Textbox = customtkinter.CTkFrame(master.mainframe, fg_color="gray20")
        self.Textbox.grid(row=0, column=5, sticky="nsw", padx=(5,5),pady=(10,0))
        master.ConfigureRowColumn(self.Textbox, 3)

        self.Textcreate(f"Today is:\n{datetime.datetime.today().strftime('%b %d, %Y (%a)\n%I:%M:%S %p')}", 0, ("arial",13))
        self.Textcreate(f"The Travellers'\n Syndicate",1, ("terminal",13))
        self.Textcreate(f"Compiler Design\nA.Y 2023-2024", 2, ("arial",13))

        master.after(1000,self.update_date)
    def update_date(self):
        self.Textcreate(f"Today is:\n{datetime.datetime.today().strftime('%b %d, %Y (%a)\n%I:%M:%S %p')}", 0,
                        ("arial", 13))
        self.after(1000, self.update_date)


    def Textcreate(self, text, column, font):
        self.Text = customtkinter.CTkLabel(self.Textbox, text=text, justify="left", font=(font), text_color="gray60", corner_radius=5, fg_color="transparent")
        self.Text.grid(row=1,column=column,ipadx=5, ipady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
