requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  claim [body-sensitive-example]:
    <py>
      <k> solutionModule => .K </k>
      <input> 13195 </input>
      <env> .Map => ?_:Map </env>
      <result> noResult => result(29) </result>
    </py>
endmodule
