requires "/tmp/audit-work/source/verification.k"

module BRIDGE-CONTEXT-BASE
  imports VERIFICATION-BASE

  claim [empty-observable-continuation]:
    <k>
      #iterNext(list(intListVals(.IntList)))
      ~> #memberCont(99)
      ~> #notB
      => true
    </k>

  claim [cons-observable-continuation]:
    <k>
      #iterNext(list(intListVals(intCons(7, .IntList))))
      ~> #memberCont(7)
      ~> #notB
      => false
    </k>
endmodule

module BRIDGE-CONTEXT-EXTENDED
  imports VERIFICATION

  claim [empty-observable-continuation]:
    <k>
      #iterNext(list(intListVals(.IntList)))
      ~> #memberCont(99)
      ~> #notB
      => true
    </k>

  claim [cons-observable-continuation]:
    <k>
      #iterNext(list(intListVals(intCons(7, .IntList))))
      ~> #memberCont(7)
      ~> #notB
      => false
    </k>
endmodule
