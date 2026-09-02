module BODY-SENSITIVITY-SPEC
  imports BODY-SENSITIVITY

  // Input 9 satisfies the real entry precondition. The mutated executable term
  // returns "wrong", while the unmutated result obligation remains "ix".
  claim [body-sensitivity-nine]:
    <k> bodyMutatedProgram => .K </k>
    <input> 9 </input>
    <env> .Map => ?_FINAL_ENV:Map </env>
    <result> noResult => result(vStr(miniRoman(9))) </result>
endmodule
