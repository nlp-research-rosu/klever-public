requires "reference-semantics/semantics.k"

module SUM-SQUARES-VERIFICATION-BASE
  imports MPY

  // Mathematical summary of the implementation's left-to-right accumulator.
  syntax Int ::= sumSquaresFrom(Int, ValSeq) [function, total]
  rule sumSquaresFrom(ACC:Int, .ValSeq) => ACC
  rule sumSquaresFrom(ACC:Int, vCons(V:Val, REST:ValSeq))
    => sumSquaresFrom(ACC +Int (ceilF(V) ^Int 2), REST)

  // Final value of the loop target; needed only to state the complete scope
  // update without hiding the target variable behind an existential.
  syntax Val ::= lastFrom(Val, ValSeq) [function, total]
  rule lastFrom(CURRENT:Val, .ValSeq) => CURRENT
  rule lastFrom(_:Val, vCons(V:Val, REST:ValSeq))
    => lastFrom(V, REST)
endmodule

// Downstream proof definition.  The rule below is textually the loop theorem
// proved as SUM-SQUARES-LOOP-SPEC.loop-correct against the BASE module.  It is
// compiled only after that proof command succeeds (see prove.sh), allowing the
// end-to-end function theorem to use the established loop lemma.
module SUM-SQUARES-VERIFICATION
  imports SUM-SQUARES-VERIFICATION-BASE

  rule
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2)))
      )
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |->
        scope(
          "lst" |-> INPUT:Val
          "number" |-> (CURRENT:Val => lastFrom(CURRENT, VS))
          "result" |-> (ACC:Int => sumSquaresFrom(ACC, VS)),
          PARENT:Parent))
      GLOBAL:Map
    </scopes>
    requires notBool (L in_keys(GLOBAL))
    [priority(40)]
endmodule
