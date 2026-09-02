requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  claim
    <k> verifyBF("Mercury", "Neptune") => .K </k>
    <planet1> "" => "Mercury" </planet1>
    <planet2> "" => "Neptune" </planet2>
    <result> noResult => tupleValue(.StringValues) </result>
endmodule
