module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  // The constructor grammar needed by the translated solution.  These are
  // syntax trees, not built-in K computations.
  syntax Pgm ::= "Module" "(" Function ")" [symbol(moduleAst)]
  syntax Function ::= "FuncDef" "(" String "," Params "," Stmt ")" [symbol(funcDefAst)]
  syntax Params ::= "Params" "(" String ")" [symbol(paramsAst)]
  syntax Stmt ::= "Return" "(" Expr ")" [symbol(returnAst)]

  syntax Expr ::= "Name" "(" String ")" [symbol(nameAst)]
                | "Int" "(" Int ")" [symbol(intAst)]
                | "ListComp" "(" Expr "," CompFor ")" [symbol(listCompAst)]
                | "Compare" "(" Expr "," CmpOp ")" [symbol(compareAst)]
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Expr ")" [symbol(compForAst)]
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")" [symbol(cmpOpAst)]

  // A free, inductive representation of Python lists of mathematical ints.
  syntax PyList ::= "nil" [symbol(nil), constructor]
                  | "cons" "(" Int "," PyList ")" [symbol(cons), constructor]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports MAP
  imports INT

  configuration
    <py>
      <k> $PGM:Pgm </k>
      <input> $INPUT:PyList </input>
    </py>

  // Function entry binds the sole formal argument to the external input.
  syntax KItem ::= "eval" "(" Expr "," Map ")" [symbol(eval)]
  rule <k> Module(FuncDef("get_positive", Params(P), Return(E)))
         => eval(E, P |-> L) ... </k>
       <input> L </input>

  // Typed projection from the untyped payload of a K Map.
  syntax PyList ::= "asList" "(" KItem ")" [function, symbol(asList)]
  rule asList(L:PyList) => L

  // A one-generator comprehension evaluates its iterable in the environment.
  // Reusing X in all three positions enforces Python's bound-name relationship.
  rule <k> eval(
              ListComp(Name(X),
                CompFor(Name(X), Name(P),
                  Compare(Name(X), CmpOp(">", Int(N))))),
              RHO)
         => filterGt(asList(RHO [ P ]), N) ... </k>

  // Mathematical meaning of stable filtering: preserve order and duplicates,
  // retaining an element exactly when the comparison is true.
  syntax PyList ::= "filterGt" "(" PyList "," Int ")" [function, symbol(filterGt)]
  rule filterGt(nil, _N) => nil
  rule filterGt(cons(I, IS), N) => cons(I, filterGt(IS, N))
    requires I >Int N
  rule filterGt(cons(I, IS), N) => filterGt(IS, N)
    requires I <=Int N
endmodule
