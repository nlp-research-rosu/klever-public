requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX
  imports MAP
  imports LIST

  // Runtime values.  IntList is deliberately inductive so symbolic inputs
  // have the same finite-list structure as Python lists.
  syntax IntList ::= "nil"
                   | "cons" "(" Int "," IntList ")"
  syntax Value   ::= "pyInt" "(" Int ")"
                   | "pyBool" "(" Bool ")"
                   | "pyList" "(" IntList ")"
                   | "funref" "(" String ")"
                   | "builtin" "(" String ")"
  syntax Values  ::= List{Value, ","}
  syntax Strings ::= List{String, ","}
  syntax Depth   ::= "z" | "s" "(" Depth ")"

  // The constructor language emitted by py2mpy.py for solution.py.
  syntax Program ::= "Module" "(" Stmts ")"
  syntax Params  ::= "Params" "(" Strings ")"
  syntax Stmts   ::= List{Stmt, ""}
  syntax Stmt    ::= "FuncDef" "(" String "," Params "," Stmts ")"
                   | "If" "(" Expr "," Stmts "," Stmts ")"
                   | "Assign" "(" Expr "," Expr ")"
                   | "Return" "(" Expr ")"
  syntax Exprs   ::= List{Expr, ","}
  syntax Expr    ::= "Int" "(" Int ")"
                   | "Name" "(" String ")"
                   | "Call" "(" Expr "," Exprs ")"
                   | "BinOp" "(" String "," Expr "," Expr ")"
                   | "Compare" "(" Expr "," CmpOps ")"
                   | "Subscript" "(" Expr "," Index ")"
  syntax CmpOps  ::= List{CmpOp, ""}
  syntax CmpOp   ::= "CmpOp" "(" String "," Expr ")"
  syntax Index   ::= Expr | Slice
  syntax Slice   ::= "Slice" "(" Bound "," Bound "," Bound ")"
  syntax Bound   ::= Expr | "NoBound"
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports BOOL
  imports STRING
  imports MAP
  imports LIST

  syntax Function ::= "closure" "(" Params "," Stmts ")"
  syntax Frame ::= "frame" "(" Map "," K ")"

  syntax KItem ::= "exec" "(" Stmts ")"
                 | "invoke" "(" String "," Values ")"
                 | "choose" "(" Stmts "," Stmts ")"
                 | "storeName" "(" String ")"
                 | "returning"
                 | "returned" "(" Depth "," Value ")"
                 | "callOne" "(" Expr ")"
                 | "applyOne" "(" Value ")"
                 | "callTwo" "(" Expr "," Expr ")"
                 | "callTwoSecond" "(" Value "," Expr ")"
                 | "applyTwo" "(" Value "," Value ")"
                 | "apply" "(" Value "," Value ")"
                 | "apply" "(" Value "," Value "," Value ")"
                 | "binLeft" "(" String "," Expr ")"
                 | "binRight" "(" String "," Value ")"
                 | "compareLeft" "(" String "," Expr ")"
                 | "compareRight" "(" String "," Value ")"
                 | "singletonTest"
                 | "listHead"
                 | "sliceTail"

  configuration
    <py>
      <k> $PGM:Program </k>
      <entry> $ENTRY:String </entry>
      <args> $ARGS:Values </args>
      <functions> .Map </functions>
      <env> .Map </env>
      <callStack> .List </callStack>
      <callDepth> z </callDepth>
    </py>

  // Module loading and statement scheduling.
  rule <k> Module(SS) => exec(SS) ~> invoke(F, VS) </k>
       <entry> F </entry>
       <args> VS </args>

  rule exec(.Stmts) => .K
  rule exec(S:Stmt SS:Stmts) => S ~> exec(SS)

  rule <k> FuncDef(F, P, BODY) => .K ... </k>
       <functions> FS => FS [ F <- closure(P, BODY) ] </functions>

  rule invoke(F, V) => apply(funref(F), V)

  // Statements.
  rule <k> If(E, THEN, ELSE) => E ~> choose(THEN, ELSE) ... </k>
  rule pyBool(true)  ~> choose(THEN, _) => exec(THEN)
  rule pyBool(false) ~> choose(_, ELSE) => exec(ELSE)

  rule <k> Assign(Name(X), E) => E ~> storeName(X) ... </k>
  rule <k> V:Value ~> storeName(X) => .K ... </k>
       <env> RHO => RHO [ X <- V ] </env>

  rule <k> Return(E) => E ~> returning ... </k>
  rule <k> V:Value ~> returning ~> _ => returned(D, V) ~> KREST </k>
       <env> _ => OLD </env>
       <callStack> ListItem(frame(OLD, KREST)) STACK => STACK </callStack>
       <callDepth> s(D) => D </callDepth>
  rule returned(_, V) => V

  // Literals and names.
  rule Int(I) => pyInt(I)
  rule <k> Name(X) => V ... </k>
       <env>... X |-> V ...</env>
  rule <k> Name(F) => funref(F) ... </k>
       <functions>... F |-> _:Function ...</functions>
  rule Name("len") => builtin("len")
  rule Name("min") => builtin("min")

  // Calls are evaluated left-to-right.  The translated solution needs unary
  // and binary calls, which are represented separately here.
  rule <k> Call(F, E) => F ~> callOne(E) ... </k>
  rule V:Value ~> callOne(E) => E ~> applyOne(V)
  rule ARG:Value ~> applyOne(F:Value) => apply(F, ARG)

  rule <k> Call(F, E1, E2) => F ~> callTwo(E1, E2) ... </k>
  rule V:Value ~> callTwo(E1, E2) => E1 ~> callTwoSecond(V, E2)
  rule V1:Value ~> callTwoSecond(F:Value, E2) => E2 ~> applyTwo(F, V1)
  rule V2:Value ~> applyTwo(F:Value, V1:Value) => apply(F, V1, V2)

  // A user-function call swaps in its local environment and saves both the
  // caller environment and continuation.  Return restores them atomically.
  rule <k> apply(funref(F), V) ~> KREST => exec(BODY) </k>
       <functions>... F |-> closure(Params(P:String), BODY) ...</functions>
       <env> OLD => P |-> V </env>
       <callStack> STACK => ListItem(frame(OLD, KREST)) STACK </callStack>
       <callDepth> D => s(D) </callDepth>

  rule apply(builtin("len"), pyList(L)) => pyInt(length(L))
  rule apply(builtin("min"), pyInt(I), pyInt(J)) => pyInt(intMin(I, J))

  // Arithmetic and comparisons.
  rule <k> BinOp(OP, L, R) => L ~> binLeft(OP, R) ... </k>
  rule LV:Value ~> binLeft(OP, R) => R ~> binRight(OP, LV)
  rule pyInt(J) ~> binRight("+", pyInt(I)) => pyInt(I +Int J)

  rule <k> Compare(L, CmpOp(OP, R)) => L ~> compareLeft(OP, R) ... </k>
  rule LV:Value ~> compareLeft(OP, R) => R ~> compareRight(OP, LV)
  rule pyInt(J) ~> compareRight("==", pyInt(I)) => pyBool(I ==Int J)

  // Integer list indexing and the only slice form used by the implementation.
  rule <k> Subscript(B, Int(0)) => B ~> listHead ... </k>
  rule pyList(cons(H, _)) ~> listHead => pyInt(H)

  rule <k> Subscript(B, Slice(Int(1), NoBound, NoBound))
        => B ~> sliceTail ... </k>
  rule pyList(cons(_, T)) ~> sliceTail => pyList(T)

  syntax Int ::= length(IntList) [function]
               | intMin(Int, Int) [function]
  rule length(nil) => 0
  rule length(cons(_, T)) => 1 +Int length(T)
  rule intMin(I, J) => I requires I <=Int J
  rule intMin(I, J) => J requires I >Int J
endmodule
