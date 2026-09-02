requires "verification.k"
module DOALG-SPEC
  imports DOALG-VERIFICATION
  claim <k> #loop(rangeObj(I:Int, vsLen(OPS:ValSeq), 1), Name("i"),
          If(Compare(Subscript(Name("ops"), Name("i")), CmpOp("==", Str("+"))),
            Assign(Name("cur"), BinOp("+", Name("cur"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))))),
            Assign(Name("cur"), BinOp("-", Name("cur"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))))))) => .K ... </k>
    <env> 1 </env>
    <scopes> -1 |-> builtinsScope  0 |-> scope(.Map, parent(-1))
       1 |-> ( scope(.Map [ "ops" <- ref(HO:Int) ] [ "nds" <- ref(HN:Int) ] [ "cur" <- CUR:Int ] [ "i" <- _:Val ], parent(0))
            => scope(.Map [ "ops" <- ref(HO) ] [ "nds" <- ref(HN) ] [ "cur" <- addFold(OPS, NDS, CUR, I, vsLen(OPS)) ] [ "i" <- ?_:Val ], parent(0)) ) </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> (HO |-> list(OPS)) (HN |-> list(NDS:ValSeq)) HREST:Map </heap>
    <heapLoc> HLM:Int </heapLoc> <ret> noRet </ret> <stack> _STK:List </stack> <exc> NoExc </exc> <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool I >=Int 0 andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1 andBool notBool (HO ==Int HN)
    [all-path]
endmodule
