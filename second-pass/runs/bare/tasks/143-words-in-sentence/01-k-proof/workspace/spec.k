requires "verification.k"

module WORDS-IN-SENTENCE-SPEC
  imports MPY-VERIFICATION

  // Inductive loop invariant: for every finite word sequence and every
  // accumulator, the small-step loop has exactly the oracle's store effect.
  claim [loop-invariant]:
    <mpy>
      <k> loop("word", WS, solutionLoopBody) => .K ... </k>
      <functions> _FS </functions>
      <env> ("result" |-> Str(A) "word" |-> Str(OLD) RHO)
             => loopEnv(WS, "result" |-> Str(A)
                            "word" |-> Str(OLD) RHO) </env>
      <result> _RES </result>
    </mpy>
    requires notBool ("result" in_keys(RHO))
             andBool notBool ("word" in_keys(RHO))

  // End-to-end symbolic contract.  splitWords is the independently executable
  // splitter from semantic.k; selectedWords is the oracle above.
  claim [symbolic-contract]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str(S))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal
               => Str(selectedWords(splitWords(S), "")) </result>
    </mpy>

  claim [example-one]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str("This is a test"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("is") </result>
    </mpy>

  claim [example-two]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str("lets go for swimming"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("go for") </result>
    </mpy>

  // The whole input has length 100: a length-2 word and the maximum possible
  // prime word length 97, separated by one space.
  claim [length-boundaries]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str(
                "aa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str(
                  "aa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") </result>
    </mpy>

  claim [composite-hundred]:
    <mpy>
      <k> load(solutionProgram)
           ~> invoke("words_in_sentence", Str(
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
           ~> finishProgram
           => .K </k>
      <functions> .Map => .Map </functions>
      <env> .Map => .Map </env>
      <result> NoneVal => Str("") </result>
    </mpy>
endmodule
