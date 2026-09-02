requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical output of the source scanner.  The arguments are:
  // remaining input, current depth, current group, groups emitted so far.
  syntax ValSeq ::= scanParenGroups(IntSeq, Int, IntSeq, ValSeq)
                    [function, total]

  rule scanParenGroups(.IntSeq, _:Int, _:IntSeq, OUT:ValSeq)
    => OUT

  rule scanParenGroups(iCons(C:Int, REST:IntSeq), D:Int,
                       CUR:IntSeq, OUT:ValSeq)
    => #if C ==Int 32
       #then scanParenGroups(REST, D, CUR, OUT)
       #else
         #if C ==Int 40
         #then
           #if (D +Int 1) ==Int 0
           #then
             scanParenGroups(
               REST,
               0,
               .IntSeq,
               valSeqConcat(
                 OUT,
                 vCons(
                   str(seqConcat(CUR, iCons(C, .IntSeq))),
                   .ValSeq)))
           #else
             scanParenGroups(
               REST,
               D +Int 1,
               seqConcat(CUR, iCons(C, .IntSeq)),
               OUT)
           #fi
         #else
           #if (D -Int 1) ==Int 0
           #then
             scanParenGroups(
               REST,
               0,
               .IntSeq,
               valSeqConcat(
                 OUT,
                 vCons(
                   str(seqConcat(CUR, iCons(C, .IntSeq))),
                   .ValSeq)))
           #else
             scanParenGroups(
               REST,
               D -Int 1,
               seqConcat(CUR, iCons(C, .IntSeq)),
               OUT)
           #fi
         #fi
       #fi

  syntax ValSeq ::= separateParenGroupsSpec(IntSeq) [function, total]
  rule separateParenGroupsSpec(S:IntSeq)
    => scanParenGroups(S, 0, .IntSeq, .ValSeq)

  // The HumanEval input domain: ASCII spaces and balanced parentheses.
  syntax Bool ::= validParenInput(IntSeq) [function, total]
                | validParenSuffix(IntSeq, Int) [function, total]

  rule validParenInput(S:IntSeq)
    => validParenSuffix(S, 0)

  rule validParenSuffix(.IntSeq, D:Int)
    => D ==Int 0

  rule validParenSuffix(iCons(32, REST:IntSeq), D:Int)
    => validParenSuffix(REST, D)

  rule validParenSuffix(iCons(40, REST:IntSeq), D:Int)
    => validParenSuffix(REST, D +Int 1)

  rule validParenSuffix(iCons(41, REST:IntSeq), D:Int)
    => validParenSuffix(REST, D -Int 1)
    requires D >Int 0

  rule validParenSuffix(iCons(41, _:IntSeq), D:Int)
    => false
    requires D <=Int 0

  rule validParenSuffix(iCons(C:Int, _:IntSeq), _:Int)
    => false
    requires C =/=Int 32 andBool C =/=Int 40 andBool C =/=Int 41
endmodule
