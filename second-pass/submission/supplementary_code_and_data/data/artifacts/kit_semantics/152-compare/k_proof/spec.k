requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [compare-loop-step]:
    <k>
      #loop(
        zipObj(
          vCons(SCORE:Val, SCORES:ValSeq),
          vCons(PREDICTED:Val, PREDICTIONS:ValSeq)),
        TupleExpr(Name("score"), Name("predicted")),
        Expr(
          Call(
            Attribute(Name("result"), "append"),
            Call(
              Name("abs"),
              BinOp("-", Name("score"), Name("predicted"))))))
      => .K ...
    </k>
    <env> 1 </env>
    <scopes>
      (-1 |-> builtinsScope
       0 |-> scope(MODULESCOPE:Map, parent(-1))
       1 |-> scope(
              ("game" |-> list(GAME:ValSeq)
               "guess" |-> list(GUESS:ValSeq)
               "result" |-> ref(0)
               "score" |-> OLDSCORE:Val
               "predicted" |-> OLDPREDICTED:Val),
              parent(0)))
      =>
      (-1 |-> builtinsScope
       0 |-> scope(MODULESCOPE, parent(-1))
       1 |-> scope(
              ("game" |-> list(GAME)
               "guess" |-> list(GUESS)
               "result" |-> ref(0)
               "score" |-> ?FINALSCORE:Val
               "predicted" |-> ?FINALPREDICTED:Val),
              parent(0)))
    </scopes>
    <heap>
      0 |-> list(PREFIX:ValSeq)
      =>
      0 |-> list(
              compareAcc(
                PREFIX,
                vCons(SCORE, SCORES),
                vCons(PREDICTED, PREDICTIONS)))
    </heap>
    <heapLoc> 1 </heapLoc>
    requires isInt(SCORE)
     andBool isInt(PREDICTED)
     andBool notBool isRefV(SCORE)
     andBool notBool isRefV(PREDICTED)
     andBool notBool isRefV(applyBin("-", SCORE, PREDICTED))
     andBool sameIntLists(SCORES, PREDICTIONS)
     andBool notBool ("abs" in_keys(MODULESCOPE))

  claim [compare-entry-empty]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "compare",
            Params("game", "guess"),
            Assign(Name("result"), ListExpr(.Exprs))
            For(
              TupleExpr(Name("score"), Name("predicted")),
              Call(Name("zip"), Name("game"), Name("guess")),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Call(
                    Name("abs"),
                    BinOp("-", Name("score"), Name("predicted")))))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(Name("compare"), list(.ValSeq), list(.ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [compare-entry-step]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "compare",
            Params("game", "guess"),
            Assign(Name("result"), ListExpr(.Exprs))
            For(
              TupleExpr(Name("score"), Name("predicted")),
              Call(Name("zip"), Name("game"), Name("guess")),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  Call(
                    Name("abs"),
                    BinOp("-", Name("score"), Name("predicted")))))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(
           Name("compare"),
           list(vCons(SCORE:Val, SCORES:ValSeq)),
           list(vCons(PREDICTED:Val, PREDICTIONS:ValSeq)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
              compareAcc(
                .ValSeq,
                vCons(SCORE, SCORES),
                vCons(PREDICTED, PREDICTIONS)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(SCORE)
     andBool isInt(PREDICTED)
     andBool notBool isRefV(SCORE)
     andBool notBool isRefV(PREDICTED)
     andBool notBool isRefV(applyBin("-", SCORE, PREDICTED))
     andBool sameIntLists(SCORES, PREDICTIONS)
endmodule
