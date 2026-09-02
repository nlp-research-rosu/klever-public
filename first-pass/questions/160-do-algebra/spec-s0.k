// spec-pow.k — ISOLATED ** pass loop invariant (STEP 3). Scan RIGHT-TO-LEFT (i = m-1-k over
// k in range(m)); '**' folds nds[i] ** cur into cur (ipow, via the `base = nds[i]*1` int-coercion
// temp so the shared ipow bridge sees an Int base); every other operator appends cur to r_nds and
// ops[i] to r_ops (each `r + [x]` #alloc's a fresh list cell → keysBelow discipline, 2 growing refs),
// then starts a fresh cur = nds[i]*1. Folds to powFold. ops/nds are READ-ONLY here → by value (no
// heap cells); only r_nds/r_ops are growing refs (keysBelow discipline, 62-derivative template).
requires "verification.k"

module DOALG-SPEC
  imports DOALG-VERIFICATION

  claim
    <k> #loop(rangeObj(K:Int, vsLen(OPS:ValSeq), 1), Name("k"),
          Assign(Name("i"), BinOp("-", BinOp("-", Name("m"), Int(1)), Name("k")))
          If(Compare(Subscript(Name("ops"), Name("i")), CmpOp("==", Str("**"))),
            Assign(Name("base"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))
            Assign(Name("cur"), BinOp("**", Name("base"), Name("cur"))),
            Assign(Name("r_nds"), BinOp("+", Name("r_nds"), ListExpr(Name("cur"))))
            Assign(Name("r_ops"), BinOp("+", Name("r_ops"), ListExpr(Subscript(Name("ops"), Name("i")))))
            Assign(Name("cur"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))))
     => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "do_algebra" <- DAV:Val ], parent(-1))
       1 |-> ( scope(.Map [ "ops" <- list(OPS) ] [ "nds" <- list(NDS:ValSeq) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(HRN:Int) ] [ "r_ops" <- ref(HRO:Int) ] [ "cur" <- C:Int ]
                         [ "k" <- _:Val ] [ "i" <- _:Val ] [ "base" <- _:Val ], parent(0))
            => scope(.Map [ "ops" <- list(OPS) ] [ "nds" <- list(NDS) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(?HRNB:Int) ] [ "r_ops" <- ref(?HROB:Int) ]
                         [ "cur" <- p3cur(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C)) ]
                         [ "k" <- ?_:Val ] [ "i" <- ?_:Val ] [ "base" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (HRN |-> list(RN:ValSeq)) (HRO |-> list(RO:ValSeq)) HREST:Map
        => (?HRNB:Int |-> list(p3nds(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C))))
           (?HROB:Int |-> list(p3ops(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C)))) ?_:Map </heap>
    <heapLoc> HLC:Int => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool allNonNeg(NDS) andBool C >=Int 0 andBool K >=Int 0
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1
     andBool 0 <=Int HRN andBool HRN <Int HLC andBool 0 <=Int HRO andBool HRO <Int HLC
     andBool keysBelow(HREST, HLC) andBool notBool (HRN ==Int HRO)
    [all-path]
endmodule
