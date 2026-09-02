// spec.k — string_to_md5, TRAP-FREE (P162). One entry claim; the IfExp
// truthiness case-splits on the emptiness atom; the md5 value is the shared
// named trust (the tests/verification/md5hex template).
//
//   kompile verification.k --backend haskell --main-module STRING-TO-MD5-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module STRING-TO-MD5-SPEC

requires "verification.k"

module STRING-TO-MD5-SPEC
  imports STRING-TO-MD5-VERIFICATION

  claim
    <k>
      FuncDef("string_to_md5", Params("text"),
        Import("hashlib")
        Return(IfExp(Name("text"),
          Call(Attribute(Call(Attribute(Name("hashlib"), "md5"),
            (Call(Attribute(Name("text"), "encode"), Str("ascii")), .Exprs)), "hexdigest"), .Exprs),
          NoneVal)))
      Assign(Name("result"), Call(Name("string_to_md5"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "string_to_md5" <- ?_:Val ] [ "result" <- s2mRes(CS) ], parent(-1))
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
