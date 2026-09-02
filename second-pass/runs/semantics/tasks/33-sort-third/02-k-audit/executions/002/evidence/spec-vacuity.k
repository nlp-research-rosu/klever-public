requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Inductive loop invariant.  It is intentionally generalized over the
  // starting index and already-built prefix so that the recursive loop state
  // is another instance of the same claim.
  claim [sort-third-loop]:
    <k>
      #loop(list(INPUT:ValSeq), Name("value"), sortThirdBody)
      ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      L |-> scope(
        "i"      |-> (I:Int => I +Int vsLen(INPUT))
        "l"      |-> LISTARG:Val
        "value"  |-> (OLD:Val => lastLoopValue(INPUT, OLD))
        "result" |-> ref(HR:Int)
        "thirds" |-> ref(HT:Int),
        parent(0))
      RESTSCOPES:Map
    </scopes>
    <heap>
      HT |-> list(SORTED:ValSeq)
      HR |-> list(
        ACC:ValSeq
        => sortThirdAcc(INPUT, SORTED, I, ACC))
      RESTHEAP:Map
    </heap>
    requires I >=Int 0

  // End-to-end claim from loading the translated module through returning the
  // freshly allocated result.  INPUT is arbitrary; the trusted sort primitive
  // remains opaque, while the complete surrounding list transformation is
  // proved.
  claim [sort-third-correct]:
    <k>
      #loadAll(sortThirdModule)
      ~> Call(Name("sort_third"), list(INPUT:ValSeq))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        .Map
        => ("sort_third" |-> sortThirdClosure),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(buildVS(INPUT, 0, vsLen(INPUT), 3))
      1 |-> list(sortVS(buildVS(INPUT, 0, vsLen(INPUT), 3)))
      2 |-> list(vCons(999, sortThird(INPUT)))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
