requires "verification.k"

module STRLEN-SPEC
  imports STRLEN-VERIFICATION

  claim
    <k>
      FuncDef("strlen", Params("string"), Return(Call(Name("len"), Name("string"))))
      Assign(Name("result"), Call(Name("strlen"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "strlen" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Int isLen(CS)
    [all-path]
endmodule
