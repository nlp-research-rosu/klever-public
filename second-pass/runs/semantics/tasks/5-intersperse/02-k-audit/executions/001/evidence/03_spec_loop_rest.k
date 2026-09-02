requires "verification.k"

module AUDIT-SPEC-LOOP-REST
  imports INTERSPERSE-VERIFICATION

  claim
    <k>
      #loop(
        list(REST), Name("number"),
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
        "number" |-> OLD
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
      =>
      SCOPES
      L |-> scope(
        "numbers" |-> list(NUMBERS)
        "number" |-> lastNumber(OLD, REST)
        "result" |-> ref(H)
        "delimeter" |-> D,
        PARENT)
    </scopes>
    <heap>
      HEAP H |-> list(vCons(A, AS))
      => HEAP H |-> list(intersperseAcc(vCons(A, AS), REST, D))
    </heap>
    requires notBool (L in_keys(SCOPES))
     andBool notBool (H in_keys(HEAP))
endmodule
