requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation: the satisfiable input "[[]]" returns true.
  claim
    <k>
      theSolution ~> start(lbr lbr rbr rbr .BString) => .K
    </k>
    <functions> .Map => .Map </functions>
    <env> .Map => .Map </env>
    <result> noResult => boolVal(false) </result>
endmodule
