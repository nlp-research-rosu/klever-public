// spec.k — prod_signs proof on the UNIFIED semantics (src/).
// Dual fold: sum of |x| times product of sign(x); None on empty.

requires "verification.k"

module PROD-SIGNS-SPEC
  imports PROD-SIGNS-VERIFICATION

  // ---- Loop invariant (circularity) — from (sum_abs=SA, sign_prod=SP, n=N) the loop
  // leaves sum_abs := SA +Int sumAbs(VS), sign_prod := SP *Int signProd(VS),
  // n := N +Int vsLen(VS). Induction on VS; the if/elif/else splits on x<0 / x>0 / x==0.
  claim
    <k>
      #loop(list(VS:ValSeq), Name("x"),
        Assign(Name("n"), BinOp("+", Name("n"), Int(1)))
        If(Compare(Name("x"), CmpOp("<", Int(0))),
          Assign(Name("sum_abs"), BinOp("+", Name("sum_abs"), BinOp("-", Int(0), Name("x"))))
          Assign(Name("sign_prod"), BinOp("*", Name("sign_prod"), UnaryOp("-", Int(1)))),
          If(Compare(Name("x"), CmpOp(">", Int(0))),
            Assign(Name("sum_abs"), BinOp("+", Name("sum_abs"), Name("x"))),
            Assign(Name("sign_prod"), BinOp("*", Name("sign_prod"), Int(0))))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> (
        scope(.Map [ "arr" <- AV:Val ] [ "sum_abs" <- SA:Int ] [ "sign_prod" <- SP:Int ] [ "n" <- N:Int ] [ "x" <- _:Val ], P:Parent) =>
        scope(.Map [ "arr" <- AV ] [ "sum_abs" <- SA +Int sumAbs(VS) ] [ "sign_prod" <- SP *Int signProd(VS) ] [ "n" <- N +Int vsLen(VS) ] [ "x" <- ?_:Val ], P)
      ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]

  // ---- Entry claim — result = prod_signs(list(VS)) ==
  //   #if (vsLen(VS) >Int 0) #then (signProd(VS) *Int sumAbs(VS)) #else noneV.
  claim
    <k>
      FuncDef("prod_signs", Params("arr"),
        Assign(Name("sum_abs"), Int(0))
        Assign(Name("sign_prod"), Int(1))
        Assign(Name("n"), Int(0))
        Assign(Name("x"), Int(0))
        For(Name("x"), Name("arr"),
          Assign(Name("n"), BinOp("+", Name("n"), Int(1)))
          If(Compare(Name("x"), CmpOp("<", Int(0))),
            Assign(Name("sum_abs"), BinOp("+", Name("sum_abs"), BinOp("-", Int(0), Name("x"))))
            Assign(Name("sign_prod"), BinOp("*", Name("sign_prod"), UnaryOp("-", Int(1)))),
            If(Compare(Name("x"), CmpOp(">", Int(0))),
              Assign(Name("sum_abs"), BinOp("+", Name("sum_abs"), Name("x"))),
              Assign(Name("sign_prod"), BinOp("*", Name("sign_prod"), Int(0))))))
        Assign(Name("result"), NoneVal)
        If(Compare(Name("n"), CmpOp(">", Int(0))),
           Assign(Name("result"), BinOp("*", Name("sign_prod"), Name("sum_abs"))),
           .Stmts)
        Return(Name("result")))
      Assign(Name("result"), Call(Name("prod_signs"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "prod_signs" <- ?_:Val ]
                       [ "result" <- #if (vsLen(VS) >Int 0) #then (signProd(VS) *Int sumAbs(VS)) #else noneV #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInt(VS)
    [all-path]
endmodule
