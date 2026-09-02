requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfiable witness text == "": the real result is "".
  claim [false-result]:
    <k>
      Call(Name("fix_spaces"), str(.IntSeq))
      => str(iCons(95, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "fix_spaces" |->
                 closureVal(("text", .ParamNames), #fixSpacesBody, 0),
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
