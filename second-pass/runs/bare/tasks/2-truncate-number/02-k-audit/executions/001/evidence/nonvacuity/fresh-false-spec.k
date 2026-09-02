requires "verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  // Reviewer mutation: falsely requires integer component 1 in every result.
  // The original entry precondition remains unchanged and is satisfied, for
  // example, by I=3, F=1, S=2 (the input 3.5).
  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(I, F, S))
      => .K
    </k>
    <env> .Map => "number" |-> num(I, F, S) </env>
    <result> noResult => num(1, F, S) </result>
    requires validPositive(num(I, F, S))
endmodule
