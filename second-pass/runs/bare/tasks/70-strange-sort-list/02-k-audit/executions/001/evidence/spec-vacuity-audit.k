requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh auditor mutation.  The real result for [1,2,3,4] is [1,4,2,3];
  // this deliberately changes the result-constraining second element to 5.
  claim
    <program> solutionProgram </program>
    <input> cons(1, cons(2, cons(3, cons(4, nil)))) </input>
    <entry> "strange_sort_list" </entry>
    <result>
      pending
      =>
      pList(cons(1, cons(5, cons(2, cons(3, nil)))))
    </result>
endmodule
