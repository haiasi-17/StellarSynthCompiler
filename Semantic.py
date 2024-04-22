import re
import Resources
import Lexer

# Type Mismatch - Assignment, Expressions
# Variable declared in scope checking
# Negative array index
# function declared? checking
# function declared? but no definition?
# function no statements inside?

class Semantic:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []
        self.identifier_scope_dict = {}
        self.scope = 0
        self.current_token_index = 0
        self.current_token = None
        self.get_lexeme = 0
        self.get_token = 1
        self.line_num = 0

    def go_next_token(self):
        while (self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][self.get_token] in ["Space","\n", "\t"]):
            self.current_token_index += 1
            
        self.current_token_index += 1
        self.current_token = self.tokens[self.current_token_index][self.get_token]

        return

    def Analyze(self):
        while self.current_token_index < len(self.tokens):
            if (self.current_token_index < len(self.tokens) and self.current_token in ["Space","\n", "\t"]):
                if self.current_token == "\n":
                    self.line_num += 1  # Increment line number when encountering a newline
                self.go_next_token()
                continue
            elif self.current_token in Resources.dataTypes:
                self.CheckfromType()
                continue
    
            self.go_next_token()
            
            
    # Differentiate Main Function, Sub Function, and Variable Declaration
    def CheckfromType(self):
        currentDataTypeCondition = self.current_token
        self.go_next_token()

        # Determine if in Main Function
        if currentDataTypeCondition == "Sun" and self.current_token == "Universe":
            self.scope += 1
            return
        
        # Determine if variable declaration
        elif currentDataTypeCondition in Resources.dataTypes_var and (self.current_token[0:-1] == "Identifier" and str(self.current_token[-1]).isdigit):
            self.go_next_token()
            
            # It isn't a variable declaration if followed by a parenthesis.
            if self.current_token == "(":
                return
            else:
            # It is a variable declaration, determine if a value is assigned, or not.
                while self.current_token not in Resources.assignable_values or self.current_token != "#":
                    self.go_next_token()
                    
            # If no value is assigned
            if self.current_token == "#":
                return
            # If value is assigned, check if data type is appropriate
            elif self.current_token not in Resources.variableAcceptedValues[currentDataTypeCondition]:
                self.errors.append(f"Semantic Error: \'{currentDataTypeCondition}\' type mismatch, expected {Resources.variableAcceptedValues[currentDataTypeCondition]}, instead got {self.current_token}")
                return
            else:
                return
                
        # Determine if in Subfunction
        elif self.current_token[0:-1] == "Identifier" and str(self.current_token[-1]).isdigit():
            
            # Determine if declaration or definition.
            while self.current_token != "#" or self.current_token != "[":
                self.go_next_token()
                
            # Is Subfunction declaration
            if self.current_token == "#":
                return
            
            # Is Subfunction definition
            elif self.current_token == "[":
                self.scope +=1
                return
        
        
            

            
            
            



            
        


if __name__ == "__main__":
    errors, tokens = Lexer.read_text('StellarSynth')
    semantic_instance = Semantic(tokens)
    semantic_instance.Analyze()
    print(semantic_instance.errors)