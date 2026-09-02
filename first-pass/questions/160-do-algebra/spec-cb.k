requires "verification.k"
module DOALG-SPEC
  imports DOALG-VERIFICATION
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
endmodule
