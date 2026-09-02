requires "verification.k"

module SPEC-HELPER-ONLY
  imports VERIFICATION

  claim
    <k>
      Return(Compare(Name("string"),
        CmpOp("==", Subscript(Name("string"),
          Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))
      ~> #endcall
      => palindromeIS(S:IntSeq)
    </k>
    <env> L0:Int => CALLER0:Int </env>
    <scopes>
      (L0 |-> scope("string" |-> str(S), parent(0))) REST0:Map
      => REST0
    </scopes>
    <scopeLoc> L0 +Int 1 => L0 </scopeLoc>
    <stack> ListItem(frame(.K, CALLER0, L0)) STACK0:List => STACK0 </stack>
    <ret> noRet </ret>
    <heap> HH:Map </heap>
    <heapLoc> NN:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L0 >Int 0 andBool notBool (L0 in_keys(REST0))

endmodule
