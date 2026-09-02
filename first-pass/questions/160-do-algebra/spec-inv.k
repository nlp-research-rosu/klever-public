// spec-inv.k — the two loop invariants in the ENTRY-COMPATIBLE form: NM:Map absorbs the extra
// function locals, `...` in <scopes> absorbs the -1/0 frames. Sanity that this generalization of
// spec-pow.k / spec-mul.k still proves before it is reused inside the entry claim (spec.k).
requires "verification.k"

module DOALG-SPEC
  imports DOALG-VERIFICATION

  // (1) ** pass invariant — ops/nds by value, r_nds/r_ops growing refs.
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
      ... 1 |-> ( scope(NM:Map [ "ops" <- list(OPS) ] [ "nds" <- list(NDS:ValSeq) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(HRN:Int) ] [ "r_ops" <- ref(HRO:Int) ] [ "cur" <- C:Int ]
                         [ "k" <- _:Val ] [ "i" <- _:Val ] [ "base" <- _:Val ], parent(0))
            => scope(NM [ "ops" <- list(OPS) ] [ "nds" <- list(NDS) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(?HRNB:Int) ] [ "r_ops" <- ref(?HROB:Int) ]
                         [ "cur" <- p3cur(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C)) ]
                         [ "k" <- ?_:Val ] [ "i" <- ?_:Val ] [ "base" <- ?_:Val ], parent(0)) ) ...
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

  // (2) combined * // + - pass invariant — ops/nds as refs, scalar total/term/sign, heap unchanged.
  claim
    <k> #loop(rangeObj(I:Int, vsLen(OPS:ValSeq), 1), Name("i"),
          Assign(Name("o"), Subscript(Name("ops"), Name("i")))
          If(Compare(Name("o"), CmpOp("==", Str("*"))),
            Assign(Name("term"), BinOp("*", Name("term"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))))),
            If(Compare(Name("o"), CmpOp("==", Str("//"))),
              Assign(Name("term"), BinOp("//", Name("term"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))))),
              If(Compare(Name("o"), CmpOp("==", Str("+"))),
                Assign(Name("total"), BinOp("+", Name("total"), BinOp("*", Name("sign"), Name("term"))))
                Assign(Name("term"), BinOp("*", Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))), Int(1)))
                Assign(Name("sign"), Int(1)),
                Assign(Name("total"), BinOp("+", Name("total"), BinOp("*", Name("sign"), Name("term"))))
                Assign(Name("term"), BinOp("*", Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))), Int(1)))
                Assign(Name("sign"), BinOp("-", Int(0), Int(1)))))))
     => .K ... </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> ( scope(NM:Map [ "ops" <- ref(HO:Int) ] [ "nds" <- ref(HN:Int) ] [ "o" <- _:Val ]
                         [ "total" <- TOTAL:Int ] [ "term" <- TERM:Int ] [ "sign" <- SIGN:Int ] [ "i" <- _:Val ], parent(0))
            => scope(NM [ "ops" <- ref(HO) ] [ "nds" <- ref(HN) ] [ "o" <- ?_:Val ]
                          [ "total" <- mafT(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                          [ "term" <- mafM(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                          [ "sign" <- mafS(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                          [ "i" <- ?_:Val ], parent(0)) ) ...
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (HO |-> list(OPS)) (HN |-> list(NDS:ValSeq)) HREST:Map </heap>
    <heapLoc> HLM:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool I >=Int 0
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1
     andBool notBool (HO ==Int HN)
    [all-path]
endmodule
