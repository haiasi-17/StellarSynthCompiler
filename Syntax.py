import re
import Resources

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.errors = []
        self.current_lexeme = None
        self.current_token = None
        self.function_is_defined = False

    #  method that peeks at the next token after the current_token
    def peek_next_token(self):
        next_index = self.current_token_index
        #  spaces, newlines, indentations does not affect the syntax of the program
        while (next_index < len(self.tokens) and
               self.tokens[next_index][1] in ["Space","\n", "\t"]):
            next_index += 1
        if next_index < len(self.tokens):
            return self.tokens[next_index][1]
        else:
            return None

    #  method that gets the next token after a token matched (via match method)
    def get_next_token(self):
        #  spaces, newlines, indentations does not affect the syntax of the program
        while (self.current_token_index < len(self.tokens) and
               self.tokens[self.current_token_index][1] in ["Space","\n", "\t"]):
            self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_lexeme, self.current_token = self.tokens[self.current_token_index]
            self.current_token_index += 1
        else:
            self.current_lexeme, self.current_token = None, None

    #  method that peeks at the previous token
    def peek_previous_token(self):
        previous_index = self.current_token_index - 1  # Adjust to the previous index
        # Skip spaces, newlines, and indentations
        while (previous_index >= 0 and
               self.tokens[previous_index][1] in ["Space", "\n", "\t"]):
            previous_index -= 1
        if 0 <= previous_index < len(self.tokens):
            return self.tokens[previous_index][1]
        else:
            return None

    #  method that analyzes if the current token is matched with the expected token
    def match(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if self.current_token is not None:
            if isinstance(expected_token, list):
                # If the expected token is a list, check if the current token matches any in the list
                if re.match(r'Identifier\d*$', self.current_token) or self.current_token in expected_token:
                    return True
                else:
                    self.errors.append(
                        f"Syntax error: Expected one of {expected_token} but found '{self.current_token}'")
                    return False
            if self.current_token == expected_token:
                return True
            elif expected_token == "Identifier" and re.match(r'Identifier\d*$', self.current_token):
                return True  # Allow matching "Identifier" regardless of the count
            else:
                self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
                return False
        else:
            self.errors.append("Syntax error: Unexpected end of input")
            return False

    #  method that handles multiple identifiers separated with comma
    def matchID_mult(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "Identifier" and re.match(r'Identifier\d*$', self.current_token):
            #  if the next is a comma proceed to check if it is followed by an identifier
            if self.peek_next_token() == ",":
                self.match(",")
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.matchID_mult("Identifier")
                # else: if it is not followed by an id, it shows the error
                else:
                    self.errors.append(f"Syntax error: Expected 'Identifier', '#', '=' "
                                       f"after '{self.peek_previous_token()}'")
            else:
                return True  # else: last identifier has no following identifiers (comma)
        else:
            self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
            return False

    #  method that handles output statement
    def match_output(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "<<":
            if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                  or "StarsysLiteral" or "True" or "False"):
                self.match(Resources.Value1)  # consume
                #  if the next is a '<<' proceed to check if it is followed by any of the given values
                if self.peek_next_token() == "<<":
                    self.match_output("<<")
                #  add display value
                elif self.peek_next_token() == "+":
                    self.match_mathop2("+")
                    if self.peek_next_token() == "<<":
                        self.match_output("<<")
                    elif self.peek_next_token() == "#":
                        return True  # terminate
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '#', '<<' but found '{self.current_token}'")
                #  subtract display value
                elif self.peek_next_token() == "-":
                    self.match_mathop2("-")
                    if self.peek_next_token() == "<<":
                        self.match_output("<<")
                    elif self.peek_next_token() == "#":
                        return True  # terminate
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '#', '<<' but found '{self.current_token}'")
                #  multiply display value
                elif self.peek_next_token() == "*":
                    self.match_mathop2("*")
                    if self.peek_next_token() == "<<":
                        self.match_output("<<")
                    elif self.peek_next_token() == "#":
                        return True  # terminate
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '#', '<<' but found '{self.current_token}'")
                #  divide display value
                elif self.peek_next_token() == "/":
                    self.match_mathop2("/")
                    if self.peek_next_token() == "<<":
                        self.match_output("<<")
                    elif self.peek_next_token() == "#":
                        return True  # terminate
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '#', '<<' but found '{self.current_token}'")
                #  modulo display value
                elif self.peek_next_token() == "%":
                    self.match_mathop2("%")
                    if self.peek_next_token() == "<<":
                        self.match_output("<<")
                    elif self.peek_next_token() == "#":
                        return True  # terminate
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '#', '<<' but found '{self.current_token}'")
                else:
                    return True  # else: last identifier has no following '<<' to display
            else:
                self.errors.append(f"Syntax error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral',"
                                   f" 'StarsysLiteral', 'True', 'False' but found '{self.peek_next_token()}'")
                return False

    #  method that handles input statement
    def match_input(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == ">>":
            if (re.match(r'Identifier\d*$', self.peek_next_token())):
                self.match("Identifier")  # consume
                #  if the next is a '>>' proceed to check if it is followed by an identifier
                if self.peek_next_token() == ">>":
                    self.match_input(">>")
                else:
                    return True  # else: last identifier has no following '>>' to display
            else:
                self.errors.append(f"Syntax error: Expected 'Identifier' but found '{self.peek_next_token()}'")
                return False

    #  method that handles condition
    def match_condition(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "(":
            if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                  or "StarsysLiteral" or "True" or "False"):
                self.match(Resources.Value1)  # consume terms
                #  if the next is a conditional operator, proceed to check if it is followed by the following values
                if (self.peek_next_token() == "==" or self.peek_next_token() == "!=" or self.peek_next_token() == "<"
                        or self.peek_next_token() == ">" or self.peek_next_token() == "<=" or self.peek_next_token() == ">="
                        or self.peek_next_token() == "||" or self.peek_next_token() == "&&" or self.peek_next_token() == "!"):
                    self.match(Resources.condop)
                    if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                            or "StarsysLiteral" or "True" or "False"):
                        self.match(Resources.Value1)
                        #  more values
                        #  if the next is a conditional operator, proceed to check if it is followed by the following values
                        if (
                            self.peek_next_token() == "==" or self.peek_next_token() == "!=" or self.peek_next_token() == "<"
                            or self.peek_next_token() == ">" or self.peek_next_token() == "<=" or self.peek_next_token() == ">="
                            or self.peek_next_token() == "||" or self.peek_next_token() == "&&" or self.peek_next_token() == "!"):
                            self.match(Resources.condop)
                            #  must be followed by these values
                            if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                                    or "StarsysLiteral" or "True" or "False"):
                                self.match_mult_condition(Resources.Value1) #  assign multiple values
                                if self.peek_next_token() == ")":
                                    return True
                                #  not closed with ')' or followed by a conditional operator
                                else:
                                    self.errors.append(f"Syntax error: Expected ')', '==', '!=', '<', '>', "
                                                       f"'<=', '>=', '&&', '||', '!' but found '{self.peek_next_token()}'")
                            #  not followed by any of the values expected after a condition operator
                            else:
                                self.errors.append(f"Syntax error: Expected 'Identifier', 'SunLiteral', "
                                                   f"'LuhmanLiteral', 'True', 'False' but found '{self.peek_next_token()}'")
                        #  single value
                        if self.peek_next_token() == ")":
                            return True  # else: last identifier has no following '>>' to display
                        #  not closed with ')' or followed by a conditional operator
                        else:
                            self.errors.append(f"Syntax error: Expected ')', '==', '!=', '<', '>', "
                                           f"'<=', '>=', '&&', '||', '!' but found '{self.peek_next_token()}'")
                    #  not followed by any of the values expected after a condition operator
                    else:
                        self.errors.append(f"Syntax error: Expected 'Identifier', 'SunLiteral', "
                                           f"'LuhmanLiteral', 'True', 'False' but found '{self.peek_next_token()}'")
                #  single value
                elif self.peek_next_token() == ")":
                    return True  # else: last identifier has no following '>>' to display
                #  not closed with ')' or followed by a conditional operator
                else:
                    self.errors.append(f"Syntax error: Expected ')', '==', '!=', '<', '>', "
                                       f"'<=', '>=', '&&', '||', '!' but found '{self.peek_next_token()}'")
            # empty condition error
            else:
                self.errors.append(f"Syntax error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral'"
                                   f", 'StarsysLiteral', 'True', 'False' but found '{self.peek_next_token()}'")
                return False

    #  method that analyzes if the current token is matched with the expected token
    def match_mult_condition(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if isinstance(expected_token, list):
            if (re.match(r'Identifier\d*$', self.current_token) or "SunLiteral" or "LuhmanLiteral"
                    or "StarsysLiteral" or "True" or "False"):
                #  if the next is a conditional operator, proceed to check if it is followed by the following values
                if (
                        self.peek_next_token() == "==" or self.peek_next_token() == "!=" or self.peek_next_token() == "<"
                        or self.peek_next_token() == ">" or self.peek_next_token() == "<=" or self.peek_next_token() == ">="
                        or self.peek_next_token() == "||" or self.peek_next_token() == "&&" or self.peek_next_token() == "!"):
                    self.match(Resources.condop)
                    #  another conditional value
                    if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                            or "StarsysLiteral" or "True" or "False"):
                        self.match_mult_condition(Resources.Value1)
                    #  not followed by a value
                    else:
                        self.errors.append(f"Syntax error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral'"
                                           f", 'StarsysLiteral', 'True', 'False' but found '{self.peek_next_token()}'")
                #  not followed by a conditional operator
                else:
                    return True



    def match_param_assign_mult(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == ",":
            #  if the next is a comma proceed to check if it is followed by Static
            if self.peek_next_token() == "Static":
                self.match("Static")
                #  if the next is a Static proceed to check if it is followed by data type
                if self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman"\
                        or self.peek_next_token() == "Starsys" or self.peek_next_token() == "Boolean":
                    self.match(Resources.Datatype2)
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")
                        if self.peek_next_token() == ",":
                            self.match_param_assign_mult(",")
                        elif self.peek_next_token() == "=":
                            self.match_param_assign("=")
                        #  no assign value (=) or next value (comma)
                        #  no more assigned values
                        elif self.peek_next_token() == ")":
                            return True
                        #  not closed with ')' or followed by any...
                        else:
                            self.errors.append(f"Syntax Error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                    # else: if it is not followed by an id, it shows the error
                    else:
                        self.errors.append(f"Syntax error: Expected 'Identifier', "
                                           f"after '{self.peek_previous_token()}'")
                #  no datatype
                else:
                    self.errors.append(f"Syntax error: Expected 'Sun', 'Luhman', 'Starsys', 'Boolean' "
                                       f"after '{self.peek_previous_token()}'")
            #  else if the next is a comma proceed to check if it is followed by data type
            elif self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman" \
                    or self.peek_next_token() == "Starsys" or self.peek_next_token() == "Boolean":
                self.match(Resources.Datatype2)
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.match("Identifier")
                    if self.peek_next_token() == ",":
                        self.match_param_assign_mult(",")
                    elif self.peek_next_token() == "=":
                        self.match_param_assign("=")
                    #  no assign value (=) or next value (comma)
                    #  no more assigned values
                    elif self.peek_next_token() == ")":
                        return True
                    #  not closed with ')' or followed by any...
                    else:
                        self.errors.append(
                                    f"Syntax Error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                # else: if it is not followed by an id, it shows the error
                else:
                    self.errors.append(f"Syntax error: Expected 'Identifier', "
                                               f"after '{self.peek_previous_token()}'")
            #  no datatype
            else:
                self.errors.append(f"Syntax error: Expected 'Static', 'Sun', 'Luhman', 'Starsys', 'Boolean' "
                                           f"after '{self.peek_previous_token()}'")
        else:
            self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
            return False

    #  method for assigning parameter with values
    def match_param_assign(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "=":
            # check if it is enclosed with parentheses
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected '#', '+', '-', '*', '/', '%', '**'")
            #  check if it is followed by these values
            elif (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                    or "StarsysLiteral" or "True" or "False"):
                self.match(Resources.Value1)
                #  followed by a comma to add another
                if self.peek_next_token() == ",":
                    self.match_param_assign_mult(",")
                    #  no more assigned values
                    if self.peek_next_token() == ")":
                        return True
                    #  not closed with ')'
                    else:
                        self.errors.append(f"Syntax Error: Expected ')' after {self.peek_previous_token()}")
                #  add is next
                elif self.peek_next_token() == "+":
                    self.match_mathop_param("+")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                #  exponentiation is next
                elif self.peek_next_token() == "**":
                    self.match_exponent_param("**")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop_param("-")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop_param("*")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop_param("/")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop_param("%")
                    if self.peek_next_token() == ")":
                        return True  # else: last identifier has no following identifiers (comma)
                    #  unexpected end
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
                elif self.peek_next_token() == ")":
                    return True  # else: last identifier has no following identifiers (comma)
                #  unexpected end
                else:
                    self.errors.append(
                        f"Syntax error: Expected ')', '+', '=', '-', '/', '%', '*', ',' after '{self.peek_previous_token()}'")
            #  else: if it is not followed by any of the value it shows the error
            else:
                self.errors.append(
                    f"Syntax error: Expected '{expected_token}' after '{self.peek_previous_token()}'")
        #  else: no equals sign
        else:
            self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
            return False

    # method for parsing multiple variable assignments with expression
    def match_mathop_param(self, expected_token):
        if (self.peek_previous_token() != "SunLiteral" and self.peek_previous_token() != "LuhmanLiteral"
                and self.peek_previous_token() != ")" and not re.match(r'Identifier\d*$', self.peek_previous_token())):
            self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral' before {self.peek_next_token()}")

        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        # check if it is enclosed with parentheses
        if expected_token == "+" or "-" or "*" or "/" or "%":
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or self.peek_next_token() == "SunLiteral"
                    or self.peek_next_token() == "LuhmanLiteral"):
                self.match(Resources.Value2)  # consume
                #  add
                if self.peek_next_token() == "+":
                    self.match_mathop_param("+")
                #  exponent
                elif self.peek_next_token() == "**":
                    self.match_exponent_param("**")
                #  subtract
                elif self.peek_next_token() == "-":
                    self.match_mathop_param("-")
                #  multiply
                elif self.peek_next_token() == "*":
                    self.match_mathop_param("*")
                #  divide
                elif self.peek_next_token() == "/":
                    self.match_mathop_param("/")
                #  modulo
                elif self.peek_next_token() == "%":
                    self.match_mathop_param("%")
                #  another variable separated with comma
                elif self.peek_next_token() == ",":
                    self.match_param_assign_mult(",")  # consume ','
                else:
                    return True
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                       f" after {self.peek_previous_token()}")

    #  method that handles multiple assigning values. ex: a = 12, b = 12, c = 12
    def match_mult_assign(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "=":
            # check if it is enclosed with parentheses
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected '#', '+', '-', '*', '/', '%', '**'")
            #  check if it is followed by these values:
            elif re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral" or "StarsysLiteral":
                self.match(Resources.Value)
                if self.peek_next_token() == ",":
                    self.match(",")
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.matchID_mult("Identifier")
                        if self.peek_next_token() == "=":
                            self.match_mult_assign("=")
                        else:
                            return True  # else: last identifier has no assigned value (=)
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '{expected_token}' after '{self.peek_previous_token()}'")
                #  add is next
                elif self.peek_next_token() == "+":
                    self.match_mathop("+")
                #  exponentiation is next
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop("%")
                else:
                    return True  # else: last identifier has no following identifiers (comma)
            #  else: if it is not followed by any of the value it shows the error
            else:
                self.errors.append(
                    f"Syntax error: Expected '{expected_token}' after '{self.peek_previous_token()}'")
        #  else: no equals sign
        else:
            self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
            return False

    #  method for Autom declaration
    def match_auto_assign(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "=":
            # check if it is enclosed with parentheses
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected '#', '+', '-', '*', '/', '%', '**'")
            #  check if it is followed by these values
            if (re.match(r'Identifier\d*$', self.peek_next_token()) or "SunLiteral" or "LuhmanLiteral"
                    or "StarsysLiteral" or "True" or "False") :
                self.match(Resources.Value1)
                if self.peek_next_token() == ",":
                    self.match(",")
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")  # consume Identifier
                        if self.peek_next_token() == "=":
                            self.match_auto_assign("=")  # Autom Path
                        else:
                            self.errors.append(f"Syntax Error: Expected {expected_token} after {self.peek_previous_token()}")# else: last identifier has no assigned value (=)
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '{expected_token}' after '{self.peek_previous_token()}'")
                #  add is next
                elif self.peek_next_token() == "+":
                    self.match_mathop("+")
                #  exponentiation is next
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop("%")
                else:
                    return True  # else: last identifier has no following identifiers (comma)
            #  else: if it is not followed by any of the value it shows the error
            else:
                self.errors.append(
                    f"Syntax error: Expected '{expected_token}' after '{self.peek_previous_token()}'")
        #  else: no equals sign
        else:
            self.errors.append(f"Syntax error: Expected '{expected_token}' but found '{self.current_token}'")
            return False

    # method for parsing multiple variable assignments with expression
    def match_mathop(self, expected_token):
        if (self.peek_previous_token() != "SunLiteral" and self.peek_previous_token() != "LuhmanLiteral"
                and self.peek_previous_token() != ")" and not re.match(r'Identifier\d*$', self.peek_previous_token())):
            self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral' before {self.peek_next_token()}")

        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        # check if it is enclosed with parentheses
        if expected_token == "+" or "-" or "*" or "/" or "%":
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or self.peek_next_token() == "SunLiteral"
                    or self.peek_next_token() == "LuhmanLiteral"):
                self.match(Resources.Value2)  # consume
                #  add
                if self.peek_next_token() == "+":
                    self.match_mathop("+")
                #  exponent
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                #  subtract
                elif self.peek_next_token() == "-":
                    self.match_mathop("-")
                #  multiply
                elif self.peek_next_token() == "*":
                    self.match_mathop("*")
                #  divide
                elif self.peek_next_token() == "/":
                    self.match_mathop("/")
                #  modulo
                elif self.peek_next_token() == "%":
                    self.match_mathop("%")
                #  another variable separated with comma
                elif self.peek_next_token() == ",":
                    self.match(",")  # consume ','
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")
                        if self.peek_next_token() == "=":
                            self.match_mult_assign("=")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                            f" after {self.peek_previous_token()}")
                else:
                    return True
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                       f" after {self.peek_previous_token()}")

    #  method for handling expression inside a parentheses
    def match_mathop2(self, expected_token):
        if (self.peek_previous_token() != "SunLiteral" and self.peek_previous_token() != "LuhmanLiteral"
                and not re.match(r'Identifier\d*$', self.peek_previous_token())):
            self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral' before {self.peek_next_token()}")

        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "+" or "-" or "*" or "/" or "%":
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected ')'")
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral" or "LuhmanLiteral"):
                self.match(Resources.Value2)  # consume
                if self.peek_next_token() == "+":
                    self.match_mathop2("+")  # consume
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop2("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop2("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop2("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop2("%")
                else:
                    return True
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                       f" after {self.peek_previous_token()}")

    # expr for array size
    def match_mathop3(self, expected_token):
        if (self.peek_previous_token() != "SunLiteral" and not
                re.match(r'Identifier\d*$', self.peek_previous_token())):
            self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral' before {self.peek_next_token()}")

        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "+" or "-" or "*" or "/" or "%":
            if self.peek_next_token() == "(":
                self.match_parenth("(")
                if self.peek_previous_token() == ")":
                    return True
                else:
                    self.errors.append(f"Syntax Error: Expected ')'")
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral"):
                self.match(Resources.Value3)  # consume
                if self.peek_next_token() == "+":
                    self.match_mathop3("+")  # consume
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop3("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop3("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop3("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop3("%")
                else:
                    return True
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', "
                                       f" after {self.peek_previous_token()}")

    #  method for values in a parentheses
    def match_parenth(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "(":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral" or "LuhmanLiteral"):
                self.match(Resources.Value2)  # consume
                # add it
                if self.peek_next_token() == "+":
                    self.match_mathop2("+")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        #  add is next
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                        #  subtract is next
                        elif self.peek_next_token() == "-":
                            self.match_mathop("-")
                        #  multiply is next
                        elif self.peek_next_token() == "*":
                            self.match_mathop("*")
                        #  divide is next
                        elif self.peek_next_token() == "/":
                            self.match_mathop("/")
                        #  modulo is next
                        elif self.peek_next_token() == "%":
                            self.match_mathop("%")
                        #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                    self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                           f" after {self.peek_previous_token()}")
                #  exponentiate
                elif self.peek_next_token() == "**":
                    self.match_exponent("**")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                            #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                    self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                           f" after {self.peek_previous_token()}")
                # subtract it
                elif self.peek_next_token() == "-":
                    self.match_mathop2("-")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        #  add is next
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                        #  subtract is next
                        elif self.peek_next_token() == "-":
                            self.match_mathop("-")
                        #  multiply is next
                        elif self.peek_next_token() == "*":
                            self.match_mathop("*")
                        #  divide is next
                        elif self.peek_next_token() == "/":
                            self.match_mathop("/")
                        #  modulo is next
                        elif self.peek_next_token() == "%":
                            self.match_mathop("%")
                        #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                        self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                                f" after {self.peek_previous_token()}")
                # multiply it
                elif self.peek_next_token() == "*":
                    self.match_mathop2("*")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        #  add is next
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                        #  subtract is next
                        elif self.peek_next_token() == "-":
                            self.match_mathop("-")
                        #  multiply is next
                        elif self.peek_next_token() == "*":
                            self.match_mathop("*")
                        #  divide is next
                        elif self.peek_next_token() == "/":
                            self.match_mathop("/")
                        #  modulo is next
                        elif self.peek_next_token() == "%":
                            self.match_mathop("%")
                        #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                        self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                                f" after {self.peek_previous_token()}")
                # divide it
                elif self.peek_next_token() == "/":
                    self.match_mathop2("/")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        #  add is next
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                        #  subtract is next
                        elif self.peek_next_token() == "-":
                            self.match_mathop("-")
                        #  multiply is next
                        elif self.peek_next_token() == "*":
                            self.match_mathop("*")
                        #  divide is next
                        elif self.peek_next_token() == "/":
                            self.match_mathop("/")
                        #  modulo is next
                        elif self.peek_next_token() == "%":
                            self.match_mathop("%")
                        #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                        self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                                f" after {self.peek_previous_token()}")
                # modulo
                elif self.peek_next_token() == "%":
                    self.match_mathop2("%")
                    if self.peek_next_token() == ")":
                        self.match(")")  # consume
                        #  add is next
                        if self.peek_next_token() == "+":
                            self.match_mathop("+")
                        #  subtract is next
                        elif self.peek_next_token() == "-":
                            self.match_mathop("-")
                        #  multiply is next
                        elif self.peek_next_token() == "*":
                            self.match_mathop("*")
                        #  divide is next
                        elif self.peek_next_token() == "/":
                            self.match_mathop("/")
                        #  modulo is next
                        elif self.peek_next_token() == "%":
                            self.match_mathop("%")
                        #  next value asisgn
                        elif self.peek_next_token() == ",":
                            self.match(",")  # consume ','
                            if re.match(r'Identifier\d*$', self.peek_next_token()):
                                self.match("Identifier")
                                if self.peek_next_token() == "=":
                                        self.match_mult_assign("=")
                                else:
                                    return True
                            else:
                                self.errors.append(
                                    f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                    f" after {self.peek_previous_token()}")
                        else:
                            return True
                    else:
                        self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', '%' "
                                                f" after {self.peek_previous_token()}")
                #  close it with Rparenth
                elif self.peek_next_token() == ")":
                    self.match(")")
                    if self.peek_next_token() == "+":
                        self.match_mathop("+")
                    #  next value asisgn
                    elif self.peek_next_token() == ",":
                        self.match(",")  # consume ','
                        if re.match(r'Identifier\d*$', self.peek_next_token()):
                            self.match("Identifier")
                            if self.peek_next_token() == "=":
                                self.match_mult_assign("=")
                            else:
                                return True
                        else:
                            self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                               f" after {self.peek_previous_token()}")
                    else:
                        return True
                else:
                    self.errors.append(f"Syntax Error: Expected '+', '-', '*', '/', "
                                       f" after {self.peek_previous_token()}")

            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier', 'SunLiteral', 'LuhmanLiteral', "
                                       f" after {self.peek_previous_token()}")

    #  method if it is an exponentiation
    def match_exponent_param(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "**":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral" or "LuhmanLiteral"):
                self.match(Resources.Value2)
                # add is next
                if self.peek_next_token() == "+":
                    self.match_mathop_param("+")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop_param("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop_param("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop_param("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop_param("%")
                #  another variable separated with comma
                elif self.peek_next_token() == ",":
                    self.match_param_assign_mult(",")  # consume ','
                else:
                    return True  # terminate
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier' after {self.peek_previous_token()}")

    #  method if it is an exponentiation
    def match_exponent(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "**":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral" or "LuhmanLiteral"):
                self.match(Resources.Value2)
                # add is next
                if self.peek_next_token() == "+":
                    self.match_mathop("+")
                #  subtract is next
                elif self.peek_next_token() == "-":
                    self.match_mathop("-")
                #  multiply is next
                elif self.peek_next_token() == "*":
                    self.match_mathop("*")
                #  divide is next
                elif self.peek_next_token() == "/":
                    self.match_mathop("/")
                #  modulo is next
                elif self.peek_next_token() == "%":
                    self.match_mathop("%")
                #  another variable separated with comma
                elif self.peek_next_token() == ",":
                    self.match(",")  # consume ','
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")
                        if self.peek_next_token() == "=":
                            self.match_mult_assign("=")
                        else:
                            return True  # terminate
                else:
                    return True  # terminate
            else:
                self.errors.append(f"Syntax Error: Expected 'Identifier' after {self.peek_previous_token()}")

    #  method to match if it is an array dec
    def match_arr_dec(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "{":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or self.peek_next_token() == "SunLiteral"):
                self.match(Resources.Value3) # consume the values
                if self.peek_next_token() == "+":
                    self.match_mathop3("+")  # size is a math expr
                    #  close it with "}" if size is fulfilled
                    if self.peek_next_token() == "}":
                        self.match("}")
                        # declare an array only
                        if self.peek_next_token() == "#":
                            self.match("#")
                        #  assign value to the declared array
                        # assign a value syntax for 1D array if followed by an equal after '}'
                        elif self.peek_next_token() == "=":
                            self.match("=")
                            # it must be followed by '['
                            if self.peek_next_token() == "[":
                                self.match_arr_value("[")
                                # close it with ']' after assigning value/s
                                if self.peek_next_token() == "]":
                                    self.match("]")
                                    # terminate it
                                    if self.peek_next_token() == "#":
                                        self.match("#")
                                    # error, no terminator
                                    else:
                                        self.errors.append(
                                            f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
                                #  error if not closed with ']'
                                else:
                                    self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                            else:
                                self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
                        # add another size to become 2D array
                        elif self.peek_next_token() == "{":
                            self.match_arr_dec2d("{")
                        #  not terminated with # or followed by an '=' after Rcurl
                        else:
                            self.errors.append(
                                f"Syntax Error: Expected '#', '=', after {self.peek_previous_token()}")
                    #  not closed with '}'
                    else:
                        self.errors.append(
                            f"Syntax Error: Expected 'Rcurlbrace' after {self.peek_previous_token()}")
                #  size is single value
                elif self.peek_next_token() == "}":
                    self.match("}")
                    if self.peek_next_token() == "#":
                        self.match("#")
                    # add another size to become 2D array
                    elif self.peek_next_token() == "{":
                        self.match_arr_dec2d("{")
                    # assign a value syntax for 1D array if followed by an equal after '}'
                    elif self.peek_next_token() == "=":
                        self.match("=")
                        # it must be followed by '['
                        if self.peek_next_token() == "[":
                            self.match_arr_value("[")
                            # close it with ']' after assigning value/s
                            if self.peek_next_token() == "]":
                                self.match("]")
                                # terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                # error, no terminator
                                else:
                                    self.errors.append(
                                        f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
                            #  error if not closed with ']'
                            else:
                                self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                        #  not started with '[' after '='
                        else:
                            self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
                    #  not terminated with # or followed by an '=' after Rcurl
                    else:
                        self.errors.append(
                            f"Syntax Error: Expected '#', '=', after {self.peek_previous_token()}")
                #  size value is not followed by any of the following (# and Rcurl)
                else:
                    self.errors.append(
                        f"Syntax Error: Expected 'Rcurlbraces', '#', after {self.peek_previous_token()}")
            #  empty size, proceed to close it with '}'
            elif self.peek_next_token() == "}":
                self.match("}")
                # assign a value syntax for 1D array (empty size)
                if self.peek_next_token() == "=":
                    self.match("=")
                    # it must be followed by '['
                    if self.peek_next_token() == "[":
                        self.match_arr_value("[")
                        # close it with ']' after assigning value/s
                        if self.peek_next_token() == "]":
                            self.match("]")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            # error, no terminator
                            else:
                                self.errors.append(f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
                        #  error if not closed with ']'
                        else:
                            self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                    else:
                        self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
                # add another size to become 2D array
                elif self.peek_next_token() == "{":
                    self.match_arr_dec2d("{")
                # if it is terminated with '#'
                # or followed by anything other than '=' while being an empty size, it says an error
                else:
                    self.errors.append(f"Syntax Error: Expected '=', 'Lcurlybrace' after {self.peek_previous_token()}")
            else:
                self.errors.append(f"Expected 'Identifier', 'Sun', 'Rcurlybrace' but found {self.peek_next_token()}")
        else:
            self.errors.append(f"Expected {expected_token} but found {self.current_token}")

    def match_arr_dec2d(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "{":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or self.peek_next_token() == "SunLiteral"):
                self.match(Resources.Value3) # consume the values
                if self.peek_next_token() == "+":
                    self.match_mathop3("+")  # size is a math expr
                    #  close it with "}" if size is fulfilled
                    if self.peek_next_token() == "}":
                        self.match("}")
                        if self.peek_next_token() == "#":
                            self.match("#")  # declare an array only
                        #  assign value to the declared array
                        # assign a value syntax for 2D array if followed by an equal after '}'
                        elif self.peek_next_token() == "=":
                            self.match("=")
                            # it must be followed by '['
                            if self.peek_next_token() == "[":
                                self.match_arr_value2d("[")  # assign 2D values
                                # close it with ']' after assigning value/s
                                if self.peek_next_token() == "]":
                                    self.match("]")
                                    # terminate it
                                    if self.peek_next_token() == "#":
                                        self.match("#")
                                    # error, no terminator
                                    else:
                                        self.errors.append(
                                            f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
                                #  error if not closed with ']'
                                else:
                                    self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                            else:
                                self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
                        #  not terminated with # or followed by an '=' after Rcurl
                        else:
                            self.errors.append(
                                f"Syntax Error: Expected '#', '=', after {self.peek_previous_token()}")
                    #  not closed with '}'
                    else:
                        self.errors.append(
                            f"Syntax Error: Expected 'Rcurlbrace' after {self.peek_previous_token()}")
                #  size is single value
                elif self.peek_next_token() == "}":
                    self.match("}")
                    if self.peek_next_token() == "#":
                        self.match("#")
                    # assign a value syntax for 2D array if followed by an equal after '}'
                    elif self.peek_next_token() == "=":
                        self.match("=")
                        # it must be followed by '['
                        if self.peek_next_token() == "[":
                            self.match_arr_value2d("[")  # assign 2D values
                            # close it with ']' after assigning value/s
                            if self.peek_next_token() == "]":
                                self.match("]")
                                # terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                # error, no terminator
                                else:
                                    self.errors.append(
                                        f"Syntax Error: Expected '#' after {self.peek_previous_token()}")
                            #  error if not closed with ']'
                            else:
                                self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                        #  not started with '[' after '='
                        else:
                            self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
                    #  not terminated with # or followed by an '=' after Rcurl
                    else:
                        self.errors.append(
                            f"Syntax Error: Expected '#', '=', after {self.peek_previous_token()}")
                #  size value is not followed by any of the following (# and Rcurl)
                else:
                    self.errors.append(
                        f"Syntax Error: Expected 'Rcurlbraces', '#', after {self.peek_previous_token()}")
            else:
                self.errors.append(f"Expected 'Identifier', 'Sun', but found {self.peek_next_token()}")
        else:
            self.errors.append(f"Expected {expected_token} but found {self.current_token}")

    # value/s in a 1D array
    def match_arr_value(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == "[":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or self.peek_next_token() == "SunLiteral" or self.peek_next_token() == "LuhmanLiteral"
                    or self.peek_next_token() == "StarsysLiteral" or self.peek_next_token() == "True"
                    or self.peek_next_token() == "False"):
                self.match(Resources.Value1)
                if self.peek_next_token() == ",":
                    self.match_mult_arr_val(",")
                    if self.peek_next_token() == "]":
                        return True # no more values next so next should be closing with ']'
                    # error no ']' found
                    else:
                        self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                else:
                    return True  # single value
            else:
                return True  # empty value

    def match_arr_value2d(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()
        #  opening sqr brkt
        if expected_token == "[":
            #  opening sqr brkt again, for 2D assign value syntax
            if self.peek_next_token() == "[":
                self.match_arr_value("[") # assign values in that inner sqr brkt
                if self.peek_next_token() == "]":
                    self.match("]")   # close it if done assigning 1st 2D values
                    if self.peek_next_token() == "]":
                        return True  # terminate it, no more 2D values next
                    # multiple 2D array values
                    elif self.peek_next_token() == ",":
                        self.match_mult_arr2d_val(",")
                        if self.peek_next_token() == "]":
                            return True # multiple array 2D value is done
                        else:
                            self.errors.append(f"Syntax Error: Expected ']', after {self.peek_previous_token()}")
                    # unexpected next, should be ']' or ','
                    else:
                        self.errors.append(f"Syntax Error: Expected ']', ',' after {self.peek_previous_token()}")
                #  error: not closed with ']'
                else:
                    self.errors.append(f"Syntax Error: Expected ']', after {self.peek_previous_token()}")
            #  syntax: [[value]] not followed
            else:
                self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")

    # method for array multiple values
    def match_mult_arr_val(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == ",":
            if (re.match(r'Identifier\d*$', self.peek_next_token())
                    or "SunLiteral" or "LuhmanLiteral" or "StarsysLiteral" or "True" or "False"):
                self.match(Resources.Value1)
                if self.peek_next_token() == ",":
                    self.match_mult_arr_val(",")  # more values
                else:
                    return True  # else: last value has no following values (comma)

    def match_mult_arr2d_val(self, expected_token):
        self.get_next_token()
        while self.current_token == "Space":
            self.get_next_token()

        if expected_token == ",":
            if self.peek_next_token() == "[":
                self.match("[")
                if (re.match(r'Identifier\d*$', self.peek_next_token())
                        or "SunLiteral" or "LuhmanLiteral" or "StarsysLiteral" or "True" or "False"):
                    self.match(Resources.Value1)
                    if self.peek_next_token() == ",":
                        self.match_mult_arr_val(",")
                        if self.peek_next_token() == "]":
                            self.match("]")
                            if self.peek_next_token() == ",":
                                self.match_mult_arr2d_val(",") # more 2D values
                            else:
                                return True # no more 2D values to add
                        else:
                            self.errors.append(f"Syntax Error: Expected ']', after {self.peek_previous_token()}")
                    #  single value
                    elif self.peek_next_token() == "]":
                        self.match("]")
                        if self.peek_next_token() == ",":
                            self.match_mult_arr2d_val(",")  # more 2D values
                        else:
                            return True  # no more 2D values to add
                    else:
                        self.errors.append(f"Syntax Error: Expected ']', after {self.peek_previous_token()}")
                #  empty value
                elif self.peek_next_token() == "]":
                    self.match("]")
                    if self.peek_next_token() == ",":
                        self.match_mult_arr2d_val(",")  # more 2D values
                    else:
                        print("dito")
                        return True  # no more 2D values to add
                # unexpected end, expected ']'
                else:
                    self.errors.append(f"Syntax Error: Expected ']',  after {self.peek_previous_token()}")

    #  method that parse the import statement
    def parse_import_statement(self):
        while self.peek_next_token() in ["Import"]:
            if self.peek_next_token() == "Import":
                self.match("Import")

                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.matchID_mult("Identifier")
                    if self.peek_next_token() == "#":
                        self.match("#")
                    elif self.peek_next_token() == "~":  # proceed to tilde syntax
                        self.parse_import_statement1()
                    else:
                        self.errors.append(
                            f"Syntax error: Expected '~', 'comma', '#' after {self.peek_previous_token()}")
                else:
                    self.errors.append(f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            else:
                break


    #  method that also parse the import statement (tilde syntax)
    def parse_import_statement1(self):
        if self.peek_next_token() == "~":
            self.match("~")
            if re.match(r'Identifier\d*$', self.peek_next_token()):
                self.matchID_mult("Identifier")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Expected '#' after {self.peek_previous_token()}")
            else:
                self.errors.append(f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
        else:
            self.errors.append(f"Syntax error: Expected '~', ',' after {self.peek_previous_token()}")

    # method for parsing variable declarations (global)
    def parse_variable_declaration(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  is it an array declaration?
            if self.peek_next_token() == "{":
                self.match_arr_dec("{")
            #  is it a subfunction?
            elif self.peek_next_token() == "(":
                self.parse_sub_function_ptype()
            #  or assign value/s?
            elif self.peek_next_token() == "=":
                self.match_mult_assign("=")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Unexpected end with {self.peek_previous_token()}"
                                        f", expected '#'")
            #  terminate?
            elif self.peek_next_token() == "#":
                self.match("#")
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '#', '=', 'Identifier', 'SunLiteral', 'LuhmanLiteral', 'StarsysLiteral' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    # method for parsing variable declarations (local) or in functions
    def parse_variable_declaration_func(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  is it an array declaration?
            if self.peek_next_token() == "{":
                self.match_arr_dec("{")
            #  or assign value/s?
            elif self.peek_next_token() == "=":
                self.match_mult_assign("=")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Unexpected end with {self.peek_previous_token()}"
                                        f", expected '#'")
            #  terminate?
            elif self.peek_next_token() == "#":
                self.match("#")
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '#', '=', 'Identifier', 'SunLiteral', 'LuhmanLiteral', 'StarsysLiteral' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    #  method for parsing Autom variable declaration
    def parse_auto_dec(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  assign value/s?
            if self.peek_next_token() == "=":
                self.match_auto_assign("=")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Unexpected end with {self.peek_previous_token()}, expected '#'")
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '#', '=', 'Identifier','SunLiteral', "
                    f"'LuhmanLiteral', 'StarsysLiteral', 'True', 'False' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    #  method for parsing boolean var declarations (global)
    def parse_boolean(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  is it an array declaration?
            if self.peek_next_token() == "{":
                self.match_arr_dec("{")
            #  is it a subfunction?
            elif self.peek_next_token() == "(":
                self.parse_sub_function_ptype()
            #  or assign value/s?
            elif self.peek_next_token() == "=":
                self.match_auto_assign("=")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Unexpected end with {self.peek_previous_token()}"
                                       f", expected '#'")
            #  terminate?
            elif self.peek_next_token() == "#":
                self.match("#")
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '#', '=', 'Identifier', 'SunLiteral', 'LuhmanLiteral', 'StarsysLiteral' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    #  method for parsing boolean var declarations (local) or in functions
    def parse_boolean_func(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  is it an array declaration?
            if self.peek_next_token() == "{":
                self.match_arr_dec("{")
            #  or assign value/s?
            elif self.peek_next_token() == "=":
                self.match_auto_assign("=")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(f"Syntax error: Unexpected end with {self.peek_previous_token()}"
                                       f", expected '#'")
            #  terminate?
            elif self.peek_next_token() == "#":
                self.match("#")
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '#', '=', 'Identifier', 'SunLiteral', 'LuhmanLiteral', 'StarsysLiteral' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    # method for parsing void subfunc
    def parse_void_declaration(self):
        if re.match(r'Identifier\d*$', self.peek_next_token()):
            self.matchID_mult("Identifier")

            #  is it an void subfunc prototype?
            if self.peek_next_token() == "(":
                self.parse_sub_function_ptype_void()
            # error: missing any of the possibilities
            else:
                self.errors.append(
                    f"Syntax Error: Expected '(' "
                    f"after {self.peek_previous_token()}")
        #  error: no identifier after the datatype
        else:
            self.errors.append(
                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")

    # method for sub function prototype (void)
    def parse_sub_function_ptype_void(self):
        if self.peek_next_token() == "(":
            self.match("(")
            if self.peek_next_token() == "Static":
                self.match("Static")
                # has parameter path
                if (self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman"
                        or self.peek_next_token() == "Boolean" or self.peek_next_token() ==  "Starsys"):
                    self.match(Resources.Datatype2)
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")
                        if self.peek_next_token() == "=":
                            self.match_param_assign("=")
                            #  close with ')' after assigning value/s
                            if self.peek_next_token() == ")":
                                self.match(")")
                                #  terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                #  error: not terminated
                                else:
                                    self.errors.append(
                                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                            #  error: not closed
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected ')' after {self.peek_previous_token()}")
                        #  check: if closed, single id no value
                        elif self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  single id is followed by a comma
                        elif self.peek_next_token() == ",":
                            self.match_param_assign_mult(",")
                            #  close with ')' after assigning value/s
                            if self.peek_next_token() == ")":
                                self.match(")")
                                #  terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                #  error: not terminated
                                else:
                                    self.errors.append(
                                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  unexpected end: no ')' to close, or comma to followed by, or (=) to assign values
                        else:
                            self.errors.append(
                                f"Syntax error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                    #  error: no identifier after the datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                #  no datatype after static
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Sun', 'Luhman', 'Boolean', 'Starsys' after {self.peek_previous_token()}")
            # has parameter path
            elif (self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman"
                        or self.peek_next_token() == "Boolean" or self.peek_next_token() ==  "Starsys"):
                self.match(Resources.Datatype2)
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.match("Identifier")
                    if self.peek_next_token() == "=":
                        self.match_param_assign("=")
                        #  close with ')' after assigning value/s
                        if self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  error: not closed
                        else:
                            self.errors.append(
                                f"Syntax error: Expected ')' after {self.peek_previous_token()}")
                    #  check: if closed, single id no value
                    elif self.peek_next_token() == ")":
                        self.match(")")
                        #  terminate it
                        if self.peek_next_token() == "#":
                            self.match("#")
                        #  error: not terminated
                        else:
                            self.errors.append(
                                f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                    #  single id is followed by a comma
                    elif self.peek_next_token() == ",":
                        self.match_param_assign_mult(",")
                        #  close with ')' after assigning value/s
                        if self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                    #  unexpected end: no ')' to close, or comma to followed by, or (=) to assign values
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                #  error: no identifier after the datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            #  no parameter
            elif self.peek_next_token() == ")":
                self.match(")")
                if self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(
                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
            else:
                self.errors.append(f"Syntax Error: Expected ')' after {self.peek_previous_token()}")

    #  method for main function
    def parse_main_function(self):
        if self.peek_next_token() == "[":
            self.parse_func_def()
            if self.peek_next_token() == "]":
                self.match("]")
                self.function_is_defined = True
            else:
                self.errors.append(
                    f"Syntax error: Expected ']' after {self.peek_previous_token()}")
        else:
            self.errors.append(
                f"Syntax error: Expected '[' after {self.peek_previous_token()}")

    # method for sub function prototype
    def parse_sub_function_ptype(self):
        if self.peek_next_token() == "(":
            self.match("(")
            if self.peek_next_token() == "Static":
                self.match("Static")
                # has parameter path
                if (self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman"
                        or self.peek_next_token() == "Boolean" or self.peek_next_token() ==  "Starsys"):
                    self.match(Resources.Datatype2)
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.match("Identifier")
                        if self.peek_next_token() == "=":
                            self.match_param_assign("=")
                            #  close with ')' after assigning value/s
                            if self.peek_next_token() == ")":
                                self.match(")")
                                #  terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                #  error: not terminated
                                else:
                                    self.errors.append(
                                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                            #  error: not closed
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected ')' after {self.peek_previous_token()}")
                        #  check: if closed, single id no value
                        elif self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  single id is followed by a comma
                        elif self.peek_next_token() == ",":
                            self.match_param_assign_mult(",")
                            #  close with ')' after assigning value/s
                            if self.peek_next_token() == ")":
                                self.match(")")
                                #  terminate it
                                if self.peek_next_token() == "#":
                                    self.match("#")
                                #  error: not terminated
                                else:
                                    self.errors.append(
                                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  unexpected end: no ')' to close, or comma to followed by, or (=) to assign values
                        else:
                            self.errors.append(
                                f"Syntax error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                    #  error: no identifier after the datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                #  no datatype after static
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Sun', 'Luhman', 'Boolean', 'Starsys' after {self.peek_previous_token()}")
            # has parameter path
            elif (self.peek_next_token() == "Sun" or self.peek_next_token() == "Luhman"
                        or self.peek_next_token() == "Boolean" or self.peek_next_token() ==  "Starsys"):
                self.match(Resources.Datatype2)
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.match("Identifier")
                    if self.peek_next_token() == "=":
                        self.match_param_assign("=")
                        #  close with ')' after assigning value/s
                        if self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                        #  error: not closed
                        else:
                            self.errors.append(
                                f"Syntax error: Expected ')' after {self.peek_previous_token()}")
                    #  check: if closed, single id no value
                    elif self.peek_next_token() == ")":
                        self.match(")")
                        #  terminate it
                        if self.peek_next_token() == "#":
                            self.match("#")
                        #  error: not terminated
                        else:
                            self.errors.append(
                                f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                    #  single id is followed by a comma
                    elif self.peek_next_token() == ",":
                        self.match_param_assign_mult(",")
                        #  close with ')' after assigning value/s
                        if self.peek_next_token() == ")":
                            self.match(")")
                            #  terminate it
                            if self.peek_next_token() == "#":
                                self.match("#")
                            #  error: not terminated
                            else:
                                self.errors.append(
                                    f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
                    #  unexpected end: no ')' to close, or comma to followed by, or (=) to assign values
                    else:
                        self.errors.append(
                            f"Syntax error: Expected ')', ',', '=' after {self.peek_previous_token()}")
                #  error: no identifier after the datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            #  no parameter
            elif self.peek_next_token() == ")":
                self.match(")")
                if self.peek_next_token() == "[":
                    self.parse_main_function()  # it is a function main??
                elif self.peek_next_token() == "#":
                    self.match("#")
                else:
                    self.errors.append(
                        f"Syntax error: Expected '#', 'Gotolerate' after {self.peek_previous_token()}")
            else:
                self.errors.append(f"Syntax Error: Expected ')' after {self.peek_previous_token()}")

    #  method for main function definition
    def parse_func_def(self):
        if self.peek_next_token() == "[":
            self.match("[")
            self.parse_statements()
        else:
            return

    #  method for statements
    def parse_statements(self):
        # Parse: is it a Sun global variable declaration or a subfunction prototype?
        while self.peek_next_token() in ["Static","Sun","Luhman","Starsys","Boolean","Autom", "Disp", "Capt", "If"]:
            #  Parse: is it a constant dec?
            if self.peek_next_token() == "Static":
                self.match("Static")  # consume Static
                # Parse: is it a Sun global variable declaration or a subfunction prototype?
                if self.peek_next_token() == "Sun":
                    self.match("Sun")  # consume Sun
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration_func()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Luhman global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Luhman":
                    self.match("Luhman")  # consume Luhman
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration_func()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Starsys global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Starsys":
                    self.match("Starsys")  # consume Starsys
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration_func()
                    else:
                        #  error: no identifier after datatype
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Boolean global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Boolean":
                    self.match("Boolean")  # consume Bool
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_boolean_func()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                #  no data type is next to Static
                else:
                    self.errors.append(f"Syntax Error: Expected 'Sun', 'Luhman', 'Starsys', 'Boolean', after {self.peek_previous_token()}")
            # Parse: is it a Sun global variable declaration or a subfunction prototype?
            elif self.peek_next_token() == "Sun":
                self.match("Sun")  # consume Sun
                #  check if there is an identifier after the datatype
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.parse_variable_declaration_func()
                #  error: no identifier after datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            # Parse: is it a Luhman global variable declaration or a subfunction prototype?
            elif self.peek_next_token() == "Luhman":
                self.match("Luhman")  # consume Luhman
                #  check if there is an identifier after the datatype
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.parse_variable_declaration_func()
                #  error: no identifier after datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            # Parse: is it a Starsys global variable declaration or a subfunction prototype?
            elif self.peek_next_token() == "Starsys":
                self.match("Starsys")  # consume Starsys
                #  check if there is an identifier after the datatype
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.parse_variable_declaration_func()
                else:
                    #  error: no identifier after datatype
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            # Parse: is it a Boolean global variable declaration or a subfunction prototype?
            elif self.peek_next_token() == "Boolean":
                self.match("Boolean")  # consume Bool
                #  check if there is an identifier after the datatype
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.parse_boolean_func()
                #  error: no identifier after datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            # Parse: is it an Autom global variable declaration?
            elif self.peek_next_token() == "Autom":
                self.match("Autom")  # consume Autom
                #  check if there is an identifier after the datatype
                if re.match(r'Identifier\d*$', self.peek_next_token()):
                    self.parse_auto_dec()
                #  error: no identifier after datatype
                else:
                    self.errors.append(
                        f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
            #  Parse: is it an output statement? (Disp)
            elif self.peek_next_token() == "Disp":
                self.match("Disp")
                #  check if there is a '<<' after the Disp keyword
                if self.peek_next_token() == "<<":
                    self.parse_disp_stmnt()
                #  error: not followed by "<<"
                else:
                    self.errors.append(
                        f"Syntax error: Expected '<<' after {self.peek_previous_token()}")
            #  Parse: is it an input statement? (Capt)
            elif self.peek_next_token() == "Capt":
                self.match("Capt")
                #  check if there is a '<<' after the Disp keyword
                if self.peek_next_token() == ">>":
                    self.parse_capt_stmnt()
                #  error: not followed by "<<"
                else:
                    self.errors.append(
                        f"Syntax error: Expected '<<' after {self.peek_previous_token()}")
            #  Parse: is an If Statement?
            elif self.peek_next_token() == "If":
                self.match("If")
                #  check if there is a '(' after the If keyword
                if self.peek_next_token() == "(":
                    self.parse_if_stmnt()
                #  error: not followed by "("
                else:
                    self.errors.append(
                            f"Syntax error: Expected '(' after {self.peek_previous_token()}")
            else:
                break


    #  method for parsing display statements
    def parse_disp_stmnt(self):
        if self.peek_next_token() == "<<":
            self.match_output("<<")
            if self.peek_next_token() == "#":
                self.match("#")
            #  not terminated
            else:
                self.errors.append(f"Syntax Error: Unexpected End, Expected '#' ")
        #  not followed by '<<'
        else:
            self.errors.append(f"Syntax Error: Expected '<<' after {self.peek_next_token()}")

    #  method for parsing input statements
    def parse_capt_stmnt(self):
        if self.peek_next_token() == ">>":
            self.match_input(">>")
            if self.peek_next_token() == "#":
                self.match("#")
            #  not terminated
            else:
                self.errors.append(f"Syntax Error: Unexpected End, Expected '#' after {self.peek_next_token()}")
        #  not followed by '<<'
        else:
            self.errors.append(f"Syntax Error: Expected '>>' after {self.peek_previous_token()}")

    #  method for parsing if statements
    def parse_if_stmnt(self):
        if self.peek_next_token() == "(":
            self.match_condition("(")
            #  condition making is done, must be enclosed with ')'
            if self.peek_next_token() == ")":
                self.match(")")
                #  must be followed by '['
                if self.peek_next_token() == "[":
                    self.match("[")
                    #  statements in an If condition
                    self.parse_statements()
                    #  nested If path
                    if self.peek_next_token() == "If":
                        self.match("If")
                        if self.peek_next_token() == "(":
                            self.parse_if_stmnt()
                        #  error: not followed by "("
                        else:
                            self.errors.append(
                                f"Syntax error: Expected '(' after {self.peek_previous_token()}")
                    #  close if condition (empty)
                    elif self.peek_next_token() == "]":
                        self.match("]")
                    #  if condition is not closed
                    else:
                        self.errors.append(f"Syntax Error: Expected ']' after {self.peek_previous_token()}")
                #  error: not followed by '['
                else:
                    self.errors.append(f"Syntax Error: Expected '[' after {self.peek_previous_token()}")
            #  not closed with ')'
            else:
                self.errors.append(f"Syntax Error: Expected ')' after {self.peek_previous_token()}")
        #  not followed by '('
        else:
            self.errors.append(f"Syntax Error: Expected '(' after {self.peek_previous_token()}")

    '''
    #  nested If path
    elif self.peek_next_token() == "If":
        self.match("If")
        if self.peek_next_token() == "(":
            self.parse_if_stmnt()
        #  error: not followed by "("
        else:
            self.errors.append(
                f"Syntax error: Expected '(' after {self.peek_previous_token()}")
    '''

    # parse the program
    def parse_top_program(self):
        if self.peek_next_token() == "Formulate":
            self.match("Formulate")
            self.parse_import_statement()

            # Flag to indicate whether it is parsing global variable declarations
            parsing_global_variables = True

            # Parse: is it a Sun global variable declaration or a subfunction prototype?
            while self.peek_next_token() in ["Static","Sun","Luhman","Starsys","Boolean","Autom","Void"]:
                #  Parse: is it a constant dec?
                if self.peek_next_token() == "Static":
                    self.match("Static")  # consume Static
                    # Parse: is it a Sun global variable declaration or a subfunction prototype?
                    if self.peek_next_token() == "Sun":
                        self.match("Sun")  # consume Sun
                        #  check if there is an identifier after the datatype
                        if re.match(r'Identifier\d*$', self.peek_next_token()):
                            self.parse_variable_declaration()
                        #  error: no identifier after datatype
                        else:
                            self.errors.append(
                                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                    # Parse: is it a Luhman global variable declaration or a subfunction prototype?
                    elif self.peek_next_token() == "Luhman":
                        self.match("Luhman")  # consume Luhman
                        #  check if there is an identifier after the datatype
                        if re.match(r'Identifier\d*$', self.peek_next_token()):
                            self.parse_variable_declaration()
                        #  error: no identifier after datatype
                        else:
                            self.errors.append(
                                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                    # Parse: is it a Starsys global variable declaration or a subfunction prototype?
                    elif self.peek_next_token() == "Starsys":
                        self.match("Starsys")  # consume Starsys
                        #  check if there is an identifier after the datatype
                        if re.match(r'Identifier\d*$', self.peek_next_token()):
                            self.parse_variable_declaration()
                        else:
                            #  error: no identifier after datatype
                            self.errors.append(
                                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                    # Parse: is it a Boolean global variable declaration or a subfunction prototype?
                    elif self.peek_next_token() == "Boolean":
                        self.match("Boolean")  # consume Bool
                        #  check if there is an identifier after the datatype
                        if re.match(r'Identifier\d*$', self.peek_next_token()):
                            self.parse_boolean()
                        #  error: no identifier after datatype
                        else:
                            self.errors.append(
                                f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                    #  no data type is next to Static
                    else:
                        self.errors.append(f"Syntax Error: Expected 'Sun', 'Luhman', 'Starsys', 'Boolean', after {self.peek_previous_token()}")
                # Parse: is it a Void subfunc prototype declaration?
                elif self.peek_next_token() == "Void":
                    self.match("Void")  # consume Void
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_void_declaration()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Sun global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Sun":
                    self.match("Sun")  # consume Sun
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration()
                        '''
                        if self.peek_next_token() == "[":
                            break
                        '''
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Luhman global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Luhman":
                    self.match("Luhman")  # consume Luhman
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Starsys global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Starsys":
                    self.match("Starsys")  # consume Starsys
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_variable_declaration()
                    else:
                        #  error: no identifier after datatype
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it a Boolean global variable declaration or a subfunction prototype?
                elif self.peek_next_token() == "Boolean":
                    self.match("Boolean")  # consume Bool
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_boolean()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                # Parse: is it an Autom global variable declaration?
                elif self.peek_next_token() == "Autom":
                    self.match("Autom")  # consume Autom
                    #  check if there is an identifier after the datatype
                    if re.match(r'Identifier\d*$', self.peek_next_token()):
                        self.parse_auto_dec()
                    #  error: no identifier after datatype
                    else:
                        self.errors.append(
                            f"Syntax error: Expected 'Identifier' after {self.peek_previous_token()}")
                else:
                    break

        else:
            self.errors.append(f"Syntax Error: Expected 'Formulate'")
            self.errors.append(f"Syntax Error: 'Import', 'ISS', 'Static', 'Boolean', 'Autom', 'Luhman', "
            f"'Starsys', 'Void', 'Class', 'Sun', 'Identifier', '(', ')', '[', ']'")


        # check if Import appeared even when not after 'Formulate'
        if self.peek_next_token() == "Import":
            self.errors.append(f"Syntax Error: 'Import' statements can only be declared after 'Formulate'")
        elif self.peek_next_token() == "Formulate":
            self.errors.append(
                f"Syntax Error: 'Formulate' keyword can only appear once and on the very top of the program")
        else:
            pass

        if not self.function_is_defined:
            self.errors.append(
                f"Syntax Error: Expected 'Sun', 'Identifier', '(', ')', '[', ']'")

    '''
    def parse_main_program(self):
        self.peek_previous_token()
        if self.peek_next_token() == "[" and self.peek_previous_token() == ")":
            self.parse_main_function()
        else:
            self.errors.append(f"Syntax Error: Main Program Missing, Expected 'Sun', 'Identifier', '('. ')', '[', ']'")
    '''

