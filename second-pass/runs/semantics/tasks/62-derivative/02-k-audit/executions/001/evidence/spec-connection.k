requires "verification-connection.k"

module SPEC-CONNECTION
  imports VERIFICATION-CONNECTION

  // Bridge-free characterization of the supplied eager enumVS function.
  // This module does not import candidate verification.k or enumIntSeq.
  claim
    <k>
      enumVS(connectionAsValSeq(VS:IntVals), N:Int)
      =>
      connectionEnum(VS, N)
    </k>
    [label(eager-enum-characterization)]
endmodule
