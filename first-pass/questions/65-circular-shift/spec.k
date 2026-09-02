// spec.k — circular_shift, TRAP-FREE (P65). One straight-line entry claim over
// canonical's real body; the branch case-splits on SHIFT > isLen(digitCodes(X));
// slices reduce via the operator-level sliceIS equations.
//
//   kompile verification.k --backend haskell --main-module CIRCULAR-SHIFT-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CIRCULAR-SHIFT-SPEC

requires "verification.k"

module CIRCULAR-SHIFT-SPEC
  imports CIRCULAR-SHIFT-VERIFICATION

  claim
    <k>
      FuncDef("circular_shift", Params("x", "shift"),
        Assign(Name("s"), Call(Name("str"), Name("x")))
        If(Compare(Name("shift"), CmpOp(">", Call(Name("len"), Name("s")))),
          Return(Subscript(Name("s"), Slice(NoBound, NoBound, UnaryOp("-", Int(1))))),
          Return(BinOp("+",
            Subscript(Name("s"), Slice(BinOp("-", Call(Name("len"), Name("s")), Name("shift")), NoBound, NoBound)),
            Subscript(Name("s"), Slice(NoBound, BinOp("-", Call(Name("len"), Name("s")), Name("shift")), NoBound))))))
      Assign(Name("result"), Call(Name("circular_shift"), X:Int, SHIFT:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "circular_shift" <- ?_:Val ] [ "result" <- circShiftRes(X, SHIFT) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0 andBool SHIFT >=Int 0
    [all-path]
endmodule
