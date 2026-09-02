// spec.k — digits proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module DIGITS-VERIFICATION --syntax-module DIGITS-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module DIGITS-SPEC

requires "verification.k"

module DIGITS-SPEC
  imports DIGITS-VERIFICATION

  // ---- Loop invariant: the digit-product loop over the digit string ----------
  // Over any IntSeq CS the body (int_digit = int(digit); if int_digit % 2 == 1 then
  // product *= int_digit, odd_count += 1) leaves
  //   product := oddProd(CS, PROD)   and   odd_count := oddCnt(CS, OC).
  // By induction on CS; the parity If case-splits on oddDigit(C) = (C-48)%2==1.
  // `digit` and `int_digit` are scratch (existential both sides) — they exist after
  // the first iteration binds them; the entry's first #strLoop unrolls into this shape.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"),
        Assign(Name("int_digit"), Call(Name("int"), Name("digit")))
        If(Compare(BinOp("%", Name("int_digit"), Int(2)), CmpOp("==", Int(1))),
           Assign(Name("product"), BinOp("*", Name("product"), Name("int_digit")))
           AugAssign(Name("odd_count"), "+", Int(1)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "digits" <- FB0:Val ], parent(-1))  L |-> ( scope(.Map [ "n" <- NV:Val ] [ "product" <- PROD:Int ] [ "odd_count" <- OC:Int ]
                              [ "digit" <- _:Val ] [ "int_digit" <- _:Val ], parent(GLB:Int))
               => scope(.Map [ "n" <- NV ] [ "product" <- oddProd(CS, PROD) ] [ "odd_count" <- oddCnt(CS, OC) ]
                              [ "digit" <- ?_:Val ] [ "int_digit" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS)
    [all-path]

  // ---- Entry claim — see ../3-below-zero/PROOF.md ----------------------------
  // After `result = digits(str(CS))` the root scope's result is:
  //   0                if there are no odd digits (oddCnt(CS,0) == 0)
  //   oddProd(CS, 1)   otherwise (product of the odd digit values).
  // CS = the digit code-sequence of str(n); str(n) of a non-negative int is exactly a
  // non-empty sequence of digit codes 48..57.  Restricted to non-empty CS (str(n) is
  // never the empty string; the loop over .IntSeq leaves the seeds 1 / 0).
  claim
    <k>
      FuncDef("digits", Params("n"),
        Assign(Name("product"), Int(1))
        Assign(Name("odd_count"), Int(0))
        For(Name("digit"), Call(Name("str"), Name("n")),
          Assign(Name("int_digit"), Call(Name("int"), Name("digit")))
          If(Compare(BinOp("%", Name("int_digit"), Int(2)), CmpOp("==", Int(1))),
             Assign(Name("product"), BinOp("*", Name("product"), Name("int_digit")))
             AugAssign(Name("odd_count"), "+", Int(1)),
             .Stmts))
        If(Compare(Name("odd_count"), CmpOp("==", Int(0))),
           Return(Int(0)),
           Return(Name("product"))))
      Assign(Name("result"), Call(Name("digits"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "digits" <- ?_:Val ]
                       [ "result" <- #if oddCnt(CS, 0) ==Int 0 #then 0 #else oddProd(CS, 1) #fi ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigit(CS) andBool CS =/=K .IntSeq
    [all-path]
endmodule
