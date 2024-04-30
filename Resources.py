
# Lexer

# Regular Definitions
LowerAlpha =            [chr(x) for x in range(97, 123)] #a-z String List
UpperAlpha =            [chr(x) for x in range(65, 91)] #A-Z String List
ComAlpha =              LowerAlpha + UpperAlpha
IdentifierUpperAlpha =  ['E', 'H', 'J', 'K', 'M', 'U', 'W', 'X', 'Y', 'Z']
DigitsNoZero =          [str(x) for x in range(1,10) ] #1-9 String List
Zero =                  ['0']
DigitsWithZero =        Zero + DigitsNoZero
AlphaNum =              DigitsWithZero + ComAlpha
TruthValues =           ["True", "False"]
AssignOp =              ['=']
RelOp =                 ['==','!=','<','>','>=','<=']
MathOp =                ['+','-','*','/','%']
LogOp =                 ['&&', '||', '!']
InpOutOp =              [">>", "<<"]
ExpoOp =                ["**"]
Operators =             AssignOp + RelOp + MathOp + LogOp + InpOutOp + ExpoOp
Minus =                 ['-']
LParenth =              ['(']
RParenth =              [')']
LSqrBrkt =              ['[']
RSqrBrkt =              [']']
LCurBrace =             ['{']
RCurBrace =             ['}']
RegDblQtMark =          ['\"']
RegSglQtMark =          ['\'']
RegQtMarks =            ['\"','\'']
Terminator =            ['#']
CommSym =               ['$']
Ampersand =             ['&']
Comma =                 [',']
Period =                ['.']
Colon =                 [':']
SemiColon =             [';']
ExclaMark =             ['!']
LessThan =              ['<']
GreaterThan =           ['>']
QstMark =               ['?']
AtMark =                ['@']
Caret =                 ['^']
UnderScore =            ['_']
BackTick =              ['`']
VerticalBar =           ['|']
Tilde =                 ['~']
Newline =               ['\n']
Tab =                   ['\t']
Null =                  ['λ']
Space =                 [" "]
PrintableChar =         AlphaNum + Space + Comma + Period + ['!', '\"', '#', '$', '%', '&', '\'', '(',
                                                             ')', '*', '+', '-', '/', ':', ';', '<', '=', '>',
                                                             '?', '@', '[', '\\', ']', '^', '_', '`', '{',
                                                             '|', '}', '~']

# Delimiters
sdelim =                Space + Tab + Newline
delim1 =                Space + Tab + Newline + LParenth
delim2 =                Space + Tab + Newline + Terminator
delim3 =                [] # Not in use
delim4 =                Space + Tab + Newline + GreaterThan
delim5 =                Space + Tab + Newline + LessThan
delim6 =                Space + Tab + Newline + LSqrBrkt
delim7 =                Space + Tab + Newline + LParenth + AlphaNum
delim8 =                Space + Tab + Newline + Terminator + ComAlpha + RParenth
delim9 =                Space + Tab + Newline
delim10 =               Space + Tab + Newline + LParenth + LSqrBrkt + Terminator
delim11 =               Space + Tab + Newline + ComAlpha
delim12 =               Space + Tab + Newline + LParenth + ComAlpha + AssignOp
delim13 =               Space + Tab + Newline + LParenth + AlphaNum + RParenth + ExclaMark + Minus + RegDblQtMark + RegSglQtMark
delim14 =               Space + Tab + Newline + Terminator + MathOp + LSqrBrkt + Ampersand + VerticalBar + LessThan + GreaterThan + AssignOp + RParenth + Comma + ["G"]
delim15 =               Space + Tab + Newline + RegSglQtMark + RegDblQtMark + AlphaNum + LSqrBrkt + RSqrBrkt
delim16 =               Space + Tab + Newline + Terminator + ComAlpha + RSqrBrkt + Comma
delim17 =               Space + Tab + Newline + AlphaNum + RegSglQtMark + RegDblQtMark + LSqrBrkt
delim18 =               PrintableChar + Tab + Newline # Unused, Was used for \' and \" delims and $ Delimiter
delim19 =               Space + Tab + Newline + AlphaNum + RCurBrace
delim20 =               Space + Tab + Newline + Terminator + AssignOp + LCurBrace + GreaterThan + LessThan + MathOp + RParenth + Comma
delim21 =               [x for x in PrintableChar if x not in RegQtMarks and x != 'n'] + Newline + Tab # Unused, formerly used for chars  that come after in string \ except n, ', "
delim22 =               Space + Tab + Newline + UpperAlpha + LSqrBrkt
delim23 =               Space + Tab + Newline + RParenth
delim24 =               Space + Tab + Newline + AlphaNum + LParenth + RegSglQtMark + RegDblQtMark
delim25 =               Space + Tab + Newline + Colon
delim26 =               Space + Tab + Newline + ComAlpha + RSqrBrkt + RParenth
delim27 =               PrintableChar + Newline + Tab # Not in use

Sun_delim =             (Space + Tab + Newline + RParenth + RCurBrace + RSqrBrkt + Terminator + Comma +
                        Ampersand + VerticalBar + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan + Tab + LSqrBrkt + Colon)
Luhman_delim =          (Space + Tab + Newline + RParenth + RSqrBrkt + Terminator + Comma + Ampersand + VerticalBar
                        + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan)
Starsys_delim =         Space + Tab + Newline + RParenth + Comma + Terminator + LessThan + RSqrBrkt + Colon
Boolean_delim =         Space + Tab + Newline + Terminator + RParenth + Ampersand + VerticalBar + ExclaMark + Comma + RSqrBrkt + Colon
Identifier_delim =      (Space + Tab + Newline + Terminator + LParenth + RParenth + LCurBrace + RSqrBrkt + MathOp
                        + Ampersand + VerticalBar + ExclaMark + AssignOp + GreaterThan + LessThan + Comma + Period + Colon + Tilde + LSqrBrkt + RCurBrace)

