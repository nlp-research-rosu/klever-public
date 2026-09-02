requires "verification.k"

// Ground execution of the exact bridge domain under the bridge-free theory.
module BRIDGE-WITNESS-BASE
  imports VERIFICATION-BASE

  claim [ground-exact-loop-base]:
    <k>
      #loop(
        list(vCons(2, vCons(3, .ValSeq))),
        Name("number"),
        AugAssign(Name("total"), "+", Name("number"))
        AugAssign(Name("product"), "*", Name("number"))
      )
      ~> Return(TupleExpr(Name("total"), Name("product")))
      ~> #endcall
      => tuple(vCons(5, vCons(6, .ValSeq)))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODULE:Scope
      1 |-> scope(
        "numbers" |-> list(vCons(2, vCons(3, .ValSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0)
      )
      =>
      -1 |-> BUILTINS
      0 |-> MODULE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// The same complete state under the bridge-bearing theory.
module BRIDGE-WITNESS-EXTENDED
  imports VERIFICATION

  claim [ground-exact-loop-extended]:
    <k>
      #loop(
        list(vCons(2, vCons(3, .ValSeq))),
        Name("number"),
        AugAssign(Name("total"), "+", Name("number"))
        AugAssign(Name("product"), "*", Name("number"))
      )
      ~> Return(TupleExpr(Name("total"), Name("product")))
      ~> #endcall
      => tuple(vCons(5, vCons(6, .ValSeq)))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODULE:Scope
      1 |-> scope(
        "numbers" |-> list(vCons(2, vCons(3, .ValSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0)
      )
      =>
      -1 |-> BUILTINS
      0 |-> MODULE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// The bridge must not match when the continuation is changed.
module BRIDGE-CONTEXT-WITNESS
  imports VERIFICATION

  claim [changed-continuation]:
    <k>
      #loop(
        list(vCons(2, vCons(3, .ValSeq))),
        Name("number"),
        AugAssign(Name("total"), "+", Name("number"))
        AugAssign(Name("product"), "*", Name("number"))
      )
      ~> Return(TupleExpr(Int(99), Int(100)))
      ~> #endcall
      => tuple(vCons(99, vCons(100, .ValSeq)))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODULE:Scope
      1 |-> scope(
        "numbers" |-> list(vCons(2, vCons(3, .ValSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0)
      )
      =>
      -1 |-> BUILTINS
      0 |-> MODULE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// A changed body falls outside the exact bridge and computes product -4.
module BRIDGE-BODY-MUTATION
  imports VERIFICATION

  claim [changed-body-old-result]:
    <k>
      #loop(
        list(vCons(2, vCons(3, .ValSeq))),
        Name("number"),
        AugAssign(Name("total"), "+", Name("number"))
        AugAssign(Name("product"), "-", Name("number"))
      )
      ~> Return(TupleExpr(Name("total"), Name("product")))
      ~> #endcall
      => tuple(vCons(5, vCons(6, .ValSeq)))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> BUILTINS:Scope
      0 |-> MODULE:Scope
      1 |-> scope(
        "numbers" |-> list(vCons(2, vCons(3, .ValSeq)))
        "total" |-> 0
        "product" |-> 1
        "number" |-> 0,
        parent(0)
      )
      =>
      -1 |-> BUILTINS
      0 |-> MODULE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
