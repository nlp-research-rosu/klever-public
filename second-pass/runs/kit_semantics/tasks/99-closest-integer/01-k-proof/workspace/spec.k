requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [closest-positive-lower]:
    <k>
      Call(Name("closest_integer"), str(CS:IntSeq))
      =>
      floorFI(decStrToF(CS))
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
       subF(decStrToF(CS), intToF(floorFI(decStrToF(CS)))),
       0.5
     )

  claim [closest-positive-upper]:
    <k>
      Call(Name("closest_integer"), str(CS:IntSeq))
      =>
      ceilF(decStrToF(CS))
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
     andBool notBool floatLt(
       subF(decStrToF(CS), intToF(floorFI(decStrToF(CS)))),
       0.5
     )

  claim [closest-nonpositive-upper]:
    <k>
      Call(Name("closest_integer"), str(CS:IntSeq))
      =>
      ceilF(decStrToF(CS))
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
    requires notBool ltIF(0, decStrToF(CS))
     andBool floatLt(
       subF(intToF(ceilF(decStrToF(CS))), decStrToF(CS)),
       0.5
     )

  claim [closest-nonpositive-lower]:
    <k>
      Call(Name("closest_integer"), str(CS:IntSeq))
      =>
      floorFI(decStrToF(CS))
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
    requires notBool ltIF(0, decStrToF(CS))
     andBool notBool floatLt(
       subF(intToF(ceilF(decStrToF(CS))), decStrToF(CS)),
       0.5
     )
endmodule
