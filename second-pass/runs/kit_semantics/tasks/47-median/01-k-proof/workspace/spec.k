requires "verification.k"

module SPEC
  imports VERIFICATION

  // Odd-sized inputs: the result is the middle value of the sorted sequence.
  claim [median-odd]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      valSeqAt(
        sortVS(VS),
        (vsLen(sortVS(VS)) -Int 1) /Int 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 1
     andBool notBool (HL in_keys(HP))

  // Even-sized integer inputs: the two center integers are averaged.
  claim [median-even-int-int]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divII(I1:Int +Int I2:Int, 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K I1
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K I2
     andBool notBool (HL in_keys(HP))

  claim [median-even-int-bool]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divII(I:Int +Int (#if B:Bool #then 1 #else 0 #fi), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K I
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K B
     andBool notBool (HL in_keys(HP))

  claim [median-even-bool-int]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divII((#if B:Bool #then 1 #else 0 #fi) +Int I:Int, 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K B
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K I
     andBool notBool (HL in_keys(HP))

  claim [median-even-bool-bool]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divII(boolAsInt(B1:Bool) +Int boolAsInt(B2:Bool), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K B1
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K B2
     andBool notBool (HL in_keys(HP))

  claim [median-even-float-float]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divFloatIntV(addF(F1:Float, F2:Float), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K F1
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K F2
     andBool notBool (HL in_keys(HP))

  claim [median-even-int-float]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divFloatIntV(addF(intToF(I:Int), F:Float), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K I
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K F
     andBool notBool (HL in_keys(HP))

  claim [median-even-float-int]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divFloatIntV(addF(F:Float, intToF(I:Int)), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K F
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K I
     andBool notBool (HL in_keys(HP))

  claim [median-even-bool-float]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divFloatIntV(addF(intToF(boolAsInt(B:Bool)), F:Float), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K B
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K F
     andBool notBool (HL in_keys(HP))

  claim [median-even-float-bool]:
    <k>
      Call(Name("median"), list(VS:ValSeq))
      =>
      divFloatIntV(addF(F:Float, intToF(boolAsInt(B:Bool))), 2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope("median" |-> solutionMedianClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      HP:Map
      =>
      (HL:Int |-> list(sortVS(VS))) HP
    </heap>
    <heapLoc> HL => HL +Int 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires vsLen(sortVS(VS)) >Int 0
     andBool pyMod(vsLen(sortVS(VS)), 2) ==Int 0
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2 -Int 1) ==K F
     andBool valSeqAt(
       sortVS(VS),
       vsLen(sortVS(VS)) /Int 2) ==K B
     andBool notBool (HL in_keys(HP))
endmodule
