requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional correctness for every semantic list of integers.
  claim <py>
          <k> VerifyRunList(SOLUTION, XS:List)
            => ListVal(#rollingMax(XS)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  // Boundary case required by the contract.
  claim <py>
          <k> VerifyRunList(SOLUTION, .List)
            => ListVal(.List) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  // Prompt example.
  claim <py>
          <k> VerifyRunList(SOLUTION,
               ListItem(1) ListItem(2) ListItem(3) ListItem(2)
               ListItem(3) ListItem(4) ListItem(2))
            => ListVal(ListItem(1) ListItem(2) ListItem(3)
                       ListItem(3) ListItem(3) ListItem(4) ListItem(4)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  // Negative values rule out an incorrect zero-initialized maximum.
  claim <py>
          <k> VerifyRunList(SOLUTION,
               ListItem(-5) ListItem(-9) ListItem(-3) ListItem(-4))
            => ListVal(ListItem(-5) ListItem(-5) ListItem(-3) ListItem(-3)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
