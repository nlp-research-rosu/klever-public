requires "/tmp/audit-work/candidate/semantic.k"

module BODY-SENSITIVITY
  imports SEMANTIC

  // Mutation: the executed program replaces semicolons, not commas.
  // For input "a,b", this returns ["a,b"], while wordsContract requires ["a","b"].
  claim [changed-program-body]:
    <k>
      Module(
        FuncDef("words_string", Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(";"), Str(" ")),
                "split"),
              .Exprs))))
      ~> invoke("words_string", "a,b")
    =>
      ListVal(wordsContract("a,b"))
    </k>
    <functions>
      .Map
    =>
      "words_string" |-> function("s",
        Return(
          Call(
            Attribute(
              Call(Attribute(Name("s"), "replace"), Str(";"), Str(" ")),
              "split"),
            .Exprs)))
    </functions>
endmodule
