requires "verification.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION

  // The actual executed constructor term is changed: the subtraction is
  // removed, while the original fractional-result obligation is retained.
  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(Call(Name("int"), Name("number")))))
      ~> invoke("truncate_number", num(3, 5, 10))
      => .K
    </k>
    <env> .Map => "number" |-> num(3, 5, 10) </env>
    <result> noResult => num(0, 5, 10) </result>
endmodule
