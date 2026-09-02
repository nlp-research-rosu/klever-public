requires "verification.k"

module NEXT-SMALLEST-LOOP-SPEC
  imports NEXT-SMALLEST-VERIFICATION

  // Loop invariant / functional-correctness theorem.  INPUT is arbitrary and
  // the three accumulator values describe an arbitrary already-scanned prefix;
  // the claim is therefore closed by circularity on every remaining element.
  claim
    <k>
      #loop(list(intVals(INPUT:Ints)),
            Name("value"),
            nextSmallestLoopBody)
      ~> nextSmallestReturn
      ~> #endcall
    =>
      nsScan(INPUT, SMALLEST:Int, SECOND:Int,
             COUNT:Int)
      ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (SC:Map
       1 |-> scope(("value" |-> OLD_VALUE:Int
                    "lst" |-> LST:Val
                    "smallest" |-> SMALLEST
                    "second" |-> SECOND
                    "count" |-> COUNT),
                   parent(0)))
    =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map => HEAP </heap>
    <heapLoc> HLOC:Int => HLOC </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1)) REST:List
    =>
      REST
    </stack>
    <ret> noRet => noRet </ret>
    <exc> EXC:Exc => EXC </exc>
    <exit-code> CODE:Int => CODE </exit-code>
    requires notBool (1 in_keys(SC))
endmodule

module NEXT-SMALLEST-ENTRY-SPEC
  imports NEXT-SMALLEST-WITH-LOOP-LEMMA

  // The entry-point theorem: loading the translated function and calling it
  // from the initial configuration establishes the loop theorem's initial
  // accumulator state.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("next_smallest"),
              (list(intVals(INPUT:Ints)), .Exprs))
    =>
      nsScan(INPUT, 0, 0, 0)
    </k>
    <env> 0 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    =>
      ?FINAL_ENTRY_SCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
