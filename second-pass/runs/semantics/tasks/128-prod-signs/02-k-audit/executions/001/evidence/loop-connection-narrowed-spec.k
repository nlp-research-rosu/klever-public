requires "bridge-free-verification.k"

module AUDIT-LOOP-CONNECTION-NARROWED-SPEC
  imports AUDIT-BRIDGE-FREE-VERIFICATION

  claim [loop-connection-narrowed]:
    <k>
      For(Name("value"), list(vCons(I:Int, VS:ValSeq)),
        If(Compare(Name("value"), CmpOp("<", Int(0))),
          Assign(Name("total"),
            BinOp("-", Name("total"), Name("value")))
          Assign(Name("sign"),
            BinOp("-", Int(0), Name("sign"))),
          Assign(Name("total"),
            BinOp("+", Name("total"), Name("value")))
          If(Compare(Name("value"), CmpOp("==", Int(0))),
            Assign(Name("sign"), Int(0)),
            .Stmts)))
      =>
      .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        M:Map
          => M
               [ "total" <- auditMagnitudeAcc(
                   vCons(I, VS), {M["total"]}:>Int) ]
               [ "sign" <- auditSignAcc(
                   vCons(I, VS), {M["sign"]}:>Int) ]
               [ "value" <- auditLastInt(vCons(I, VS)) ],
        P:Parent)
      ...
    </scopes>
    requires "total" in_keys(M) andBool "sign" in_keys(M)
     andBool notBool ("$cells" in_keys(M))
     andBool auditAllInts(VS)
endmodule
