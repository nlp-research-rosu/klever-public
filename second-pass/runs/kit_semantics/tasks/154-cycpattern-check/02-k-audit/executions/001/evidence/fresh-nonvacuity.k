requires "verification.k"

module FRESH-NONVACUITY
  imports VERIFICATION

  // Fresh false result obligation: "baa" is not initially in "abab", but its
  // left rotation "aba" is. The exact submitted body must therefore return
  // true, so the false destination below must remain unprovable.
  claim [false-rotation-result]:
    <k>
      Call(
        Name("cycpattern_check"),
        Str("abab"),
        Str("baa"))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "cycpattern_check" |->
          closureVal(
            ("a", "b"),
            Expr(
              Str(
                "Return whether b or one of its rotations is a substring of a."))
            Assign(
              Name("result"),
              Compare(Name("b"), CmpOp("in", Name("a"))))
            Assign(Name("rotation"), Name("b"))
            Assign(Name("c"), Str(""))
            For(
              Name("c"),
              Subscript(
                Name("b"),
                Slice(NoBound, UnaryOp("-", Int(1)), NoBound)),
              Assign(
                Name("rotation"),
                BinOp(
                  "+",
                  Subscript(
                    Name("rotation"),
                    Slice(Int(1), NoBound, NoBound)),
                  Name("c")))
              Assign(
                Name("result"),
                BoolOp(
                  "or",
                  Name("result"),
                  Compare(
                    Name("rotation"),
                    CmpOp("in", Name("a"))))))
            Return(Name("result")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
