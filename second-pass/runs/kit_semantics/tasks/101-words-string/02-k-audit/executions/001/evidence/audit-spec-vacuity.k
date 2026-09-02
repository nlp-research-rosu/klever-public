requires "/tmp/audit-work/reconstruction/verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-result mutation.  For the satisfying input "a,b", the exact
  // program returns ["a", "b"], not the single token ["ab"] demanded here.
  claim [false-single-token]:
    <k>
      #loadAll(Module(
        FuncDef(
          "words_string",
          Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs)))))
      ~> Call(
           Name("words_string"),
           str(iCons(97, iCons(44, iCons(98, .IntSeq)))))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
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
      0 |-> list(
        vCons(
          str(iCons(97, iCons(98, .IntSeq))),
          .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
