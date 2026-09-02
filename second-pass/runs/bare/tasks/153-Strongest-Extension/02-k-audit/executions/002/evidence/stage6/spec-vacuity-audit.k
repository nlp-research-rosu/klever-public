requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result obligation.  The satisfying input's actual strongest
  // extension is SErviNGSliCes, not Cheese.
  claim
    <py>
      <k> StrongestProgram ~> #start => .K </k>
      <env> .Map => ?_:Map </env>
      <functions> .Map => ?_:Map </functions>
      <inputClass> "Slices" </inputClass>
      <inputExtensions>
        strVal("SErviNGSliCes") ; strVal("Cheese") ; strVal("StuFfed")
      </inputExtensions>
      <result> noResult => returned(strVal("Slices.Cheese")) </result>
    </py>
endmodule
