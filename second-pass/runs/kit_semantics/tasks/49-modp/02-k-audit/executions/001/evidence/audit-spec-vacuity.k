requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      Call(Name("modp"), Int(3), Int(5))
      =>
      4
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "modp" |->
          closureVal(
            ("n", "p"),
            Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p"))),
            0
          ),
        parent(-1)
      )
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
