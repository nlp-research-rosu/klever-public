requires "/tmp/audit-work/161-solve/scratch/verification.k"

module BODY-SENSITIVITY
  imports VERIFICATION

  claim [wrong-alphabetic-return]:
    <k>
      #loadAll(Module(
        FuncDef(
          "solve",
          Params("s"),
          Expr(
            Str("Toggle letter case, or reverse a string containing no letters."))
          Assign(Name("swapped"), Str(""))
          Assign(Name("reversed_s"), Str(""))
          Assign(Name("has_letter"), Bool(false))
          Assign(Name("c"), Str(""))
          For(Name("c"), Name("s"), loopBody)
          // Deliberate body mutation: alphabetic input returns reversed_s.
          If(
            Name("has_letter"),
            Return(Name("reversed_s")) .Stmts,
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
               "answer" |-> solveResult(iCons(97, .IntSeq))
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
