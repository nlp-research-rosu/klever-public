requires "verification.k"

// Fresh audit mutation: add one to the even-digit result. For N = 0 the real
// and formal result is (1, 0), while this destination requires (2, 0).
module EVEN-ODD-SPEC-VACUITY
  imports EVEN-ODD-VERIFICATION-SUMMARY

  claim
    <k>
      Call(Name("even_odd_count"), Int(N:Int))
    =>
      tuple(vCons(
        evenDigits(strToCodes(Int2String(absInt(N)))) +Int 1,
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
