module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= "Module" "(" Stmts ")"

  // Statement sequences are juxtaposed by py2mpy.py.
  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "Return" "(" Expr ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"

  syntax Params ::= "Params" "(" Strs ")"
  syntax Strs ::= List{String, ","}

  syntax Exprs ::= List{Expr, ","}
  syntax Expr ::= "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "Str" "(" String ")"
                | "Name" "(" String ")"
                | "ListExpr" "(" Exprs ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "Subscript" "(" Expr "," Index ")"

  syntax CmpOps ::= List{CmpOp, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"

  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP

  // Runtime values. Values is a proper, finite sequence, so ListV is a
  // direct model of a Python list for the fragment used by solution.py.
  syntax Value ::= "IntV" "(" Int ")"
                 | "BoolV" "(" Bool ")"
                 | "StrV" "(" String ")"
                 | "ListV" "(" Values ")"
                 | "NoneV"
  syntax Values ::= List{Value, ","}

  syntax Closure ::= "closure" "(" Params "," Stmts ")"
  syntax KItem ::= "#prepend" "(" Value ")"

  // A program is loaded as a map of function closures, then derivative is
  // invoked with the single list supplied in the ARGS configuration cell.
  syntax Value ::= "#run" "(" Pgm "," Value ")" [function]
                 | "#call" "(" String "," Values "," Map ")"
                 | "#exec" "(" Stmts "," Map "," Map ")"
                 | "#choose" "(" Value "," Stmts "," Stmts "," Map "," Map ")" [function]
                 | "#eval" "(" Expr "," Map "," Map ")" [function]
                 | "#bin" "(" String "," Value "," Value ")" [function]
                 | "#equal" "(" Value "," Value ")" [function]
                 | "#head" "(" Value ")" [function]
                 | "#tail" "(" Value ")" [function]

  syntax Values ::= "#evalArgs" "(" Exprs "," Map "," Map ")" [function]
                  | "#concat" "(" Values ";" Values ")" [function]
  syntax Map ::= "#collect" "(" Stmts ")" [function]
               | "#bind" "(" Params "," Values ")" [function]

  configuration
    <mpy>
      <k> #run($PGM:Pgm, $ARGS:Value) </k>
    </mpy>

  // Module loading and calls.
  rule #run(Module(SS), ARG) => #call("derivative", ARG, #collect(SS))

  rule #collect(.Stmts) => .Map
  rule #collect(FuncDef(F, PS, BODY) REST)
    => (F |-> closure(PS, BODY)) #collect(REST)

  rule #bind(Params(.Strs), .Values) => .Map
  rule #bind(Params(X, XS), (V, VS))
    => (X |-> V) #bind(Params(XS), VS)

  rule #call(F, VS, (F |-> closure(PS, BODY)) FUNS)
    => #exec(BODY, #bind(PS, VS), (F |-> closure(PS, BODY)) FUNS)

  // Return evaluation. The list-plus-recursive-call form uses an explicit
  // continuation, preserving Python's evaluation order while keeping the
  // recursive call visible at the head of <k> for symbolic reasoning.
  rule #exec(Return(ListExpr(ES)) _REST, ENV, FUNS)
    => #eval(ListExpr(ES), ENV, FUNS)
  rule #exec(Return(Call(Name(F), ES)) _REST, ENV, FUNS)
    => #call(F, #evalArgs(ES, ENV, FUNS), FUNS)
  rule <k>
         #exec(
           Return(BinOp("+", ListExpr(LEFT), Call(Name(F), RIGHT))) _REST,
           ENV,
           FUNS)
       => #call(F, #evalArgs(RIGHT, ENV, FUNS), FUNS)
          ~> #prepend(ListV(#evalArgs(LEFT, ENV, FUNS)))
       ... </k>
  rule <k> ListV(YS) ~> #prepend(ListV(XS)) => ListV(#concat(XS ; YS)) ... </k>
  // Constructor-directed versions of Python's list-empty test. These are
  // ordinary semantic transitions (rather than equations), allowing kprove
  // to split a symbolic finite list into its empty/nonempty cases.
  rule #exec(
          If(Compare(Name(X), CmpOp("==", ListExpr(.Exprs))), THEN, _ELSE) _REST,
          (X |-> ListV(.Values)) ENV,
          FUNS)
    => #exec(THEN, (X |-> ListV(.Values)) ENV, FUNS)
  rule #exec(
          If(Compare(Name(X), CmpOp("==", ListExpr(.Exprs))), _THEN, ELSE) _REST,
          (X |-> ListV((V, VS))) ENV,
          FUNS)
    => #exec(ELSE, (X |-> ListV((V, VS))) ENV, FUNS)
  rule #exec(.Stmts, _ENV, _FUNS) => NoneV

  rule #choose(BoolV(true),  THEN, _ELSE, ENV, FUNS) => #exec(THEN, ENV, FUNS)
  rule #choose(BoolV(false), _THEN, ELSE, ENV, FUNS) => #exec(ELSE, ENV, FUNS)

  // Expression evaluation for the constructors exercised by solution.mpy.
  rule #eval(Int(I), _ENV, _FUNS) => IntV(I)
  rule #eval(Bool(B), _ENV, _FUNS) => BoolV(B)
  rule #eval(Str(S), _ENV, _FUNS) => StrV(S)
  rule #eval(Name(X), (X |-> V:Value) _ENV, _FUNS) => V
  rule #eval(ListExpr(ES), ENV, FUNS) => ListV(#evalArgs(ES, ENV, FUNS))
  rule #eval(BinOp(OP, L, R), ENV, FUNS)
    => #bin(OP, #eval(L, ENV, FUNS), #eval(R, ENV, FUNS))
  rule #eval(Compare(L, CmpOp("==", R)), ENV, FUNS)
    => #equal(#eval(L, ENV, FUNS), #eval(R, ENV, FUNS))
  rule #eval(Call(Name(F), ES), ENV, FUNS)
    => #call(F, #evalArgs(ES, ENV, FUNS), FUNS)
  rule #eval(Subscript(E, Int(0)), ENV, FUNS)
    => #head(#eval(E, ENV, FUNS))
  rule #eval(Subscript(E, Slice(Int(1), NoBound, NoBound)), ENV, FUNS)
    => #tail(#eval(E, ENV, FUNS))

  rule #evalArgs(.Exprs, _ENV, _FUNS) => .Values
  rule #evalArgs((E, ES), ENV, FUNS)
    => (#eval(E, ENV, FUNS), #evalArgs(ES, ENV, FUNS))

  // Python integer arithmetic and list concatenation.
  rule #bin("+", IntV(I), IntV(J)) => IntV(I +Int J)
  rule #bin("*", IntV(I), IntV(J)) => IntV(I *Int J)
  rule #bin("+", ListV(XS), ListV(YS)) => ListV(#concat(XS ; YS))

  rule #concat(.Values ; YS) => YS
  rule #concat((V, VS) ; YS) => (V, #concat(VS ; YS))

  // Equality is complete for integers, booleans, strings, and the only list
  // comparison used by the program (against []).
  rule #equal(IntV(I), IntV(J)) => BoolV(I ==Int J)
  rule #equal(BoolV(B), BoolV(C)) => BoolV(B ==Bool C)
  rule #equal(StrV(S), StrV(T)) => BoolV(S ==String T)
  rule #equal(ListV(.Values), ListV(.Values)) => BoolV(true)
  rule #equal(ListV((_V, _VS)), ListV(.Values)) => BoolV(false)
  rule #equal(ListV(.Values), ListV((_V, _VS))) => BoolV(false)

  rule #head(ListV((V, _VS))) => V
  rule #tail(ListV(.Values)) => ListV(.Values)
  rule #tail(ListV((_V, VS))) => ListV(VS)
endmodule
