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
Operators =             AssignOp + RelOp + MathOp + LogOp + InpOutOp
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
G = ["G"] # for delim 14, Rparenth uses this: subfunc()Gotolerate

# Delimiters
sdelim =                Space
delim1 =                Space + LParenth + RParenth
delim2 =                Space + Terminator
delim3 =                Colon
delim4 =                Space + GreaterThan
delim5 =                Space + LessThan
delim6 =                Space + LSqrBrkt
delim7 =                Space + LParenth + AlphaNum
delim8 =                Space + Terminator + ComAlpha + RParenth
delim9 =                Space + Newline
delim10 =               Space + LParenth + LSqrBrkt + Terminator
delim11 =               Space + ComAlpha
delim12 =               Space + LParenth + ComAlpha + AssignOp
delim13 =               Space + LParenth + AlphaNum + RParenth + ExclaMark + Minus + RegDblQtMark + RegSglQtMark
delim14 =               Space + Terminator + MathOp + LSqrBrkt + Ampersand + VerticalBar + LessThan + GreaterThan + AssignOp + Newline + Comma + RParenth + G
delim15 =               Space + Newline + RegSglQtMark + RegDblQtMark + AlphaNum + LSqrBrkt + RSqrBrkt
delim16 =               Space + Newline + Terminator + ComAlpha + RSqrBrkt + Comma
delim17 =               Space + AlphaNum + RegSglQtMark + RegDblQtMark + LSqrBrkt
delim18 =               PrintableChar + Newline + RParenth
delim19 =               Space + AlphaNum + RCurBrace
delim20 =               Space + Terminator + AssignOp + LCurBrace + GreaterThan + LessThan + MathOp + RParenth
delim21 =               [x for x in PrintableChar if x not in RegQtMarks and x != 'n'] + Newline
delim22 =               Space + Newline + UpperAlpha
delim23 =               Space + RParenth
delim24 =               Space + AlphaNum + LParenth + RegSglQtMark + RegDblQtMark
delim25 =               Space + Colon
delim26 =               Space + ComAlpha + Newline + RSqrBrkt + RParenth
delim27 =               PrintableChar + Newline + Tab

Sun_delim =             (Space + RParenth + RCurBrace + RSqrBrkt + Terminator + Comma +
                        Ampersand + VerticalBar + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan)
Luhman_delim =          (Space + RParenth + RSqrBrkt + Terminator + Comma + Ampersand + VerticalBar
                        + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan)
Starsys_delim =         Space + RParenth + Comma + Terminator + LessThan
Boolean_delim =         Space + Terminator + RParenth + Ampersand + VerticalBar + ExclaMark + Comma + RSqrBrkt 
Identifier_delim =      (Space + Terminator + LParenth + RParenth + LCurBrace + RSqrBrkt + MathOp
                        + Ampersand + VerticalBar + ExclaMark + AssignOp + GreaterThan + LessThan + Comma + Period + Colon + Tilde + LSqrBrkt + Newline + RCurBrace)

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
                        "ISS":          delim6,
                        "Import":       sdelim,
                        "Latch":        delim1,
                        "Launch":       sdelim,
                        "Luhman":       delim1,
                        "Navgto":       sdelim,
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
                        "\n":           delim27,
                        "\t":           delim27,
                        "(":            delim13,
                        ")":            delim14,
                        "[":            delim15,
                        "]":            delim16,
                        ",":            delim17,
                        "$":            delim18,
                        "{":            delim19,
                        "}":            delim20,
                        "#":            delim26,
                        "\"":           delim18,
                        "\'":           delim18,
                        "\\":           delim21,
                        ".":            AlphaNum,
                        ":":            delim22,
                        "::":           ComAlpha,
                        "~":            delim11,
                        "Identifier":   Identifier_delim,
                        "SunLiteral":   Sun_delim,
                        "LuhmanLiteral": Luhman_delim,
                        "StarsysLiteral": Starsys_delim,
                        "Space":        delim27
                    }

Datatype = ["Sun", "Luhman", "Starsys"]
Datatype1 = "Boolean"
Datatype2 = ["Sun", "Luhman", "Starsys","Boolean"]
Datatype3 = ["Sun", "Luhman"]
Value = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral", "Identifier"]
Value1 = ["SunLiteral", "LuhmanLiteral", "StarsysLiteral", "Identifier", "True", "False"]
Value2 = ["SunLiteral", "LuhmanLiteral", "Identifier"]
Value3 = ["SunLiteral", "Identifier"]
bool_lit = ["True", "False"]
mathop = ["+","-","*","/", "%", "**"]
condop = ["==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "+", "-", "*", "/", "%"]
loopup = ["++", "--"]
loopbrkcont = ["Deviate", "Proceed"]
