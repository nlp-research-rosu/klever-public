requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [helper]:
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

  claim [entry]:
    <k> solutionProgram ~> start => pyInt(oddIndexEvenSum(VALUES)) </k>
    <input> pyList(VALUES) </input>
    <functions> .Map => "add" |-> function("lst",
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
    <env> .Map </env>
    <callStack> .List </callStack>
endmodule
