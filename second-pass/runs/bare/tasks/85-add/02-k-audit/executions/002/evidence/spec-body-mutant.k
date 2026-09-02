requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  // Context-independent recursive-call summary.  Its arbitrary K suffix,
  // caller environment, and caller stack make the claim reusable at the
  // recursive call, which is the induction step of the proof.
  claim
    <k> (pyList(VALUES) ~> userCall("add") => pyInt(oddIndexEvenSum(VALUES))) ... </k>
    <input> INPUT </input>
    <functions> "add" |-> function("lst",
      IfExp(
        Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))),
        Int(1),
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

  // End-to-end theorem for the exact translated constructor tree.
  claim
    <k> solutionProgramMutant ~> start => pyInt(oddIndexEvenSum(VALUES)) </k>
    <input> pyList(VALUES) </input>
    <functions> .Map => "add" |-> function("lst",
      IfExp(
        Compare(Call(Name("len"), Name("lst")), CmpOp("<", Int(2))),
        Int(1),
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
