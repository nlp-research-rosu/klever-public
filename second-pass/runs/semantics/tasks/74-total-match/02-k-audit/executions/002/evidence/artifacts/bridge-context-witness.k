requires "verification.k"

module BRIDGE-CONTEXT-WITNESS
  imports TOTAL-MATCH-VERIFICATION

  // False under fixed semantics. The real loop overwrites item with "a", so
  // the trailing Name("item") returns "a". The proof-local For bridge skips
  // that binding effect and therefore returns the old value "z".
  claim
    <k>
      For(
        Name("item"),
        list(strVals(ssCons(iCons(97, .IntSeq), .StrSeq))),
        AugAssign(
          Name("acc"),
          "+",
          Call(Name("len"), Name("item"))) .Stmts)
      ~> Name("item")
      => str(iCons(122, .IntSeq))
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
      1  |-> scope(
        (("acc" |-> 0) ("item" |-> str(iCons(122, .IntSeq)))
          => ("acc" |-> 1) ("item" |-> str(iCons(122, .IntSeq)))),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
