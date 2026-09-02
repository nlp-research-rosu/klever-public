requires "verification-no-bridges.k"

module BRIDGE-CONNECTION-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  claim [isinstance-true-connection]:
    <k> #applyK(toCall(builtinV("isinstance")),
                 (V:Val, typeV("str"), .Vals))
      => true
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires stringCaseKey(V)

  claim [isinstance-false-connection]:
    <k> #applyK(toCall(builtinV("isinstance")),
                 (V:Val, typeV("str"), .Vals))
      => false
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires notBool stringCaseKey(V)

  claim [islower-true-connection]:
    <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
      => true
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires stringCaseKey(V) andBool lowerCaseKey(V)

  claim [islower-false-connection]:
    <k> #applyK(toCall(boundMethodV(V:Val, "islower")), .Vals)
      => false
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires stringCaseKey(V) andBool notBool lowerCaseKey(V)

  claim [isupper-true-connection]:
    <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
      => true
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires stringCaseKey(V) andBool upperCaseKey(V)

  claim [isupper-false-connection]:
    <k> #applyK(toCall(boundMethodV(V:Val, "isupper")), .Vals)
      => false
    </k>
    <env> E:Int </env>
    <scopes> SC:Map </scopes>
    <scopeLoc> SL:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> RS:RetState </ret>
    <exc> EX:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires stringCaseKey(V) andBool notBool upperCaseKey(V)
endmodule
