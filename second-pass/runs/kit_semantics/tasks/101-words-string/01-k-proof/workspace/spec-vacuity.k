requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: words_string("") returns [], not [""].
  claim [false-result]:
    <k>
      Call(Name("words_string"), str(.IntSeq))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "words_string" |-> closureVal(
          ("s", .ParamNames),
          (Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs))
            .Stmts),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(str(.IntSeq), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
