requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module TARGET-NEGATIVE
  imports VERIFICATION
  claim <py>
          <k> VerifyRunList(SOLUTION,
               ListItem(-5) ListItem(-9) ListItem(-3) ListItem(-4))
            => ListVal(ListItem(-5) ListItem(-5) ListItem(-3) ListItem(-3)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
