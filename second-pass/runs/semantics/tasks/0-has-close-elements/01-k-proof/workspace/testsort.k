requires "reference-semantics/semantics.k"
module TESTSORT
  imports MPY
  syntax ValSeq ::= FloatSeq
  syntax FloatSeq ::= ".ValSeq" [klabel(.ValSeq)]
                    | "vCons" "(" Float "," FloatSeq ")" [klabel(vCons)]
endmodule
