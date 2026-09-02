requires "/tmp/audit-work/154-cycpattern-check/candidate/verification.k"

module SPEC-LEMMA
  imports VERIFICATION-BASE

  claim [loop-invariant]:
    <k>
      #loop(
        str(REM),
        Name("char"),
        If(
          Compare(Name("pattern"), CmpOp("in", Name("a"))),
          Return(Bool(true)),
          .Stmts)
        Assign(
          Name("pattern"),
          BinOp(
            "+",
            Subscript(
              Name("pattern"),
              Slice(Int(1), NoBound, NoBound)),
            Name("char")))
        .Stmts)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
    =>
      rotationsLoop(A, P, REM)
      ~> CONT
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (1 |-> scope(
         ("a" |-> str(A))
         ("b" |-> str(B))
         ("char" |-> str(CH))
         ("pattern" |-> str(P)),
         parent(0))
       0 |-> scope(G, parent(-1))
       -1 |-> BS:Scope)
    =>
      (0 |-> scope(G, parent(-1))
       -1 |-> BS)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <stack>
      (ListItem(frame(CONT:K, 0, 1)) REST:List => REST)
    </stack>
    <ret> noRet </ret>
endmodule

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [entry-point]:
    <k>
      Call(
        Name("cycpattern_check"),
        str(A), str(B), .Exprs)
    =>
      rotationsLoop(A, B, B)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "cycpattern_check" |->
          closureVal(
            ("a", "b", .ParamNames),
            Assign(Name("pattern"), Str(""))
            Assign(Name("char"), Str(""))
            For(
              Name("char"),
              Name("b"),
              If(
                Compare(
                  Name("pattern"),
                  CmpOp("in", Name("a"))),
                Return(Bool(true)),
                .Stmts)
              Assign(
                Name("pattern"),
                BinOp(
                  "+",
                  Subscript(
                    Name("pattern"),
                    Slice(Int(1), NoBound, NoBound)),
                  Name("char")))
              .Stmts)
            Return(Bool(false))
            .Stmts,
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
endmodule
