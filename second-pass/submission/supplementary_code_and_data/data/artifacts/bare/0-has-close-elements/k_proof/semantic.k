requires "domains.md"

module MPY-SYNTAX
  imports BOOL-SYNTAX
  imports FLOAT-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                | "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Strings ::= List{String, ","}
  syntax Params ::= "Params" "(" Strings ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr | Slice
  syntax Bound ::= Expr | "NoBound"
  syntax Slice ::= "Slice" "(" Bound "," Bound "," Bound ")"

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Float" "(" Float ")"
                | "Bool" "(" Bool ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports BOOL
  imports INT
  imports K-EQUAL
  imports MAP
  imports STRING

  syntax PVal ::= VInt(Int)
                | VRat(Int, Int)
                | VBool(Bool)
                | VList(PValues)
                | "VNone"
  syntax PValues ::= List{PVal, ","}
  syntax Function ::= function(Params, Stmts)

  // The configuration takes the translated module as $PGM and a comma-separated
  // entry-point argument list as $ARGS.
  configuration <k> runProgram($PGM:Pgm, $ARGS:PValues) </k>

  syntax PVal ::= runProgram(Pgm, PValues)
                | call(String, PValues, Map) [function]
                | exec(Stmts, Map, Map) [function]
                | branch(PVal, Stmts, Stmts, Stmts, Map, Map) [function]
                | eval(Expr, Map, Map) [function]
                | subValue(PVal, PVal) [function]
                | absValue(PVal) [function]
                | compareValue(String, PVal, PVal) [function]
                | subscriptValue(PVal, PVal) [function]
                | sliceOne(PVal) [function]
                | lengthValue(PVal) [function]
  syntax PValues ::= evalExprs(Exprs, Map, Map) [function]
  syntax Stmts ::= concatStmts(Stmts, Stmts) [function]
  syntax Map ::= collect(Stmts) [function]
               | bind(Params, PValues) [function]
  syntax KItem ::= "verify" "(" PValues ")"

  rule runProgram(Module(SS), ARGS)
    => call("has_close_elements", ARGS, collect(SS))

  rule collect(.Stmts) => .Map
  rule collect(ImportFrom(_, _) REST) => collect(REST)
  rule collect(FuncDef(F, P, BODY) REST)
    => (F |-> function(P, BODY)) collect(REST)

  rule bind(Params(.Strings), .PValues) => .Map
  rule bind(Params(X, XS), V, VS)
    => (X |-> V) bind(Params(XS), VS)

  rule call(F, VS, (F |-> function(P, BODY)) REST)
    => exec(BODY, bind(P, VS), (F |-> function(P, BODY)) REST)

  rule exec(Return(E) _REST, ENV, FS) => eval(E, ENV, FS)
  rule exec(If(COND, THEN, ELSE) REST, ENV, FS)
    => branch(eval(COND, ENV, FS), THEN, ELSE, REST, ENV, FS)

  rule branch(VBool(B), THEN, ELSE, REST, ENV, FS)
    => #if B
       #then exec(concatStmts(THEN, REST), ENV, FS)
       #else exec(concatStmts(ELSE, REST), ENV, FS)
       #fi
  rule branch((#if B #then V1:PVal #else V2:PVal #fi),
              THEN, ELSE, REST, ENV, FS)
    => #if B
       #then branch(V1, THEN, ELSE, REST, ENV, FS)
       #else branch(V2, THEN, ELSE, REST, ENV, FS)
       #fi [simplification]

  rule concatStmts(.Stmts, REST) => REST
  rule concatStmts((S:Stmt SS:Stmts), REST)
    => S concatStmts(SS, REST)

  rule eval(Name(X), (X |-> V) _REST, _) => V
  rule eval(Int(I), _, _) => VInt(I)
  rule eval(Bool(B), _, _) => VBool(B)

  rule eval(BinOp("-", L, R), ENV, FS)
    => subValue(eval(L, ENV, FS), eval(R, ENV, FS))
  rule eval(Compare(L, CmpOp(OP, R)), ENV, FS)
    => compareValue(OP, eval(L, ENV, FS), eval(R, ENV, FS))

  rule eval(Call(Name("len"), E), ENV, FS)
    => lengthValue(eval(E, ENV, FS))
  rule eval(Call(Name("abs"), E), ENV, FS)
    => absValue(eval(E, ENV, FS))
  rule eval(Call(Name(F), ES), ENV, FS)
    => call(F, evalExprs(ES, ENV, FS), FS)
    requires F =/=String "len" andBool F =/=String "abs"

  rule evalExprs(.Exprs, _, _) => .PValues
  rule evalExprs(E, ES, ENV, FS)
    => eval(E, ENV, FS), evalExprs(ES, ENV, FS)

  rule eval(Subscript(E, I:Expr), ENV, FS)
    => subscriptValue(eval(E, ENV, FS), eval(I, ENV, FS))
  rule eval(Subscript(E, Slice(Int(1), NoBound, NoBound)), ENV, FS)
    => sliceOne(eval(E, ENV, FS))

  rule lengthValue(VList(VS)) => VInt(lengthValues(VS))
  syntax Int ::= lengthValues(PValues) [function]
  rule lengthValues(.PValues) => 0
  rule lengthValues(_V, VS) => 1 +Int lengthValues(VS)

  rule subscriptValue(VList(V, _), VInt(0)) => V
  rule sliceOne(VList(_V, VS)) => VList(VS)

  rule subValue(VInt(I), VInt(J)) => VInt(I -Int J)
  rule subValue(VRat(A, B), VRat(C, D))
    => VRat((A *Int D) -Int (C *Int B), B *Int D)
  rule subValue(VRat(A, B), VInt(I)) => VRat(A -Int (I *Int B), B)
  rule subValue(VInt(I), VRat(A, B)) => VRat((I *Int B) -Int A, B)

  rule absValue(VInt(I)) => VInt(absInt(I))
  rule absValue(VRat(A, B)) => VRat(absInt(A), B)

  rule compareValue("==", VInt(I), VInt(J)) => VBool(I ==Int J)
  rule compareValue("<", VInt(I), VInt(J)) => VBool(I <Int J)
  rule compareValue("<", VRat(A, B), VRat(C, D))
    => VBool(A *Int D <Int C *Int B)
    requires B >Int 0 andBool D >Int 0
  rule compareValue("<", VRat(A, B), VInt(I))
    => VBool(A <Int I *Int B)
    requires B >Int 0
  rule compareValue("<", VInt(I), VRat(A, B))
    => VBool(I *Int B <Int A)
    requires B >Int 0
endmodule

module MPY
  imports MPY-SEMANTIC
endmodule
