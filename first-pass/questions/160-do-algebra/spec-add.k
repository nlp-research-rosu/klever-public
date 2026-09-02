// spec-add.k — ISOLATED + - pass loop invariant (STEP 1 of the 160 proof). The scalar accumulator
// `cur` folds over the +/- operators to addFold; the pass reads ops/nds (heap refs) and does NO
// allocation, so the heap is unchanged (no ?FRESH). Operator branch via the codesProj compare bridge.
requires "verification.k"

module DOALG-SPEC
  imports DOALG-VERIFICATION

  claim
    <k> #loop(rangeObj(I:Int, vsLen(OPS:ValSeq), 1), Name("i"),
          If(Compare(Subscript(Name("ops"), Name("i")), CmpOp("==", Str("+"))),
            Assign(Name("cur"), BinOp("+", Name("cur"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1))))),
            Assign(Name("cur"), BinOp("-", Name("cur"), Subscript(Name("nds"), BinOp("+", Name("i"), Int(1)))))))
     => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
       1 |-> ( scope(.Map [ "ops" <- list(OPS:ValSeq) ] [ "nds" <- list(NDS:ValSeq) ] [ "cur" <- CUR:Int ] [ "i" <- _:Val ], parent(0))
            => scope(.Map [ "ops" <- list(OPS) ] [ "nds" <- list(NDS) ] [ "cur" <- addFold(OPS, NDS, CUR, I, vsLen(OPS)) ] [ "i" <- ?_:Val ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HREST:Map </heap>
    <heapLoc> HLM:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allStr(OPS) andBool allInt(NDS) andBool I >=Int 0
     andBool vsLen(NDS) ==Int vsLen(OPS) +Int 1
    [all-path]
endmodule
