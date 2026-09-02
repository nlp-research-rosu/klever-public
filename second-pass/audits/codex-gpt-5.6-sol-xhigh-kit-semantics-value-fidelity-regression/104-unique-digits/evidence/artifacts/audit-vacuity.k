requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: the prompt example actually returns [1, 15, 33].
  // This claim deliberately drops 33 from the result-bearing heap object.
  claim [example-drops-33]:
    <k>
      #loadAll(Module(
        FuncDef("unique_digits", Params("x"), #uniqueDigitsBody)))
      ~> Call(
           Name("unique_digits"),
           list(vCons(15,
                vCons(33,
                vCons(1422,
                vCons(1, .ValSeq))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?SC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(1, vCons(15, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
