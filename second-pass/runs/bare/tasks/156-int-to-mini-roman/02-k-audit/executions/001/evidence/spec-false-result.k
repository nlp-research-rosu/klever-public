module ROMAN-SPEC-FALSE-RESULT
  imports ROMAN-VERIFICATION

  // Reviewer-authored false mutation: for every satisfying input the demanded
  // value has one additional exclamation mark.
  claim [false-result-mutation]:
    <k> romanProgram => .K </k>
    <input> N:Int </input>
    <env> .Map => ?_FINAL_ENV:Map </env>
    <result>
      noResult => result(vStr(miniRoman(N) +String "!"))
    </result>
    requires (1 <=Int N) andBool (N <=Int 1000)
endmodule
