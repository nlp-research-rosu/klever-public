requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("value"),
        Assign(
          Name("current"),
          Call(
            Name("min"),
            Name("value"),
            BinOp("+", Name("current"), Name("value"))))
        Assign(
          Name("minimum"),
          Call(Name("min"), Name("minimum"), Name("current"))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(MODULE:Map, parent(-1))
       1 |-> scope(
              "nums"    |-> NUMS:Val
              "current" |-> (C:Int =>
                              kadaneCurrent(VS, C))
              "minimum" |-> (B:Int =>
                              kadaneMinimum(VS, C, B))
              "value"   |-> (_OLD:Val => ?LAST:Val),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
         andBool notBool ("min" in_keys(MODULE))

  claim [target]:
    <k>
      Call(
        Name("minSubArraySum"),
        list(vCons(H:Int, XS:ValSeq)))
      => kadaneMinimum(vCons(H, XS), 0, H)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              "minSubArraySum" |->
                closureVal(
                  "nums", .ParamNames,
                  Assign(Name("current"), Int(0))
                  Assign(
                    Name("minimum"),
                    Subscript(Name("nums"), Int(0)))
                  For(
                    Name("value"),
                    Name("nums"),
                    Assign(
                      Name("current"),
                      Call(
                        Name("min"),
                        Name("value"),
                        BinOp(
                          "+",
                          Name("current"),
                          Name("value"))))
                    Assign(
                      Name("minimum"),
                      Call(
                        Name("min"),
                        Name("minimum"),
                        Name("current"))))
                  Return(Name("minimum"))
                  .Stmts,
                  0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(XS)
endmodule
