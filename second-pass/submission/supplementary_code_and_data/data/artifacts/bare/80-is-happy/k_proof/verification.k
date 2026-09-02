requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // Independent mathematical reading of the prompt.  #allTriples is true
  // exactly when every length-three window has pairwise-distinct code points.
  syntax Bool ::= #distinct3 ( Int , Int , Int ) [function, total]
  rule #distinct3(A, B, C)
    => notBool (A ==Int B)
       andBool notBool (A ==Int C)
       andBool notBool (B ==Int C)

  syntax Bool ::= #allTriples ( PString ) [function, total]
  rule #allTriples(eps) => true
  rule #allTriples(ch(_A, eps)) => true
  rule #allTriples(ch(_A, ch(_B, eps))) => true
  rule #allTriples(ch(A, ch(B, ch(C, REST))))
    => #distinct3(A, B, C)
       andBool #allTriples(ch(B, ch(C, REST)))

  syntax Bool ::= #happy ( PString ) [function, total]
  rule #happy(eps) => false
  rule #happy(ch(_A, eps)) => false
  rule #happy(ch(_A, ch(_B, eps))) => false
  rule #happy(ch(A, ch(B, ch(C, REST))))
    => #allTriples(ch(A, ch(B, ch(C, REST))))

  // The exact constructor tree emitted in solution.mpy.  Giving it a name
  // keeps proof claims readable while still forcing the semantics to execute
  // precisely the translated implementation.
  syntax Program ::= "#solution" [function]
  rule #solution =>
    Module(
      FuncDef("is_happy", Params("s"),
        If(Compare(Call(Name("len"), Name("s")), CmpOp("<", Int(3))),
          Return(Bool(false)),
          .Stmts)
        Return(Call(Name("check_happy_triples"), Name("s"))))
      FuncDef("check_happy_triples", Params("s"),
        If(Compare(Call(Name("len"), Name("s")), CmpOp("<", Int(3))),
          Return(Bool(true)),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(0)),
                   CmpOp("==", Subscript(Name("s"), Int(1)))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(0)),
                   CmpOp("==", Subscript(Name("s"), Int(2)))),
          Return(Bool(false)),
          .Stmts)
        If(Compare(Subscript(Name("s"), Int(1)),
                   CmpOp("==", Subscript(Name("s"), Int(2)))),
          Return(Bool(false)),
          .Stmts)
        Return(Call(Name("check_happy_triples"),
                    Subscript(Name("s"),
                              Slice(Int(1), NoBound, NoBound))))))
endmodule
