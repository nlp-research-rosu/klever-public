module MINI-PYTHON-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= List{Expr, ","}
  syntax Strings ::= List{String, ","}

  syntax Params ::= "Params" "(" Strings ")"

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "Return" "(" Expr ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "TupleExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Subscript" "(" Expr "," Expr ")"
endmodule

module MINI-PYTHON
  imports MINI-PYTHON-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports BASIC-K

  syntax Value ::= vInt(Int)
                 | vStr(String)
                 | vTuple(Strings)
  syntax KResult ::= Value

  syntax Result ::= "noResult" | result(Value)

  configuration
    <mini-python>
      <k> $PGM:Pgm </k>
      <input> $INPUT:Int </input>
      <env> .Map </env>
      <result> noResult </result>
    </mini-python>

  syntax KItem ::= exec(Stmts)
                 | stmt(Stmt)
                 | eval(Expr)
                 | assignTo(String)
                 | binLeft(String, Expr)
                 | binRight(String, Value)
                 | subscriptIndex(Expr)
                 | subscriptApply(Value)
                 | "returning"

  syntax Strings ::= tupleStrings(Exprs) [function]
  rule tupleStrings(.Exprs) => .Strings
  rule tupleStrings(Str(S) , ES) => S , tupleStrings(ES)

  syntax String ::= tupleAt(Strings, Int) [function]
  rule tupleAt(S:String , _REST:Strings, I) => S
    requires I ==Int 0
    [simplification, concrete(I)]
  rule tupleAt(_S:String , REST:Strings, I) => tupleAt(REST, I -Int 1)
    requires I >Int 0
    [simplification, concrete(I)]

  rule <k> Module(FuncDef(_F, Params(P:String), BODY)) => exec(BODY) </k>
       <input> I </input>
       <env> .Map => P |-> vInt(I) </env>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => stmt(S) ~> exec(SS) ... </k>

  rule <k> stmt(Assign(Name(X), E)) => eval(E) ~> assignTo(X) ... </k>
  rule <k> V:Value ~> assignTo(X) => .K ... </k>
       <env> ENV => ENV [ X <- V ] </env>

  rule <k> stmt(Return(E)) ~> _REST => eval(E) ~> returning </k>
  rule <k> V:Value ~> returning => .K </k>
       <result> noResult => result(V) </result>

  rule <k> eval(Int(I)) => vInt(I) ... </k>
  rule <k> eval(Str(S)) => vStr(S) ... </k>
  rule <k> eval(TupleExpr(ES)) => vTuple(tupleStrings(ES)) ... </k>
  rule <k> eval(Name(X)) => ENV[X] ... </k>
       <env> ENV </env>
    requires X in_keys(ENV)

  rule <k> eval(BinOp(OP, LEFT, RIGHT))
        => eval(LEFT) ~> binLeft(OP, RIGHT) ... </k>
  rule <k> LEFT:Value ~> binLeft(OP, RIGHT)
        => eval(RIGHT) ~> binRight(OP, LEFT) ... </k>

  rule <k> vInt(I2) ~> binRight("//", vInt(I1))
        => vInt(I1 /Int I2) ... </k>
    requires I2 =/=Int 0
  rule <k> vInt(I2) ~> binRight("%", vInt(I1))
        => vInt(I1 modInt I2) ... </k>
    requires I2 =/=Int 0
  rule <k> vInt(I2) ~> binRight("+", vInt(I1))
        => vInt(I1 +Int I2) ... </k>
  rule <k> vStr(S2) ~> binRight("+", vStr(S1))
        => vStr(S1 +String S2) ... </k>

  rule <k> eval(Subscript(BASE, INDEX))
        => eval(BASE) ~> subscriptIndex(INDEX) ... </k>
  rule <k> BASE:Value ~> subscriptIndex(INDEX)
        => eval(INDEX) ~> subscriptApply(BASE) ... </k>
  rule <k> vInt(I) ~> subscriptApply(vTuple(ITEMS))
        => vStr(tupleAt(ITEMS, I)) ... </k>
endmodule
