requires "verification.k"

module FLIP-CASE-SPEC
  imports FLIP-CASE-VERIFICATION

  claim
    <k>
      FuncDef("flip_case", Params("string"), Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)))
      Assign(Name("result"), Call(Name("flip_case"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "flip_case" <- ?_:Val ] [ "result" <- ?R:Val ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==K str(mapSwap(CS))
    [all-path]
endmodule
