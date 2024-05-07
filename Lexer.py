import Resources
import os

# Splits the Contents into Lines
class Lexer:
    def __init__(self, contents):
        self.contents = contents
        self.Tokens, self.Errors = [], []
        self.line, self.lines = None, None
        self.line_num, self.column_num = 0, 0
        self.starsys_flag, self.sl_com_flag, self.not_keyword_flag = False, False, False
        self.identifier_count = 0
        self.letter_count = 0
        self.current_lexeme = ""
        self.pos = -1
        self.current_char = ""

    def split_content_into_lines(self):
        self.lines = self.contents.splitlines(keepends=True)
        self.split_lines()
        return self.Errors, self.Tokens

    # Splits the Lines to single line and processes the self.current_characters of each line.
    def split_lines(self):
        for self.line in self.lines:
            self.line_num += 1
            self.column_num = 0
            self.pos = -1
            self.current_char = ""
            self.process_line()

    def process_line(self):
        while self.pos < len(self.line):
            self.advance()
            if self.current_char is None and self.current_lexeme == "":
                break
            elif self.starsys_flag is True:
                self.process_starsys()
                continue
            elif self.current_char == " ":
                self.process_space()
                continue
            elif self.current_char.isupper() and self.not_keyword_flag is False:
                self.process_keyword()
                continue
            elif (self.current_char.isupper() and self.not_keyword_flag is True) or self.current_char.islower():
                self.process_identifier()
                continue
            elif self.current_char == "=" or self.current_char == "!" or self.current_char == "<" or self.current_char == ">" or self.current_char == "+" or self.current_char == "-" or self.current_char == "*" or self.current_char == "/" or self.current_char == "%" or self.current_char == "&" or self.current_char == "|" or self.current_char == "~":
                self.process_operator()
                continue
            elif self.current_char.isdigit():
                self.process_digit()
                continue
            elif self.current_char == '(' or self.current_char == ')' or self.current_char == '{' or self.current_char == '}' or self.current_char == '[' or self.current_char == ']' or self.current_char == ',' or self.current_char == '.' or self.current_char == ':':
                self.process_punctuator()
                continue
            elif self.current_char == "#":
                self.process_terminator()
                continue
            elif self.current_char == "$":
                self.process_comment()
                continue
            elif self.current_char == "\n":
                self.process_newline()
                continue
            elif self.current_char == "\t":
                self.process_tab()
                continue
            elif self.current_char == "\"" or self.current_char == "\'":
                self.process_starsys()
                continue
            else:
                self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_char)} is not a recognized character.")

    def advance(self):
        self.pos += 1
        self.column_num += 1
        if self.pos < len(self.line):
            self.current_char = self.line[self.pos]
        else:
            self.current_char = None

    def retreat(self):
        if self.pos >= 0:
            self.pos -= 1
        self.column_num -= 1
        if self.pos < 0:
            self.current_char = None
        else:
            self.current_char = self.line[self.pos]

    def letter_not_match(self):
        self.retreat()
        self.not_keyword_flag = True
        return False

    def process_keyword(self):
        self.retreat()
        while self.not_keyword_flag is False:
            self.advance()
            if self.current_char == 'A':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'u':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'o':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'm':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == "B":
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'o':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'o':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'l':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'e':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'a':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'n':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == "C":
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'a':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'p':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'l':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'a':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 's':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 's':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == "D":
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'v':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'i':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'a':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'e':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'i':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 's':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'i':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'n':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'e':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'g':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 'r':
                                                self.letter_count += 1
                                                self.current_lexeme += self.current_char
                                                self.advance()
                                                if self.current_char == 'a':
                                                    self.letter_count += 1
                                                    self.current_lexeme += self.current_char
                                                    self.advance()
                                                    if self.current_char == 't':
                                                        self.letter_count += 1
                                                        self.current_lexeme += self.current_char
                                                        self.advance()
                                                        if self.current_char == 'e':
                                                            self.letter_count += 1
                                                            self.current_lexeme += self.current_char
                                                            break
                                                        else:
                                                            self.letter_not_match()
                                                            break
                                                    else:
                                                        self.letter_not_match()
                                                        break
                                                else:
                                                    self.letter_not_match()
                                                    break
                                            else:
                                                self.letter_not_match()
                                                break
                                        else:
                                            self.letter_not_match()
                                            break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        elif self.current_char == 'p':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    elif self.current_char == 'v':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'r':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'F':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'a':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'l':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 's':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'e':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'o':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'r':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        elif self.current_char == 'm':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'u':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'l':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'a':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 't':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 'e':
                                                self.letter_count += 1
                                                self.current_lexeme += self.current_char
                                                break
                                            else:
                                                self.letter_not_match()
                                                break
                                        else:
                                            self.letter_not_match()
                                            break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'G':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'o':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'o':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'l':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'e':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'r':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'a':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 't':
                                                self.letter_count += 1
                                                self.current_lexeme += self.current_char
                                                self.advance()
                                                if self.current_char == 'e':
                                                    self.letter_count += 1
                                                    self.current_lexeme += self.current_char
                                                    break
                                                else:
                                                    self.letter_not_match()
                                                    break
                                            else:
                                                self.letter_not_match()
                                                break
                                        else:
                                            self.letter_not_match()
                                            break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'I':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'S':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'S':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'f':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    break
                elif self.current_char == 'm':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'p':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'o':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'r':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'L':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'a':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'c':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'h':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    elif self.current_char == 'u':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'n':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'c':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'h':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'u':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'h':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'm':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'a':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'n':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'N':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'a':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'v':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'g':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 't':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'o':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'o':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'm':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'i':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'n':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'a':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'l':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'O':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 't':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'h':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'r':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break


            elif self.current_char == 'P':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'r':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'f':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'o':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'r':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'm':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'r':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'v':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'a':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'e':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    elif self.current_char == 'o':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'c':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'e':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'e':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'd':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        elif self.current_char == 't':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'e':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'c':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 't':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'e':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 'd':
                                                self.letter_count += 1
                                                self.current_lexeme += self.current_char
                                                break
                                            else:
                                                self.letter_not_match()
                                                break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'u':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'b':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'l':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'i':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'c':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'R':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'r':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'i':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'e':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'v':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'e':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            break
                                        else:
                                            self.letter_not_match()
                                            break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'S':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'c':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'e':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'n':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'a':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'r':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'i':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'o':
                                            self.letter_count += 1
                                            self.current_lexeme += self.current_char
                                            break
                                        else:
                                            self.letter_not_match()
                                            break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'p':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'a':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'n':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 't':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'a':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'r':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 's':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'y':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 's':
                                        self.letter_count += 1
                                        self.current_lexeme += self.current_char
                                        break
                                    else:
                                        self.letter_not_match()
                                        break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        elif self.current_char == 't':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'i':
                                self.letter_count += 1
                                self.current_lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'c':
                                    self.letter_count += 1
                                    self.current_lexeme += self.current_char
                                    break
                                else:
                                    self.letter_not_match()
                                    break
                            else:
                                self.letter_not_match()
                                break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'u':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'n':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'T':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 's':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                elif self.current_char == 'r':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'u':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break

            elif self.current_char == 'V':
                self.letter_count += 1
                self.current_lexeme += self.current_char
                self.advance()
                if self.current_char == 'o':
                    self.letter_count += 1
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        self.letter_count += 1
                        self.current_lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'd':
                            self.letter_count += 1
                            self.current_lexeme += self.current_char
                            break
                        else:
                            self.letter_not_match()
                            break
                    else:
                        self.letter_not_match()
                        break
                else:
                    self.letter_not_match()
                    break
            else:
                self.letter_not_match()

        self.advance()
        if self.current_char in Resources.ComAlpha + ["_"] + Resources.DigitsWithZero and self.not_keyword_flag is False:
            self.not_keyword_flag = True
        self.retreat()

        if self.not_keyword_flag is True:
            if self.letter_count > 0:
                for i in range(self.letter_count):
                    self.retreat()
            self.current_lexeme = ""
            self.letter_count = 0
            return

        self.advance()
        if self.current_char in Resources.WordSymbolDelims[self.current_lexeme]:
            self.Tokens.append([self.current_lexeme, self.current_lexeme])
            self.current_lexeme = ""
            self.letter_count = 0
            self.retreat()
            return
        else:
            self.Errors.append(
                f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
            self.current_lexeme = ""
            self.letter_count = 0
            return

    def process_identifier(self):
        while self.current_char in Resources.AlphaNum + ["_"]:
            self.current_lexeme += self.current_char
            self.advance()
            if len(self.current_lexeme) == 15:
                break

        if len(self.current_lexeme) == 15 and self.current_char in Resources.AlphaNum + ["_"]:
            self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: \'{self.current_lexeme}\' identifier length is 15 max. Expected sun delimiter, instead got {repr(self.current_char)}.")
            self.current_lexeme = ""
            return False

        elif self.current_char in Resources.Identifier_delim:
            self.identifier_count += 1
            self.Tokens.append([self.current_lexeme, f"Identifier{self.identifier_count}"])
            self.current_lexeme = ""
            self.not_keyword_flag = False
            self.retreat()
            return

        elif self.current_char not in Resources.Identifier_delim:
            self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: identifier {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
            self.current_lexeme = ""
            self.not_keyword_flag = False
            return

    def process_operator(self):
        if self.current_char == "=":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "=":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == "!":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "=":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == "<":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "=":
                self.current_lexeme += self.current_char
            elif self.current_char == "<":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == ">":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "=":
                self.current_lexeme += self.current_char
            elif self.current_char == ">":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == "&":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "&":
                self.current_lexeme += self.current_char
            else:
                self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} is not a recognized character.")
                self.current_lexeme = ""
                self.retreat()
                return False
        elif self.current_char == "|":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "|":
                self.current_lexeme += self.current_char
            else:
                self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} is not a recognized character.")
                self.current_lexeme = ""
                self.retreat()
                return False
        elif self.current_char == "+":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "+":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == "-":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "-":
                self.current_lexeme += self.current_char
            elif self.current_char.isdigit():
                self.process_digit()
                return
            else:
                self.retreat()
        elif self.current_char == "*":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == "*":
                self.current_lexeme += self.current_char
            else:
                self.retreat()
        elif self.current_char == "/":
            self.current_lexeme += self.current_char
        elif self.current_char == "%":
            self.current_lexeme += self.current_char
        elif self.current_char == "~":
            self.current_lexeme += self.current_char

        self.advance()
        if self.current_char in Resources.WordSymbolDelims[self.current_lexeme]:
            self.Tokens.append([self.current_lexeme, self.current_lexeme])
            self.retreat()
        else:
            self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
        self.current_lexeme = ""
        return

    def process_digit(self):
        sign = ""
        if self.current_lexeme == "-":
            sign = "-"
            self.current_lexeme = ""

        if self.current_char == '0':
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char in Resources.Sun_delim:
                self.current_lexeme = sign + self.current_lexeme # Remove this line if unsigned zero is preferred.
                self.Tokens.append([self.current_lexeme, "SunLiteral"])
                self.current_lexeme = ""
                self.retreat()
                return
            if self.current_char in Resources.Period:
                self.advance()
                if self.current_char in Resources.DigitsWithZero:
                    self.retreat()
                    self.process_luhman(sign)
                    return
            else:
                self.Errors.append(
                    f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                self.current_lexeme = ""
                return
        else:
            self.retreat()

        while True:
            self.advance()
            if len(self.current_lexeme) == 10 and self.current_char in Resources.DigitsWithZero:
                self.Errors.append(
                    f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                self.current_lexeme = ""
                self.retreat()
                return
            elif len(self.current_lexeme) <= 10 and self.current_char == Resources.Period[0]:
                self.process_luhman(sign)
                return
            elif self.current_char not in Resources.DigitsWithZero:
                self.current_lexeme = sign + self.current_lexeme
                if self.current_char in Resources.Sun_delim:
                    self.Tokens.append([self.current_lexeme, "SunLiteral"])
                    self.current_lexeme = ""
                    self.retreat()
                    return
                else:
                    self.Errors.append(
                        f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                self.current_lexeme = ""
                return
            elif self.current_char in Resources.DigitsWithZero:
                self.current_lexeme += self.current_char

    def process_luhman(self, sign):
        self.current_lexeme += self.current_char
        count = len(self.current_lexeme)

        while True:
            self.advance()
            if (len(self.current_lexeme) - count) == 5 and self.current_char in Resources.DigitsWithZero:
                self.Errors.append(
                    f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                self.current_lexeme = ""
                return
            elif self.current_char not in Resources.DigitsWithZero:
                self.current_lexeme = sign + self.current_lexeme
                if self.current_char in Resources.Luhman_delim:
                    if self.current_lexeme[-1] == '0':
                        self.retreat()
                        self.retreat()
                        if self.current_char in Resources.Period:
                            self.Tokens.append([self.current_lexeme, "LuhmanLiteral"])
                            self.current_lexeme = ""
                            self.advance()
                            return
                        else:
                            self.advance()
                            self.advance()
                        self.Errors.append(
                            f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                        self.current_lexeme = ""
                        return
                    else:
                        self.Tokens.append([self.current_lexeme, "LuhmanLiteral"])
                        self.current_lexeme = ""
                        self.retreat()
                        return
                else:
                    if self.current_lexeme[-1] == Resources.Period[0]:
                        self.Errors.append(
                            f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                    else:
                        self.Errors.append(
                            f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(sign + self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                    self.current_lexeme = ""
                    return
            elif self.current_char in Resources.DigitsWithZero:
                self.current_lexeme += self.current_char
    def process_punctuator(self):
        if self.current_char == "(":
            self.current_lexeme += self.current_char
        elif self.current_char == ")":
            self.current_lexeme += self.current_char
        elif self.current_char == "{":
            self.current_lexeme += self.current_char
        elif self.current_char == "}":
            self.current_lexeme += self.current_char
        elif self.current_char == "[":
            self.current_lexeme += self.current_char
        elif self.current_char == "]":
            self.current_lexeme += self.current_char
        elif self.current_char == ",":
            self.current_lexeme += self.current_char
        elif self.current_char == ".":
            self.current_lexeme += self.current_char
        elif self.current_char == ":":
            self.current_lexeme += self.current_char
            self.advance()
            if self.current_char == ":":
                self.current_lexeme += self.current_char
            else:
                self.retreat()

        self.advance()
        if self.current_char in Resources.WordSymbolDelims[self.current_lexeme]:
            self.Tokens.append([self.current_lexeme, self.current_lexeme])
            self.retreat()
        else:
            self.Errors.append(f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
        self.current_lexeme = ""
        return

    def process_terminator(self):
        if self.current_char == "#":
            self.current_lexeme += "#"

        self.advance()
        if self.current_char in Resources.WordSymbolDelims[self.current_lexeme]:
            self.Tokens.append([self.current_lexeme, self.current_lexeme])
            self.retreat()
        else:
            self.Errors.append(
                f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
        self.current_lexeme = ""
        return

    #####################################################################################################################
    def process_comment(self):
        if self.current_char == "$" and self.sl_com_flag is False:
            self.sl_com_flag = True

        while (self.sl_com_flag is True and self.current_char is not None) and self.current_char != "\n":
            if self.current_char in Resources.PrintableChar or self.current_char == "\t":
                self.current_lexeme += self.current_char
                self.advance()

        if self.current_char is None:
            self.Errors.append(
                f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
            self.current_lexeme = ""
            self.sl_com_flag = False
            return
        elif self.current_char == "\n":
            self.current_lexeme = ""
            self.sl_com_flag = False
            self.retreat()
            return

    def process_space(self):
        if self.current_char == Resources.Space[0]:
            self.Tokens.append(["Space", "Space"])
            self.current_lexeme = ""
            return

    def process_newline(self):
        if self.current_char == "\n":
            self.current_lexeme += self.current_char
            self.Tokens.append([self.current_lexeme, "\n"])
            self.current_lexeme = ""
            return

    def process_tab(self):
        if self.current_char == "\t":
            self.current_lexeme += self.current_char
            self.Tokens.append([self.current_lexeme, "\t"])
            self.current_lexeme = ""
            return

    def process_starsys(self):
        if self.starsys_flag is False:
            if self.current_char == "\'":
                self.current_lexeme += "\'"
            elif self.current_char == "\"":
                self.current_lexeme += "\""
            self.starsys_flag = True
            return
        elif self.starsys_flag is True and self.current_char is not None:
            while self.current_char in Resources.PrintableChar or self.current_char == "\t" or self.current_char == "\n":
                if (self.current_lexeme[0] == "\"" and self.current_char == "\"") or (self.current_lexeme[0] == "\'" and self.current_char == "\'"):
                    self.current_lexeme += self.current_char
                    self.advance()
                    if self.current_char in Resources.Starsys_delim:
                        self.Tokens.append([self.current_lexeme, "StarsysLiteral"])
                        self.current_lexeme = ""
                        self.starsys_flag = False
                        self.retreat()
                        return
                    else:
                        self.Errors.append(
                            f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
                        self.current_lexeme = ""
                        self.starsys_flag = False
                        return

                elif self.current_char in Resources.PrintableChar or (self.current_char == "\t" or self.current_char == "\n"):
                    if self.current_char == "\n":
                        self.current_lexeme += "\n"
                        return
                    elif self.current_char == "\t":
                        self.current_lexeme += "\t"
                        return
                    else:
                        self.current_lexeme += self.current_char
                self.advance()

        elif self.starsys_flag is True and (self.line_num == len(self.lines) and self.current_char is None):
            self.Errors.append(
                f"(Line {self.line_num}, Column {self.column_num}) | Lexical Error: {repr(self.current_lexeme)} has invalid delimiter {repr(self.current_char)}.")
            self.current_lexeme = ""
            self.starsys_flag = False
            return


            
def read_text(source):
    # Checks if passed argument is a file, if it is, read it.
    if (os.path.isfile(source)):
        contents = open(source, "r").read() 
    # else passed contents are string. This if else is needed to accommodate the if name below of passing a file, and the passing of string arguments from the .get of inputext in the widget texteditor in the compiler tkinter ui.
    else:
        contents = source
    lexer_instance = Lexer(contents)
    errors, tokens = lexer_instance.split_content_into_lines()
    return errors, tokens


if __name__ == "__main__":
    errors, tokens = read_text('StellarSynth')
    print(errors, tokens)

"""
Algorithm:

Split Content into Lines
Split Lines into Line
Read Each self.current_character of a Line
Perform Operations on CurLexeme based on Conditions

"""
