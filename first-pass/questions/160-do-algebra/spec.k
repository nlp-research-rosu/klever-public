// spec.k — do_algebra ENTRY proof (STEP 4). The REAL 2-pass evaluator, NO interception. The entry
// runs the whole FuncDef; the two loops fold via the invariants (1)/(2) to powFold/mulAddFold, so
// `out` is the VERIFIED daResult(OPS, NDS) composition. .append() gives stable heap refs (149 pattern).
requires "verification.k"

module DOALG-SPEC
  imports DOALG-VERIFICATION

  // (1) ** pass invariant — ops/nds by value, r_nds/r_ops STABLE refs (in-place .append()).
  claim
    <k> #loop(rangeObj(K:Int, vsLen(OPS:ValSeq), 1), Name("k"),
          Assign(Name("i"), BinOp("-", BinOp("-", Name("m"), Int(1)), Name("k")))
          If(Compare(Subscript(Name("ops"), Name("i")), CmpOp("==", Str("**"))),
            Assign(Name("base"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))
            Assign(Name("cur"), BinOp("**", Name("base"), Name("cur"))),
            Expr(Call(Attribute(Name("r_nds"), "append"), Name("cur")))
            Expr(Call(Attribute(Name("r_ops"), "append"), Subscript(Name("ops"), Name("i"))))
            Assign(Name("cur"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))))
     => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "do_algebra" <- DAV:Val ], parent(-1))
       1 |-> ( scope(.Map [ "operator" <- list(OPS) ] [ "operand" <- list(NDS:ValSeq) ]
                         [ "ops" <- list(OPS) ] [ "nds" <- list(NDS) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(HRN:Int) ] [ "r_ops" <- ref(HRO:Int) ] [ "cur" <- C:Int ]
                         [ "k" <- _:Val ] [ "i" <- _:Val ] [ "base" <- _:Val ], parent(0))
            => scope(.Map [ "operator" <- list(OPS) ] [ "operand" <- list(NDS) ]
                         [ "ops" <- list(OPS) ] [ "nds" <- list(NDS) ] [ "m" <- vsLen(OPS) ]
                         [ "r_nds" <- ref(HRN) ] [ "r_ops" <- ref(HRO) ]
                         [ "cur" <- p3cur(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C)) ]
                         [ "k" <- ?_:Val ] [ "i" <- ?_:Val ] [ "base" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (HRN |-> list(RN:ValSeq)) (HRO |-> list(RO:ValSeq)) HREST:Map
        => (HRN |-> list(p3nds(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C))))
           (HRO |-> list(p3ops(powFold(OPS, NDS, K, vsLen(OPS), RN, RO, C)))) HREST </heap>
    <ret> noRet </ret> <stack> _STK:List </stack> <exc> NoExc </exc> <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool allNonNeg(NDS) andBool C >=Int 0 andBool K >=Int 0
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1 andBool notBool (HRN ==Int HRO)
    [all-path]

  // (2) combined * // + - pass invariant — ops/nds refs, scalar total/term/sign, heap unchanged.
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
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "do_algebra" <- DAV:Val ], parent(-1))
       1 |-> ( scope(.Map [ "operator" <- OPV:Val ] [ "operand" <- ODV:Val ] [ "m" <- MV:Val ]
                         [ "r_ops" <- RPV:Val ] [ "r_nds" <- RNV:Val ] [ "cur" <- CURV:Val ]
                         [ "k" <- KV:Val ] [ "base" <- BV:Val ]
                         [ "ops" <- ref(HO:Int) ] [ "nds" <- ref(HN:Int) ] [ "o" <- _:Val ]
                         [ "total" <- TOTAL:Int ] [ "term" <- TERM:Int ] [ "sign" <- SIGN:Int ] [ "i" <- _:Val ], parent(0))
            => scope(.Map [ "operator" <- OPV ] [ "operand" <- ODV ] [ "m" <- MV ]
                         [ "r_ops" <- RPV ] [ "r_nds" <- RNV ] [ "cur" <- CURV ]
                         [ "k" <- KV ] [ "base" <- BV ]
                         [ "ops" <- ref(HO) ] [ "nds" <- ref(HN) ] [ "o" <- ?_:Val ]
                         [ "total" <- mafT(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                         [ "term" <- mafM(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                         [ "sign" <- mafS(mulAddFold(OPS, NDS, TOTAL, TERM, SIGN, I, vsLen(OPS))) ]
                         [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (HO |-> list(OPS)) (HN |-> list(NDS:ValSeq)) HREST:Map </heap>
    <heapLoc> HLM:Int </heapLoc>
    <ret> noRet </ret> <stack> _STK:List </stack> <exc> NoExc </exc> <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool I >=Int 0
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1 andBool notBool (HO ==Int HN)
    [all-path]

  // (3) ENTRY — run the whole do_algebra; the two loops fold to (1)/(2), so out = daResult(OPS, NDS).
  claim
    <k>
      FuncDef("do_algebra", Params("operator", "operand"),
        Assign(Name("ops"), Name("operator"))
        Assign(Name("nds"), Name("operand"))
        Assign(Name("m"), Call(Name("len"), Name("ops")))
        Assign(Name("r_ops"), ListExpr(.Exprs))
        Assign(Name("r_nds"), ListExpr(.Exprs))
        Assign(Name("cur"), BinOp("*", Subscript(Name("nds"), Name("m")), Int(1)))
        Assign(Name("k"), Int(0))
        Assign(Name("i"), Int(0))
        Assign(Name("base"), Int(0))
        For(Name("k"), Call(Name("range"), Name("m")),
          Assign(Name("i"), BinOp("-", BinOp("-", Name("m"), Int(1)), Name("k")))
          If(Compare(Subscript(Name("ops"), Name("i")), CmpOp("==", Str("**"))),
            Assign(Name("base"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))
            Assign(Name("cur"), BinOp("**", Name("base"), Name("cur"))),
            Expr(Call(Attribute(Name("r_nds"), "append"), Name("cur")))
            Expr(Call(Attribute(Name("r_ops"), "append"), Subscript(Name("ops"), Name("i"))))
            Assign(Name("cur"), BinOp("*", Subscript(Name("nds"), Name("i")), Int(1)))))
        Expr(Call(Attribute(Name("r_nds"), "append"), Name("cur")))
        Assign(Name("ops"), Subscript(Name("r_ops"), Slice(NoBound, NoBound, Int(-1))))
        Assign(Name("nds"), Subscript(Name("r_nds"), Slice(NoBound, NoBound, Int(-1))))
        Assign(Name("total"), Int(0))
        Assign(Name("term"), BinOp("*", Subscript(Name("nds"), Int(0)), Int(1)))
        Assign(Name("sign"), Int(1))
        Assign(Name("o"), Int(0))
        For(Name("i"), Call(Name("range"), Call(Name("len"), Name("ops"))),
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
        Return(BinOp("+", Name("total"), BinOp("*", Name("sign"), Name("term")))))
      Assign(Name("out"), Call(Name("do_algebra"), list(OPS:ValSeq), list(NDS:ValSeq)))
     => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
       0 |-> scope(.Map [ "do_algebra" <- ?_:Val ] [ "out" <- daResult(OPS, NDS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 => ?_:Int </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret> <stack> .List </stack> <exc> NoExc </exc> <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool allNonNeg(NDS)
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1 andBool vsLen(OPS) >=Int 0
    [all-path]
endmodule
