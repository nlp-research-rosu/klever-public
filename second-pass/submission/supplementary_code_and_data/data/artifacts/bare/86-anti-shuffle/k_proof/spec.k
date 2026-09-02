module SPEC
  imports VERIFICATION

  // Inductive lemma for insertion into a sorted word.  K is an arbitrary
  // caller continuation, so the lemma applies to recursive and nested calls.
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

  // Inductive lemma for the word scanner.  Its proof uses insert-correct.
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

  // Universal functional-correctness theorem for every input string.
  claim [universal-correct]:
    <python>
      <k> run(solutionProgram, S:String) => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => antiShuffleSpec(S) </result>
    </python>

  // Contract examples, plus explicit coverage of repeated/edge spaces.
  claim [example-hi]:
    <python>
      <k> run(solutionProgram, "Hi") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "Hi" </result>
    </python>

  claim [example-hello]:
    <python>
      <k> run(solutionProgram, "hello") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "ehllo" </result>
    </python>

  claim [example-prompt]:
    <python>
      <k> run(solutionProgram, "Hello World!!!") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "Hello !!!Wdlor" </result>
    </python>

  claim [spaces-preserved]:
    <python>
      <k> run(solutionProgram, "  ba  dc ") => .K </k>
      <functions> .Stmts => solutionFunctions </functions>
      <env> .Map </env>
      <result> "" => "  ab  cd " </result>
    </python>
endmodule
