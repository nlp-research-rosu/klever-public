requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module TARGET-EMPTY
  imports VERIFICATION
  claim <py>
          <k> VerifyRunList(SOLUTION, .List)
            => ListVal(.List) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
