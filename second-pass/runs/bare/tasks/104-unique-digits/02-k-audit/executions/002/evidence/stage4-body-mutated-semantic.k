requires "domains.md"

module MPY-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX
  imports STRING-SYNTAX

  syntax Program ::= "Module" "(" Stmts ")"
                   | "solutionProgram" [function, total]
  syntax Stmts ::= List{Stmt, ""}

  syntax Stmt ::= "FuncDef" "(" String "," Params "," Stmts ")"
                | "If" "(" Expr "," Stmts "," Stmts ")"
                | "Return" "(" Expr ")"

  syntax Params ::= "Params" "(" Strings ")"
  syntax Strings ::= List{String, ","}

  syntax Expr ::= "Name" "(" String ")"
                | "Int" "(" Int ")"
                | "Bool" "(" Bool ")"
                | "BinOp" "(" String "," Expr "," Expr ")"
                | "Compare" "(" Expr "," CmpOps ")"
                | "Call" "(" Expr "," Exprs ")"
                | "ListComp" "(" Expr "," CompFors ")"

  syntax Exprs ::= List{Expr, ","}
  syntax CmpOp ::= "CmpOp" "(" String "," Expr ")"
  syntax CmpOps ::= List{CmpOp, ","}
  syntax CompFor ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
  syntax CompFors ::= List{CompFor, ""}

  syntax IntSeq ::= ".Ints"
                  | "cons" "(" Int "," IntSeq ")"
  syntax PyVal ::= "pyList" "(" IntSeq ")"
                 | "pyBool" "(" Bool ")"
endmodule

module MPY-SEMANTIC
  imports MPY-SYNTAX
  imports INT
  imports BOOL

  syntax KItem ::= "invoke" "(" String "," PyVal ")"

  configuration <k> $PGM:Program ~> invoke("unique_digits", $ARGS:PyVal) </k>

  // This macro connects execution to the untranslated CPython AST.  It
  // deliberately mentions every node in solution.mpy: changing the
  // implementation invalidates both concrete execution and the proof.
  rule solutionProgram
       => Module(
           FuncDef("no_even_digit", Params("n"),
             If(Compare(Name("n"), CmpOp("==", Int(0))),
               Return(Bool(false)),
               .Stmts)
             If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
               Return(Bool(false)),
               .Stmts)
             Return(Call(Name("no_even_digit"),
               BinOp("//", Name("n"), Int(10)))))
           FuncDef("unique_digits", Params("x"),
             Return(Call(Name("sorted"),
               ListComp(Name("n"),
                 CompFor(Name("n"), Name("x"),
                   Call(Name("no_even_digit"), Name("n"))))))))

  syntax Bool ::= "isUniqueDigitsProgram" "(" Program ")" [function]
  rule isUniqueDigitsProgram(
         Module(
           FuncDef("no_even_digit", Params("n"),
             If(Compare(Name("n"), CmpOp("==", Int(0))),
               Return(Bool(true)),
               .Stmts)
             If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(0))),
               Return(Bool(false)),
               .Stmts)
             Return(Call(Name("no_even_digit"),
               BinOp("//", Name("n"), Int(10)))))
           FuncDef("unique_digits", Params("x"),
             Return(Call(Name("sorted"),
               ListComp(Name("n"),
                 CompFor(Name("n"), Name("x"),
                   Call(Name("no_even_digit"), Name("n")))))))))
       => true

  // Executable meaning of the source constructs used above.  no_even_digit
  // scans base-10 digits; the comprehension filters without changing
  // multiplicity; sorted performs insertion sort.
  syntax Bool ::= "oddDigits" "(" Int ")" [function, total]
  rule oddDigits(N) => false requires N <Int 0
  rule oddDigits(0) => true
  rule oddDigits(N) => false
    requires N >Int 0 andBool N %Int 2 ==Int 0
  rule oddDigits(N) => oddDigits(N /Int 10)
    requires N >Int 0 andBool N %Int 2 =/=Int 0

  syntax IntSeq ::= "filterOddDigits" "(" IntSeq ")" [function, total]
  rule filterOddDigits(.Ints) => .Ints
  rule filterOddDigits(cons(N, NS)) => cons(N, filterOddDigits(NS))
    requires oddDigits(N)
  rule filterOddDigits(cons(N, NS)) => filterOddDigits(NS)
    requires notBool oddDigits(N)

  syntax IntSeq ::= "insertSorted" "(" Int "," IntSeq ")" [function, total]
  rule insertSorted(N, .Ints) => cons(N, .Ints)
  rule insertSorted(N, cons(M, MS)) => cons(N, cons(M, MS))
    requires N <=Int M
  rule insertSorted(N, cons(M, MS)) => cons(M, insertSorted(N, MS))
    requires N >Int M

  syntax IntSeq ::= "sortInts" "(" IntSeq ")" [function, total]
  rule sortInts(.Ints) => .Ints
  rule sortInts(cons(N, NS)) => insertSorted(N, sortInts(NS))

  syntax IntSeq ::= "uniqueDigitsMeaning" "(" IntSeq ")" [function, total]
  rule uniqueDigitsMeaning(NS) => sortInts(filterOddDigits(NS))

  rule <k> P:Program ~> invoke("unique_digits", pyList(NS))
        => pyList(uniqueDigitsMeaning(NS)) ... </k>
    requires isUniqueDigitsProgram(P)
endmodule
