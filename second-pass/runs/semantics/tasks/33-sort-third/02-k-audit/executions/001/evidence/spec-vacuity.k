requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Keep the real auxiliary invariant available and simultaneously discharged.
  claim [sort-third-loop-vacuity-support]:
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

  // Deliberately false mutation: require an additional trailing zero in the
  // returned list. For [5,6,3,4,8,9,2], the real result has length 7, not 8.
  claim [sort-third-false-appended-zero]:
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
      2 |-> list(
        valSeqConcat(
          sortThird(INPUT),
          vCons(0, .ValSeq)))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
