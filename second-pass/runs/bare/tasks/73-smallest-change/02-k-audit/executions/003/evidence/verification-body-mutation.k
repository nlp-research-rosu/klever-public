requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Mathematical specification.  Each outer pair is independent: an equal
  // pair costs zero, while an unequal pair necessarily and sufficiently costs
  // one edit.  Removing that pair therefore defines the minimum recursively.
  syntax Int ::= minimumPalindromeChanges(List) [function, total]

  rule minimumPalindromeChanges(L) => 0
    requires size(L) <=Int 1 [simplification]
  rule minimumPalindromeChanges(L)
    => minimumPalindromeChanges(range(L, 1, 1))
    requires size(L) >Int 1
     andBool {L[0]}:>Int ==Int {L[-1]}:>Int [simplification]
  rule minimumPalindromeChanges(L)
    => 1 +Int minimumPalindromeChanges(range(L, 1, 1))
    requires size(L) >Int 1
     andBool notBool ({L[0]}:>Int ==Int {L[-1]}:>Int) [simplification]

  // This function constant expands to the exact Stmts tree in solution.mpy.
  // It keeps claims readable while still proving the translated body itself.
  syntax Stmts ::= "#smallestChangeBody" [function, symbol(smallestChangeBody)]
  rule #smallestChangeBody =>
    If(Compare(Call(Name("len"), Name("arr")), CmpOp("<=", Int(1))),
      Return(Int(0)),
      .Stmts)
    If(Compare(Subscript(Name("arr"), Int(0)),
               CmpOp("==", Subscript(Name("arr"), UnaryOp("-", Int(1))))),
      Return(Call(Name("smallest_change"),
                  Subscript(Name("arr"),
                            Slice(Int(1), UnaryOp("-", Int(1)), NoBound)))),
      .Stmts)
    Return(BinOp("+", Int(2),
                 Call(Name("smallest_change"),
                      Subscript(Name("arr"),
                                Slice(Int(1), UnaryOp("-", Int(1)), NoBound)))))
endmodule
