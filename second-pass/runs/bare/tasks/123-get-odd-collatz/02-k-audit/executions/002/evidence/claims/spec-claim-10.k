requires "verification.k"

module SPEC-CLAIM-10
  imports VERIFICATION

  claim [odd-step]:
    <python>
      <k> exec(collatzBranch .Stmts) => .K </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env>
        ("n" |-> vi(2 *Int M +Int 1) "odds" |-> vl(OS))
        => ("n" |-> vi(6 *Int M +Int 4)
            "odds" |-> vl(appendInts(OS, (2 *Int M +Int 1) :: .Ints)))
      </env>
      <result> noResult </result>
    </python>
    requires M >Int 0

  // Independent checks on the observers used to state the output contract.
endmodule
