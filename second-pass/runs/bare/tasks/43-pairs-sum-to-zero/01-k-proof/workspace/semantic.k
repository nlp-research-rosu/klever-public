module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "Assign" "(" Expr "," Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" StringList ")"
  syntax StringList ::= List{String, ","}

  syntax Expr ::= "Bool" "(" Bool ")"
                | "Int" "(" Int ")"
                | "Name" "(" String ")"
                | "UnaryOp" "(" String "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Subscript" "(" Expr "," Index ")"
                | "Call" "(" Expr "," Exprs ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports MAP

  // Integer lists are a semantic value domain, independent of the source AST.
  syntax ISeq ::= ".ISeq" [symbol(seqNil)]
                | Int "::" ISeq [symbol(seqCons)]

  syntax PyVal ::= "pyInt" "(" Int ")"
                 | "pyBool" "(" Bool ")"
                 | "pyList" "(" ISeq ")"
                 | "pyNone"

  syntax KItem ::= "run" "(" Program "," ISeq ")"
                 | "functionEnd"
                 | "ifStmt" "(" Bool "," Stmts "," Stmts ")"

  syntax PyVal ::= "eval" "(" Expr "," Map ")" [function]
                 | "negVal" "(" PyVal ")" [function]
                 | "atZero" "(" PyVal ")" [function]
                 | "tailVal" "(" PyVal ")" [function]
                 | "containsVal" "(" PyVal "," PyVal ")" [function]
  syntax Bool ::= "truth" "(" PyVal ")" [function]
  syntax ISeq ::= "asList" "(" PyVal ")" [function]

  syntax Bool ::= "isEmpty" "(" ISeq ")" [function, total]
  syntax Bool ::= "member" "(" Int "," ISeq ")" [function, total]
  syntax Bool ::= "hasZeroPair" "(" ISeq ")" [function, total]
  syntax Int ::= "first" "(" ISeq ")" [function, total]
  syntax ISeq ::= "rest" "(" ISeq ")" [function, total]

  configuration
    <mpy>
      <k> run($PGM:Program, $INPUT:ISeq) </k>
      <program> $PGM </program>
      <env> .Map </env>
    </mpy>

  // A translated one-argument function is entered with its parameter bound.
  rule <k> run(Module(FuncDef(_F, Params(P:String), BODY)), INPUT)
        => BODY ~> functionEnd ... </k>
       <env> .Map => P |-> pyList(INPUT) </env>

  // The translator represents statement blocks as juxtaposed statement lists.
  rule <k> (S:Stmt SS:Stmts) => S ~> SS ... </k>
  rule <k> .Stmts => .K ... </k>

  rule <k> Assign(Name(X), E) => .K ... </k>
       <env> RHO => RHO [ X <- eval(E, RHO) ] </env>

  rule <k> If(E, THEN, ELSE) => ifStmt(truth(eval(E, RHO)), THEN, ELSE) ... </k>
       <env> RHO </env>
  rule <k> ifStmt(B, THEN, _ELSE) => THEN ... </k> requires B
  rule <k> ifStmt(B, _THEN, ELSE) => ELSE ... </k> requires notBool B

  // Calls in tail-return position re-enter the same translated definition.
  rule <k> Return(Call(Name(F), ARG:Expr)) ~> _REST
        => run(Module(FuncDef(F, Params(P:String), BODY)),
               asList(eval(ARG, RHO))) </k>
       <program> Module(FuncDef(F, Params(P:String), BODY)) </program>
       <env> RHO => .Map </env>

  rule <k> Return(Bool(B)) ~> _REST => pyBool(B) </k>
       <env> _RHO => .Map </env>
  rule <k> functionEnd => pyNone ... </k>

  rule eval(Bool(B), _RHO) => pyBool(B)
  rule eval(Int(I), _RHO) => pyInt(I)
  rule eval(Name(X), (X |-> V) _RHO) => V
  rule eval(UnaryOp("not", E), RHO) => pyBool(notBool truth(eval(E, RHO)))
  rule eval(UnaryOp("-", E), RHO) => negVal(eval(E, RHO))
  rule eval(Subscript(E, Int(0)), RHO) => atZero(eval(E, RHO))
  rule eval(Subscript(E, Slice(Int(1), NoBound, NoBound)), RHO)
    => tailVal(eval(E, RHO))
  rule eval(Compare(L, CmpOp("in", R)), RHO)
    => containsVal(eval(L, RHO), eval(R, RHO))

  rule negVal(pyInt(I)) => pyInt(0 -Int I)
  rule atZero(pyList(L)) => pyInt(first(L))
  rule tailVal(pyList(L)) => pyList(rest(L))
  rule containsVal(pyInt(I), pyList(L)) => pyBool(member(I, L))

  rule truth(pyBool(B)) => B
  rule truth(pyInt(I)) => I =/=Int 0
  rule truth(pyList(L)) => notBool isEmpty(L)
  rule asList(pyList(L)) => L

  rule isEmpty(.ISeq) => true
  rule isEmpty(_I :: _IS) => false
  rule first(I :: _IS) => I
  rule rest(_I :: IS) => IS
  rule member(_I, .ISeq) => false
  rule member(I, J :: JS) => (I ==Int J) orBool member(I, JS)
endmodule
