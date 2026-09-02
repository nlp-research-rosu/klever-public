// spec.k — longest proof on the UNIFIED semantics (src/).
// First-longest reduce with an Optional (None) accumulator `best`.

requires "verification.k"

module LONGEST-SPEC
  imports LONGEST-VERIFICATION

  // ---- Loop invariant (circularity) — from best=B the loop leaves
  // best := longestReduce(VS, B). Induction on VS; the short-circuit `best is None or
  // len(s) > len(best)` lines up with select. best is None (seed) or a string.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("s"),
        If(BoolOp("or", Compare(Name("best"), CmpOp("is", NoneVal)),
             Compare(Call(Name("len"), Name("s")), CmpOp(">", Call(Name("len"), Name("best"))))),
           Assign(Name("best"), Name("s")),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "longest" <- FB0:Val ], parent(-1))  L |-> (
        scope(.Map [ "strings" <- SV:Val ] [ "best" <- B:Val ] [ "s" <- _:Val ], parent(GLB:Int)) =>
        scope(.Map [ "strings" <- SV ] [ "best" <- longestReduce(VS, B) ] [ "s" <- ?_:Val ], parent(GLB))
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS) andBool isStr(B)
    [all-path]

  // ---- Entry claim — result = longest(list(VS)) == longestReduce(VS, noneV).
  claim
    <k>
      FuncDef("longest", Params("strings"),
        Assign(Name("best"), NoneVal)
        Assign(Name("s"), Str(""))
        For(Name("s"), Name("strings"),
          If(BoolOp("or", Compare(Name("best"), CmpOp("is", NoneVal)),
               Compare(Call(Name("len"), Name("s")), CmpOp(">", Call(Name("len"), Name("best"))))),
             Assign(Name("best"), Name("s")),
             .Stmts))
        Return(Name("best")))
      Assign(Name("result"), Call(Name("longest"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "longest" <- ?_:Val ] [ "result" <- longestReduce(VS, noneV) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(VS)
    [all-path]
endmodule
