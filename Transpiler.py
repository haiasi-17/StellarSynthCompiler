import Resources
import Lexer
import subprocess
import os.path

class Transpiler:
    def __init__(self, tokens, filename):
        self.filename = filename
        self.tokens = tokens
        self.tokenIndex = 0
        self.currentToken = None
        self.translatedTokens = []
        self.translatedTokensIndex = 0
        
        self.dataType = None
        self.f_cpp = None
        self.isVarDec = False
        
        self.expoString = ""
        self.operandOne = ""
        self.operandTwo = ""
        self.parenthCount = 0
        self.removeTokenCount = 0
        
        self.mainfuncFlag = False
        
        self.goNextTokenCount = 0
        self.goBackTokenCount = 0 
        self.prevTokenParenth = False
        self.nextTokenParenth = False
        
        self.isDisp = False
        self.isCapt = False
        
        self.identCount = 0
        
    def stellarTranslator(self):
        self.currentToken = self.tokens[self.tokenIndex][0]
        while self.tokenIndex < (len(self.tokens)-1):
            # Remove Formulate and Disintegrate from the beginning of the program.
            if self.currentToken == "Formulate" or self.currentToken == "Disintegrate":
                self.tokens.pop(self.tokenIndex)
                self.currentToken = self.tokens[self.tokenIndex][0] # Do not increment as the number of tokens decreases because of the removed element.
                continue 
            
            # Convert exponentiation operator to c++ pow function
            elif self.currentToken == "**": 
                # i = a+4**10                                       -> i = a+pow(4,10) Check
                # i = 3+(a+4)**10                                   -> i = 3+pow((a+4),10) Check
                # i = 3+(a+4)**(b+10)                               -> i = 3+pow((a+4),(b+10)) Check
                # i = 3+a**(b+10)                                   -> i = 3+pow(a,(b+10)) Check
                # i = 3+(a+(4-2))**10                               -> i = 3+pow((a+(4-2)), 10) Check
                # i = 3+10**(a+(4-2))                               -> i = 3+pow(10, (a+(4-2))) Check
                # i = 3+(b-(2-10))**(a+(4-2))                       -> i = 3+pow((b-(2-10), (a+(4-2))) Check
                
                
                # i = a + 4 ** 10                                   -> i = a +pow(4,10) Check
                # i = 3 + ( a + 4 ) ** 10                           -> i = pow((a+4),10) Check
                # i = 3 + ( a + 4 ) ** ( b + 10 )                   -> i = pow((a+4),(b+10)) Check
                # i = 3 + a ** ( b + 10 )                           -> i = pow(a,(b+10))  Check
                # i = 3 + ( a + ( 4 - 2 ) ) ** 10                   -> i = pow((a+(4-2)), 10) Check
                # i = 3 + 10 ** ( a + ( 4 - 2 ) )                   -> i = pow(10, (a+(4-2))) 
                # i = 3 + ( b - ( 2 - 10 ) ) ** ( a + ( 4 - 2 ) )   -> i = pow((b-(2-10), (a+(4-2))) 
                
                # Check to see if the previous token of the exponentiation operator is a parenthesis.
                self.go_back_token()
                self.goBackTokenCount +=1
                
                while self.currentToken in Resources.whitespaces:
                    self.go_back_token()
                    self.goBackTokenCount += 1
                    
                if self.currentToken == ")": self.prevTokenParenth = True
                
                # Go back to exponentiation operator token
                while self.goBackTokenCount > 0:
                    self.go_next_token()
                    self.goBackTokenCount -= 1
                
                # Check to see if the next token of the exponentiation operator is a parenthesis.
                self.go_next_token()
                self.goNextTokenCount +=1
                
                while self.currentToken in Resources.whitespaces or self.currentToken == "Space":
                    self.go_next_token()
                    self.goNextTokenCount += 1
                    
                if self.currentToken == "(": self.nextTokenParenth = True
                
                # Go back to exponentiation operator token
                while self.goNextTokenCount > 0:
                    self.go_back_token()
                    self.goNextTokenCount -= 1
                
                # Check if there are parentheses
                if self.prevTokenParenth is True or self.nextTokenParenth is True:
                    
                    # Check if the parentheses comes before the exponentiation operator
                    if self.prevTokenParenth is True:
                        self.go_back_token()
                        
                        # Skip whitespaces
                        while self.currentToken in Resources.whitespaces:
                            self.go_back_token()
                            self.removeTokenCount += 1   
                                
                        if self.currentToken == ")":
                            self.parenthCount += 1
                            self.removeTokenCount += 1
                            
                            # Find its pair of opening parenthesis, Go back to the leftmost parenthesis of the operand
                            self.go_back_token()
                            self.removeTokenCount += 1
                            
                            while self.currentToken != "(" or self.parenthCount > 0:
                                # if have a closing parenthesis, decrement parenthcount, else increment parenthcount
                                if self.currentToken == "(":
                                    self.parenthCount -= 1
                                elif self.currentToken == ")":
                                    self.parenthCount += 1
                                # Go back a token if the parenth count is > zero, else the last remaining pair of closing parenthesis is the current token, and no need to go back a token anymore.
                                if self.parenthCount > 0:
                                    self.go_back_token()
                                    self.removeTokenCount +=1
                                    
                            # We get the entire operandOne
                            while self.currentToken != "**":
                                self.operandOne += self.currentToken
                                self.go_next_token()
                            
                            # Check to see if the next token of the exponentiation operator is a parenthesis also.
                            self.go_next_token()
                            
                            while self.currentToken in Resources.whitespaces or self.currentToken == "Space":
                                self.go_next_token()
                                self.goNextTokenCount +=1
                            
                            # If it is a parenthesis, get the entire expression as operandTwo.
                            if self.currentToken == "(":
                                self.parenthCount += 1
                                self.goNextTokenCount += 1
                                
                                # Find its pair of closing parenthesis, Go to the rightmost parenthesis of the operand
                                self.go_next_token()
                                self.goNextTokenCount += 1
                                
                                while self.currentToken != ")" or self.parenthCount > 0:
                                    # if have an opening parenthesis, decrement parenthcount, else increment parenthcount
                                    if self.currentToken == ")":
                                        self.parenthCount -= 1
                                    elif self.currentToken == "(":
                                        self.parenthCount += 1
                                    # Go to next token if the parenth count is > zero, else the last remaining pair of opening parenthesis is the current token, and no need to go next a token anymore.
                                    if self.parenthCount > 0:
                                        self.go_next_token()
                                        self.goNextTokenCount +=1
                                        
                                # Go to exponentiation token
                                while self.currentToken != "**":   
                                    self.go_back_token()
                                
                                # Go to the end point of the operandTwo, while getting the entire operandTwo
                                while self.goNextTokenCount > 0:
                                    self.go_next_token()
                                    if self.currentToken == "Space": 
                                        self.operandTwo += Resources.whitespaces[0]
                                    else:
                                        self.operandTwo += self.currentToken
                                    self.goNextTokenCount -= 1
                                    
                                # Remove operandOne from translatedTokens
                                while self.removeTokenCount > 0:
                                    self.translatedTokens.pop()
                                    self.removeTokenCount -= 1

                                # Construct the expression
                                self.expoString = f"pow({self.operandOne}, {self.operandTwo})"
                                
                                # Append to translatedtokens
                                self.translatedTokens.append([self.expoString, self.expoString])
                                
                                # Go to next token, and reset used variables.
                                self.go_next_token()
                                self.expoString = ""
                                self.operandOne = ""
                                self.operandTwo = ""
                                self.prevTokenParenth = False
                                continue
                            
                            # Else just get operandtwo and append.
                            else: 
                           
                                # We get operandtwo
                                self.operandTwo = self.currentToken
                                
                                # Remove operandOne from translatedTokens
                                while self.removeTokenCount > 0:
                                    self.translatedTokens.pop()
                                    self.removeTokenCount -= 1
                                
                                # Construct the expression
                                self.expoString = f"pow({self.operandOne}, {self.operandTwo})"
                                
                                # Append to translatedtokens
                                self.translatedTokens.append([self.expoString, self.expoString])
                                
                                # Go to next token, and reset used variables.
                                self.go_next_token()
                                self.expoString = ""
                                self.operandOne = ""
                                self.operandTwo = ""
                                self.prevTokenParenth = False
                                continue
                            
                    # If the parentheses come after the exponentiation token.
                    elif self.nextTokenParenth is True:
                        
                        self.go_next_token()
                        
                        # Skip whitespaces
                        while self.currentToken in Resources.whitespaces or self.currentToken == "Space":
                            self.go_next_token()
                            self.goNextTokenCount += 1
                                
                        # If it is a parenthesis, get the entire expression as operandTwo.
                        if self.currentToken == "(":
                            self.parenthCount += 1
                            self.goNextTokenCount += 1
                            
                            # Find its pair of closing parenthesis.
                            self.go_next_token()
                            self.goNextTokenCount += 1

                            while self.currentToken != ")" or self.parenthCount > 0:
                                # if have an opening parenthesis, decrement parenthcount, else increment parenthcount
                                if self.currentToken == ")":
                                    self.parenthCount -= 1
                                elif self.currentToken == "(":
                                    self.parenthCount += 1
                                # Go to next token if the parenth count is > zero, else the last remaining pair of opening parenthesis is the current token, and no need to go next a token anymore.
                                if self.parenthCount > 0:
                                    self.go_next_token()
                                    self.goNextTokenCount +=1
                                    
                            # Go to exponentiation token
                            while self.currentToken != "**":   
                                self.go_back_token()
                                
                            # Go to the end point of the operandTwo, while getting the entire operandTwo  
                            while self.goNextTokenCount > 0:
                                self.go_next_token()
                                if self.currentToken == "Space": 
                                    self.operandTwo += Resources.whitespaces[0]
                                else:
                                    self.operandTwo += self.currentToken
                                self.goNextTokenCount -= 1
                            
                            # Go to exponentiation token
                            while self.currentToken != "**":   
                                self.go_back_token()
                                self.goBackTokenCount +=1
                            
                            # Go to the token before the exponentiation token
                            self.go_back_token()
                            self.goBackTokenCount +=1
                            
                            # Skip whitespaces
                            while self.currentToken in Resources.whitespaces:
                                self.go_back_token()
                                self.goBackTokenCount +=1
                                self.removeTokenCount +=1
                            
                            # Check if the operandone is also a parenthesis expression, if so get the entire operandOne.
                            if self.currentToken == ")":
                                self.parenthCount += 1
                                self.removeTokenCount += 1
                                
                                # Find its pair of opening parenthesis.
                                self.go_back_token()
                                self.removeTokenCount += 1
                                
                                while self.currentToken != "(" or self.parenthCount > 0:
                                    # if have a closing parenthesis, decrement parenthcount, else increment parenthcount
                                    if self.currentToken == "(":
                                        self.parenthCount -= 1
                                    elif self.currentToken == ")":
                                        self.parenthCount += 1
                                    # Go back a token if the parenth count is > zero, else the last remaining pair of closing parenthesis is the current token, and no need to go back a token anymore.
                                    if self.parenthCount > 0:
                                        self.go_back_token()
                                        self.removeTokenCount +=1
                                        
                                # We get the entire operandOne
                                while self.currentToken != "**":
                                    self.operandOne += self.currentToken
                                    self.go_next_token()

                                # Remove operandOne from translatedTokens
                                while self.removeTokenCount > 0:
                                    self.translatedTokens.pop()
                                    self.removeTokenCount -= 1
                                    
                                # Return to the end point of the operandTwo
                                while self.goBackTokenCount > 0:
                                    self.go_next_token()
                                    self.goBackTokenCount -= 1

                                # Construct the expression
                                self.expoString = f"pow({self.operandOne}, {self.operandTwo})"
                                
                                # Append to translatedtokens
                                self.translatedTokens.append([self.expoString, self.expoString])

                                # Go to next token, and reset used variables.
                                self.go_next_token()
                                self.expoString = ""
                                self.operandOne = ""
                                self.operandTwo = ""
                                self.nextTokenParenth = False
                                continue
                                
                            else: 
                                self.removeTokenCount += 1   
                                        
                                # We get operandone
                                self.operandOne = self.currentToken
                                
                                # Remove operandOne from translatedTokens
                                while self.removeTokenCount > 0:
                                    self.translatedTokens.pop()
                                    self.removeTokenCount -= 1
                                
                                # Construct the expression
                                self.expoString = f"pow({self.operandOne}, {self.operandTwo})"
                                
                                # Append to translatedtokens
                                self.translatedTokens.append([self.expoString, self.expoString])
                                
                                # Return to the end point of the operandTwo
                                while self.goBackTokenCount > 0:
                                    self.go_next_token()
                                    self.goBackTokenCount -= 1
                                
                                # Go to next token, and reset used variables.
                                self.go_next_token()
                                self.expoString = ""
                                self.operandOne = ""
                                self.operandTwo = ""
                                self.nextTokenParenth = False
                                continue 
                
                # No parenthesis in this expression
                else:
                    
                    # Go back to the token before the exponentiation operator
                    self.go_back_token()
                    self.removeTokenCount += 1
                    
                    # If whitespace, skip until token is reached.
                    while self.currentToken in Resources.whitespaces:
                        self.go_back_token()
                        self.removeTokenCount += 1
                    
                    # Store the operandone
                    self.operandOne = self.tokens[self.tokenIndex][0]
                    
                    # Go back to exponentiation operator
                    while self.currentToken != "**":   
                        self.go_next_token()
                    
                    # Go to the token after the exponentiation operator
                    self.go_next_token()
                    
                    # If whitespace, skip until token is reached.
                    while self.currentToken in Resources.whitespaces or self.currentToken == "Space":
                        self.go_next_token()
                    
                    # Store the operandtwo
                    self.operandTwo = self.tokens[self.tokenIndex][0]
                    
                    # Remove operandOne from translatedTokens
                    while self.removeTokenCount > 0:
                        self.translatedTokens.pop()
                        self.removeTokenCount -= 1
                    
                    # Construct the expression
                    self.expoString = f"pow({self.operandOne}, {self.operandTwo})"
                    
                    # Append to translatedtokens
                    self.translatedTokens.append([self.expoString, self.expoString])
                    
                    self.go_next_token()
                    self.expoString = ""
                    self.operandOne = ""
                    self.operandTwo = ""
                    continue
                
            # If current token is Disp, pad it with an "endl" before the terminator so that line buffering is implmemented and it is flushed in the stdout. 
            # This is so that when StellarSynthcompiler runs the exectuable, it properly knows the end of each line because "endl" adds a newline at end of each disp and flushes it to the stdout.
            # This condition will only evaluate to True if we curToken is Disp and isDisp is false meaning we just encountered it, or isDisp is true, and curToken is # meaning we have reached the end of the statement and just need to pad it.
            elif (self.currentToken == "Disp" and self.isDisp is False) or (self.isDisp is True and self.currentToken == "#"):
                
                # We have encountered a disp statement, set isDisp to true so that we pad endl before the terminator of this statement.
                if self.currentToken == "Disp" and self.isDisp is False:
                    self.isDisp = True
                    continue
                # We reached the terminator of this Disp statement. Now all we have to do is pad it.
                elif (self.isDisp is True and self.currentToken == "#"):
                    # append the endl
                    self.translatedTokens.append(["<< endl","<< endl"])
                    # append the teminator
                    self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = Resources.StellarCPlusPlusDict[self.currentToken] 
                    self.translatedTokens.append(self.tokens[self.tokenIndex])
                    
                    # go next token and set isDisp to false.
                    self.go_next_token()
                    
                    self.isDisp = False
                    continue
            # if current token is a Capt token, a request for input is needed. Send a string to signal StellarSynth compiler that input awaits.
            elif (self.currentToken == "Capt" and self.isCapt is False):
                self.isCapt = True
                self.translatedTokens.append([f"cout << \"{Resources.inputSignal}\" << endl;\n"])
                continue
                
            # Set Sun as int instead of long long
            elif self.currentToken == "Universe" and self.mainfuncFlag == False:                 
                # Go back to the Sun Token.
                while self.currentToken != "long long":
                    self.go_back_token()
                    self.goBackTokenCount += 1
                
                # We have reached sun Token, pop all translated tokens until Sun
                for i in range(self.goBackTokenCount):
                    self.translatedTokens.pop()
                else:
                    #  Set Sun to int and append
                    self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = "int"
                    self.translatedTokens.append(self.tokens[self.tokenIndex])
                    
                self.go_next_token()
                
                # Go back to universe token, appending token to translated if not universe token.
                while self.currentToken != "Universe":
                    self.translatedTokens.append(self.tokens[self.tokenIndex])
                    self.go_next_token()
                    
                # We have reached universe token, append and go next token.
                self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = Resources.StellarCPlusPlusDict[self.currentToken]
                self.translatedTokens.append(self.tokens[self.tokenIndex])
                self.go_next_token()
                
                self.goBackTokenCount = 0
                self.mainfuncFlag = True
                continue
                  
            # Replace StellarSynth Token with its C++ Counterpart.
            elif self.currentToken in Resources.StellarCPlusPlusDict:
                # If it is a string typecast operator, convert datatype Starsys to 'to_string' then append to translated tokens.
                if self.currentToken == "Starsys":
                    self.go_next_token()
                    if self.currentToken == "(":
                        self.go_back_token()
                        
                        self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = "to_string" 
                        self.translatedTokens.append(self.tokens[self.tokenIndex])
                        self.go_next_token()
                        continue
                    # If it isn't just append the translated counterpart to translated tokens.
                    else:
                        self.go_back_token()
                        self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = Resources.StellarCPlusPlusDict[self.currentToken] 
                        self.translatedTokens.append(self.tokens[self.tokenIndex])
                        self.go_next_token()
                        continue
                else:
                    # getline method 
                    if self.currentToken == "Capt" and self.isCapt == True:
                        tempvar = "iss "
                        tempidentlist = []
                                              
                        while self.currentToken != "#":
                            self.go_next_token()
                            if self.tokens[self.tokenIndex][1][0:10] == "Identifier":
                                self.identCount += 1
                                tempidentlist.append(self.currentToken)
                        
                        while self.currentToken != "Capt":
                            self.go_back_token()
                                
                        # if multiple variables, separates by space.
                        if len(tempidentlist) > 1:
                            # getline(cin, line); append to translated tokens
                            self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = Resources.StellarCPlusPlusDict[self.currentToken] 
                            self.translatedTokens.append(self.tokens[self.tokenIndex])
                            
                            # istringstream iss(line); append to translated tokens
                            self.translatedTokens.append([Resources.getlineDistribStatement])
                            
                            for i in range(self.identCount):
                                tempvar += f">> {tempidentlist[i]}"
                            tempvar += ";"
                            # iss >> ident1 >> ident2 >> ident3 append to translated tokens
                            self.translatedTokens.append([tempvar])
                        # if one variable string only, gets entire line.
                        else:
                            # getline(cin, <ident>); append to translated tokens
                            self.tokens[self.tokenIndex][0] = self.tokens[self.tokenIndex][1] = f"getline(cin, {tempidentlist[0]});\n" 
                            self.translatedTokens.append([f"getline(cin, {tempidentlist[0]});\n"])
                        
                        while self.currentToken != "#":
                                self.go_next_token()
                            
                        self.isCapt = False
                        tempvar = None
                        tempidentlist = None
                        self.identCount = 0
                        self.go_next_token()
                        continue     
                
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
        convertedcppCode = ''
        
        # Initialize with some needed headers.
        for header in Resources.headerInclude:
            convertedcppCode += header
            
        # Concatenate all translatedtokens to the cppCode string
        while self.translatedTokensIndex < (len(self.translatedTokens)-1):
            convertedcppCode += self.translatedTokens[self.translatedTokensIndex][0]
            self.translatedTokensIndex +=1
        
        # Write the convertedCppCode to a cpp file named after the file, or "Output.cpp" if file is not opened or saved in compiler.
        if self.filename is None:
            self.f_cpp = "Output.cpp"
            directory = '.\\cpp\\Output\\'
            f_exec = '.\\cpp\\Output\\Output.exe'
        else:
            self.f_cpp = self.filename+".cpp"
            directory = '.\\cpp\\' + self.filename + "\\"
            f_exec = directory + self.filename + ".exe"      

        file_path = os.path.join(directory, self.f_cpp)

        # If directory doesn't exist, make one.
        if not os.path.isdir(directory):
            os.makedirs(directory)  # Create parent directories if necessary

        # Write the cpp file into its folder under cpp folder.
        with open(file_path, 'w+') as fout:
            fout.write(convertedcppCode)
            
        # Compile the program and create exe into its folder under cpp folder.
        compile_cmd = "g++ -std=c++20 {} -o {}".format(file_path, f_exec)
        subprocess.call(compile_cmd, shell=True)

        # Generate the Gimple Representation into its folder under cpp folder.
        gimple_file_path = os.path.splitext(file_path)[0] + ".s"
        gimple_cmd = "g++ -fdump-tree-gimple -c {} -o {}".format(file_path, gimple_file_path)
        subprocess.call(gimple_cmd, shell=True)
        
        return f_exec
    
        """
        This part of the program does not accept input, only outputs. If you want this, Remove return f_exec. and modify lines 450-464 in compiler2.
        
        # Run the program
        try:
            p = subprocess.Popen(f_exec, shell=True,
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                 text=True, bufsize=1)
        except Exception as e:
            print("Error executing subprocess:", e)

        # Everything from line 158 to 173 is temporary, as the inputting and outputting haven't been finalized yet. This method only accepts input once and runs the program after.
        # If no input, comment lines 158 - 162 and run.
        # Read input from console
        #input_variables = input("Enter input variables: ") 

        # Provide input to the process
        #p.stdin.write(input_variables.encode())
        #p.stdin.flush()
        
        try:
            # Read the output from stdout and stderr
            error, output = p.communicate()

            # Decode output to readable string
            error = error.decode()
            output = output.decode()
        except Exception as e:
            print("Error communicating with subprocess:", e)
        
        # Return output to Compiler
        return output, error"""
        

if __name__ == "__main__":
    errors, tokens = Lexer.read_text('StellarSynth')
    transpilerInstance = Transpiler(tokens, None)
    transpilerInstance.stellarTranslator()
    transpilerInstance.writetoCPPFile()
    

""" 
Algorithm:
1. Translate StellarSynth to C++
2. Write C++ to cpp file, writing the necessary headers and namespaces.
3. Run CPP File in StellarSynthCompiler
"""  

