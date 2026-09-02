// spec.k — check_dict_case on the UNIFIED semantics (src/). BOUNDED entry (no loop): the buggy
// early-break canonical inspects only keys[0]/keys[1], so the whole function unrolls to a finite
// case-split on the opaque key predicates (verification.k) and the result is `checkDictRes(KS)`. The
// entry store carries the builtins frame (-1) so the `str` type argument resolves. See ./PROOF.md.
//
//   kompile verification.k --backend haskell --main-module CHECK-DICT-CASE-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module CHECK-DICT-CASE-SPEC

requires "verification.k"

module CHECK-DICT-CASE-SPEC
  imports CHECK-DICT-CASE-VERIFICATION

  // ---- Entry claim — result = check_dict_case(dictV(KS, WS)) == checkDictRes(KS): the buggy 2-key
  // case-form over the ordered keys KS. WS (the values) is irrelevant. No domain constraint (keys are
  // arbitrary symbolic Vals; type/case is decided by the opaque key predicates).
  claim
    <k>
      FuncDef("check_dict_case", Params("d"),
        Assign(Name("keys"), Call(Name("list"), Call(Attribute(Name("d"), "keys"), .Exprs)))
        Assign(Name("n"), Call(Name("len"), Name("keys")))
        If(Compare(Name("n"), CmpOp("==", Int(0))), Return(Bool(false)), .Stmts)
        Assign(Name("k0"), Subscript(Name("keys"), Int(0)))
        If(UnaryOp("not", Call(Name("isinstance"), (Name("k0"), Name("str")))),
          Return(Bool(false)), .Stmts)
        If(Call(Attribute(Name("k0"), "isupper"), .Exprs),
          Assign(Name("first"), Str("upper")),
          If(Call(Attribute(Name("k0"), "islower"), .Exprs),
            Assign(Name("first"), Str("lower")),
            Return(Bool(false))))
        If(Compare(Name("n"), CmpOp("==", Int(1))), Return(Bool(true)), .Stmts)
        Assign(Name("k1"), Subscript(Name("keys"), Int(1)))
        If(UnaryOp("not", Call(Name("isinstance"), (Name("k1"), Name("str")))),
          Return(Bool(false)), .Stmts)
        If(Compare(Name("first"), CmpOp("==", Str("upper"))),
          Return(Call(Attribute(Name("k1"), "isupper"), .Exprs)),
          Return(Call(Attribute(Name("k1"), "islower"), .Exprs))))
      Assign(Name("result"), Call(Name("check_dict_case"), dictV(KS:ValSeq, WS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(.Map [ "check_dict_case" <- ?_:Val ] [ "result" <- checkDictRes(KS) ], parent(-1))
      -1 |-> builtinsScope
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
