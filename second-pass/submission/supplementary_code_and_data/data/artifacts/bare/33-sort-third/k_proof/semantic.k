module MPY-SYNTAX
  imports INT-SYNTAX
  imports STRING-SYNTAX

  syntax Pgm ::= Program
  syntax Program ::= "Module" "(" Stmts ")" [symbol(Module)]

  syntax Stmts ::= List{Stmt, ""}
  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")" [symbol(FuncDef)]
                | "Assign" "(" Expr "," Expr ")"                [symbol(Assign)]
                | "Return" "(" Expr ")"                         [symbol(Return)]

  syntax Params ::= "Params" "(" StringList ")" [symbol(Params)]
  syntax StringList ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"                         [symbol(Name)]
                | "Int" "(" Int ")"                             [symbol(IntExpr)]
                | "Subscript" "(" Expr "," Index ")"           [symbol(Subscript)]
                | "Call" "(" Expr "," Exprs ")"                [symbol(Call)]
  syntax Exprs ::= List{Expr, ","}

  syntax Index ::= Expr
                 | "Slice" "(" Bound "," Bound "," Bound ")" [symbol(Slice)]
  syntax Bound ::= Expr | "NoBound"

  // Runtime values. HumanEval exercises this task on finite integer lists.
  syntax Ints ::= List{Int, ","}
  syntax Value ::= "VList" "(" Ints ")" [symbol(VList)]
                 | "VInt" "(" Int ")"   [symbol(VInt)]
endmodule

module SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports MAP

  syntax ExecResult ::= "returned" "(" Value ")" [symbol(returned)]
                      | "finished" "(" Map ")"    [symbol(finished)]
                      | "exec" "(" Stmts "," Map ")" [function, symbol(exec)]

  syntax Value ::= "eval" "(" Expr "," Map ")" [function, symbol(eval)]
                 | "sliceThird" "(" Value ")"   [function, symbol(sliceThird)]
                 | "sortedValue" "(" Value ")"  [function, symbol(sortedValue)]
                 | "assignThird" "(" Value "," Value ")"
                     [function, symbol(assignThird)]

  syntax Ints ::= "thirds" "(" Ints ")" [function, symbol(thirds)]
                | "thirdsFrom" "(" Int "," Ints ")"
                    [function, symbol(thirdsFrom)]
                | "sortInts" "(" Ints ")" [function, symbol(sortInts)]
                | "insertInt" "(" Int "," Ints ")"
                    [function, symbol(insertInt)]
                | "replaceThirdInts" "(" Int ";" Ints ";" Ints ")"
                    [function, symbol(replaceThirdInts)]

  configuration
    <sort-third>
      <k> $PGM:Pgm </k>
      <input> $INPUT:Value </input>
      <result> .K </result>
    </sort-third>

  // A one-function HumanEval module is loaded and its requested entry point is
  // invoked with INPUT. The function body itself is then interpreted below.
  rule <k> Module(FuncDef("sort_third", Params(P:String), BODY))
            => exec(BODY, P |-> ARG) ...</k>
       <input> ARG </input>

  rule <k> returned(V) => .K ...</k>
       <result> .K => V </result>

  rule eval(Name(X), RHO) => {RHO [ X ]}:>Value
    requires X in_keys(RHO)
  rule eval(Int(I), _) => VInt(I)
  rule eval(Subscript(E, Slice(NoBound, NoBound, NoBound)), RHO)
    => eval(E, RHO)
  rule eval(Subscript(E, Slice(NoBound, NoBound, Int(3))), RHO)
    => sliceThird(eval(E, RHO))
  rule eval(Call(Name("sorted"), E), RHO)
    => sortedValue(eval(E, RHO))

  rule sliceThird(VList(IS)) => VList(thirds(IS))
  rule sortedValue(VList(IS)) => VList(sortInts(IS))
  rule assignThird(VList(IS), VList(RS))
    => VList(replaceThirdInts(0 ; IS ; RS))

  rule exec(.Stmts, RHO) => finished(RHO)
  rule exec(Assign(Name(X), E) REST, RHO)
    => exec(REST, RHO [ X <- eval(E, RHO) ])
  rule exec(
         Assign(Subscript(Name(X), Slice(NoBound, NoBound, Int(3))), E) REST,
         RHO)
    => exec(REST,
         RHO [ X <- assignThird({RHO [ X ]}:>Value, eval(E, RHO)) ])
    requires X in_keys(RHO)
  rule exec(Return(E) _REST, RHO) => returned(eval(E, RHO))

  rule thirds(IS) => thirdsFrom(0, IS)
  rule thirdsFrom(_, .Ints) => .Ints
  rule thirdsFrom(0, I, IS) => I, thirdsFrom(2, IS)
  rule thirdsFrom(N, _I, IS) => thirdsFrom(N -Int 1, IS)
    requires N >Int 0

  rule sortInts(.Ints) => .Ints
  rule sortInts(I, IS) => insertInt(I, sortInts(IS))
  rule insertInt(I, .Ints) => I
  rule insertInt(I, J, JS) => I, J, JS
    requires I <=Int J
  rule insertInt(I, J, JS) => J, insertInt(I, JS)
    requires I >Int J

  rule replaceThirdInts(_ ; .Ints ; .Ints) => .Ints
  rule replaceThirdInts(0 ; _I, IS ; R, RS)
    => R, replaceThirdInts(2 ; IS ; RS)
  rule replaceThirdInts(N ; I, IS ; RS)
    => I, replaceThirdInts(N -Int 1 ; IS ; RS)
    requires N >Int 0
endmodule
