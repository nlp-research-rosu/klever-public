requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION

  // Loop invariant/circularity: D is a positive candidate below N.  The
  // semantics and reference scan both either return D when it divides N or
  // continue with D - 1.  At D = 1 the non-divisor branch is impossible.
  claim
    <k>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
      => firstDivisorAtOrBelow(N, D) ~> .K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "n" |-> N
        "divisor" |-> D,
        parent(0))
      =>
      SC
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1 andBool D >=Int 1 andBool D <Int N
    [label(loopCorrect)]
endmodule

module INIT-SPEC
  imports VERIFICATION

  claim
    <k>
      Assign(Name("divisor"), BinOp("-", Name("n"), Int(1)))
      While(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      Return(Name("divisor"))
      ~> #endcall
      =>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      SC:Map
      1 |-> scope("n" |-> N, parent(0))
      =>
      SC
      1 |-> scope(
        "n" |-> N
        "divisor" |-> ?D:Int,
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?D ==Int N -Int 1
    [label(initCorrect)]
endmodule

module PREFIX-SPEC
  imports VERIFICATION

  // Finite public-entry prefix: load the exact translated function, call it,
  // bind n, skip its docstring, initialize divisor, and reach the loop head.
  // LOOP-SPEC starts at precisely this state (with SC equal to the two global
  // scopes), so the two claims compose into the end-to-end result.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "largest_divisor",
            Params("n"),
            largestDivisorBody())))
      ~> Call(Name("largest_divisor"), Int(N))
      =>
      #while(
        Compare(
          BinOp("%", Name("n"), Name("divisor")),
          CmpOp("!=", Int(0))),
        AugAssign(Name("divisor"), "-", Int(1)))
      ~> Return(Name("divisor")) .Stmts
      ~> #endcall
      ~> .K
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "largest_divisor" |->
          closureVal("n", largestDivisorBody(), 0),
        parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "n" |-> N
        "divisor" |-> ?D:Int,
        parent(0))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List => ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1
    ensures ?D ==Int N -Int 1
    [label(prefixCorrect)]
endmodule
