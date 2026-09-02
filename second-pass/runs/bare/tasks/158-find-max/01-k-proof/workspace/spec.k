requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant: starting from candidate (BEST, BESTCOUNT), executing the
  // source loop over REST returns exactly the independent contract fold.
  claim [loop-correct]:
    <mpy>
      <k> loop("word", REST, solutionLoopBody)
           ~> exec(Return(Name("best")) .Stmts)
        => .K </k>
      <words> _ALL </words>
      <best> BEST => ?FINALBEST:String </best>
      <bestCount> BESTCOUNT => ?FINALCOUNT:Int </bestCount>
      <word> _OLDWORD => ?FINALWORD:String </word>
      <count> _OLDCOUNT => ?LASTCOUNT:Int </count>
      <result> noResult
        => result(strVal(
             candidateWord(maxCandidate(
               REST, candidate(BEST, BESTCOUNT))))) </result>
    </mpy>

  // The exact translated program initializes the contract accumulator and
  // reaches precisely the loop configuration covered by loop-correct.  Thus
  // this claim composed with loop-correct is the end-to-end proof.
  claim [program-initializes]:
    <mpy>
      <k> solutionAST
        => loop("word", WORDS, solutionLoopBody)
             ~> exec(Return(Name("best")) .Stmts) </k>
      <words> WORDS </words>
      <best> "" </best>
      <bestCount> -1 </bestCount>
      <word> "" </word>
      <count> 0 </count>
      <result> noResult </result>
    </mpy>

  // Direct composed theorem: the exact AST returns the contract value for
  // every finite Words input.  loop-correct supplies the inductive circularity.
  claim [find-max-correct]:
    <mpy>
      <k> solutionAST => .K </k>
      <words> WORDS </words>
      <best> "" => ?FINALBEST:String </best>
      <bestCount> -1 => ?FINALCOUNT:Int </bestCount>
      <word> "" => ?FINALWORD:String </word>
      <count> 0 => ?LASTCOUNT:Int </count>
      <result> noResult => result(strVal(findMaxSpec(WORDS))) </result>
    </mpy>
endmodule
