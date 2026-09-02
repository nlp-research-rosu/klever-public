requires "verification.k"

module AUDIT-SPEC-LOOP-FIRST
  imports INTERSPERSE-VERIFICATION

  claim
    <k>
      #loop(
        list(vCons(V, REST)), Name("number"),
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
      =>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "number" |-> lastNumber(V, REST)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap>
      HEAP H |-> list(.ValSeq)
      => HEAP H |-> list(intersperseAcc(.ValSeq, vCons(V, REST), D))
    </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))
endmodule
