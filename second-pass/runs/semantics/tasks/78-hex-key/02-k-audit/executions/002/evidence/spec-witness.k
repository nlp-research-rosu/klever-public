requires "verification.k"

module HEX-KEY-WITNESS-SPEC
  imports HEX-KEY-VERIFICATION

  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBody)))
      ~> Call(Name("hex_key"), str(.IntSeq))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       =>
       0 |-> scope(
         "hex_key" |-> closureVal(("num", .ParamNames), hexKeyBody, 0),
         parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(witness-empty)]

  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBody)))
      ~> Call(
           Name("hex_key"),
           str(iCons(50, iCons(65, iCons(51, iCons(68, .IntSeq))))))
      => 3
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       =>
       0 |-> scope(
         "hex_key" |-> closureVal(("num", .ParamNames), hexKeyBody, 0),
         parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(witness-mixed)]
endmodule
