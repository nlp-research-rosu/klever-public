requires "verification.k"

module CONCATENATE-PINNING
  imports CONCATENATE-VERIFICATION

  // Mechanical constructor-level normalization check against the exact term
  // in the trusted-translator-regenerated solution.mpy.
  claim [module-term]:
    concatenateModule
    =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("concatenate", Params("strings"),
        Assign(Name("result"), Str(""))
        Assign(Name("string"), Str(""))
        For(Name("string"), Name("strings"),
          AugAssign(Name("result"), "+", Name("string")))
        Return(Name("result")))
    )
endmodule
