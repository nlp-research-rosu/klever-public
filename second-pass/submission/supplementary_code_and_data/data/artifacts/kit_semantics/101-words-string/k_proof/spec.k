requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [words-string]:
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
      ~> Call(Name("words_string"), str(CS:IntSeq))
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
      0 |-> list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
