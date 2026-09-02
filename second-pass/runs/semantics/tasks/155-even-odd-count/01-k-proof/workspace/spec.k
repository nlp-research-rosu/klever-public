requires "verification.k"

module EVEN-ODD-LOOP-SPEC
  imports EVEN-ODD-VERIFICATION

  // Inductive loop invariant.  kprove closes the nonempty case circularly
  // after executing one real iteration of #digitLoopBody.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), #digitLoopBody)
      ~> CONT:K
    =>
      CONT
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> #evenOddModuleScope
      1  |-> scope(
        "num"        |-> N:Int
        "even_count" |-> E:Int
        "odd_count"  |-> O:Int
        "digit"      |-> D:Val,
        parent(0))
    =>
      -1 |-> builtinsScope
      0  |-> #evenOddModuleScope
      1  |-> scope(
        "num"        |-> N
        "even_count" |-> E +Int evenDigits(CS)
        "odd_count"  |-> O +Int oddDigits(CS)
        "digit"      |-> lastSeen(CS, D),
        parent(0))
    </scopes>
endmodule

module EVEN-ODD-SPEC
  imports EVEN-ODD-VERIFICATION-SUMMARY

  // Calling the loaded solution on any mathematical integer returns exactly
  // the two counts over abs(num)'s decimal representation.
  claim
    <k>
      Call(Name("even_odd_count"), Int(N:Int))
    =>
      tuple(vCons(
        evenDigits(strToCodes(Int2String(absInt(N)))),
        vCons(
          oddDigits(strToCodes(Int2String(absInt(N)))),
          .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> #evenOddModuleScope
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
