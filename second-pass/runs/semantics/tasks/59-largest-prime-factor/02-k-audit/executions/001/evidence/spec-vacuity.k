requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: for the satisfying state N=12, F=2, L=1 this
  // demands 4 although the loop and lpfSpec both return 3.
  claim [false-off-by-one-loop-result]:
    <k>
      #while(lpfCondition, lpfStep)
      ~> (Return(Name("factor")) .Stmts)
      ~> #endcall
      => (lpfSpec(N, F) +Int 1) ~> CONT
    </k>
    <env> L => CALLER </env>
    <scopes>
      SC (L |-> scope(("n" |-> N) ("factor" |-> F), parent(0)))
      => SC
    </scopes>
    <scopeLoc> L +Int 1 => L </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, L)) REST
      => REST
    </stack>
    <ret> noRet </ret>
    requires N >Int 1
     andBool F >Int 1
     andBool L >=Int 1
     andBool notBool (L in_keys(SC))
    [circularity]
endmodule
