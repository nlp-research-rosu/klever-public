requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Reviewer body-sensitivity mutation: replace the submitted call with
  // Return(Str("WRONG")) while retaining the original expected result.
  claim [changed-body]:
    <k>
      Module(
        FuncDef("flip_case", Params("string"),
          Return(Str("WRONG"))))
      => strVal("hELLO")
    </k>
    <arg> "Hello" </arg>
    <functions>
      .Map
      =>
      "flip_case" |->
        function(Params("string"), Return(Str("WRONG")))
    </functions>
    <env> .Map </env>
endmodule
