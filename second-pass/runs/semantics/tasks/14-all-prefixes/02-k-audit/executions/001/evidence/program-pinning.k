requires "verification.k"

module PROGRAM-PINNING
  imports VERIFICATION

  // Reviewer-side execution check: loading the named term used by the entry
  // claim must install exactly the function body in trusted-translator output.
  claim
    <k> #loadAll(solutionModule()) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "all_prefixes" |->
          closureVal(
            "string",
            .ParamNames,
            Expr(Str("Return all nonempty prefixes of string, shortest first."))
            Assign(Name("prefixes"), ListExpr(.Exprs))
            For(
              Name("end"),
              Call(
                Name("range"),
                Int(1),
                BinOp(
                  "+",
                  Call(Name("len"), Name("string")),
                  Int(1))),
              Expr(
                Call(
                  Attribute(Name("prefixes"), "append"),
                  Subscript(
                    Name("string"),
                    Slice(NoBound, Name("end"), NoBound)))))
            Return(Name("prefixes"))
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
    [label(program-term-equality)]
endmodule
