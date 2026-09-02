requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is the executable body emitted in solution.mpy, packaged as a value
  // so a claim can call it with arbitrary K integers.
  syntax Val ::= "multiplyClosure" [function, total]
  rule multiplyClosure
    => closureVal(
         ("a", "b"),
         (Expr(
            Str(
              "Complete the function that takes two integers and returns\n    the product of their unit digits.\n    Assume the input is always valid.\n    Examples:\n    multiply(148, 412) should return 16.\n    multiply(19, 28) should return 72.\n    multiply(2020, 1851) should return 0.\n    multiply(14,-15) should return 20.\n    "))
          Return(
            BinOp(
              "*",
              BinOp("%", Name("a"), Int(10)),
              BinOp("%", Name("b"), Int(10))))),
         0)

  syntax KItem ::= "#runMultiply" "(" Int "," Int ")"
  rule <k> #runMultiply(A:Int, B:Int)
        => Call(multiplyClosure, A, B) ... </k>

  // Contract vocabulary: Python's unit digit is its remainder modulo 10.
  syntax Int ::= unitDigit(Int) [function, total]
  rule unitDigit(I:Int) => pyMod(I, 10)

  syntax Int ::= unitDigitProduct(Int, Int) [function, total]
  rule unitDigitProduct(A:Int, B:Int)
    => unitDigit(A) *Int unitDigit(B)
endmodule
