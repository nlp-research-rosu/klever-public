requires "reference-semantics/semantics.k"

module WORDS-STRING-MODULE-CONNECTION
  imports MPY

  // Bridge-free fixed-semantics check: loading the exact submitted MPY module
  // creates exactly the literal closure used by the entry claim.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "words_string",
            Params("s"),
            Return(
              Call(
                Attribute(
                  Call(
                    Attribute(Name("s"), "replace"),
                    (Str(","), Str(" "), .Exprs)),
                  "split"),
                .Exprs)))))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "words_string" |->
          closureVal(
            ("s", .ParamNames),
            Return(
              Call(
                Attribute(
                  Call(
                    Attribute(Name("s"), "replace"),
                    (Str(","), Str(" "), .Exprs)),
                  "split"),
                .Exprs))
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
    <exit-code> 0 </exit-code>
endmodule
