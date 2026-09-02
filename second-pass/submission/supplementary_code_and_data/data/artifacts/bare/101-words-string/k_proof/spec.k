requires "semantic.k"

module SPEC
  imports SEMANTIC

  // Universal functional-correctness claim for every input string.
  claim [words-string-general]:
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
    => ListVal(wordsContract(S))
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

  // The two examples from prompt.py are also executable proof obligations.
  claim [prompt-example-hi]:
    <k>
      Module(
        FuncDef("words_string", Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs))))
      ~> invoke("words_string", "Hi, my name is John")
    =>
      ListVal(ListItem("Hi") ListItem("my") ListItem("name")
              ListItem("is") ListItem("John"))
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

  claim [prompt-example-numbers]:
    <k>
      Module(
        FuncDef("words_string", Params("s"),
          Return(
            Call(
              Attribute(
                Call(Attribute(Name("s"), "replace"), Str(","), Str(" ")),
                "split"),
              .Exprs))))
      ~> invoke("words_string", "One, two, three, four, five, six")
    =>
      ListVal(ListItem("One") ListItem("two") ListItem("three")
              ListItem("four") ListItem("five") ListItem("six"))
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
