requires "domains.md"

module MPY-SYNTAX
  imports DOMAINS

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Expr" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"
  syntax Exprs  ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}

  syntax Expr ::= "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Slice ")"

  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP

  syntax Value ::= intVal(Int) | strVal(String) | boolVal(Bool)
  syntax Function ::= function(Params, Stmts)
  syntax Returned ::= returned(Value)

  syntax KItem ::= eval(Expr)
                 | addLeft(Expr) | addRight(Value)
                 | cmpLeft(String, Expr) | cmpRight(String, Value)
                 | ifFrame(Stmts, Stmts)
                 | lenFrame()
                 | callArgOne(Expr) | callArgTwo(Value)
                 | invoke(Value, Value)
                 | prefixBase(Expr) | prefixEnd(Value)
                 | tailFrame()
                 | makeReturn() | returnFrame(Map)

  configuration
    <py>
      <k> $PGM:Program </k>
      <functions> .Map </functions>
      <env> .Map </env>
    </py>

  // Statement-list execution and function installation.
  rule <k> Module(SS) => SS ... </k>
  rule <k> .Stmts => .K ... </k>
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> V:Value ~> .Stmts => V ... </k>

  rule <k> FuncDef(N, P, B) => .K ... </k>
       <functions> F => F [ N <- function(P, B) ] </functions>

  rule <k> Expr(E) => eval(E) ... </k>

  // Literals, variables, integer addition, and the comparisons used here.
  rule <k> eval(Int(I)) => intVal(I) ... </k>
  rule <k> eval(Str(S)) => strVal(S) ... </k>
  rule <k> eval(Name(N)) => V ... </k>
       <env>... N |-> V ...</env>

  rule <k> eval(BinOp("+", L, R)) => eval(L) ~> addLeft(R) ... </k>
  rule <k> V:Value ~> addLeft(R) => eval(R) ~> addRight(V) ... </k>
  rule <k> intVal(J) ~> addRight(intVal(I)) => intVal(I +Int J) ... </k>

  rule <k> eval(Compare(L, CmpOp(OP, R)))
        => eval(L) ~> cmpLeft(OP, R) ... </k>
  rule <k> V:Value ~> cmpLeft(OP, R)
        => eval(R) ~> cmpRight(OP, V) ... </k>
  rule <k> strVal(S2) ~> cmpRight("==", strVal(S1))
        => boolVal(S1 ==String S2) ... </k>
  rule <k> intVal(I2) ~> cmpRight("<", intVal(I1))
        => boolVal(I1 <Int I2) ... </k>

  // Branch rules split symbolic execution on the Boolean condition.
  rule <k> If(C, T, E) => eval(C) ~> ifFrame(T, E) ... </k>
  rule <k> boolVal(B) ~> ifFrame(T, _E) => T ... </k> requires B
  rule <k> boolVal(B) ~> ifFrame(_T, E) => E ... </k> requires notBool B

  // len, the two slice shapes emitted by solution.py, and entry-point calls.
  rule <k> eval(Call(Name("len"), E)) => eval(E) ~> lenFrame() ... </k>
  rule <k> strVal(S) ~> lenFrame() => intVal(lengthString(S)) ... </k>

  rule <k> eval(Subscript(E, Slice(NoBound, Call(Name("len"), H), NoBound)))
        => eval(E) ~> prefixBase(H) ... </k>
  rule <k> strVal(S) ~> prefixBase(H)
        => eval(Call(Name("len"), H)) ~> prefixEnd(strVal(S)) ... </k>
  rule <k> intVal(I) ~> prefixEnd(strVal(S))
        => strVal(substrString(S, 0, I)) ... </k>

  rule <k> eval(Subscript(E, Slice(Int(1), NoBound, NoBound)))
        => eval(E) ~> tailFrame() ... </k>
  rule <k> strVal(S) ~> tailFrame()
        => strVal(substrString(S, 1, lengthString(S))) ... </k>

  rule <k> eval(Call(Name("how_many_times"), E1, E2))
        => eval(E1) ~> callArgOne(E2) ... </k>
  rule <k> V1:Value ~> callArgOne(E2)
        => eval(E2) ~> callArgTwo(V1) ... </k>
  rule <k> V2:Value ~> callArgTwo(V1) => invoke(V1, V2) ... </k>

  // Calls use a fresh two-argument environment and restore their caller's map.
  rule <k> invoke(V1, V2) => B ~> returnFrame(OLD) ... </k>
       <functions>... "how_many_times" |->
          function(Params("string", "substring"), B) ...</functions>
       <env> OLD =>
          ("string" |-> V1
           "substring" |-> V2)
       </env>

  rule <k> Return(E) => eval(E) ~> makeReturn() ... </k>
  rule <k> V:Value ~> makeReturn() => returned(V) ... </k>

  // A return discards the remainder of its current statement block only.
  rule <k> returned(V) ~> (_S:Stmt) => returned(V) ... </k>
  rule <k> returned(V) ~> (_SS:Stmts) => returned(V) ... </k>
  rule <k> returned(V) ~> returnFrame(OLD) => V ... </k>
       <env> _ => OLD </env>
endmodule
