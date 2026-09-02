requires "verification.k"

module IS-PALINDROME-SPEC
  imports IS-PALINDROME-VERIFICATION

  // ---- Loop invariant (circularity) — mirrored-index scan over the remaining range; result staged in <ret>.
  claim
    <k>
      #loop(rangeObj(I:Int, N:Int, 1), Name("i"),
        If(Compare(
          Subscript(Name("text"), Name("i")),
          CmpOp(
            "!=",
            Subscript(
              Name("text"),
              BinOp(
                "-",
                BinOp("-", Call(Name("len"), Name("text")), Int(1)),
                Name("i"))))),
          Return(Bool(false)),
          .Stmts))
      ~> Return(Bool(true)) .Stmts ~> #endcall
    => #pop </k>
    <ret> noRet => retV(?R:Bool) </ret>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "is_palindrome" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "text" <- str(CS:IntSeq) ] [ "i" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "text" <- str(CS) ] [ "i" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool N ==Int isLen(CS)
    ensures ?R ==Bool palFrom(CS, I)
    [all-path]

  // ---- Entry claim — result = is_palindrome(str(CS)) == palFrom(CS, 0).
  claim
    <k>
      FuncDef("is_palindrome", Params("text"),
        For(Name("i"), Call(Name("range"), Call(Name("len"), Name("text"))),
          If(Compare(
            Subscript(Name("text"), Name("i")),
            CmpOp(
              "!=",
              Subscript(
                Name("text"),
                BinOp(
                  "-",
                  BinOp("-", Call(Name("len"), Name("text")), Int(1)),
                  Name("i"))))),
            Return(Bool(false)),
            .Stmts))
        Return(Bool(true)))
      Assign(Name("result"), Call(Name("is_palindrome"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_palindrome" <- ?_:Val ] [ "result" <- ?R:Bool ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool palFrom(CS, 0)
    [all-path]
endmodule
