requires "semantic.k"

module VERIFICATION
  imports MPY

  // A named copy of the exact constructor tree emitted in solution.mpy.
  // This lets each claim focus on inputs and outputs while still executing
  // the translated Python program through the semantics.
  syntax Module ::= "solutionModule" [function]
  rule solutionModule =>
    Module(
      FuncDef("is_bored", Params("S"),
        Assign(Name("count"), Int(0))
        For(Name("sentence"),
          Call(
            Attribute(
              Call(
                Attribute(
                  Call(Attribute(Name("S"), "replace"), Str("!"), Str(".")),
                  "replace"),
                Str("?"), Str(".")),
              "split"),
            Str(".")),
          If(
            Call(
              Attribute(
                Call(Attribute(Name("sentence"), "strip"), .Exprs),
                "startswith"),
              Str("I ")),
            AugAssign(Name("count"), "+", Int(1)),
            .Stmts))
        Return(Name("count"))))

  // Contract-level model: normalize sentence delimiters, split into
  // sentences, trim Python whitespace, and count an initial word "I".
  syntax Int ::= boredSpec(String) [function]
               | countBored(Values) [function]
               | boolInt(Bool) [function]
  rule boredSpec(S) =>
    countBored(splitDots(replaceAll(replaceAll(S, "!", "."), "?", ".")))
  rule countBored(nil) => 0
  rule countBored(cons(vStr(S), REST))
    => boolInt(startsWith(strip(S), "I ")) +Int countBored(REST)
  rule boolInt(true) => 1
  rule boolInt(false) => 0
endmodule
