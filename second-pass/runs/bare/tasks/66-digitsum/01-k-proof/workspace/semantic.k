requires "verification.k"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]

  // The translator prints statement sequences by juxtaposition.
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Assign" "(" Expr "," Expr ")"                 [symbol(Assign)]
                | "For" "(" Expr "," Expr "," Stmts ")"       [symbol(For)]
                | "If" "(" Expr "," Stmts "," Stmts ")"       [symbol(If)]
                | "Return" "(" Expr ")"                          [symbol(Return)]

  syntax Params ::= "Params" "(" String ")" [symbol(Params)]

  syntax Expr ::= "Name" "(" String ")"                      [symbol(Name)]
                | "Int" "(" Int ")"                          [symbol(IntExpr)]
                | "Str" "(" String ")"                       [symbol(Str)]
                | "BinOp" "(" String "," Expr "," Expr ")" [symbol(BinOp)]
                | "Call" "(" Expr "," Expr ")"              [symbol(Call)]
                | "Compare" "(" Expr "," CmpOps ")"         [symbol(Compare)]

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(CmpOp)]
endmodule

module DIGIT-SUM-SEMANTICS
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports K-EQUAL

  syntax Value ::= "intVal" "(" Int ")"
                 | "strVal" "(" String ")"
                 | "boolVal" "(" Bool ")"
  syntax Result ::= "noResult" | Value

  syntax KItem ::= "execute" "(" Stmts ")"
                 | "execStmt" "(" Stmt ")"
                 | "loopString" "(" String "," String "," Stmts ")"
                 | "addUpper" "(" String ")"

  syntax Value ::= "eval" "(" Expr "," Map ")" [function]
  syntax Value ::= "addValues" "(" Value "," Value ")" [function]
                 | "ordValue" "(" Value ")" [function]
                 | "compareLE3" "(" Value "," Value "," Value ")" [function]
  syntax String ::= "stringOf" "(" Value ")" [function]
  syntax Bool ::= "truthOf" "(" Value ")" [function]
  syntax Int ::= "pythonUpperOrd" "(" String ")" [function]

  rule eval(Int(I), _) => intVal(I)
  rule eval(Str(S), _) => strVal(S)
  // A just-assigned local is immediately visible even when the surrounding
  // symbolic map is otherwise unknown.
  rule eval(Name(X), _ENV [ X <- V ]) => {V}:>Value [simplification]
  rule eval(Name(X), ENV [ Y <- _V ]) => eval(Name(X), ENV)
    requires X =/=String Y [simplification]
  rule eval(Name(X), (X |-> V) REST) => {V}:>Value
    requires notBool (X in_keys(REST))
  rule eval(BinOp("+", LEFT, RIGHT), ENV)
    => addValues(eval(LEFT, ENV), eval(RIGHT, ENV))
  rule eval(Call(Name("ord"), ARG), ENV)
    => ordValue(eval(ARG, ENV))
  rule eval(Compare(LEFT,
          CmpOp("<=", MIDDLE), CmpOp("<=", RIGHT)), ENV)
    => compareLE3(eval(LEFT, ENV), eval(MIDDLE, ENV), eval(RIGHT, ENV))

  rule addValues(intVal(I), intVal(J)) => intVal(I +Int J)
  rule ordValue(strVal(S)) => intVal(ordChar(S))
  rule compareLE3(strVal(A), strVal(B), strVal(C))
    => boolVal((ordChar(A) <=Int ordChar(B))
               andBool (ordChar(B) <=Int ordChar(C)))
  rule stringOf(strVal(S)) => S
  rule truthOf(boolVal(B)) => B
  rule pythonUpperOrd(C)
    => #if ordChar(C) >=Int 65 andBool ordChar(C) <=Int 90
       #then ordChar(C)
       #else 0
       #fi

  configuration
    <digit-sum>
      <k> $PGM:Program </k>
      <input> $INPUT:String </input>
      <env> .Map </env>
      <result> noResult </result>
    </digit-sum>

  // Loading the one-argument definition binds the supplied input as Python
  // would, then executes the function body.
  rule <k> Module(FuncDef("digitSum", Params("s"), BODY))
            => execute(BODY) ... </k>
       <input> S </input>
       <env> .Map => "s" |-> strVal(S) </env>

  rule <k> execute(.Stmts) => .K ... </k>
  rule <k> execute(S SS) => execStmt(S) ~> execute(SS) ... </k>

  rule <k> execStmt(Assign(Name(X), E)) => .K ... </k>
       <env> ENV => ENV[X <- eval(E, ENV)] </env>

  // This exact translated if-statement is evaluated atomically.  The #if is
  // the ordinary conditional denotation: it adds ord(char) in the uppercase
  // case and zero otherwise, without forcing a symbolic branch.
  rule <k> execStmt(If(Compare(Str("A"),
                    CmpOp("<=", Name(X)), CmpOp("<=", Str("Z"))),
                  Assign(Name("total"),
                    BinOp("+", Name("total"),
                      Call(Name("ord"), Name(X)))),
                  .Stmts))
            => .K ... </k>
       <env> ENV
              => ENV["total" <-
                   addValues(eval(Name("total"), ENV),
                     intVal(pythonUpperOrd(
                       stringOf(eval(Name(X), ENV)))))]
       </env>

  rule <k> execStmt(For(Name(X), ITER, BODY))
            => loopString(X, stringOf(eval(ITER, ENV)), BODY) ... </k>
       <env> ENV </env>

  rule <k> loopString(_X, "", _BODY) => .K ... </k>
  rule <k> loopString("char", S,
              If(Compare(Str("A"),
                   CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                 Assign(Name("total"),
                   BinOp("+", Name("total"),
                     Call(Name("ord"), Name("char")))),
                 .Stmts)
              .Stmts)
            => addUpper(substrString(S, 0, 1))
            ~> loopString("char",
                 substrString(S, 1, lengthString(S)),
                 If(Compare(Str("A"),
                      CmpOp("<=", Name("char")), CmpOp("<=", Str("Z"))),
                    Assign(Name("total"),
                      BinOp("+", Name("total"),
                        Call(Name("ord"), Name("char")))),
                    .Stmts)
                 .Stmts) ... </k>
    requires S =/=String ""

  rule <k> addUpper(C) => .K ... </k>
       <env> ("total" |-> intVal(A)) FRAME
              => ("total" |-> intVal(A +Int pythonUpperOrd(C))) FRAME
       </env>
    requires notBool ("total" in_keys(FRAME))

  rule <k> execStmt(Return(E)) ~> _REST => .K </k>
       <env> ENV => .Map </env>
       <result> noResult => eval(E, ENV) </result>
endmodule

module SEMANTIC
  imports DIGIT-SUM-SEMANTICS
  imports DIGIT-SUM-VERIFICATION
endmodule
