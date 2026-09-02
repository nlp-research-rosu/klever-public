requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Reviewer mutation: the real result for "Hello" is "hELLO", not "hELLo".
  claim [false-result]:
    <k>
      Module(
        FuncDef("flip_case", Params("string"),
          Return(Call(Attribute(Name("string"), "swapcase"), .Exprs))))
      => strVal("hELLo")
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
endmodule
