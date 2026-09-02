requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(str(CS:IntSeq), Name("char"), #fixSpacesLoopBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L:Int |-> scope(
        "char"   |-> (CH:Val      => charAfter(CS, CH))
        "result" |-> (str(R:IntSeq) => str(resultAfter(CS, R, P)))
        "spaces" |-> (str(P:IntSeq) => str(pendingAfter(CS, P)))
        "text"   |-> str(T:IntSeq),
        PAR:Parent)
      ...
    </scopes>

  claim [target]:
    <k>
      Call(Name("fix_spaces"), str(CS:IntSeq))
      => str(fixedSpaces(CS))
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
