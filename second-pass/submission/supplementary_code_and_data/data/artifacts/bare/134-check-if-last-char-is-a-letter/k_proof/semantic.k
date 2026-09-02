requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= Stmt
                 | Stmt Stmts

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Bool" "(" Bool ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BoolOp" "(" String "," Exprs ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Expr ")"
                | "Attribute" "(" Expr "," String ")"
                | "Call" "(" Expr "," Exprs ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports MAP
  imports STRING

  syntax PyVal ::= pyBool(Bool)
                 | pyInt(Int)
                 | pyStr(String)

  syntax PyVal ::= eval(Expr, Map) [function]
  syntax PyVal ::= evalUnary(String, PyVal) [function]
  syntax PyVal ::= evalBool2(String, PyVal, PyVal) [function]
  syntax PyVal ::= evalBool3(String, PyVal, PyVal, PyVal) [function]
  syntax PyVal ::= evalCompare(String, PyVal, PyVal) [function]
  syntax PyVal ::= evalLen(PyVal) [function]
  syntax PyVal ::= evalIsAlpha(PyVal) [function]
  syntax PyVal ::= evalSubscript(PyVal, PyVal) [function]

  syntax Bool ::= isAlphaString(String) [function]
                | isAlphaChars(String, Int) [function]
                | isLetterChar(String) [function]
  syntax String ::= atString(String, Int) [function]

  configuration
    <python>
      <k> $PGM:Program ~> runEntry("check_if_last_char_is_a_letter", $TXT:String) </k>
    </python>

  syntax KItem ::= runEntry(String, String)

  rule <k> Module(FuncDef(F, Params(P:String), Return(E))) ~> runEntry(F, S)
         => eval(E, P |-> pyStr(S))
       ... </k>

  rule eval(Bool(B), _) => pyBool(B)
  rule eval(Int(I),  _) => pyInt(I)
  rule eval(Str(S),  _) => pyStr(S)
  rule eval(Name(N), ENV) => {ENV[N]}:>PyVal
    requires N in_keys(ENV)

  rule eval(UnaryOp(OP, E), ENV) => evalUnary(OP, eval(E, ENV))
  rule evalUnary("-", pyInt(I)) => pyInt(0 -Int I)

  rule eval(BoolOp(OP, E1, E2), ENV)
    => evalBool2(OP, eval(E1, ENV), eval(E2, ENV))
  rule eval(BoolOp(OP, E1, E2, E3), ENV)
    => evalBool3(OP, eval(E1, ENV), eval(E2, ENV), eval(E3, ENV))
  rule evalBool2("and", pyBool(B1), pyBool(B2)) => pyBool(B1 andBool B2)
  rule evalBool2("or",  pyBool(B1), pyBool(B2)) => pyBool(B1 orBool B2)
  rule evalBool3("and", pyBool(B1), pyBool(B2), pyBool(B3))
    => pyBool(B1 andBool B2 andBool B3)
  rule evalBool3("or", pyBool(B1), pyBool(B2), pyBool(B3))
    => pyBool(B1 orBool B2 orBool B3)

  rule eval(Compare(E1, CmpOp(OP, E2)), ENV)
    => evalCompare(OP, eval(E1, ENV), eval(E2, ENV))
  rule evalCompare("==", pyInt(I1), pyInt(I2)) => pyBool(I1 ==Int I2)
  rule evalCompare("==", pyStr(S1), pyStr(S2)) => pyBool(S1 ==String S2)
  rule evalCompare(">",  pyInt(I1), pyInt(I2)) => pyBool(I1 >Int I2)

  rule eval(Call(Name("len"), E), ENV) => evalLen(eval(E, ENV))
  rule evalLen(pyStr(S)) => pyInt(lengthString(S))

  rule eval(Call(Attribute(E, "isalpha"), .Exprs), ENV)
    => evalIsAlpha(eval(E, ENV))
  rule evalIsAlpha(pyStr(S)) => pyBool(isAlphaString(S))

  rule eval(Subscript(E1, E2), ENV)
    => evalSubscript(eval(E1, ENV), eval(E2, ENV))
  rule evalSubscript(pyStr(S), pyInt(I)) => pyStr(atString(S, I))

  rule atString(S, I) => substrString(S, I, I +Int 1)
    requires I >=Int 0
  rule atString(S, I) => substrString(S,
                                      lengthString(S) +Int I,
                                      lengthString(S) +Int I +Int 1)
    requires I <Int 0

  rule isAlphaString("") => false
  rule isAlphaString(S) => isAlphaChars(S, 0)
    requires lengthString(S) >Int 0

  rule isAlphaChars(S, I) => true
    requires I >=Int lengthString(S)
  rule isAlphaChars(S, I)
    => isLetterChar(substrString(S, I, I +Int 1))
       andBool isAlphaChars(S, I +Int 1)
    requires I >=Int 0 andBool I <Int lengthString(S)

  // The benchmark's alphabetic-character domain.  This explicit definition
  // avoids the unavailable STRING.category hook in the Haskell prover.
  rule isLetterChar(C)
    => lengthString(C) ==Int 1
       andBool findString("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
                          C,
                          0) >=Int 0
endmodule
