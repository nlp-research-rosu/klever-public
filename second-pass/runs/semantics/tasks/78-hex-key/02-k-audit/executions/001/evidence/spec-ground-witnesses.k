requires "verification.k"

module HEX-KEY-GROUND-WITNESSES
  imports HEX-KEY-VERIFICATION

  // A concrete state satisfying the entry precondition: empty input.
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

  // A concrete state satisfying the entry precondition: "AB" (codes 65, 66).
  claim
    <k>
      #loadAll(Module(
        FuncDef("hex_key", Params("num"), hexKeyBody)))
      ~> Call(Name("hex_key"),
              str(iCons(65, iCons(66, .IntSeq))))
      => 1
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
    [label(witness-AB)]
endmodule
