requires "/tmp/audit-work/9-rolling-max/build/verification.k"

module TARGET-UNIVERSAL
  imports VERIFICATION
  claim <py>
          <k> VerifyRunList(SOLUTION, XS:List)
            => ListVal(#rollingMax(XS)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
