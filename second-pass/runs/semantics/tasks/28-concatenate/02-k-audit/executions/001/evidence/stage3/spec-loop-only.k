requires "/tmp/audit-work/28-concatenate/verification.k"

module AUDIT-CONCATENATE-SPEC-LOOP
  imports CONCATENATE-VERIFICATION

  claim [audit-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("string"),
        concatenateLoopBody
      )
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        ("result" |-> str(A:IntSeq)
         "string" |-> OLD_STRING:Val
         "strings" |-> ARGUMENT:Val)
        =>
        ("result" |-> str(concatenateValues(A, VS))
         "string" |-> finalLoopValue(OLD_STRING, VS)
         "strings" |-> ARGUMENT),
        parent(0)
      )
    </scopes>
    requires allStringValues(VS)
endmodule
