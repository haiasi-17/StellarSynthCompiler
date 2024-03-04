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
sdelim =                Space + Tab
delim1 =                Space + Tab + LParenth
delim2 =                Space + Tab + Terminator
delim3 =                [] # Not in use
delim4 =                Space + Tab + GreaterThan
delim5 =                Space + Tab + LessThan
delim6 =                Space + Tab + LSqrBrkt
delim7 =                Space + Tab + LParenth + AlphaNum
delim8 =                Space + Tab + Terminator + ComAlpha + RParenth
delim9 =                Space + Tab + Newline
delim10 =               Space + Tab + LParenth + LSqrBrkt + Terminator
delim11 =               Space + Tab + ComAlpha
delim12 =               Space + Tab + LParenth + ComAlpha + AssignOp
delim13 =               Space + Tab + LParenth + AlphaNum + RParenth + ExclaMark + Minus + RegDblQtMark + RegSglQtMark
delim14 =               Space + Tab + Terminator + MathOp + LSqrBrkt + Ampersand + VerticalBar + LessThan + GreaterThan + AssignOp + Newline + RParenth + Comma + ["G"]
delim15 =               Space + Tab + Newline + RegSglQtMark + RegDblQtMark + AlphaNum + LSqrBrkt + RSqrBrkt
delim16 =               Space + Tab + Newline + Terminator + ComAlpha + RSqrBrkt + Comma
delim17 =               Space + Tab + AlphaNum + RegSglQtMark + RegDblQtMark + LSqrBrkt
delim18 =               PrintableChar + Tab + Newline # Unused, Was used for \' and \" delims and $ Delimiter
delim19 =               Space + Tab + AlphaNum + RCurBrace
delim20 =               Space + Tab + Terminator + AssignOp + LCurBrace + GreaterThan + LessThan + MathOp + RParenth
delim21 =               [x for x in PrintableChar if x not in RegQtMarks and x != 'n'] + Newline + Tab # Formerly used for chars  that come after in string \ except n, ', "
delim22 =               Space + Tab + Newline + UpperAlpha + LSqrBrkt
delim23 =               Space + Tab + RParenth
delim24 =               Space + Tab + AlphaNum + LParenth + RegSglQtMark + RegDblQtMark
delim25 =               Space + Tab + Colon
delim26 =               Space + Tab + ComAlpha + Newline + RSqrBrkt + RParenth
delim27 =               PrintableChar + Newline + Tab # Not in use

Sun_delim =             (Space + RParenth + RCurBrace + RSqrBrkt + Terminator + Comma +
                        Ampersand + VerticalBar + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan + Tab + LSqrBrkt)
Luhman_delim =          (Space + RParenth + RSqrBrkt + Terminator + Comma + Ampersand + VerticalBar
                        + ExclaMark + MathOp + AssignOp + GreaterThan + LessThan + Tab)
Starsys_delim =         Space + RParenth + Comma + Terminator + LessThan + RSqrBrkt + Tab
Boolean_delim =         Space + Terminator + RParenth + Ampersand + VerticalBar + ExclaMark + Comma + RSqrBrkt + Tab
Identifier_delim =      (Space + Terminator + LParenth + RParenth + LCurBrace + RSqrBrkt + MathOp
                        + Ampersand + VerticalBar + ExclaMark + AssignOp + GreaterThan + LessThan + Comma + Period + Colon + Tilde + LSqrBrkt + Newline + RCurBrace + Tab)

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
                        "ISS":          delim2,
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
