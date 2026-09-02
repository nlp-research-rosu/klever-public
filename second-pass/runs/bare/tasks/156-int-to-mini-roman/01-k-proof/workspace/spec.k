module ROMAN-SPEC
  imports ROMAN-VERIFICATION

  claim [int-to-mini-roman-correct]:
    <k> romanProgram => .K </k>
    <input> N:Int </input>
    <env> .Map => ?_FINAL_ENV:Map </env>
    <result> noResult => result(vStr(miniRoman(N))) </result>
    requires (1 <=Int N) andBool (N <=Int 1000)
endmodule
