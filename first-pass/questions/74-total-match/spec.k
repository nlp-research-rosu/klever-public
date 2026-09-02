// spec.k — total_match proof on the UNIFIED semantics (src/). Two sequential loops sum
// the string lengths of lst1 and lst2; return the shorter (lst1 on a tie).

requires "verification.k"

module TOTAL-MATCH-SPEC
  imports TOTAL-MATCH-VERIFICATION

  // ---- Loop invariant 1: the length-sum over lst1. l1 := L1 +Int totalLen(VS).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        Assign(Name("l1"), BinOp("+", Name("l1"), Call(Name("len"), Name("s")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "total_match" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "lst1" <- L1V:Val ] [ "lst2" <- L2V:Val ] [ "l1" <- L1:Int ] [ "s" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "lst1" <- L1V ] [ "lst2" <- L2V ] [ "l1" <- L1 +Int totalLen(VS) ] [ "s" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  // ---- Loop invariant 2: the length-sum over lst2. l2 := L2 +Int totalLen(VS).
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        Assign(Name("l2"), BinOp("+", Name("l2"), Call(Name("len"), Name("s")))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "total_match" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "lst1" <- L1V:Val ] [ "lst2" <- L2V:Val ] [ "l1" <- L1:Int ] [ "l2" <- L2:Int ] [ "s" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "lst1" <- L1V ] [ "lst2" <- L2V ] [ "l1" <- L1 ] [ "l2" <- L2 +Int totalLen(VS) ] [ "s" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]

  // ---- Entry claim — result = total_match(list(VS1), list(VS2)) =
  //   #if (totalLen(VS1) <=Int totalLen(VS2)) #then list(VS1) #else list(VS2).
  claim
    <k>
      FuncDef("total_match", Params("lst1", "lst2"),
        Assign(Name("l1"), Int(0))
        Assign(Name("s"), Str(""))
        For(Name("s"), Name("lst1"),
          Assign(Name("l1"), BinOp("+", Name("l1"), Call(Name("len"), Name("s")))))
        Assign(Name("l2"), Int(0))
        For(Name("s"), Name("lst2"),
          Assign(Name("l2"), BinOp("+", Name("l2"), Call(Name("len"), Name("s")))))
        Assign(Name("result"), Name("lst2"))
        If(Compare(Name("l1"), CmpOp("<=", Name("l2"))),
           Assign(Name("result"), Name("lst1")),
           .Stmts)
        Return(Name("result")))
      Assign(Name("result"), Call(Name("total_match"), list(VS1:ValSeq) , list(VS2:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "total_match" <- ?_:Val ]
                       [ "result" <- #if (totalLen(VS1) <=Int totalLen(VS2)) #then list(VS1) #else list(VS2) #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS1) andBool allStr(VS2)
    [all-path]
endmodule
