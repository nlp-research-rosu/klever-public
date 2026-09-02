requires "verification.k"

module AUDIT-SPEC-LOOP-EMPTY
  imports INTERSPERSE-VERIFICATION

  claim
    <k>
      #loop(
        list(.ValSeq), Name("number"),
        If(Name("result"),
          Expr(Call(Attribute(Name("result"), "append"), Name("delimeter"))),
          .Stmts)
        Expr(Call(Attribute(Name("result"), "append"), Name("number"))))
      ~> CONT
      => CONT
    </k>
    <env> L </env>
    <scopes>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap> HEAP H |-> list(.ValSeq) </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))
endmodule
