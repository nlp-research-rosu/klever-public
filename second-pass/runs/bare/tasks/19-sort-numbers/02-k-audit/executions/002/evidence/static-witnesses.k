requires "verification.k"

module STATIC-WITNESSES
  imports VERIFICATION

  // The last validNumerals rule overlaps the explicit empty-string rule.
  claim [valid-empty-true]:
    <k> validNumerals("") => true </k>

  claim [valid-empty-false]:
    <k> validNumerals("") => false </k>

  // This alternate program exposes the over-broad modeling of Python strip:
  // CPython returns "one", but the generated semantics removes the last byte.
  claim [strip-overbreadth]:
    <k>
      Module(
        FuncDef(
          "sort_numbers",
          Params("numbers"),
          Return(Call(Attribute(Name("numbers"), "strip"), .Exprs))))
      ~> invoke("one")
      => VStr("on")
    </k>
endmodule
