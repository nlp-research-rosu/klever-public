requires "helper-witness-verification.k"

module UNIQUE-DIGITS-HELPER-FALSE-CONCLUSION
  imports UNIQUE-DIGITS-HELPER-FALSE-WITNESS

  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "_all_digits_odd",
            Params("n"),
            oddDigitsBody)))
      ~> Call(Name("_all_digits_odd"), Int(2))
    =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "_all_digits_odd" |->
          closureVal(("n", .ParamNames), oddDigitsBody, 0),
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
