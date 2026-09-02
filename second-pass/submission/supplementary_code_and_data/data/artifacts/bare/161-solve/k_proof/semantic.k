// A deliberately small Python semantics for the constructor subset emitted by
// solution.py.  Python strings are represented as lists of Unicode code points;
// the case operations below cover the ASCII letters used by the HumanEval task.

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Exprs ::= List{Expr, ","}
  syntax Params ::= "Params" "(" String ")"

  syntax Expr ::= "Name"       "(" String ")"
                | "Str"        "(" String ")"
                | "Bool"       "(" Bool ")"
                | "Int"        "(" Int ")"
                | "UnaryOp"    "(" String "," Expr ")"
                | "Attribute"  "(" Expr "," String ")"
                | "Call"       "(" Expr "," Exprs ")"
                | "IfExp"      "(" Expr "," Expr "," Expr ")"
                | "GenExp"     "(" Expr "," CompFor ")"
                | "Subscript"  "(" Expr "," SliceSpec ")"

  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax SliceBound ::= "NoBound" | Expr
  syntax SliceSpec ::= "Slice" "(" SliceBound "," SliceBound "," SliceBound ")"

  syntax Stmt ::= "Return"  "(" Expr ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
  syntax Stmts ::= List{Stmt, ""}
  syntax Program ::= "Module" "(" Stmts ")"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  // Inductive Python-string values.  pstr is a concrete-input convenience;
  // symbolic proofs quantify directly over PString.
  syntax PString ::= ".PString"
                   | Int "::" PString
                   | "pstr" "(" String ")" [function]
  syntax PString ::= "pstrAt" "(" String "," Int ")" [function]

  rule pstr(S) => pstrAt(S, 0)
  rule pstrAt(S, I) => .PString
    requires I >=Int lengthString(S)
  rule pstrAt(S, I) => ordChar(substrString(S, I, I +Int 1)) :: pstrAt(S, I +Int 1)
    requires I <Int lengthString(S)

  // Character classification and case reversal.
  syntax Bool ::= "isAlpha" "(" Int ")" [function, total]
  rule isAlpha(C) => (C >=Int 65 andBool C <=Int 90)
                     orBool (C >=Int 97 andBool C <=Int 122)

  syntax Int ::= "toggle" "(" Int ")" [function, total]
  rule toggle(C) => C +Int 32
    requires C >=Int 65 andBool C <=Int 90
  rule toggle(C) => C -Int 32
    requires C >=Int 97 andBool C <=Int 122
  rule toggle(C) => C
    requires notBool isAlpha(C)

  syntax Bool ::= "hasAlpha" "(" PString ")" [function, total]
  rule hasAlpha(.PString) => false
  rule hasAlpha(C :: S) => isAlpha(C) orBool hasAlpha(S)

  syntax PString ::= "swapCase" "(" PString ")" [function, total]
  rule swapCase(.PString) => .PString
  rule swapCase(C :: S) => toggle(C) :: swapCase(S)

  syntax PString ::= "reverse" "(" PString ")" [function, total]
                   | "reverseAcc" "(" PString "," PString ")" [function, total]
  rule reverse(S) => reverseAcc(S, .PString)
  rule reverseAcc(.PString, ACC) => ACC
  rule reverseAcc(C :: S, ACC) => reverseAcc(S, C :: ACC)

  syntax PString ::= "ifPString" "(" Bool "," PString "," PString ")" [function, total]
  rule ifPString(true, THEN, _) => THEN
  rule ifPString(false, _, ELSE) => ELSE

  // Expression evaluation for the pure expression used by solve.  This keeps
  // the AST visible: any/isalpha supplies the test, swapcase the then arm, and
  // the [::-1] slice the else arm.
  syntax Bool ::= "evalBool" "(" Expr "," PString ")" [function]
  syntax PString ::= "evalString" "(" Expr "," PString ")" [function]

  rule evalBool(
         Call(Name("any"),
           GenExp(Call(Attribute(Name(C), "isalpha"), _ARGS),
             CompFor(Name(C), Name("s"), _IFS))),
         S) => hasAlpha(S)

  rule evalString(IfExp(TEST, THEN, ELSE), S) =>
    ifPString(evalBool(TEST, S), evalString(THEN, S), evalString(ELSE, S))
  rule evalString(Call(Attribute(Name("s"), "swapcase"), _ARGS), S) => swapCase(S)
  rule evalString(
         Subscript(Name("s"),
           Slice(NoBound, NoBound, UnaryOp("-", Int(1)))),
         S) => reverse(S)

  syntax Result ::= "noResult" | PString

  configuration
    <humanEval>
      <k> $PGM:Program </k>
      <input> $INPUT:PString </input>
      <result> noResult </result>
    </humanEval>

  rule <k> Module(FuncDef("solve", Params("s"), Return(E))) => .K </k>
       <input> S </input>
       <result> noResult => evalString(E, S) </result>
endmodule
