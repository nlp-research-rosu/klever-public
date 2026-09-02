requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // End-to-end theorem for every finite integer array.  The program syntax is
  // the exact py2mpy translation, while the destination is the independent
  // minimum-even/first-index scan contract above.
  claim
    <py>
      <k> solutionProgram ~> start => .K </k>
      <args> VArray(ID, 0, LENGTH) </args>
      <env> .Map => .Map </env>
      <funs> .Map => solutionFunctions </funs>
      <stack> .List => .List </stack>
      <result> VNone
        => specScanArray(ID, 0, LENGTH, 0, 0, 0, 0) </result>
    </py>
    requires LENGTH >=Int 0
endmodule
