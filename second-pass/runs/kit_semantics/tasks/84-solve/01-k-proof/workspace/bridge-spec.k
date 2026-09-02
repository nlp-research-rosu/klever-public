requires "bridge-verification.k"

module BRIDGE-SPEC
  imports BRIDGE-VERIFICATION

  claim [mod10-horner]:
    <k>
      applyBin("%", D:Int +Int 10 *Int Q:Int, 10) ~> REST:K
      =>
      D ~> REST
    </k>
    requires 0 <=Int D andBool D <Int 10

  claim [floordiv10-horner]:
    <k>
      applyBin("//", D:Int +Int 10 *Int Q:Int, 10) ~> REST:K
      =>
      Q ~> REST
    </k>
    requires 0 <=Int D andBool D <Int 10

  claim [mod10-expanded]:
    <k>
      (((D:Int +Int 10 *Int Q:Int) %Int 10 +Int 10) %Int 10) ~> REST:K
      =>
      D ~> REST
    </k>
    requires 0 <=Int D andBool D <Int 10

  claim [quotient-expanded]:
    <k>
      ((D:Int +Int 10 *Int Q:Int -Int D) /Int 10) ~> REST:K
      =>
      Q ~> REST
    </k>
    requires 0 <=Int D andBool D <Int 10
endmodule
