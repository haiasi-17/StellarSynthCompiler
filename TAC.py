import Resources
import Lexer

class ThreeAddressCode:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = 0 # Used to track current token index
        self.currentToken = None
        self.tempVariableCount = 0 # Used to track current count of temp variable (the n in tn)
        self.tempVariabledict = {} # Used to store all the temp variables and their values (t0 : 1+2)
        self.tempVariabledictIndex = 0 # Used to keep track of what index of the tempvardict is the the topmost.
        self.variabledict = {} # Used to keep track of all the variable dict (a = 2)
        self.indexNextOperator = None # Used to determine the index of the operator to be executed.
        self.assignIdent = None # Stores the identifier for assignment statements
        self.operandOne = None
        self.operandTwo = None
        self.currentDatatype = None
        self.tacOutput = ""
        self.tacString = ""
        self.expression = ""
        self.tempexpression = ""
        self.startParenthIndex = None
        self.endParenthIndex = None
        
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
                
                # Check if it is a function declaration, if so, skip it.
                self.go_next_token() # Current Token == either (, = or #.

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
                    # Assign the above tempvariable to the current token.
                    self.tacString += f"\n{self.currentToken} = {list(self.tempVariabledict.keys())[self.tempVariabledictIndex]}"
                    # Assign the current token with its value to the variable dict
                    self.variabledict[self.currentToken] = self.tempVariabledict[f"t{self.tempVariabledictIndex}"]
                    
                    # Increment the tempvardictindex, and the tempVarCount
                    self.tempVariableCount += 1
                    self.tempVariabledictIndex += 1

                    # Assign the finished tacString to tacOutput, reset tacInput, go next token and continue.
                    self.tacOutput += self.tacString
                    self.tacString = ""
                    self.go_next_token
                    continue
                    
                elif self.currentToken in Resources.AssignOp: # Sun x = (a+(3+(4-3))*b)  Sun x = (a+(3)) Sun x = y*(-3) Sun y = (a+3-2) Sun x = -(3)
                    # Store the identifier, to use later.
                    self.assignIdent = self.currentToken
                    self.go_next_token() # This is so that we don't include the assignment operator in the expression.
                    
                    # Find the terminator, so that the entire expression is found.
                    while self.currentToken not in Resources.Terminator:
                        self.expression += self.currentToken
                        self.go_next_token()
                    # Current token is terminator, and the entire expression is in self.expression
                    print(self.expression)
                    # Determine order of operations in self.expression. Sun y = 3**3+5*5%2-2
                    if '(' not in self.expression:
                        while len(self.expression) > 2:
                            if(self.expression.find("**")): # Do account for the extra character for exponentiation
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("**")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+3] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+3:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                                
                            elif(self.expression.find("*")):
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("*")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+2] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+2:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                            
                            elif(self.expression.find("/")):
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("/")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+2] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+2:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                            
                            elif(self.expression.find("%")):
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("%")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+2] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+2:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                            
                            elif(self.expression.find("+")):
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("+")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+2] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+2:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                            
                            elif(self.expression.find("-")):
                                # Find the index of the operator
                                self.indexNextOperator = self.expression.find("-")
                                # Assign both operands, and the exponentiation operator to self.tempexpression for tac generation.
                                self.tempexpression = self.expression[self.indexNextOperator-1:self.indexNextOperator+2] 
                                
                                # Assign the 2-address tempexpression to tempvariable
                                self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                                # Store it in the tempvariabledict.
                                self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                                
                                # Increment the tempvardictindex, and the tempVarCount
                                self.tempVariableCount += 1
                                self.tempVariabledictIndex += 1
                                
                                # Replace the subexpression with the tempvar containing the subexpression.
                                self.expression = self.expression[0: self.indexNextOperator-1] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.indexNextOperator+2:]
                                
                                # Reset variables used for next tacgeneration
                                self.tempexpression = ""
                                self.indexNextOperator = None
                                
                    
                        
                   
                    
                    
                    
                    """
                    # In case that it is a nested parentheses expression. Find the innermost pair of parentheses expression.
                    while '(' in self.expression: 
                        self.startParenthIndex = self.expression.rfind("(")
                        self.endParenthIndex = self.expression.find(")", self.startParenthIndex)
                        # Inner most pair of parenthesis found, store the expression within in self.tempexpression for tac generation.
                        self.tempexpression = self.expression[self.startParenthIndex:self.endParenthIndex+1]
                        # Remove the parentheses from self.tempexpression
                        self.tempexpression = self.tempexpression[1:-1]
                        
                        # Determine order of operations of self.tempexpression, then generate tac for self.tempexpression
                        if(self.tempexpression.find("**")): # Do account for the extra character for exponentiation
                            pass
                        
                        elif(self.tempexpression.find("*")):
                            pass
                        
                        elif(self.tempexpression.find("/")):
                            pass
                        
                        elif(self.tempexpression.find("%")):
                            pass
                        
                        elif(self.tempexpression.find("+")):
                            pass
                        
                        elif(self.tempexpression.find("-")):
                            pass
                        
                            
                        
                        
                        # Assign the 2-address tempexpression to tempvariable
                        self.tacString += f"t{self.tempVariableCount} = {self.tempexpression}"
                        # Store it in the tempvariabledict.
                        self.tempVariabledict[f"t{self.tempVariableCount}"] = {self.tempexpression}
                        
                        # Increment the tempvardictindex, and the tempVarCount
                        self.tempVariableCount += 1
                        self.tempVariabledictIndex += 1
                        
                        # Replace the subexpression with the tempvar containing the subexpression.
                        self.expression = self.expression[0: self.startParenthIndex] + list(self.tempVariabledict.keys())[self.tempVariabledictIndex-1] + self.expression[self.endParenthIndex+1:]
                        
                        self.tempexpression = ""
                        
                        print(f"{self.expression}")
                        """

                    

                        
                        
                        
                    
            elif self.currentToken in Resources.conditionalStart:
                pass
            elif self.currentToken in Resources.iterativeStart:
                pass
            else:
                self.go_next_token()
        return self.tacOutput
            
    def go_next_token(self):
        # if length of tokens is 18. Max accepted value to be accepted in condition is 16. Later to be incremented as the last element.
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
    
    
    
    def assignmentExpressionHandler(self):
        pass
    
    def conditionalStatementHandler(self):
        pass
        
    def iterationStatementHandler(self):
        pass
        

if __name__ == "__main__":
    errors, tokens = Lexer.read_text('StellarSynth')
    tacInstance = ThreeAddressCode(tokens)
    tacOutput = tacInstance.generate_TAC()
    print(tacOutput)
    
# Functions?
# Imports?
# Methods?
# Classes? 
# Essentially those using . operator