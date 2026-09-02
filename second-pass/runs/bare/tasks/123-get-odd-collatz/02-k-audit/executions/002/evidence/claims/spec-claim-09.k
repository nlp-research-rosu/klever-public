requires "verification.k"

module SPEC-CLAIM-09
  imports VERIFICATION

  claim [even-step]:
    <python>
      <k> exec(collatzBranch .Stmts) => .K </k>
      <input> 0 </input>
      <functions> .Map </functions>
      <env>
        ("n" |-> vi(2 *Int M) "odds" |-> vl(OS))
        => ("n" |-> vi(M) "odds" |-> vl(OS))
      </env>
      <result> noResult </result>
    </python>
    requires M >Int 0

  // Symbolic branch correctness for every odd term greater than one.
endmodule
