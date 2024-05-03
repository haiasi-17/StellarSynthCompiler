import Resources
import Lexer
import subprocess

class Transpiler:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = 0
        self.currentToken = None
        self.translatedTokens = []
        self.translatedTokensIndex = 0
        self.dataType = None
        self.f_cpp = None
        self.isVarDec = False
        
    def stellarTranslator(self):
        self.currentToken = self.tokens[self.tokenIndex][0]
        while self.tokenIndex < (len(self.tokens)-1):
        # Remove Formulate from the beginning of the program.
            if self.currentToken == "Formulate" or self.currentToken == "Disintegrate":
                self.tokens.pop(self.tokenIndex)
                self.currentToken = self.tokens[self.tokenIndex][0] # Do not increment as the number of tokens decreases because of the removed element.
                continue 
            # Temporary solution, import is currently non-functional.
            elif self.currentToken == "Import":
                # Remove entire import statement.
                while self.currentToken != "\n":
                    self.tokens.pop(self.tokenIndex)     
                    self.currentToken = self.tokens[self.tokenIndex][0] # Do not increment as the number of tokens decreases because of the removed element.
                continue 
            # Replace StellarSynth Token with its C++ Counterpart.
            elif self.currentToken in Resources.StellarCPlusPlusDict:
                self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = Resources.StellarCPlusPlusDict[self.currentToken] 
                self.translatedTokens.append(self.tokens[self.tokenIndex])
                self.go_next_token()
                continue
            # If it is a Starsys literal, either replace it with double quotes if it uses single quotes then append, or just append.
            elif self.tokens[self.tokenIndex][1] == "StarsysLiteral":
                tempvar = "\""
                # Convert Starsys literal to use double quotes.
                if  self.tokens[self.tokenIndex][0][0] == '\'':
                    tempvar += self.tokens[self.tokenIndex][0][1:-1]
                    tempvar += "\""
                    self.tokens[self.tokenIndex][0] = tempvar
                self.translatedTokens.append([self.tokens[self.tokenIndex][0],self.tokens[self.tokenIndex][1]])
                self.go_next_token()
                continue
            # Check if it is an identifier.
            elif self.tokens[self.tokenIndex][1][0:10] == "Identifier":
                storeIdent = self.currentToken # Store identifier to be used later.
                
                # Go back to the data type token, only skipping the whitespaces on its way there and stopping at the first non-whitespace token.
                backCount = 1
                self.go_back_token()
                while self.currentToken not in Resources.transdefaultvalueDict and self.currentToken in Resources.whitespaces:
                    self.go_back_token()
                    backCount += 1
                
                # This is to check if the identifier is part of a variable declaration, or its just an identifier.
                if self.currentToken in Resources.transdefaultvalueDict:
                    # If it has a corresponding data type it is part of it, assign for future reference and set flag to true.
                    self.dataType = self.currentToken
                    self.isVarDec = True
                
                # Return to the identifier token
                for x in range(backCount):
                    self.go_next_token()
                
                self.go_next_token() # Go to next token of identifier
                nextCount = 1
                
                # If next token is whitespace, loop to find the next token, skip the whitespaces.
                while self.currentToken in Resources.whitespaces:
                    self.go_next_token()
                    nextCount += 1

                # If it is an identifier and next token minus whitespaces is #, it is a default vardec initialization, assign its value.
                if self.currentToken == "#" and self.isVarDec == True:
                    self.translatedTokens.append([storeIdent,storeIdent])
                    self.translatedTokens.append(["=","="])
                    self.translatedTokens.append([Resources.transdefaultvalueDict[self.dataType],Resources.transdefaultvalueDict[self.dataType]])
                    self.isVarDec = False
                    self.dataType = None
                    continue
                # Else if it is an identifier and the next token minus whitespaces isn't #. Append the identifier token and continue.
                else:
                    # It is a variable declaration with assigned value, set the flags to false for next iteration.
                    if self.isVarDec == True:
                        self.isVarDec = False
                        self.dataType = None
                        
                    # Go back to identifier token
                    for x in range(nextCount):
                        self.go_back_token()
                    self.translatedTokens.append(self.tokens[self.tokenIndex])
                    self.go_next_token()
                    continue
                
            # Is both a StellarSynth and C++ Token. Append to translatedtokens list.
            else:
                self.translatedTokens.append(self.tokens[self.tokenIndex])
                self.go_next_token()
                continue
        
    def go_next_token(self):
    # if length of tokens is 18. Max accepted value to be accepted in condition is 16. Later to be incremented as the last element cause 0-17 indexing.
        if (self.tokenIndex < (len(self.tokens)-1) and self.tokenIndex > -1) and self.currentToken != None:
            self.tokenIndex += 1
            self.currentToken = self.tokens[self.tokenIndex][0]
        return
    
    def go_back_token(self):
        if (self.tokenIndex < (len(self.tokens)-1) and self.tokenIndex > -1) and self.currentToken != None:
            self.tokenIndex -= 1
            self.currentToken = self.tokens[self.tokenIndex][0]
        return
    
    def writetoCPPFile(self):
        # Initialize with some needed headers.
        convertedcppCode = '#include <iostream>\n#include <string>\nusing namespace std;'
             
        # Concatenate all translatedtokens to the cppCode string
        while self.translatedTokensIndex < (len(self.translatedTokens)-1):
            convertedcppCode += self.translatedTokens[self.translatedTokensIndex][0]
            self.translatedTokensIndex +=1
        
        # Write the convertedCppCode to a cpp file named Output
        self.f_cpp = "Output.cpp"
        with open(self.f_cpp, 'w') as fout:
            fout.write(convertedcppCode)
            
        # Compile the program
        f_exec = "Output.exe"
        compile_cmd = "g++ {} -o {}".format(self.f_cpp, f_exec)
        subprocess.call(compile_cmd, shell=True)

        # Run the program
        p = subprocess.Popen(f_exec, shell=True,
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

        # Read input from console
        input_variables = input("Enter input variables: ")

        # Provide input to the process
        p.stdin.write(input_variables.encode())
        p.stdin.flush()

        # Read the output from stdout and stderr
        output, error = p.communicate()

        # Display the output in the console
        if output:
            print("Output:")
            print(output.decode())
        if error:
            print("Error:")
            print(error.decode())
        

if __name__ == "__main__":
    errors, tokens = Lexer.read_text('StellarSynth')
    transpilerInstance = Transpiler(tokens)
    transpilerInstance.stellarTranslator()
    transpilerInstance.writetoCPPFile()

""" 
Features that differ in the C++ Language:
    Exponentiation Operator -> No Solution yet.
    Importation -> Temporary Solution. Removed from Program.
    Type Conversion -> Currently utilizing implicit type conversion of c++, no idea how to modify it. Explicit is covered na. However, there might be inconsistencies with c++ type conversion with our rules.
    Default Value -> Implemented rules in our language
    
Algorithm:
1. Translate StellarSynth to C++
2. Write C++ to cpp file, writing the necessary headers and namespaces.
3. Run CPP File in StellarSynthCompiler
"""  

