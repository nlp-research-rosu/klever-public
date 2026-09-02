requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Loop invariant for state 0: the current sentence has contained only
  // leading whitespace.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"), boredLoopBody)
      ~> Return(Name("count"))
      ~> #endcall
      => bored0(CS, N)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL:Map, parent(-1))
        1 |-> scope(
          ("S" |-> str(INPUT:IntSeq))
          ("count" |-> N:Int)
          ("state" |-> 0)
          ("ch" |-> CH:Val)
          ("code" |-> CODE:Int),
          parent(0)
        )
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL, parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("ord" in_keys(GLOBAL))
    [label(loop-state-0)]

  // Loop invariant for state 1: the first non-whitespace character was "I"
  // and its following character has not been consumed yet.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"), boredLoopBody)
      ~> Return(Name("count"))
      ~> #endcall
      => bored1(CS, N)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL:Map, parent(-1))
        1 |-> scope(
          ("S" |-> str(INPUT:IntSeq))
          ("count" |-> N:Int)
          ("state" |-> 1)
          ("ch" |-> CH:Val)
          ("code" |-> CODE:Int),
          parent(0)
        )
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL, parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("ord" in_keys(GLOBAL))
    [label(loop-state-1)]

  // Loop invariant for state 2: the current sentence cannot be a boredom.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"), boredLoopBody)
      ~> Return(Name("count"))
      ~> #endcall
      => bored2(CS, N)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL:Map, parent(-1))
        1 |-> scope(
          ("S" |-> str(INPUT:IntSeq))
          ("count" |-> N:Int)
          ("state" |-> 2)
          ("ch" |-> CH:Val)
          ("code" |-> CODE:Int),
          parent(0)
        )
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(GLOBAL, parent(-1))
      )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("ord" in_keys(GLOBAL))
    [label(loop-state-2)]

  // Direct full-function proof of the prompt's first example.
  claim
    <k>
      Call(Name("is_bored"), Str("Hello world"))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          boredFunctionBody,
          0
        ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(prompt-example-0-false)]

  // Direct full-function proof of the prompt's second example.
  claim
    <k>
      Call(
        Name("is_bored"),
        Str("The sky is blue. The sun is shining. I love this weather")
      )
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "is_bored" |-> closureVal(
          ("S", .ParamNames),
          boredFunctionBody,
          0
        ),
        parent(-1)
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(prompt-example-1)]
endmodule
