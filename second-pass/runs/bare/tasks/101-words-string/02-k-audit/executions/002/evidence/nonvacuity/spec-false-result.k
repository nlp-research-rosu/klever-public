requires "/tmp/audit-work/candidate/semantic.k"

module SPEC-FALSE-RESULT
  imports SEMANTIC

  // Fresh false result obligation.
  // Satisfying witness: empty function map and input "a,b".
  // Real result is ["a", "b"], while this mutation requires ["a"].
  claim [drops-second-word]:
    <k>
      Module(
        FuncDef("words_string", Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs))))
      ~> invoke("words_string", "a,b")
    =>
      ListVal(ListItem("a"))
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
