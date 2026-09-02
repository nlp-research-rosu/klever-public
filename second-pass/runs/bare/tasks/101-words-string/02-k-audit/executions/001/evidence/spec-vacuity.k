requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  // Fresh audit mutation: prepend an extra word to the result for every input.
  // This is false for the satisfying ground input S = "", whose real result is [].
  claim [audit-false-extra-word]:
    <k>
      Module(
        FuncDef("words_string", Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs))))
      ~> invoke("words_string", S)
    => ListVal(ListItem("__AUDIT_FALSE__") wordsContract(S))
    </k>
    <functions>
      .Map
    =>
      "words_string" |-> function("s",
        Return(
          Call(
            Attribute(
              Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
              "split"),
            .Exprs)))
    </functions>
endmodule
