requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Val ::= "multiplyClosureMutant" [function, total]
  rule multiplyClosureMutant
    => closureVal(
         ("a", "b"),
         (Expr(
            Str(
              "Complete the function that takes two integers and returns\n    the product of their unit digits.\n    Assume the input is always valid.\n    Examples:\n    multiply(148, 412) should return 16.\n    multiply(19, 28) should return 72.\n    multiply(2020, 1851) should return 0.\n    multiply(14,-15) should return 20.\n    "))
          Return(
            BinOp(
              "*",
              BinOp("%", Name("a"), Int(9)),
              BinOp("%", Name("b"), Int(10))))),
         0)

  syntax KItem ::= "#runMultiplyMutant" "(" Int "," Int ")"
  rule <k> #runMultiplyMutant(A:Int, B:Int)
        => Call(multiplyClosureMutant, A, B) ... </k>

  syntax Int ::= unitDigitMutant(Int) [function, total]
  rule unitDigitMutant(I:Int) => pyMod(I, 10)

  syntax Int ::= unitDigitProductMutant(Int, Int) [function, total]
  rule unitDigitProductMutant(A:Int, B:Int)
    => unitDigitMutant(A) *Int unitDigitMutant(B)
endmodule
