requires "verification.k"

module CLOSEST-INT-SPEC
  imports CLOSEST-INT-VERIFICATION

  // ---- The trailing-zero-strip while (co-inductive circularity): value folds
  // to str(stripZ(CS)). Frame 1 holds value + the two import-bound builtins.
  claim
    <k>
      #while(Compare(
        Subscript(Name("value"), UnaryOp("-", Int(1))),
        CmpOp("==", Str("0"))),
        Assign(
          Name("value"),
          Subscript(
            Name("value"),
            Slice(NoBound, UnaryOp("-", Int(1)), NoBound))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "closest_integer" <- _:Val ], parent(-1))
       1 |-> (
         scope(.Map [ "value" <- str(CS:IntSeq) ]
                    [ "floor" <- builtinV("floor") ] [ "ceil" <- builtinV("ceil") ], parent(0)) =>
         scope(.Map [ "value" <- str(stripZ(CS)) ]
                    [ "floor" <- builtinV("floor") ] [ "ceil" <- builtinV("ceil") ], parent(0))
       )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires hasNonZ(CS)
    [all-path]

  // ---- Entry — result = ciModel(CS), the real code's opaque-float
  // composition over the stripped codes. Domain guard: the old 3-conjunct
  // decimal-numeral guard (nonempty integer part, |int| < 10^6, <= 6 frac
  // digits) — excludes the canonical-ValueError bare-dot family and keeps
  // float() exact on the half question (see PROOF.md).
  claim
    <k>
      FuncDef("closest_integer", Params("value"),
        ImportFrom("math", "floor", "ceil")
        If(Compare(
          Call(Attribute(Name("value"), "count"), Str(".")),
          CmpOp("==", Int(1))),
          While(Compare(
            Subscript(Name("value"), UnaryOp("-", Int(1))),
            CmpOp("==", Str("0"))),
            Assign(
              Name("value"),
              Subscript(
                Name("value"),
                Slice(NoBound, UnaryOp("-", Int(1)), NoBound)))),
          .Stmts)
        Assign(Name("num"), Call(Name("float"), Name("value")))
        If(Compare(
          Subscript(
            Name("value"),
            Slice(UnaryOp("-", Int(2)), NoBound, NoBound)),
          CmpOp("==", Str(".5"))),
          If(Compare(Name("num"), CmpOp(">", Int(0))),
            Assign(Name("res"), Call(Name("ceil"), Name("num"))),
            Assign(Name("res"), Call(Name("floor"), Name("num")))),
          If(Compare(Call(Name("len"), Name("value")), CmpOp(">", Int(0))),
            Assign(
              Name("res"),
              Call(Name("int"), Call(Name("round"), Name("num")))),
            Assign(Name("res"), Int(0))))
        Return(Name("res")))
      Assign(Name("result"), Call(Name("closest_integer"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "closest_integer" <- ?_:Val ]
                       [ "result" <- ciModel(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires intDigits(bodyOf(CS)) =/=K .IntSeq
     andBool magOf(intDigits(bodyOf(CS))) <Int 1000000
     andBool isLen(fracDigits(bodyOf(CS))) <=Int 6
    [all-path]
endmodule
