// A deliberately small Python semantics for the AST constructors emitted by
// py2mpy.py.  It covers exactly the fragment used by solution.mpy.  Runtime
// Python strings and booleans are wrapped in Val so that they cannot be
// confused with source-level Str(...) and Bool(...) expressions.

module MPY-SYNTAX
  imports DOMAINS

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "For" "(" Expr "," Expr "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Str" "(" String ")"
                | "Int" "(" Int ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "TupleExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Exprs ::= List{Expr, ","}
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP

  syntax Val ::= strVal(String)
               | boolVal(Bool)
               | tupleVal(Val, Val)

  syntax ExecResult ::= normal(Map) | returned(Val)

  // krun supplies the two Python arguments as configuration variables.
  configuration <k> execute($PGM:Pgm, $S:String, $C:String) </k>

  syntax KItem ::= execute(Pgm, String, String)
  syntax ExecResult ::= exec(Stmts, Map) [function]
  syntax Val ::= eval(Expr, Map) [function]
  syntax Val ::= getVal(Map, String) [function]
  syntax String ::= asString(Val) [function]
  syntax Bool ::= asBool(Val) [function]

  // Mathematical string operations used by Python's loop and [::-1].
  syntax String ::= deleteChars(String, String) [function]
                  | reverseString(String) [function]

  rule getVal((X:String |-> V:Val) _REST:Map, X) => V
  rule asString(strVal(S)) => S
  rule asBool(boolVal(B)) => B

  // The hooked concatenation evaluates concrete operands.  This algebraic
  // identity is also needed when the right operand is a symbolic string.
  rule "" +String S => S [simplification]

  rule deleteChars("", _) => ""
  rule deleteChars(S, C)
    => deleteChars(substrString(S, 1, lengthString(S)), C)
    requires lengthString(S) >Int 0
     andBool findString(C, substrString(S, 0, 1), 0) >=Int 0
  rule deleteChars(S, C)
    => substrString(S, 0, 1)
       +String deleteChars(substrString(S, 1, lengthString(S)), C)
    requires lengthString(S) >Int 0
     andBool findString(C, substrString(S, 0, 1), 0) <Int 0

  rule reverseString("") => ""
  rule reverseString(S)
    => reverseString(substrString(S, 1, lengthString(S)))
       +String substrString(S, 0, 1)
    requires lengthString(S) >Int 0

  rule eval(Name(X), ENV) => getVal(ENV, X)
  rule eval(Str(S), _) => strVal(S)
  rule eval(BinOp("+", E1, E2), ENV)
    => strVal(asString(eval(E1, ENV)) +String asString(eval(E2, ENV)))
  rule eval(Compare(E1, CmpOp("not in", E2)), ENV)
    => boolVal(findString(asString(eval(E2, ENV)),
                          asString(eval(E1, ENV)), 0) <Int 0)
  rule eval(Compare(E1, CmpOp("==", E2)), ENV)
    => boolVal(asString(eval(E1, ENV)) ==String asString(eval(E2, ENV)))
  rule eval(TupleExpr(E1, E2), ENV)
    => tupleVal(eval(E1, ENV), eval(E2, ENV))
  rule eval(Subscript(E, Slice(NoBound, NoBound, UnaryOp("-", Int(1)))), ENV)
    => strVal(reverseString(asString(eval(E, ENV))))

  rule exec(.Stmts, ENV) => normal(ENV)
  rule exec(Assign(Name(X), E) REST, ENV)
    => exec(REST, ENV [ X <- eval(E, ENV) ])
  rule exec(If(COND, THEN, _ELSE) REST, ENV)
    => exec(THEN REST, ENV)
    requires asBool(eval(COND, ENV))
  rule exec(If(COND, _THEN, ELSE) REST, ENV)
    => exec(ELSE REST, ENV)
    requires notBool asBool(eval(COND, ENV))
  rule exec(Return(E) _REST, ENV) => returned(eval(E, ENV))

  // The source-level loop iterates over s one character at a time.  Its body
  // is kept syntactic in solution.mpy; this rule gives that filtering idiom
  // the same left-to-right behavior as repeated Python loop iterations.
  rule exec(
         For(Name(CH), Name(SVAR),
           If(Compare(Name(CH), CmpOp("not in", Name(CVAR))),
             Assign(Name(RVAR), BinOp("+", Name(RVAR), Name(CH))),
             .Stmts))
         REST,
         ENV)
    => exec(
         REST,
         ENV [ RVAR <- strVal(
           asString(getVal(ENV, RVAR))
           +String deleteChars(asString(getVal(ENV, SVAR)),
                                asString(getVal(ENV, CVAR)))) ])

  rule <k>
         execute(
           Module(FuncDef("reverse_delete", Params("s", "c"), BODY)),
           S, C)
         => exec(BODY,
              ("s" |-> strVal(S))
              ("c" |-> strVal(C)))
       </k>
endmodule
