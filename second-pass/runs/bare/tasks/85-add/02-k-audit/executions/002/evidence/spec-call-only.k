requires "verification.k"

module SPEC-CALL-ONLY
  imports VERIFICATION

  claim [recursive-call]:
    <k> (pyList(VALUES) ~> userCall("add") => pyInt(oddIndexEvenSum(VALUES))) ... </k>
    <input> INPUT </input>
    <functions> "add" |-> function("lst",
      IfExp(
        Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))),
        Int(0),
        BinOp(
          "+",
          IfExp(
            Compare(
              BinOp("%", Subscript(Name("lst"), Int(1)), Int(2)),
              CmpOp("==", Int(0))),
            Subscript(Name("lst"), Int(1)),
            Int(0)),
          Call(
            Name("add"),
            Subscript(Name("lst"), Slice(Int(2), NoBound, NoBound)))))) </functions>
    <env> CALLERENV </env>
    <callStack> CALLERSTACK </callStack>
endmodule
