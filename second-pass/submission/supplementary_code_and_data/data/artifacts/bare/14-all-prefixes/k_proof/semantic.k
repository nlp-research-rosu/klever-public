module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
                   | "Run" "(" Program "," Expr ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Exprs ::= NeList{Expr, ","}
  syntax Strings ::= List{String, ","}

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "Assign" "(" Expr "," Expr ")"
                | "While" "(" Expr "," Stmts ")"
                | "Expr" "(" Expr ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Str" "(" String ")"
                | "ListExpr" "(" ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports STRING
  imports K-EQUAL

  syntax Value ::= intVal(Int)
                 | strVal(String)
                 | boolVal(Bool)
                 | listVal(Values)
                 | "noneVal"
  syntax Values ::= "vnil" | vcons(Value, Values)

  syntax Env ::= "emptyEnv" | bind(String, Value, Env)
  syntax Function ::= function(String, Stmts)
  syntax FEnv ::= "emptyFEnv" | fbind(String, Function, FEnv)

  syntax KItem ::= exec(Stmts)
                 | loop(Expr, Stmts)
                 | restoreEnv(Env)
                 | returning(Value)
                 | invoke(Function, Value, Env)

  syntax Value ::= lookup(String, Env) [function]
  rule lookup(X, bind(X, V, _)) => V
  rule lookup(X, bind(Y, _, REST)) => lookup(X, REST)
    requires X =/=String Y

  syntax Env ::= update(String, Value, Env) [function]
  rule update(X, V, emptyEnv) => bind(X, V, emptyEnv)
  rule update(X, V, bind(X, _, REST)) => bind(X, V, REST)
  rule update(X, V, bind(Y, W, REST)) => bind(Y, W, update(X, V, REST))
    requires X =/=String Y

  syntax Function ::= flookup(String, FEnv) [function]
  rule flookup(X, fbind(X, FN, _)) => FN
  rule flookup(X, fbind(Y, _, REST)) => flookup(X, REST)
    requires X =/=String Y

  syntax Values ::= snoc(Values, Value) [function]
  rule snoc(vnil, V) => vcons(V, vnil)
  rule snoc(vcons(H, T), V) => vcons(H, snoc(T, V))

  syntax Value ::= eval(Expr, Env) [function]
  rule eval(Int(I), _) => intVal(I)
  rule eval(Str(S), _) => strVal(S)
  rule eval(Name(X), ENV) => lookup(X, ENV)
  rule eval(ListExpr(), _) => listVal(vnil)
  rule eval(BinOp("+", A, B), ENV) => addVal(eval(A, ENV), eval(B, ENV))
  rule eval(Call(Name("len"), E), ENV) => lenVal(eval(E, ENV))
  rule eval(Compare(A, CmpOp("<=", B)), ENV)
    => lessEqVal(eval(A, ENV), eval(B, ENV))
  rule eval(Subscript(E, Slice(NoBound, HI, NoBound)), ENV)
    => prefixVal(eval(E, ENV), eval(HI, ENV))

  syntax Value ::= addVal(Value, Value) [function]
                 | lenVal(Value) [function]
                 | lessEqVal(Value, Value) [function]
                 | prefixVal(Value, Value) [function]
                 | appendVal(Value, Value) [function]
  rule addVal(intVal(I), intVal(J)) => intVal(I +Int J)
  rule lenVal(strVal(S)) => intVal(lengthString(S))
  rule lessEqVal(intVal(I), intVal(J)) => boolVal(I <=Int J)
  rule prefixVal(strVal(S), intVal(I)) => strVal(substrString(S, 0, I))
  rule appendVal(listVal(VS), V) => listVal(snoc(VS, V))

  syntax Bool ::= truth(Value) [function]
  rule truth(boolVal(B)) => B

  configuration
    <mpy>
      <k> $PGM:Program </k>
      <env> emptyEnv </env>
      <functions> emptyFEnv </functions>
    </mpy>

  rule <k> Run(Module(SS), E) => exec(SS) ~> E ... </k>
  rule <k> Module(SS) => exec(SS) ... </k>

  rule <k> exec(.Stmts) => .K ... </k>
  rule <k> exec(S SS) => S ~> exec(SS) ... </k>

  rule <k> ImportFrom(_, _) => .K ... </k>
  rule <k> FuncDef(F, Params(P), BODY) => .K ... </k>
       <functions> FUNS => fbind(F, function(P, BODY), FUNS) </functions>
  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> ENV => update(X, eval(E, ENV), ENV) </env>
  rule <k> Expr(Call(Attribute(Name(X), "append"), E)) => .K ... </k>
       <env> ENV => update(X, appendVal(lookup(X, ENV), eval(E, ENV)), ENV) </env>
  rule <k> While(COND, BODY) => loop(COND, BODY) ... </k>
  rule <k> loop(COND, BODY) => exec(BODY) ~> loop(COND, BODY) ... </k>
       <env> ENV </env>
    requires truth(eval(COND, ENV))
  rule <k> loop(COND, _) => .K ... </k>
       <env> ENV </env>
    requires notBool truth(eval(COND, ENV))

  rule <k> Call(Name(F), ARG) => invoke(flookup(F, FUNS), eval(ARG, ENV), ENV) ... </k>
       <env> ENV </env>
       <functions> FUNS </functions>
  rule <k> invoke(function(P, BODY), V, OLD) => exec(BODY) ~> restoreEnv(OLD) ... </k>
       <env> _ => bind(P, V, emptyEnv) </env>

  rule <k> Return(E) => returning(eval(E, ENV)) ... </k>
       <env> ENV </env>
  rule <k> returning(V) ~> exec(_) => returning(V) ... </k>
  rule <k> returning(V) ~> restoreEnv(OLD) => V ... </k>
       <env> _ => OLD </env>
endmodule

module SEMANTIC
  imports MPY
endmodule
