// spec.k — f on the UNIFIED semantics (src/). First NESTED-loop proof: three loop
// invariants (two inner, one outer) + the entry. See ./PROOF.md.
//
//   kompile verification.k --backend haskell \
//     --main-module F-VERIFICATION --syntax-module MPY-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module F-SPEC

requires "verification.k"

module F-SPEC
  imports F-VERIFICATION

  // ---- INNER factorial loop invariant ----------------------------------------
  // The inner body `x *= j` over #loop(rangeObj(J,HI,1), j, ...) leaves x := factFold(J,HI,X)
  // (j scratch).  n/ret/i are loop-constant.  Induction on the index range (J, HI).  Used
  // inside the outer step's EVEN branch with (J,HI) = (2, i+1) after the first inner iteration.
  claim
    <k>
      #loop(rangeObj(J:Int, HI:Int, 1), Name("j"),
        AugAssign(Name("x"), "*", Name("j")))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "f" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ret" <- RET:Val ] [ "i" <- IV:Val ]
                              [ "x" <- X:Int ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "n" <- NV ] [ "ret" <- RET ] [ "i" <- IV ]
                              [ "x" <- factFold(J, HI, X) ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- INNER triangular-sum loop invariant -----------------------------------
  // The inner body `x += j` leaves x := sumFold(J, HI, X).  Used inside the outer step's
  // ODD branch.
  claim
    <k>
      #loop(rangeObj(J:Int, HI:Int, 1), Name("j"),
        AugAssign(Name("x"), "+", Name("j")))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "f" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ret" <- RET:Val ] [ "i" <- IV:Val ]
                              [ "x" <- X:Int ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "n" <- NV ] [ "ret" <- RET ] [ "i" <- IV ]
                              [ "x" <- sumFold(J, HI, X) ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- OUTER list-build loop invariant ---------------------------------------
  // The outer body at index i:
  //   if i % 2 == 0: x=1; <inner *= loop>; ret += [x]   # x = i!
  //   else:          x=0; <inner += loop>; ret += [x]   # x = 1+..+i
  // leaves ret := list(valSeqConcat(R, retFrom(I, HI)))  (i/x/j per-iteration scratch).
  // Per iteration the inner loop (via the two INNER invariants) makes x = elemAt(I), the
  // `if i%2==0` split lines up with elemAt's branch, and `ret += [x]` left-appends
  // [elemAt(I)] — collapsed by the reassoc + right-identity lemmas to retFrom(I, HI).
  // requires I >= 1 so each inner range(1, i+1) runs at least once.
  claim
    <k>
      #loop(rangeObj(I:Int, HI:Int, 1), Name("i"),
        If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
          Assign(Name("x"), Int(1))
          For(Name("j"), Call(Name("range"), (Int(1), BinOp("+", Name("i"), Int(1)))),
            AugAssign(Name("x"), "*", Name("j")))
          AugAssign(Name("ret"), "+", ListExpr(Name("x"))),
          Assign(Name("x"), Int(0))
          For(Name("j"), Call(Name("range"), (Int(1), BinOp("+", Name("i"), Int(1)))),
            AugAssign(Name("x"), "+", Name("j")))
          AugAssign(Name("ret"), "+", ListExpr(Name("x")))))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "f" <- _:Val ], parent(-1))
       1 |-> ( scope(.Map [ "n" <- NV:Val ] [ "ret" <- ref(HN3_0:Int) ] [ "i" <- _:Val ]
                              [ "x" <- _:Val ] [ "j" <- _:Val ], parent(0))
               => scope(.Map [ "n" <- NV ] [ "ret" <- ref(?HN3_0B:Int) ]
                              [ "i" <- ?_:Val ] [ "x" <- ?_:Val ] [ "j" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <ret> noRet </ret>
    <heap> (HN3_0 |-> list(R:ValSeq)) HRST3:Map
        => (?HN3_0B |-> list(valSeqConcat(R, retFrom(I, HI)))) ?FRESH3:Map HRST3 </heap>
    <heapLoc> HLC3:Int => ?HLC4:Int </heapLoc>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 1
     andBool 0 <=Int HN3_0 andBool HN3_0 <Int HLC3 andBool keysBelow(HRST3, HLC3)
    ensures 0 <=Int ?HN3_0B andBool ?HN3_0B <Int ?HLC4 andBool HLC3 <=Int ?HLC4
     andBool keysBelow(?FRESH3, ?HLC4)
     andBool notBool (?HN3_0B in_keys(?FRESH3)) andBool notBool (?HN3_0B in_keys(HRST3))
    [all-path]

  // ---- Entry claim -----------------------------------------------------------
  // After `result = f(N)`, the root scope's result is fRes(N) = list(retFrom(1, N+1)): the
  // length-N list whose element at index i (1-based, i = 1..N) is i! if i even else 1+..+i.
  // Domain N >= 1 (the docstring's "list of size n"; for N=0 the loop is empty and f returns
  // [] — outside this entry's claim; mirrors 139's first-iteration-unroll so the loop var i is
  // bound when the circularity applies).
  claim
    <k>
      FuncDef("f", Params("n"),
        Assign(Name("ret"), ListExpr(.Exprs))
        For(Name("i"), Call(Name("range"), (Int(1), BinOp("+", Name("n"), Int(1)))),
          If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
            Assign(Name("x"), Int(1))
            For(Name("j"), Call(Name("range"), (Int(1), BinOp("+", Name("i"), Int(1)))),
              AugAssign(Name("x"), "*", Name("j")))
            AugAssign(Name("ret"), "+", ListExpr(Name("x"))),
            Assign(Name("x"), Int(0))
            For(Name("j"), Call(Name("range"), (Int(1), BinOp("+", Name("i"), Int(1)))),
              AugAssign(Name("x"), "+", Name("j")))
            AugAssign(Name("ret"), "+", ListExpr(Name("x")))))
        Return(Name("ret")))
      Assign(Name("result"), Call(Name("f"), Int(N:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "f" <- ?_:Val ] [ "result" <- ref(?RH:Int) ], parent(-1))
    </scopes>
    <heap> .Map => (?RH |-> list(retFrom(1, N +Int 1))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
    [all-path]
endmodule
