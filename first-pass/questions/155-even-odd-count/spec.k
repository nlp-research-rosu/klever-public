// spec.k — the reachability claims kprove discharges. On the UNIFIED semantics.
//
//   kompile verification.k --backend haskell \
//     --main-module EVEN-ODD-COUNT-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module EVEN-ODD-COUNT-SPEC --depth 2000

requires "verification.k"

module EVEN-ODD-COUNT-SPEC
  imports EVEN-ODD-COUNT-VERIFICATION

  // ---- Loop invariant: the dual-accumulator fold over the digit string ----------
  // Iterating `for i in str(CS)` with body `if int(i)%2==0: even+=1 else odd+=1` leaves
  //   even_count := evenCnt(CS, EC),  odd_count := oddCnt(CS, OC).
  // Induction on CS via #iterNext (str(CS) => str(.IntSeq) | str(iCons(C,R))); the parity If
  // case-splits on evenDigit(C). `int(i)` = int(str(iCons(C,.IntSeq))) = C-48 needs C a digit,
  // hence requires allDigit(CS) (preserved under peeling). `i` ends bound to some 1-char str.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("i"),
        If(Compare(BinOp("%", Call(Name("int"), Name("i")), Int(2)), CmpOp("==", Int(0))),
           AugAssign(Name("even_count"), "+", Int(1)),
           AugAssign(Name("odd_count"), "+", Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "even_odd_count" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "num" <- NV:Val ] [ "even_count" <- EC:Int ] [ "odd_count" <- OC:Int ]
                              [ "i" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "num" <- NV ] [ "even_count" <- evenCnt(CS, EC) ] [ "odd_count" <- oddCnt(CS, OC) ]
                              [ "i" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS)
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // The input integer is presented as the opaque carrier intOfD(CS) (STR-INT-DECIMAL-LEMMAS).
  // abs(intOfD(CS)) => intOfD(CS) (it is >= 0); str(intOfD(CS)) => str(CS) (the trusted bridge,
  // valid for a canonical decimal CS). So the loop folds CS and after `result = even_odd_count(
  // intOfD(CS))` the root result is the tuple (evenCnt(CS,0), oddCnt(CS,0)) — (#even, #odd)
  // digits. Domain: CS a canonical decimal (validDec) with all digit codes (allDigit) — the
  // digit-strings of every non-negative integer, so the claim is complete over that domain.
  claim
    <k>
      FuncDef("even_odd_count", Params("num"),
        Assign(Name("even_count"), Int(0))
        Assign(Name("odd_count"), Int(0))
        For(Name("i"), Call(Name("str"), Call(Name("abs"), Name("num"))),
          If(Compare(BinOp("%", Call(Name("int"), Name("i")), Int(2)), CmpOp("==", Int(0))),
             AugAssign(Name("even_count"), "+", Int(1)),
             AugAssign(Name("odd_count"), "+", Int(1))))
        Return(TupleExpr(Name("even_count"), Name("odd_count"))))
      Assign(Name("result"), Call(Name("even_odd_count"), intOfD(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "even_odd_count" <- ?_:Val ]
                       [ "result" <- tuple(vCons(evenCnt(CS, 0), vCons(oddCnt(CS, 0), .ValSeq))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validDec(CS) andBool allDigit(CS)
    [all-path]
endmodule
