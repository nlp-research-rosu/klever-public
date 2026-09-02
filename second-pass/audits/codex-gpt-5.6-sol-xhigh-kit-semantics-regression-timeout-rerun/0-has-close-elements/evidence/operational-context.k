requires "verification.k"

module AUDIT-INNER-CONTEXT-BASE
  imports VERIFICATION-BASE

  claim [inner-context-base]:
    <k> #loop(list(vCons(F:Float, .ValSeq)),
              Name("other"), HC-INNER-BODY)
         ~> Assign(Name("i"), Int(99))
        => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "numbers"   |-> list(vCons(F, .ValSeq))
             "threshold" |-> T:Float
             "result"    |-> false
             "i"         |-> (0 => 99)
             "number"    |-> F
             "j"         |-> (0 => 1)
             "other"     |-> (0.0 => F),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-INNER-CONTEXT-EXTENDED
  imports VERIFICATION-INNER

  claim [inner-context-extended]:
    <k> #loop(list(vCons(F:Float, .ValSeq)),
              Name("other"), HC-INNER-BODY)
         ~> Assign(Name("i"), Int(99))
        => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "numbers"   |-> list(vCons(F, .ValSeq))
             "threshold" |-> T:Float
             "result"    |-> false
             "i"         |-> (0 => 99)
             "number"    |-> F
             "j"         |-> (0 => 1)
             "other"     |-> (0.0 => F),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-OUTER-CONTEXT-BASE
  imports VERIFICATION-INNER

  claim [outer-context-base]:
    <k> #loop(list(.ValSeq), Name("number"), HC-OUTER-BODY)
         ~> Assign(Name("result"), Bool(true))
        => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "numbers"   |-> list(.ValSeq)
             "threshold" |-> T:Float
             "result"    |-> (false => true)
             "i"         |-> 0
             "number"    |-> 0.0
             "j"         |-> 0
             "other"     |-> 0.0,
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-OUTER-CONTEXT-EXTENDED
  imports VERIFICATION-OUTER

  claim [outer-context-extended]:
    <k> #loop(list(.ValSeq), Name("number"), HC-OUTER-BODY)
         ~> Assign(Name("result"), Bool(true))
        => .K </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "has_close_elements" |->
               closureVal(("numbers", "threshold"),
                          HC-FUNCTION-BODY, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "numbers"   |-> list(.ValSeq)
             "threshold" |-> T:Float
             "result"    |-> (false => true)
             "i"         |-> 0
             "number"    |-> 0.0
             "j"         |-> 0
             "other"     |-> 0.0,
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
