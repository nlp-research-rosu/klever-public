requires "verification.k"

module CONCATENATE-PINNING-CONFIG
  imports CONCATENATE-VERIFICATION

  // A configuration reachability form avoids the Haskell backend's
  // unsupported bare functional-claim path while checking the same
  // constructor normalization.
  claim [module-term-config]:
    <k>
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
    </k>
endmodule
