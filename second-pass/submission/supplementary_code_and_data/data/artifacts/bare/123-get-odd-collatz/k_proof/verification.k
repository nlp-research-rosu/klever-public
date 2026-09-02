requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // These three definitions spell the translated submission once for use in
  // claims.  They are equations over the very same AST constructors parsed
  // from solution.mpy; they do not bypass the operational semantics.
  syntax Stmt ::= "collatzBranch" [function, total]
  rule collatzBranch =>
    If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1)), .CmpOps),
       Assign(Name("odds"),
              BinOp("+", Name("odds"), ListExpr(Name("n"), .Exprs)))
       Assign(Name("n"),
              BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
       Assign(Name("n"), BinOp("//", Name("n"), Int(2))))

  syntax Stmt ::= "collatzLoop" [function, total]
  rule collatzLoop =>
    While(Compare(Name("n"), CmpOp("!=", Int(1)), .CmpOps), collatzBranch)

  syntax Pgm ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("get_odd_collatz", Params("n", .Ids),
        Assign(Name("odds"), ListExpr(.Exprs))
        collatzLoop
        Return(Call(Name("sorted"),
                    BinOp("+", Name("odds"), ListExpr(Int(1), .Exprs)),
                    .Exprs))))

  // Executable observers used by validation claims.
  syntax Bool ::= isSorted(Ints) [function, total]
  rule isSorted(.Ints) => true
  rule isSorted(_I :: .Ints) => true
  rule isSorted(I :: J :: JS) =>
       (I <=Int J andBool isSorted(J :: JS))

  syntax Bool ::= allOdd(Ints) [function, total]
  rule allOdd(.Ints) => true
  rule allOdd(I :: IS) =>
       ((I %Int 2) ==Int 1 andBool allOdd(IS))

  // Non-functional wrappers ensure observer claims take an operational proof
  // step instead of being normalized while the claim itself is parsed.
  syntax KItem ::= "checkSorted" "(" Ints ")"
                 | "checkAllOdd" "(" Ints ")"
  rule <k> checkSorted(IS) => isSorted(sortInts(IS)) ... </k>
  rule <k> checkAllOdd(IS) => allOdd(IS) ... </k>
endmodule
