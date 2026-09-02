requires "verification-loops.k"

module LOOP-SPEC
  imports VERIFICATION-LOOPS

  claim [loop-empty]:
    <k>
      #loop(list(.ValSeq), Name("e"),
        If(Compare(Name("e"), CmpOp("<", Name("t"))),
          Continue, .Stmts)
        Return(Bool(false)))
      ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      GLOBALS:Map
      1 |-> scope(
        "l" |-> list(ORIGINAL:ValSeq)
        "t" |-> T:Int
        "e" |-> OLD:Val,
        parent(0))
      =>
      (1 |-> scope(
        "l" |-> list(ORIGINAL)
        "t" |-> T
        "e" |-> lastVisited(.ValSeq, OLD, T),
        parent(0))
       GLOBALS) [1 <- undef]
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> H:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [loop-cons]:
    <k>
      #loop(list(vCons(V:Val, REST:ValSeq)), Name("e"),
        If(Compare(Name("e"), CmpOp("<", Name("t"))),
          Continue, .Stmts)
        Return(Bool(false)))
      ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
      => allBelow(vCons(V, REST), T)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      GLOBALS:Map
      1 |-> scope(
        "l" |-> list(ORIGINAL:ValSeq)
        "t" |-> T:Int
        "e" |-> OLD:Val,
        parent(0))
      =>
      (1 |-> scope(
        "l" |-> list(ORIGINAL)
        "t" |-> T
        "e" |-> lastVisited(vCons(V, REST), OLD, T),
        parent(0))
       GLOBALS) [1 <- undef]
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> H:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericVal(V) andBool numericSeq(REST)

  claim [for-empty]:
    <k>
      For(Name("e"), list(.ValSeq),
        If(Compare(Name("e"), CmpOp("<", Name("t"))),
          Continue, .Stmts)
        Return(Bool(false)))
      ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      GLOBALS:Map
      1 |-> scope(
        "l" |-> list(ORIGINAL:ValSeq)
        "t" |-> T:Int
        "e" |-> OLD:Val,
        parent(0))
      =>
      (1 |-> scope(
        "l" |-> list(ORIGINAL)
        "t" |-> T
        "e" |-> lastVisited(.ValSeq, OLD, T),
        parent(0))
       GLOBALS) [1 <- undef]
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> H:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [for-cons]:
    <k>
      For(Name("e"), list(vCons(V:Val, REST:ValSeq)),
        If(Compare(Name("e"), CmpOp("<", Name("t"))),
          Continue, .Stmts)
        Return(Bool(false)))
      ~> (Return(Bool(true)) .Stmts):Stmts ~> #endcall
      => allBelow(vCons(V, REST), T)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      GLOBALS:Map
      1 |-> scope(
        "l" |-> list(ORIGINAL:ValSeq)
        "t" |-> T:Int
        "e" |-> OLD:Val,
        parent(0))
      =>
      (1 |-> scope(
        "l" |-> list(ORIGINAL)
        "t" |-> T
        "e" |-> lastVisited(vCons(V, REST), OLD, T),
        parent(0))
       GLOBALS) [1 <- undef]
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> H:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires numericVal(V) andBool numericSeq(REST)
endmodule
