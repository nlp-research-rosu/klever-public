requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")" [symbol]

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax Strings ::= List{String, ","}

  syntax Params ::= "Params" "(" Strings ")" [symbol]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol]

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol]
                | "Assign" "(" Expr "," Expr ")" [symbol]
                | "If" "(" Expr "," Stmts "," Stmts ")" [symbol]
                | "Return" "(" Expr ")" [symbol]

  syntax Expr ::= "Name" "(" String ")" [symbol]
                | "Int" "(" Int ")" [symbol]
                | "Str" "(" String ")" [symbol]
                | "Bool" "(" Bool ")" [symbol]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol]
                | "UnaryOp" "(" String "," Expr ")" [symbol]
                | "BoolOp" "(" String "," Exprs ")" [symbol]
                | "Compare" "(" Expr "," CmpOps ")" [symbol]
                | "Subscript" "(" Expr "," Expr ")" [symbol]
                | "Attribute" "(" Expr "," String ")" [symbol]
                | "Call" "(" Expr "," Exprs ")" [symbol]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING

  syntax PyVal ::= VInt(Int) | VStr(String) | VBool(Bool) [symbol]
                 | IteVal(Bool, PyVal, PyVal) [symbol]
  syntax Env ::= "EmptyEnv" | Bind(String, PyVal, Env) [symbol]
  syntax ExecResult ::= Normal(Env) | Returned(PyVal) [symbol]
                      | IfExec(Bool, ExecResult, ExecResult) [symbol]

  syntax KItem ::= runProgram(Program, String) [function, total, symbol]
  syntax PyVal ::= eval(Expr, Env) [function, total, symbol]
                 | lookupVal(String, Env) [function, total, symbol]
  syntax ExecResult ::= exec(Stmts, Env) [function, total, symbol]
                      | continue(ExecResult, Stmts) [function, total, symbol]
  syntax Bool ::= asBool(PyVal) [function, total, symbol]
                | compareVals(String, PyVal, PyVal) [function, total, symbol]
                | endsWith(String, String) [function, total, symbol]
  syntax PyVal ::= addVals(PyVal, PyVal) [function, total, symbol]
                 | subscriptVal(PyVal, PyVal) [function, total, symbol]
  syntax Bool ::= boolOp(String, Exprs, Env) [function, total, symbol]
  syntax PyVal ::= resultValue(ExecResult) [function, total, symbol]
  // A direct hook keeps symbolic counting as a total primitive. The Domains
  // library's derived recursive count function is equivalent concretely, but
  // unfolds only after a symbolic find and therefore cannot drive proofs.
  syntax Int ::= occurrences(String, String) [function, total, symbol]
  rule occurrences(S, NEEDLE) => countAllOccurrences(S, NEEDLE) [concrete]

  configuration <k> runProgram($PGM:Program, $INPUT:String) </k>

  rule runProgram(
         Module(FuncDef("file_name_check", Params("file_name"), BODY)),
         S
       ) => resultValue(exec(BODY, Bind("file_name", VStr(S), EmptyEnv)))

  rule resultValue(Returned(V)) => V
  rule resultValue(IfExec(B, R1, R2))
    => IteVal(B, resultValue(R1), resultValue(R2))

  rule IteVal(true, V, _OTHER) => V
  rule IteVal(false, _OTHER, V) => V
  rule IfExec(true, R, _OTHER) => R
  rule IfExec(false, _OTHER, R) => R

  rule exec(.Stmts, RHO) => Normal(RHO)
  rule exec(Assign(Name(X), E) SS, RHO)
    => exec(SS, Bind(X, eval(E, RHO), RHO))
  rule exec(Return(E) SS, RHO) => Returned(eval(E, RHO))
  rule exec(If(E, THEN, ELSE) SS, RHO)
    => IfExec(
         asBool(eval(E, RHO)),
         continue(exec(THEN, RHO), SS),
         continue(exec(ELSE, RHO), SS)
       )

  rule continue(Normal(RHO), SS) => exec(SS, RHO)
  rule continue(Returned(V), _SS) => Returned(V)
  rule continue(IfExec(B, R1, R2), SS)
    => IfExec(B, continue(R1, SS), continue(R2, SS))

  rule eval(Name(X), RHO) => lookupVal(X, RHO)
  rule lookupVal(X, Bind(X, V, _RHO)) => V
  rule lookupVal(X, Bind(Y, _V, RHO)) => lookupVal(X, RHO)
    requires X =/=String Y
  rule eval(Int(I), _RHO) => VInt(I)
  rule eval(Str(S), _RHO) => VStr(S)
  rule eval(Bool(B), _RHO) => VBool(B)
  rule eval(BinOp("+", E1, E2), RHO)
    => addVals(eval(E1, RHO), eval(E2, RHO))
  rule eval(UnaryOp("not", E), RHO) => VBool(notBool asBool(eval(E, RHO)))
  rule eval(BoolOp(OP, ES), RHO) => VBool(boolOp(OP, ES, RHO))
  rule eval(Compare(E1, CmpOp(OP, E2)), RHO)
    => VBool(compareVals(OP, eval(E1, RHO), eval(E2, RHO)))
  rule eval(Subscript(E1, E2), RHO)
    => subscriptVal(eval(E1, RHO), eval(E2, RHO))

  syntax String ::= getString(PyVal) [function, total, symbol]
  rule getString(VStr(S)) => S

  rule eval(Call(Name("len"), E), RHO)
    => VInt(lengthString(getString(eval(E, RHO))))
  rule eval(Call(Attribute(E, "count"), Str(NEEDLE)), RHO)
    => VInt(occurrences(getString(eval(E, RHO)), NEEDLE))
  rule eval(Call(Attribute(E, "endswith"), Str(SUFFIX)), RHO)
    => VBool(endsWith(getString(eval(E, RHO)), SUFFIX))

  rule addVals(VInt(I1), VInt(I2)) => VInt(I1 +Int I2)
  rule subscriptVal(VStr(S), VInt(I))
    => VStr(substrString(S, I, I +Int 1))

  rule asBool(VBool(B)) => B

  rule boolOp("and", E1:Expr, E2:Expr, RHO)
    => asBool(eval(E1, RHO)) andBool asBool(eval(E2, RHO))
  rule boolOp("or", E1:Expr, E2:Expr, RHO)
    => asBool(eval(E1, RHO)) orBool asBool(eval(E2, RHO))
  rule boolOp("or", E1:Expr, E2:Expr, E3:Expr, RHO)
    => asBool(eval(E1, RHO))
       orBool asBool(eval(E2, RHO))
       orBool asBool(eval(E3, RHO))

  rule compareVals("==", VInt(I1), VInt(I2)) => I1 ==Int I2
  rule compareVals("!=", VInt(I1), VInt(I2)) => I1 =/=Int I2
  rule compareVals(">", VInt(I1), VInt(I2)) => I1 >Int I2
  rule compareVals("<=", VStr(S1), VStr(S2)) => S1 <=String S2

  rule endsWith(S, SUFFIX)
    => substrString(
         S,
         lengthString(S) -Int lengthString(SUFFIX),
         lengthString(S)
       ) ==String SUFFIX
    requires lengthString(S) >=Int lengthString(SUFFIX)
  rule endsWith(S, SUFFIX) => false
    requires lengthString(S) <Int lengthString(SUFFIX)
endmodule
