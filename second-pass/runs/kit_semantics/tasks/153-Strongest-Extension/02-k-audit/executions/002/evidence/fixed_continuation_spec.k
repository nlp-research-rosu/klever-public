requires "verification.k"

module FIXED-CONTINUATION-SPEC
  imports VERIFICATION-BASE

  // The observable assignment after the inner loop must remain and execute.
  claim [inner-continuation]:
    <k>
      #loop(
        str(iCons(65, .IntSeq)),
        Name("character"),
        INNER-BODY
      )
      ~> Assign(Name("strongest"), Str("after"))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "class_name" |-> str(iCons(67, .IntSeq))
        "extensions" |-> list(.ValSeq)
        "strongest" |-> (
          str(.IntSeq)
          => str(
               iCons(
                 97,
                 iCons(102, iCons(116, iCons(101, iCons(114, .IntSeq))))
               )
             )
        )
        "best_strength" |-> noneV
        "extension" |-> str(iCons(65, .IntSeq))
        "strength" |-> (0 => 1)
        "character" |-> (
          str(.IntSeq) => str(iCons(65, .IntSeq))
        ),
        parent(0)
      )
      ...
    </scopes>
endmodule
