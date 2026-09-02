requires "verification.k"

module AUDITOR-FALSE-SPEC
  imports VERIFICATION

  // Fresh audit mutation: the real positive-near branch returns floor(F), but
  // this destination falsely requires floor(F) + 1.  A concrete satisfying
  // witness is "15.3": the real result is 15 and this mutation demands 16.
  claim [false-positive-lower-off-by-one]:
    <k>
      Call(Name("closest_integer"), str(CS:IntSeq))
      =>
      floorFI(decStrToF(CS)) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "closest_integer" |-> closureVal(
          "value",
          Assign(Name("number"), Call(Name("float"), Name("value")))
          Assign(
            Name("lower"),
            Call(Attribute(Name("math"), "floor"), Name("number"))
          )
          Assign(
            Name("upper"),
            Call(Attribute(Name("math"), "ceil"), Name("number"))
          )
          If(
            Compare(Name("number"), CmpOp(">", Int(0))),
            If(
              Compare(
                BinOp("-", Name("number"), Name("lower")),
                CmpOp("<", Float(0.5))
              ),
              Return(Name("lower")),
              .Stmts
            )
            Return(Name("upper")),
            .Stmts
          )
          If(
            Compare(
              BinOp("-", Name("upper"), Name("number")),
              CmpOp("<", Float(0.5))
            ),
            Return(Name("upper")),
            .Stmts
          )
          Return(Name("lower")),
          0
        ),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires ltIF(0, decStrToF(CS))
     andBool floatLt(
       subF(
         decStrToF(CS),
         intToF(floorFI(decStrToF(CS)))
       ),
       0.5
     )
endmodule
