requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A mathematical reference encoder, deliberately separate from the AST
  // interpreter.  It consumes one character per recursive call.
  syntax String ::= encodeSpec(String) [function]

  rule encodeSpec(S) => "" requires lengthString(S) ==Int 0
  rule encodeSpec(S)
    => encodedChar(substrString(S, 0, 1))
       +String encodeSpec(substrString(S, 1, lengthString(S)))
    requires lengthString(S) =/=Int 0

  // Normalize the one associativity shape introduced by accumulator updates.
  rule S +String "" => S [simplification]
  rule "" +String S => S [simplification]
  rule (S1 +String S2) +String S3 => S1 +String (S2 +String S3)
    [simplification]

  // The exact tree generated from solution.py.  Keeping it here ties the
  // proofs to the submitted program rather than to a hand-written surrogate.
  syntax Stmts ::= encodeBody() [function]
  syntax Pgm ::= encodeProgram() [function]

  rule encodeBody() =>
    Assign(Name("result"), Str(""))
    For(Name("char"), Name("message"), encodeLoopBody())
    Return(Name("result"))

  rule encodeProgram() =>
    Module(
      FuncDef("encode", Params("message"), encodeBody()))
endmodule
