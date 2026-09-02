requires "verification.k"
module DOALG-SPEC
  imports DOALG-VERIFICATION
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
endmodule
