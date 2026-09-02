requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation: the real program returns [] for [].
  // Requiring [0] is false in the concrete satisfying state below.
  claim
    <program> solutionProgram </program>
    <input> nil </input>
    <entry> "strange_sort_list" </entry>
    <result> pending => pList(cons(0, nil)) </result>
endmodule
