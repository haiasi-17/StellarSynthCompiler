import Resources
import Lexer

class ThreeAddressCode:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = 0 # Used to track current token index
        self.currentToken = None # Stores current token
        self.tempVariableCount = 0 # Used to track current count of temp variable (the n in tn)
        self.tempVariabledict = {} # Used to store all the temp variables and their values (t0 : 1+2)
        self.tempVariabledictIndex = 0 # Used to keep track of what index of the tempvardict is the the topmost.
        self.variabledict = {} # Used to keep track of all the variable dict (a = 2)
        self.indexNextOperator = None # Used to determine the index of the operator to be executed.
        self.assignIdent = None # Stores the identifier for assignment statements
        self.operandOneStartIndex = None # Stores the starting index of operand one (left of operator)
        self.operandTwoStartIndex = None # Stores the starting index of operand two (right of operator)
        self.currentDatatype = None # Stores current data type
        self.tacOutput = "" # Stores the complete program tac output
        self.tacString = "" # Stores the tac output of a specific code block to be added to the tacOutput
        self.expression = "" # Stores the entire expression statement
        self.tempexpression = "" # Stores a subexpression within the expression statement
        self.tempexpression1 = "" # Used in parenthesisexpressionhandler to store subexpressions that are within parenthenses
        self.startParenthIndex = None # Stores the starting index of the parentheses
        self.endParenthIndex = None # Stores the ending index of the parentheses
    
    def go_next_token(self):
        # if length of tokens is 18. Max accepted value to be accepted in condition is 16. Later to be incremented as the last element cause 0-17 indexing.
        if (self.tokenIndex < (len(self.tokens)-1) and self.tokenIndex > -1) and self.currentToken != None:
            self.tokenIndex += 1
            self.currentToken = self.tokens[self.tokenIndex][0]
            while self.currentToken in Resources.whitespace and (self.tokenIndex < (len(self.tokens)-1) and self.currentToken != None):
                self.tokenIndex += 1
                self.currentToken = self.tokens[self.tokenIndex][0]
        return
    
    def go_back_token(self):
        if (self.tokenIndex < (len(self.tokens)-1) and self.tokenIndex > -1) and self.currentToken != None:
            self.tokenIndex -= 1
            self.currentToken = self.tokens[self.tokenIndex][0]
            while self.currentToken in Resources.whitespace and (self.tokenIndex < (len(self.tokens)-1) and self.currentToken != None):
                self.tokenIndex -= 1
                self.currentToken = self.tokens[self.tokenIndex][0]
        return
        
    def generate_TAC(self):
        self.currentToken = self.tokens[self.tokenIndex][0]
        while self.tokenIndex < (len(self.tokens)-1):

            # Check if it is a whitespace, if so, skip it.
            if self.currentToken in Resources.whitespace:
                self.go_next_token()
               
            # Check if current token is a data type. Which means it could either be a function dec or def, vardec.
            elif self.currentToken in Resources.dataTypes_var:
                
                # Store the current data type, to use later.
                self.currentDatatype = self.currentToken
                
                self.go_next_token() # Current Token == Identifier
                
                # Check if it is a Main Function Definition, if so, skip it.
                if self.currentToken == "Universe":
                    self.go_next_token
                    continue
                
                self.go_next_token() # Current Token == either (, =, # or [.
                
                # Check if it is a function declaration, if so, skip it.
                if self.currentToken in Resources.LParenth:
                    while self.currentToken not in Resources.Terminator:
                        self.go_next_token()
                    continue
                
                # Check if it is a declaration with no assignment operator, if so, assign corresponding datatype default value, and append to tac output.
                elif self.currentToken in Resources.Terminator:
                    self.go_back_token()
                    
                    # Assign t of x the default value
                    self.tacString += f"\nt{self.tempVariableCount} = {Resources.defaultvalueDict[self.currentDatatype]}"
                    # Store it in the tempvariabledict.
                    self.tempVariabledict[f"t{self.tempVariableCount}"] = {Resources.defaultvalueDict[self.currentDatatype]}
                    # Assign the above tempvariable to the identifier
                    self.tacString += f"\n{self.currentToken} = {list(self.tempVariabledict.keys())[self.tempVariabledictIndex]}"
                    # Assign the current token with its value to the variable dict
                    self.variabledict[self.currentToken] = self.tempVariabledict[f"t{self.tempVariabledictIndex}"]
                    
                    # Increment the tempvardictindex, and the tempVarCount
                    self.tempVariableCount += 1
                    self.tempVariabledictIndex += 1

                    # Assign the finished tacString to tacOutput, reset tacString, go next token and continue.
                    self.tacOutput += self.tacString
                    self.tacString = ""
                    self.go_next_token
                    continue
                
                # Check if it is a variable declaration using assignment operator
                elif self.currentToken in Resources.AssignOp:
                    self.go_back_token() # Go to identifier token
                    # Store the identifier, to use later.
                    self.assignIdent = self.currentToken
                    self.go_next_token() # This is so that we don't include the assignment operator in the expression.
                    self.go_next_token() # This is so that we don't include the assignment operator in the expression.

                    # Find the terminator, so that the entire expression is found.
                    while self.currentToken not in Resources.Terminator:
                        self.expression += self.currentToken
                        self.go_next_token()
                    # Current token is terminator, and the entire expression is in self.expression
                    
                    
                    # Sun y = 34**34+5*5%2-2 CHECK
                    # Sun x = (a+(3+(4-3*4))*b)  
                    # Sun x = (a+(3)) 
                    # Sun x = y*(-3)
                    # Sun y = (a+3-2) 
                    # Sun x = -(3)
                    
                    # Determine order of operations in self.expression.
                    # If it is an expression with no parentheses, just handle the expression using EMD Mod AS. 
                    if '(' not in self.expression:
                        self.vardecExpressionHandler()
                        
                    # If it is a expression with parentheses, find the innermost parentheses to be executed as per PEMDAS
                    elif  '(' in self.expression:
                        self.vardecParenthExpressionHandler()

                elif self.currentToken in Resources.LSqrBrkt:
                    pass
                        
                        
            elif self.currentToken in Resources.conditionalStart:
                pass
            elif self.currentToken in Resources.iterativeStart:
                pass
            else:
                self.go_next_token()
                
        return self.tacOutput
    
    def vardecParenthExpressionHandler(self): # This function handles variable declarations using parentheses
        while '(' in self.expression: 
            self.startParenthIndex = self.expression.rfind("(")
            self.endParenthIndex = self.expression.find(")", self.startParenthIndex)
            # Inner most pair of parenthesis found, store the expression within in self.tempexpression for tac generation.
            self.tempexpression = self.expression[self.startParenthIndex:self.endParenthIndex+1]
            # Remove the parentheses pair of expression from self.tempexpression
            self.tempexpression = self.tempexpression[1:-1]
            
            # Determine order of operations of self.tempexpression, then generate tac for self.tempexpression.
            self.parenthExpressionHandler()
            
            # Replace the subexpression with the tempvar containing the subexpression, while not including the parentheses when put back in.
            self.expression = self.expression[0: self.startParenthIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.endParenthIndex+1:]
            
            # Increment the tempvardictindex, and the tempVarCount for next pair of parentheses
            self.tempVariableCount += 1
            self.tempVariabledictIndex += 1
            
            # Reset tempexpression for the next pair of parenthesis.
            self.tempexpression = ""
        else:
            # Decrement the tempvardictindex, and the tempVarCount to compensate for the incrementing of the last iteration of the while loop.
            self.tempVariableCount -= 1
            self.tempVariabledictIndex -= 1
            
        # Assign the final tempvariable to the identifier.
        self.tacString += f"\n{self.assignIdent} = {list(self.tempVariabledict.keys())[self.tempVariabledictIndex]}"
        # Assign the current token with its value to the variable dict
        self.variabledict[self.assignIdent] = self.tempVariabledict[f"t{self.tempVariabledictIndex}"]
        # Reset self.expression value and selfassignident.
        self.expression = ""
        self.assignIdent = None
    
    
    def parenthExpressionHandler(self): # This function handles the expressions inside parentheses
        while (self.tempexpression.count("+") + self.tempexpression.count("-") + self.tempexpression.count("/") + self.tempexpression.count("%") + (self.tempexpression.count("*")-(self.tempexpression.count("**")*2))+ self.tempexpression.count("**")) > 1:
            if(self.tempexpression.count("**") > 0): # Do account for the extra character for exponentiation
                # Find the index of the exponentiation operator starting from the right most side as per its mathematical associativity
                self.indexNextOperator = self.tempexpression.rfind("**")
                
                # Find the operand one and two of the exponentiation operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+2

                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp + ['(']:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp + [')']:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the exponentiation operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.tempexpression[self.operandTwoStartIndex+1:]

                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""            
            
            elif(self.tempexpression.count("*")-(self.tempexpression.count("**")*2) > 0):
                # Find the index of the multiplication operator, left-associative
                self.indexNextOperator = self.tempexpression.find("*")
            
                # Find the operand one and two of the multiplication operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the multiplication operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.tempexpression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
            elif(self.tempexpression.count("/") > 0):
                # Find the index of the division operator, left-associative
                self.indexNextOperator = self.tempexpression.find("/")
            
                # Find the operand one and two of the division operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the division operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.tempexpression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
                                
            elif(self.tempexpression.count("%") > 0):
                # Find the index of the modulo operator, left-associative
                self.indexNextOperator = self.tempexpression.find("%")
            
                # Find the operand one and two of the modulo operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the modulo operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
            
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.tempexpression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
                                    
            elif(self.tempexpression.count("+") > 0):
                # Find the index of the addition operator, left-associative
                self.indexNextOperator = self.tempexpression.find("+")
                
                # Find the operand one and two of the addition operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the addition operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.tempexpression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                            
            elif(self.tempexpression.count("-") > 0):
                # Find the index of the subtraction operator, left-associative
                self.indexNextOperator = self.tempexpression.find("-")
            
                # Find the operand one and two of the subtraction operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                while self.operandOneStartIndex > 0 and self.tempexpression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.tempexpression) - 1 and self.tempexpression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the subtraction operator to self.tempexpression1 for tac generation.
                self.tempexpression1 = self.tempexpression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression1 to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression1}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression1}
                # Replace the subexpression with the tempvar containing the subexpression.
                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.tempexpression = self.tempexpression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.tempexpression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression1 = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""

        # Now tempexpression has the final operator to be executed, and the two operands.
        # We assign this tempexpression to its final tempvariable
        self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
        # Store it in the tempvariabledict.
        self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
        
        # Reset variables used for the next tacgeneration
        self.tempexpression1 = ""
        self.indexNextOperator = None
        self.operandOneStartIndex = None
        self.operandTwoStartIndex = None

        # Assign the finished tacString to tacOutput, reset tacString and continue.
        self.tacOutput += self.tacString
        self.tacString = ""
        return
    
    
    def vardecExpressionHandler(self): # This function handles variable declarations with expressions of operator Expo, Multi, Divi, Modu, Add, Sub.
        # Loop that continues if the number of Mathop in the expression is greater than one, meaning it can't yet be assigned to identifier.
        while (self.expression.count("+") + self.expression.count("-") + self.expression.count("/") + self.expression.count("%") + (self.expression.count("*")-(self.expression.count("**")*2))+ self.expression.count("**")) > 1:
            
            if(self.expression.count("**") > 0): # Do account for the extra character for exponentiation
                # Find the index of the exponentiation operator starting from the right most side as per its mathematical associativity
                self.indexNextOperator = self.expression.rfind("**")
                
                # Find the operand one and two of the exponentiation operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+2
            
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.operandTwoStartIndex+1:]

                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""            
            
            elif(self.expression.count("*")-(self.expression.count("**")*2) > 0):
                # Find the index of the multiplication operator, left-associative
                self.indexNextOperator = self.expression.find("*")
            
                # Find the operand one and two of the multiplication operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the multiplication operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
            elif(self.expression.count("/") > 0):
                # Find the index of the division operator, left-associative
                self.indexNextOperator = self.expression.find("/")
            
                # Find the operand one and two of the division operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the division operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
                                
            elif(self.expression.count("%") > 0):
                # Find the index of the modulo operator, left-associative
                self.indexNextOperator = self.expression.find("%")
            
                # Find the operand one and two of the modulo operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the modulo operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
            
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
                                    
            elif(self.expression.count("+") > 0):
                # Find the index of the addition operator, left-associative
                self.indexNextOperator = self.expression.find("+")
                
                # Find the operand one and two of the addition operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the addition operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                            
            elif(self.expression.count("-") > 0):
                # Find the index of the subtraction operator, left-associative
                self.indexNextOperator = self.expression.find("-")
            
                # Find the operand one and two of the subtraction operator
                self.operandOneStartIndex = self.indexNextOperator-1
                self.operandTwoStartIndex = self.indexNextOperator+1    
            
                while self.operandOneStartIndex > 0 and self.expression[self.operandOneStartIndex - 1] not in Resources.MathOp:
                    self.operandOneStartIndex -= 1
                while self.operandTwoStartIndex < len(self.expression) - 1 and self.expression[self.operandTwoStartIndex + 1] not in Resources.MathOp:
                    self.operandTwoStartIndex += 1
                
                # Assign both operands, and the subtraction operator to self.tempexpression for tac generation.
                self.tempexpression = self.expression[self.operandOneStartIndex: self.operandTwoStartIndex+1]
                
                # Assign the 2-address tempexpression to tempvariable
                self.tacString += f"\nt{self.tempVariableCount} = {self.tempexpression}"
                # Store it in the tempvariabledict.
                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                
                # Replace the subexpression with the tempvar containing the subexpression.

                # first one refers to all expressions before operand one, second refers to the tempvar, third refers to all expressions after operandtwo.
                self.expression = self.expression[:self.operandOneStartIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex] + self.expression[self.operandTwoStartIndex+1:]
                
                # Increment the tempvardictindex, and the tempVarCount
                self.tempVariableCount += 1
                self.tempVariabledictIndex += 1
                
                # Reset variables used for the next tacgeneration
                self.tempexpression = ""
                self.indexNextOperator = None
                self.operandOneStartIndex = None
                self.operandTwoStartIndex = None

                # Assign the finished tacString to tacOutput, reset tacString and continue.
                self.tacOutput += self.tacString
                self.tacString = ""
                
        # Now expression has the final operator to be executed, and the two operands.
        # We assign this expression to its final tempvariable
        self.tacString += f"\nt{self.tempVariableCount} = {self.expression}"
        # Store it in the tempvariabledict.
        self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.expression}
        
        # Assign the above tempvariable to the identifier.
        self.tacString += f"\n{self.assignIdent} = {list(self.tempVariabledict.keys())[self.tempVariabledictIndex]}"
        # Assign the current token with its value to the variable dict
        self.variabledict[self.assignIdent] = self.tempVariabledict[f"t{self.tempVariabledictIndex}"]
        
        # Reset variables used for the next tacgeneration
        self.tempexpression = ""
        self.indexNextOperator = None
        self.operandOneStartIndex = None
        self.operandTwoStartIndex = None
        self.expression = ""

        # Assign the finished tacString to tacOutput, reset tacString and continue.
        self.tacOutput += self.tacString
        self.tacString = ""
        return
        

if __name__ == "__main__":
    errors, tokens = Lexer.read_text('StellarSynth')
    tacInstance = ThreeAddressCode(tokens)
    tacOutput = tacInstance.generate_TAC()
    print(tacOutput)



# vardec default Check
# vardec no parenth assign expression value check
# vardec with parenth check

# arrdec assign?
# unary minus?
# decrementation? pre and post
# incrementation? pre and post
# Functions?
# Imports?
# Methods?
# Classes? 
# Essentially those using . operator