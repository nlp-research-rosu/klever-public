requires "verification.k"

module SPEC
  imports VERIFICATION

  // For every input String, execution of the translated solution returns the
  // contract operation.  S is unconstrained and therefore symbolic.
  claim
    <k>
      Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
      => strVal(flipSpec(S))
    </k>
    <arg> S:String </arg>
    <functions>
      .Map
      =>
      "flip_case" |->
        function(Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)))
    </functions>
    <env> .Map </env>

  // The prompt's example is also a concrete end-to-end theorem.
  claim
    <k>
      Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
      => strVal("hELLO")
    </k>
    <arg> "Hello" </arg>
    <functions>
      .Map
      =>
      "flip_case" |->
        function(Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)))
    </functions>
    <env> .Map </env>

  // Unicode case mappings and expansions are part of Python's string API;
  // German sharp-s expands to "SS" and Greek delta changes case here.
  claim
    <k>
      Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
      => strVal("sTRASSE \xce\xb4ELTA")
    </k>
    <arg> "Stra\xc3\x9fe \xce\x94elta" </arg>
    <functions>
      .Map
      =>
      "flip_case" |->
        function(Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs)))
    </functions>
    <env> .Map </env>
endmodule
