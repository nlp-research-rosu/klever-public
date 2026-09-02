requires "verification.k"

module CAR-RACE-COLLISION-SPEC
  imports CAR-RACE-COLLISION-VERIFICATION

  claim
    <k>
      FuncDef("car_race_collision", Params("n"), Return(BinOp("**", Name("n"), Int(2))))
      Assign(Name("result"), Call(Name("car_race_collision"), N:Int))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "car_race_collision" <- ?_:Val ] [ "result" <- ?R:Int ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    // the shared ** bridge (lemmas/arith.k) keeps the power as the opaque
    // ipow atom (^Int is partial and hangs on symbolic exponents)
    ensures ?R ==Int ipow(N, 2)
    [all-path]
endmodule
