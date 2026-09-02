requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module FRESH-VACUITY
  imports VERIFICATION

  // Fresh result mutation: the true rolling maximum for [2,1] is [2,2],
  // but this destination deliberately requires [2,1].
  claim <py>
          <k> VerifyRunList(
                 SOLUTION,
                 ListItem(2) ListItem(1))
            => ListVal(ListItem(2) ListItem(1)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
