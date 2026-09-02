requires "semantic.k"

module VERIFICATION
  imports MPY

  syntax Int ::= squareCeil(NumValue) [function]
               | sumSquares(PList) [function, total]
               | sumSquaresFrom(Int, PList) [function, total]

  rule squareCeil(V) => ceilInt(V) *Int ceilInt(V)

  rule sumSquares(VS) => sumSquaresFrom(0, VS)
  rule sumSquaresFrom(A, nil) => A
  rule sumSquaresFrom(A, cons(V, VS))
    => sumSquaresFrom(A +Int squareCeil(V), VS)
endmodule
