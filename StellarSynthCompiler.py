import tkinter as tk
from tkinter import filedialog, ttk
import subprocess

from Syntax import SyntaxAnalyzer


class MainWindow:
    def __init__(self, master):
        self.opened_file_flag = False
        self.master = master
        self.master.title("StellarSynth Compiler")
        self.master.resizable(False, False)
        self.master.geometry("1280x720")
        self.master.configure(bg='#a09fff')
        self.master.iconbitmap("Astronaut.ico")
        self.UpdateDelay = 300
        self.s_index = 0
        self.s = "-> STELLARSYNTH COMPILER <- " * 10000

        self.main_frame = tk.Frame(self.master, bg='#f3f3ff', width=1240, height=680, bd=1, relief="solid")
        self.main_frame.grid(row=1, column=1)
        self.grid_configure(self.master)

        self.lexer_button = tk.Button(self.main_frame, text="Lexer", bg="#dbdbff", bd=1, relief="solid", width=10, command=self.run_lexical)
        self.lexer_button.place(x=15, y=40)

        self.syntax_button = tk.Button(self.main_frame, text="Syntax", bg="#dbdbff", bd=1, relief="solid", width=10, command=self.run_syntax)
        self.syntax_button.place(x=105, y=40)

        self.semantic_button = tk.Button(self.main_frame, text="Semantic", bg="#dbdbff", bd=1, relief="solid", width=10)
        self.semantic_button.place(x=195, y=40)

        self.open_button = tk.Button(self.main_frame, text="Open",bg="#dbdbff", bd=1, relief="solid", width=10, command=self.open_file)
        self.open_button.place(x=647, y=40)

        self.save_button = tk.Button(self.main_frame, text="Save",bg="#dbdbff", bd=1, relief="solid", width=10, command=self.save_file)
        self.save_button.place(x=737, y=40)

        self.stellar_synth_logo = tk.Label(self.main_frame, text=self.s, bg="BLACK", fg="#dbdbff", font=("terminal", 18))
        self.stellar_synth_logo.place(x=0, y=0)

        self.editor_with_scrollbar = tk.Frame(self.main_frame)
        self.editor_with_scrollbar.place(x=15, y=80, width=800, height=380)

        self.editor = tk.Text(self.editor_with_scrollbar, wrap="none", font=("Courier New", 11))
        self.editor.pack(expand=True, fill="both", side="left")
        self.editor.bind("<KeyRelease>", self.user_writes)

        self.scrollbar = tk.Scrollbar(self.editor_with_scrollbar, command=self.editor.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.editor['yscrollcommand'] = self.scrollbar.set

        self.errors_result = tk.Listbox(self.main_frame, bg="black", fg="white",font=("Courier New", 10))
        self.errors_result.place(x=14, y=460, width=802, height=200)

        self.Lexeme_Token_Table = ttk.Treeview(self.main_frame, columns=("Number","Lexeme", "Token"), show="headings")
        self.Lexeme_Token_Table.heading("Number", text="Num.")
        self.Lexeme_Token_Table.heading("Lexeme", text="Lexeme")
        self.Lexeme_Token_Table.heading("Token", text="Token")
        self.Lexeme_Token_Table.column("Number", width=50)
        self.Lexeme_Token_Table.column("Lexeme", width=165)
        self.Lexeme_Token_Table.column("Token", width=165)
        self.Lexeme_Token_Table_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.Lexeme_Token_Table.yview)
        self.Lexeme_Token_Table.configure(yscrollcommand=self.Lexeme_Token_Table_scrollbar.set)
        self.Lexeme_Token_Table.place(x=820, y=80, width=380, height=580)
        self.Lexeme_Token_Table_scrollbar.place(x=1195, y=80, height=580)

        self.master.after(self.UpdateDelay, self.update)

    def tag_rows(self, tree):
        for i, item in enumerate(tree.get_children()):
            tag = 'even' if i % 2 == 0 else 'odd'
            tree.tag_configure(tag, background='#E8E8E8' if tag == 'even' else '#FFFFFF')
            for col in tree['columns']:
                tree.item(item, tags=(tag,))
    def grid_configure(self, widget):
        for i in range(3):
            widget.rowconfigure(i, weight=1)
            widget.columnconfigure(i, weight=1)

    def update(self):
        double = self.s
        display = double[self.s_index:self.s_index + 77]
        self.stellar_synth_logo.config(text=display)

        self.s_index += 1
        if self.s_index >= len(double) // 2:
            self.s_index = 0

        self.master.after(self.UpdateDelay, self.update)

    def user_writes(self, event):
        if self.opened_file_flag is True:
            self.opened_file_flag = False

    def use_user_input(self):
        if self.opened_file_flag is False:
            input_text = self.editor.get("1.0", "end-1c")

            with open("StellarSynth", "w") as file:
                file.write(input_text)
        else:
            return

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, content)
                self.opened_file_flag = True

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.get("1.0", tk.END))

    def run_lexical(self):
        try:
            self.use_user_input()
            result = subprocess.check_output(['python', 'Lexer.py'], universal_newlines=True)

            lines = result.strip().split('\n')

            errors = eval(lines[0]) if lines else []
            tokens = eval(lines[1]) if len(lines) > 1 else []

            self.errors_result.delete(0, tk.END)

            if not errors:
                self.errors_result.insert(tk.END, " StellarSynth -> No errors found during tokenization.")
            else:
                for error in errors:
                    self.errors_result.insert(tk.END, f" StellarSynth -> {error}")

            self.Lexeme_Token_Table.delete(*self.Lexeme_Token_Table.get_children())
            if not tokens:
                self.errors_result.insert(tk.END, " StellarSynth -> Tokens list is empty.")
            else:
                tok_count = 0
                for lexeme, token in tokens:
                    if token == "\n" or token == "\t":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tempval2 = repr(token)
                        tempval2 = tempval2[1:-1]
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count, tempval1, tempval2))
                    elif token == "StarsysLiteral":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count,tempval1, token))
                    else:
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count,lexeme, token))

            self.tag_rows(self.Lexeme_Token_Table)
            self.errors_result.insert(tk.END, "")
            self.errors_result.insert(tk.END, " StellarSynth -> Tokenization Complete.")

        except Exception as e:
            print(f"Error: {e}")

    def run_syntax(self):
        try:
            self.use_user_input()
            result = subprocess.check_output(['python', 'Lexer.py'], universal_newlines=True)

            lines = result.strip().split('\n')

            errors = eval(lines[0]) if lines else []
            tokens = eval(lines[1]) if len(lines) > 1 else []

            self.errors_result.delete(0, tk.END)

            if not errors:
                self.errors_result.insert(tk.END, "StellarSynth -> No errors found during tokenization.")
            else:
                for error in errors:
                    self.errors_result.insert(tk.END, f"StellarSynth -> {error}")

            self.Lexeme_Token_Table.delete(*self.Lexeme_Token_Table.get_children())

            if not tokens:
                self.errors_result.insert(tk.END, "StellarSynth -> Tokens list is empty.")
            else:
                tok_count = 0
                for lexeme, token in tokens:
                    if token == "\n" or token == "\t":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tempval2 = repr(token)
                        tempval2 = tempval2[1:-1]
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count, tempval1, tempval2))
                    elif token == "StarsysLiteral":
                        tempval1 = repr(lexeme)
                        tempval1 = tempval1[1:-1]
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count, tempval1, token))
                    else:
                        tok_count += 1
                        self.Lexeme_Token_Table.insert("", tk.END, values=(tok_count, lexeme, token))

                self.tag_rows(self.Lexeme_Token_Table)
                self.errors_result.insert(tk.END, "")
                self.errors_result.insert(tk.END, "StellarSynth -> Tokenization Complete.")

            # Now, you can integrate the SyntaxAnalyzer and call its methods with the tokens list
            syntax_analyzer = SyntaxAnalyzer(tokens)
            syntax_analyzer.parse_top_program()
            #  syntax_analyzer.parse_main_program()

            if syntax_analyzer.errors:
                for error in syntax_analyzer.errors:
                    self.errors_result.insert(tk.END, f"StellarSynth -> {error}")
            else:
                self.errors_result.insert(tk.END, "StellarSynth -> Syntax is correct")

        except Exception as e:
            print(f"Error: {e}")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()






































