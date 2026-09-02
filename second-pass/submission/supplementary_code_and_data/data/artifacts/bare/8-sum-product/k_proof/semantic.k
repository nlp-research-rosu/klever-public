requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Module
  syntax Stmt
  syntax Stmts
  syntax Expr
  syntax Params
  syntax Strings

  syntax Module ::= "Module" "(" Stmts ")" [symbol(Module)]
  syntax Stmts ::= List{Stmt, ""} [symbol(Stmts)]
  syntax Strings ::= List{String, ","} [symbol(Strings)]

  syntax Stmt ::= "ImportFrom" "(" String "," Strings ")"
                [symbol(ImportFrom)]
                | "FuncDef" "(" String "," Params "," Stmts ")"
                [symbol(FuncDef)]
                | "Return" "(" Expr ")"
                [symbol(Return)]

  syntax Params ::= "Params" "(" String ")" [symbol(Params)]

  syntax Expr ::= "Name" "(" String ")" [symbol(Name)]
                | "TupleExpr" "(" Expr "," Expr ")"
                [symbol(TupleExpr)]
                | "Call" "(" Expr "," Expr ")"
                [symbol(Call)]
endmodule

module MPY
  imports MPY-SYNTAX
  imports INT
  imports MAP

  syntax Ints
  syntax Ints ::= ".Ints" [symbol(noInts)]
                | Int "," Ints [symbol(consInts)]

  syntax PyVal
  syntax PyVal ::= "PyInt" "(" Int ")" [symbol(PyInt)]
                 | "PyList" "(" Ints ")" [symbol(PyList)]
                 | "PyTuple" "(" PyVal "," PyVal ")" [symbol(PyTuple)]

  syntax Closure
  syntax Closure ::= "Closure" "(" String "," Expr ")"
                     [symbol(Closure)]

  syntax KItem ::= "#exec" "(" Stmts ")" [symbol(execStmts)]
                 | "#invoke" "(" String "," PyVal ")"
                   [symbol(invoke)]

  syntax Int ::= sumInts(Ints) [function, total]
               | productInts(Ints) [function, total]
  syntax PyVal ::= eval(Expr, Map) [function]
                 | sumValue(PyVal) [function]
                 | productValue(PyVal) [function]
                 | lookupValue(Map, String) [function]

  configuration
    <python>
      <k> $PGM:Module </k>
      <input> $INPUT:PyVal </input>
      <functions> .Map </functions>
      <result> .K </result>
    </python>

  rule <k> Module(SS) => #exec(SS) ~> #invoke("sum_product", V) ... </k>
       <input> V </input>

  rule #exec(.Stmts) => .K
  rule #exec(S SS) => S ~> #exec(SS)

  rule ImportFrom(_, _) => .K

  rule <k> FuncDef(F, Params(P), Return(E)) => .K ... </k>
       <functions> FS => FS [ F <- Closure(P, E) ] </functions>

  rule <k> #invoke(F, V) => .K ... </k>
       <functions> ... F |-> Closure(P, E) ... </functions>
       <result> .K => eval(E, P |-> V) </result>

  rule eval(Name(X), ENV) => lookupValue(ENV, X)
  rule lookupValue((X |-> V:PyVal) _REST, X) => V
  rule eval(TupleExpr(A, B), ENV)
       => PyTuple(eval(A, ENV), eval(B, ENV))
  rule eval(Call(Name("sum"), A), ENV)
       => sumValue(eval(A, ENV))
  rule eval(Call(Name("prod"), A), ENV)
       => productValue(eval(A, ENV))

  rule sumValue(PyList(IS)) => PyInt(sumInts(IS))
  rule productValue(PyList(IS)) => PyInt(productInts(IS))

  rule sumInts(.Ints) => 0
  rule sumInts(I , IS) => I +Int sumInts(IS)
  rule productInts(.Ints) => 1
  rule productInts(I , IS) => I *Int productInts(IS)
endmodule
