requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module TARGET-PROMPT
  imports VERIFICATION
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
endmodule
