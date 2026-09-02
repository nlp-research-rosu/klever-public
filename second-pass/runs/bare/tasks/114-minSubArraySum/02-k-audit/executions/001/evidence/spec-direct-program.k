requires "verification.k"

module SPEC-DIRECT-PROGRAM
  imports VERIFICATION

  claim [prefix-helper]:
    <py>
      <k> apply(funref("min_prefix_sum"), pyList(cons(H, T))) ~> K
        => returned(D, pyInt(minPrefix(cons(H, T)))) ~> K </k>
      <entry> ENTRY </entry>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> RHO </env>
      <callStack> STACK </callStack>
      <callDepth> D </callDepth>
    </py>

  claim [target-call]:
    <py>
      <k> apply(funref("minSubArraySum"), pyList(cons(H, T))) ~> K
        => returned(D, pyInt(minSubarray(cons(H, T)))) ~> K </k>
      <entry> ENTRY </entry>
      <args> ARGS </args>
      <functions> solutionFunctions </functions>
      <env> RHO </env>
      <callStack> STACK </callStack>
      <callDepth> D </callDepth>
    </py>

  // The left side below is the trusted-translator output, embedded directly
  // rather than reached through the solutionProgram definitional constant.
  claim [direct-entry]:
    <py>
      <k>
        Module(
          FuncDef("min_prefix_sum", Params("nums"),
            If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
              Return(Subscript(Name("nums"), Int(0))),
              .Stmts)
            Assign(
              Name("tail_min"),
              Call(
                Name("min_prefix_sum"),
                Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
            Return(
              Call(
                Name("min"),
                Subscript(Name("nums"), Int(0)),
                BinOp("+", Subscript(Name("nums"), Int(0)), Name("tail_min")))))
          FuncDef("minSubArraySum", Params("nums"),
            If(Compare(Call(Name("len"), Name("nums")), CmpOp("==", Int(1))),
              Return(Subscript(Name("nums"), Int(0))),
              .Stmts)
            Assign(
              Name("tail_min"),
              Call(
                Name("minSubArraySum"),
                Subscript(Name("nums"), Slice(Int(1), NoBound, NoBound))))
            Assign(
              Name("prefix_min"),
              Call(Name("min_prefix_sum"), Name("nums")))
            Return(Call(Name("min"), Name("tail_min"), Name("prefix_min")))))
          => pyInt(minSubarray(cons(H, T))) ~> .K
      </k>
      <entry> "minSubArraySum" </entry>
      <args> pyList(cons(H, T)) </args>
      <functions> .Map => solutionFunctions </functions>
      <env> .Map </env>
      <callStack> .List </callStack>
      <callDepth> z </callDepth>
    </py>
endmodule
