requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [multiply-correct]:
    <k>
      Call(Name("multiply"), Int(A:Int), Int(B:Int))
      =>
      pyMod(A, 10) *Int pyMod(B, 10)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "multiply" |->
          closureVal(
            ("a", "b"),
            Return(
              BinOp(
                "*",
                BinOp("%", Name("a"), Int(10)),
                BinOp("%", Name("b"), Int(10))
              )
            ),
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
endmodule
