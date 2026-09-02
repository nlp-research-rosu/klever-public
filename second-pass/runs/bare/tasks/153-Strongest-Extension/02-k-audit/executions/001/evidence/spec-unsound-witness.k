requires "verification.k"

module SPEC-UNSOUND-WITNESS
  imports VERIFICATION

  // U1: ASCII-only isUpperChar makes the real program's result false.
  claim [unicode-upper]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> "C" </inputClass>
      <inputExtensions> strVal("--") ; strVal("É") </inputExtensions>
      <result> noResult => returned(strVal("C.--")) </result>
    </py>

  // U2: ASCII-only isLowerChar makes the real program's result false.
  claim [unicode-lower]:
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> "C" </inputClass>
      <inputExtensions> strVal("é") ; strVal("--") </inputExtensions>
      <result> noResult => returned(strVal("C.é")) </result>
    </py>
endmodule
