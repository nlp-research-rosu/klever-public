requires "/tmp/audit-work/37-sort-even-audit/reconstruction-fresh/spec.k"

module SPEC-VACUITY-AUDIT
  imports SPEC

  // Deliberately false ground mutation.  This is the exact entry precondition
  // instantiated at VS = .ValSeq; the real result is [], not [0].
  claim [sort-even-false-empty-is-zero]:
    <k>
      Call(Name("sort_even"), list(.ValSeq))
      ~> #observeResult
    =>
      list(vCons(0, .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
        ("sort_even" |-> sortEvenClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?MUTHEAP </heap>
    <heapLoc> 0 => ?MUTHL </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
