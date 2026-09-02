module SEMANTIC-SYNTAX
  imports INT
  imports STRING

  // The concrete syntax emitted by py2mpy.py for solution.py.
  syntax PyModule ::= "Module" "(" PyStmt ")"
  syntax PyStmt   ::= "FuncDef" "(" String "," Params "," PyStmt ")"
                    | "Return" "(" PyExpr ")"
  syntax Params   ::= "Params" "(" String "," String ")"
  syntax PyExpr   ::= "Name" "(" String ")"
                    | "Call" "(" PyExpr "," PyExpr ")"
                    | "BinOp" "(" String "," PyExpr "," PyExpr ")"

  // Values are deliberately restricted to the integer-list fragment needed
  // by this HumanEval problem.
  syntax Ints ::= List{Int, ","}
  syntax PyValue ::= "list" "(" Ints ")"
                   | "set" "(" Ints ")"
endmodule

module SEMANTIC
  imports SEMANTIC-SYNTAX
  imports BOOL

  configuration
    <py>
      <k> $PGM:PyModule </k>
      <l1> $L1:PyValue </l1>
      <l2> $L2:PyValue </l2>
    </py>

  // Integer-list operations used to model Python set conversion,
  // intersection, and sorted.  A set is represented by a duplicate-free
  // Ints sequence; its incidental order is unobservable after sorted.
  syntax Bool ::= "containsInt" "(" Int ";" Ints ")" [function]
  rule containsInt(_ ; .Ints) => false
  rule containsInt(I ; J, IS) => (I ==Int J) orBool containsInt(I ; IS)

  syntax Ints ::= "uniqueInts" "(" Ints ")" [function]
  rule uniqueInts(.Ints) => .Ints
  rule uniqueInts(I, IS) => uniqueInts(IS)
    requires containsInt(I ; IS)
  rule uniqueInts(I, IS) => I, uniqueInts(IS)
    requires notBool containsInt(I ; IS)

  syntax Ints ::= "intersectInts" "(" Ints ";" Ints ")" [function]
  rule intersectInts(.Ints ; _) => .Ints
  rule intersectInts(I, IS ; JS) => I, intersectInts(IS ; JS)
    requires containsInt(I ; JS)
  rule intersectInts(I, IS ; JS) => intersectInts(IS ; JS)
    requires notBool containsInt(I ; JS)

  syntax Ints ::= "insertInt" "(" Int ";" Ints ")" [function]
  rule insertInt(I ; .Ints) => I, .Ints
  rule insertInt(I ; J, IS) => I, J, IS
    requires I <=Int J
  rule insertInt(I ; J, IS) => J, insertInt(I ; IS)
    requires I >Int J

  syntax Ints ::= "sortInts" "(" Ints ")" [function]
  rule sortInts(.Ints) => .Ints
  rule sortInts(I, IS) => insertInt(I ; sortInts(IS))

  syntax PyValue ::= "makeSet" "(" PyValue ")" [function]
                   | "setAnd" "(" PyValue ";" PyValue ")" [function]
                   | "sortedValue" "(" PyValue ")" [function]
  rule makeSet(list(IS)) => set(uniqueInts(IS))
  rule setAnd(set(IS) ; set(JS)) => set(intersectInts(IS ; JS))
  rule sortedValue(set(IS)) => list(sortInts(IS))
  rule sortedValue(list(IS)) => list(sortInts(IS))

  // Compositional expression evaluation.  Parameter names are carried by
  // the evaluator, so Name has ordinary lexical lookup for this two-argument
  // function fragment.
  syntax PyValue ::= "eval" "(" PyExpr ";" String ";" PyValue ";"
                              String ";" PyValue ")" [function]
  rule eval(Name(X) ; X ; V1 ; _ ; _) => V1
  rule eval(Name(Y) ; X ; _ ; Y ; V2) => V2
    requires X =/=String Y
  rule eval(Call(Name("set"), E) ; X ; V1 ; Y ; V2)
    => makeSet(eval(E ; X ; V1 ; Y ; V2))
  rule eval(Call(Name("sorted"), E) ; X ; V1 ; Y ; V2)
    => sortedValue(eval(E ; X ; V1 ; Y ; V2))
  rule eval(BinOp("&", E1, E2) ; X ; V1 ; Y ; V2)
    => setAnd(eval(E1 ; X ; V1 ; Y ; V2) ;
              eval(E2 ; X ; V1 ; Y ; V2))

  syntax KItem ::= "execute" "(" PyStmt ";" String ";" PyValue ";"
                               String ";" PyValue ")"

  // Loading the translated module binds its two parameters to the two input
  // cells and executes its body.  Return replaces the control term by the
  // expression's value.
  rule <k> Module(FuncDef("common", Params(X, Y), BODY))
        => execute(BODY ; X ; V1 ; Y ; V2) ... </k>
       <l1> V1 </l1>
       <l2> V2 </l2>
  rule <k> execute(Return(E) ; X ; V1 ; Y ; V2)
        => eval(E ; X ; V1 ; Y ; V2) ... </k>
endmodule
