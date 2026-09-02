requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Mutation: the letter branch appends `c` instead of `c.swapcase()`.
  // The original expected result for the witness "a" is still "A".
  claim [mutated-body]:
    <k>
      #loadAll(Module(
        FuncDef(
          "solve",
          Params("s"),
          Expr(
            Str(
              "Toggle letter case, or reverse a string containing no letters."))
          Assign(Name("swapped"), Str(""))
          Assign(Name("reversed_s"), Str(""))
          Assign(Name("has_letter"), Bool(false))
          Assign(Name("c"), Str(""))
          For(
            Name("c"),
            Name("s"),
            Assign(
              Name("reversed_s"),
              BinOp("+", Name("c"), Name("reversed_s")))
            If(
              Call(Attribute(Name("c"), "isalpha"), .Exprs),
              AugAssign(Name("swapped"), "+", Name("c"))
              Assign(Name("has_letter"), Bool(true))
              .Stmts,
              AugAssign(Name("swapped"), "+", Name("c"))
              .Stmts)
            .Stmts)
          If(
            Name("has_letter"),
            Return(Name("swapped")) .Stmts,
            .Stmts)
          Return(Name("reversed_s"))
          .Stmts)
        Assign(
          Name("answer"),
          Call(Name("solve"), str(iCons(97, .IntSeq))))
        .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(
               "answer" |-> str(iCons(65, .IntSeq))
               "solve"  |-> ?SOLVE:Val,
               parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
