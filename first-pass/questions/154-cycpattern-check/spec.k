// spec.k — cycpattern_check, TRAP-FREE (P154). Bool-accumulator scan (`found`):
// the inner/outer loops fold `found` via guarded case-split on the raw
// window-equality atom (the is_prime primeAcc rung, nested — see is-prime-rung /
// nested-loop-rung). No early return, so ONE invariant per loop (not competing
// FOUND/NOT-FOUND claims) + entry over the single FuncDef.
//
//   kompile verification.k --backend haskell --main-module CYCPATTERN-CHECK-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CYCPATTERN-CHECK-SPEC

requires "verification.k"

module CYCPATTERN-CHECK-SPEC
  imports CYCPATTERN-CHECK-VERIFICATION

  // ---- inner j-loop invariant (circularity): found := foundJ(...) over [J, JHI)
  claim
    <k>
      #loop(rangeObj(J:Int, JHI:Int, 1), Name("j"),
        If(Compare(
            Subscript(Name("a"), Slice(Name("i"), BinOp("+", Name("i"), Name("l")), NoBound)),
            CmpOp("==",
              Subscript(Name("pat"), Slice(Name("j"), BinOp("+", Name("j"), Name("l")), NoBound)))),
          Assign(Name("found"), Bool(true)),
          .Stmts))
    => .K ... </k>
    <env> EL:Int </env>
    <scopes>
      ... EL |-> ( scope(.Map [ "a" <- str(AS:IntSeq) ] [ "b" <- str(BS:IntSeq) ] [ "l" <- L:Int ]
                             [ "pat" <- str(PS:IntSeq) ] [ "found" <- F:Bool ] [ "i" <- IV:Int ] [ "j" <- _:Val ], PR:Parent)
               => scope(.Map [ "a" <- str(AS) ] [ "b" <- str(BS) ] [ "l" <- L ]
                             [ "pat" <- str(PS) ] [ "found" <- foundJ(AS, PS, IV, J, JHI, L, F) ] [ "i" <- IV ] [ "j" <- ?_:Val ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires J >=Int 0 andBool IV >=Int 0 andBool L >=Int 0
     andBool IV +Int L <=Int isLen(AS)
     andBool JHI <=Int isLen(PS) -Int L +Int 1
    [all-path]

  // ---- outer i-loop invariant (circularity): found := foundI(...) over [I, IHI).
  // The body is the inner For; the inner invariant folds it to foundJ per step.
  claim
    <k>
      #loop(rangeObj(I:Int, IHI:Int, 1), Name("i"),
        For(Name("j"), Call(Name("range"), BinOp("+", Name("l"), Int(1))),
          If(Compare(
              Subscript(Name("a"), Slice(Name("i"), BinOp("+", Name("i"), Name("l")), NoBound)),
              CmpOp("==",
                Subscript(Name("pat"), Slice(Name("j"), BinOp("+", Name("j"), Name("l")), NoBound)))),
            Assign(Name("found"), Bool(true)),
            .Stmts)))
    => .K ... </k>
    <env> EL:Int </env>
    <scopes>
      ... -1 |-> builtinsScope GLB |-> scope(.Map [ "cycpattern_check" <- _:Val ], parent(-1)) EL |-> (
             scope(.Map [ "a" <- str(AS:IntSeq) ] [ "b" <- str(BS:IntSeq) ] [ "l" <- L:Int ]
                        [ "pat" <- str(PS:IntSeq) ] [ "found" <- F:Bool ] [ "i" <- _:Val ] [ "j" <- _:Val ], parent(GLB:Int))
          => scope(.Map [ "a" <- str(AS) ] [ "b" <- str(BS) ] [ "l" <- L ]
                        [ "pat" <- str(PS) ] [ "found" <- foundI(AS, PS, I, IHI, L +Int 1, L, F) ] [ "i" <- ?_:Val ] [ "j" <- ?_:Val ], parent(GLB)) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool L >=Int 0
     andBool IHI <=Int isLen(AS) -Int L +Int 1
     andBool isLen(PS) >=Int L +Int L
    [all-path]

  // ---- entry: result == cycRes(AS, BS)
  claim
    <k>
      FuncDef("cycpattern_check", Params("a", "b"),
        Assign(Name("l"), Call(Name("len"), Name("b")))
        Assign(Name("pat"), BinOp("+", Name("b"), Name("b")))
        Assign(Name("found"), Bool(false))
        Assign(Name("i"), Int(0))
        Assign(Name("j"), Int(0))
        For(Name("i"), Call(Name("range"),
            BinOp("+", BinOp("-", Call(Name("len"), Name("a")), Name("l")), Int(1))),
          For(Name("j"), Call(Name("range"), BinOp("+", Name("l"), Int(1))),
          If(Compare(
              Subscript(Name("a"), Slice(Name("i"), BinOp("+", Name("i"), Name("l")), NoBound)),
              CmpOp("==",
                Subscript(Name("pat"), Slice(Name("j"), BinOp("+", Name("j"), Name("l")), NoBound)))),
            Assign(Name("found"), Bool(true)),
            .Stmts)))
        Return(Name("found")))
      Assign(Name("result"), Call(Name("cycpattern_check"), (str(AS:IntSeq), str(BS:IntSeq))))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "cycpattern_check" <- ?_:Val ] [ "result" <- cycRes(AS, BS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
