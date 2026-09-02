module SPEC-VACUITY
  imports VERIFICATION

  // Exact helper claim, already reconstructed independently in module SPEC.
  claim [insert-correct]:
    <python>
      <k>
        invoke("insert_char", vals(C:String, W:String, B:String)) ~> K:K
        => val(refInsert(C, W, B)) ~> K
      </k>
      <functions> solutionFunctions </functions>
      <env> ENV:Map => ENV </env>
      <result> _R:String </result>
    </python>

  // Exact dependent helper claim, already reconstructed independently.
  claim [process-correct]:
    <python>
      <k>
        invoke("process_words", vals(T:String, W:String, R:String)) ~> K:K
        => val(refProcess(T, W, R)) ~> K
      </k>
      <functions> solutionFunctions </functions>
      <env> ENV:Map => ENV </env>
      <result> _OUT:String </result>
    </python>

  // Deliberately false: the satisfying input "ba" actually returns "ab".
  claim [false-result]:
    <python>
      <k> run(solutionProgram, "ba") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "ba" </result>
    </python>
endmodule