WordSymbolDelims =      {
                        "Autom":        sdelim,
                        "Boolean":      delim1,
                        "Capt":         delim4,
                        "Class":        sdelim,
                        "Deviate":      delim2,
                        "Disintegrate": delim9,
                        "Disp":         delim5,
                        "Divert":       delim1,
                        "False":        Boolean_delim,
                        "Fore":         delim1,
                        "Formulate":    delim9,
                        "Gotolerate":   delim10,
                        "If":           delim1,
                        "ISS":          sdelim,
                        "Import":       sdelim,
                        "Latch":        delim1,
                        "Launch":       sdelim,
                        "Luhman":       delim1,
                        "Nominal":      delim25,
                        "Other":        delim6,
                        "Perform":      delim6,
                        "Private":      delim25,
                        "Proceed":      delim2,
                        "Protected":    delim25,
                        "Public":       delim25,
                        "Retrieve":     delim2,
                        "Scenario":     sdelim,
                        "Span":         delim1,
                        "Starsys":      delim1,
                        "Static":       sdelim,
                        "Sun":          delim1,
                        "Test":         delim6,
                        "True":         Boolean_delim,
                        "Void":         delim23,
                        "=":            delim24,
                        "==":           delim24,
                        "!=":           delim24,
                        "<":            delim24,
                        ">":            delim24,
                        "<=":           delim24,
                        ">=":           delim24,
                        "<<":           delim24,
                        ">>":           delim7,
                        "+":            delim7,
                        "++":           delim8,
                        "-":            delim7,
                        "--":           delim8,
                        "*":            delim7,
                        "**":           delim7,
                        "/":            delim7,
                        "%":            delim7,
                        "&&":           delim7,
                        "||":           delim7,
                        "!":            delim12,
                        "(":            delim13,
                        ")":            delim14,
                        "[":            delim15,
                        "]":            delim16,
                        ",":            delim17,
                        "{":            delim19,
                        "}":            delim20,
                        "#":            delim26,
                        ".":            AlphaNum,
                        ":":            delim22,
                        "::":           ComAlpha,
                        "~":            delim11,
                        "Identifier":   Identifier_delim,
                        "SunLiteral":   Sun_delim,
                        "LuhmanLiteral": Luhman_delim,
                        "StarsysLiteral": Starsys_delim,
                        "Comment":      Newline
                    }

# Syntax

Datatype = ["Sun", "Luhman", "Starsys"]
Datatype1 = "Boolean"
Datatype2 = ["Sun", "Luhman", "Starsys","Boolean"]
Datatype3 = ["Sun", "Luhman"]
Value = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral", "Identifier"]
Value1 = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral", "Identifier", "True", "False"]
Value2 = ["SunLiteral", "LuhmanLiteral", "Identifier"]
Value3 = ["SunLiteral", "Identifier"]
Value4 = ["SunLiteral", "LuhmanLiteral", "True", "False"]
Value5 = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral"]
Value6 = ["StarsysLiteral", "True", "False"]
bool_lit = ["True", "False"]
mathop = ["+","-","*","/", "%", "**"]
mathop1 = ["+","-","*","/", "%"]
condop = ["==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "+", "-", "*", "/", "%"]
loopup = ["++", "--"]
loopbrkcont = ["Deviate", "Proceed"]
ret_str_bool = ["StarsysLiteral", "True", "False"]
access_specifier = ["Public", "Private", "Protected"]


# Semantic
dataTypes = ["Sun", "Luhman", "Boolean", "Void", "Starsys"]
dataTypes_var = ["Sun", "Luhman", "Boolean", "Starsys"]
assignable_values = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral", "Identifier", "True", "False"]
variableAcceptedValues = {
    "Sun"       : ["SunLiteral", "Identifier"],
    "Luhman"    : ["LuhmanLiteral", "Identifier"],
    "Starsys"    : ["StarsysLiteral", "Identifier"],
    "Boolean"    : ["True", "False", "Identifier"],
}

# Three Address Code
whitespace = ["Space", "\t", "\n"]
conditionalStart = ["If", "Else", "Else If"]
iterativeStart = ["Fore", "Span", "Perform"]

defaultvalueDict= {"Sun"    : 0,
                   "Luhman" : 0.0,
                   "Boolean": False,
                   "Starsys": ""}

# Transpiler
StellarCPLusPlusDict = {
    "Autom"         : "auto",
    "Boolean"       : "bool",
    "Deviate"       : "break",
    "Scenario"      : "case",
    "Latch"         : "catch",
    "Class"         : "class", 
    "Static"        : "const",
    "Proceed"       : "continue",
    "Nominal"       : "default",
    "Perform"       : "do",
    "Other"         : "else",
    "False"         : "false",
    "Luhman"        : "float",
    "Fore"          : "for",
    "If"            : "if",
    "Import"        : "import", # Python style import not c++
    "Sun"           : "int",
    "Gotolerate"    : "noexcept",
    "Private"       : "private",
    "Protected"     : "protected",
    "Public"        : "public",
    "Retrieve"      : "return",
    "ISS"           : "struct", # 
    "Divert"        : "switch",
    "Launch"        : "throw", # Exceptions thrown is class of c++ std
    "True"          : "true",
    "Test"          : "try",
    "Void"          : "void",
    "Span"          : "span",
    "Starsys"       : "string", # STD Library
    "Capt"          : "cin", # STD Library
    "Disp"          : "cout", # STD Library
}