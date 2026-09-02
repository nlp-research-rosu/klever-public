requires "stage4_body_mutated_verification.k"

module STAGE4-BODY-MUTATED-SPEC
  imports VERIFICATION

  // False for the mutated program's fixed semantics: it returns 999 and
  // binds n. The retained bridge nevertheless makes this claim close.
  claim [body-sensitivity-n1]:
    <k> primeFibProgram => .K </k>
    <env> .Map </env>
    <n> 1 </n>
    <result> noResult => 2 </result>
endmodule
