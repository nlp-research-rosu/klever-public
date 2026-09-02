// spec.k — decode_cyclic proof on the UNIFIED semantics (src/).
//
//   kompile verification.k --backend haskell \
//     --main-module DECODE-CYCLIC-VERIFICATION --syntax-module DECODE-CYCLIC-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module DECODE-CYCLIC-SPEC

requires "verification.k"

module DECODE-CYCLIC-SPEC
  imports DECODE-CYCLIC-VERIFICATION

  // ---- Loop invariant (the circularity) — see ../3-below-zero/PROOF.md -------
  // FIVE accumulators (result, c0, c1, buf, count) over CS.  From their starting values the
  // loop leaves each as its summary of CS.  By induction on CS; the count==0/1 If-chain and
  // the count==3 If line up with each summary's four branch-split rules (all on `count`).
  claim
    <k>
      #loop(str(CS:IntSeq), Name("ch"),
        If(Compare(Name("count"), CmpOp("==", Int(0))),
           Assign(Name("c0"), Name("ch")),
           If(Compare(Name("count"), CmpOp("==", Int(1))),
              Assign(Name("c1"), Name("ch")),
              .Stmts))
        Assign(Name("buf"), BinOp("+", Name("buf"), Name("ch")))
        Assign(Name("count"), BinOp("+", Name("count"), Int(1)))
        If(Compare(Name("count"), CmpOp("==", Int(3))),
           Assign(Name("result"), BinOp("+", BinOp("+", BinOp("+", Name("result"), Name("ch")), Name("c0")), Name("c1")))
           Assign(Name("buf"), Str(""))
           Assign(Name("count"), Int(0)),
           .Stmts))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "s" <- SV:Val ] [ "result" <- str(RESULT:IntSeq) ] [ "c0" <- str(C0:IntSeq) ]
                              [ "c1" <- str(C1:IntSeq) ] [ "buf" <- str(BUF:IntSeq) ] [ "count" <- COUNT:Int ]
                              [ "ch" <- _:Val ], P:Parent)
               => scope(.Map [ "s" <- SV ] [ "result" <- str(decRes(CS, RESULT, C0, C1, COUNT)) ]
                              [ "c0" <- str(decC0(CS, C0, COUNT)) ] [ "c1" <- str(decC1(CS, C1, COUNT)) ]
                              [ "buf" <- str(decBuf(CS, BUF, COUNT)) ] [ "count" <- decCount(CS, COUNT) ]
                              [ "ch" <- ?_:Val ], P) ) ...
    </scopes>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]

  // ---- Entry claim — see ../3-below-zero/PROOF.md ----------------------------
  // After `result = decode_cyclic(str(CS))`, the root scope's result is the loop output
  // followed by the leftover buffer: seqConcat(decRes(CS,...), decBuf(CS,...)), for symbolic CS.
  claim
    <k>
      FuncDef("decode_cyclic", Params("s"),
        Assign(Name("result"), Str(""))
        Assign(Name("c0"), Str(""))
        Assign(Name("c1"), Str(""))
        Assign(Name("buf"), Str(""))
        Assign(Name("count"), Int(0))
        Assign(Name("ch"), Str(""))
        For(Name("ch"), Name("s"),
          If(Compare(Name("count"), CmpOp("==", Int(0))),
             Assign(Name("c0"), Name("ch")),
             If(Compare(Name("count"), CmpOp("==", Int(1))),
                Assign(Name("c1"), Name("ch")),
                .Stmts))
          Assign(Name("buf"), BinOp("+", Name("buf"), Name("ch")))
          Assign(Name("count"), BinOp("+", Name("count"), Int(1)))
          If(Compare(Name("count"), CmpOp("==", Int(3))),
             Assign(Name("result"), BinOp("+", BinOp("+", BinOp("+", Name("result"), Name("ch")), Name("c0")), Name("c1")))
             Assign(Name("buf"), Str(""))
             Assign(Name("count"), Int(0)),
             .Stmts))
        Assign(Name("result"), BinOp("+", Name("result"), Name("buf")))
        Return(Name("result")))
      Assign(Name("result"), Call(Name("decode_cyclic"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "decode_cyclic" <- ?_:Val ]
                       [ "result" <- str(seqConcat(decRes(CS, .IntSeq, .IntSeq, .IntSeq, 0), decBuf(CS, .IntSeq, 0))) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
