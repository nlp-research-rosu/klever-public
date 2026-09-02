requires "/tmp/audit-work/fresh/verification.k"

module AUDIT-SPEC-VACUITY
  imports EVEN-ODD-VERIFICATION-SUMMARY

  // Deliberately false: for every integer, demand one extra even digit.
  // Witness N = 0: the real and claimed original result is (1, 0), while
  // this mutation demands (2, 0).
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
