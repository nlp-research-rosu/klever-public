requires "verification.k"

module SPEC-AUDIT-FALSE
  imports VERIFICATION

  // Fresh reviewer mutation. The precondition witness n=49 is valid, but the
  // real largest proper divisor is 7, not the deliberately required 8.
  claim [false-entry-49]:
    <k> Call(Name("largest_divisor"), Int(49)) => 8 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "largest_divisor" |->
          closureVal(
            "n",
            Assign(
              Name("divisor"),
              BinOp("-", Name("n"), Int(1)))
            While(
              Compare(
                BinOp("%", Name("n"), Name("divisor")),
                CmpOp("!=", Int(0))),
              Assign(
                Name("divisor"),
                BinOp("-", Name("divisor"), Int(1))) .Stmts)
            Return(Name("divisor")) .Stmts,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
