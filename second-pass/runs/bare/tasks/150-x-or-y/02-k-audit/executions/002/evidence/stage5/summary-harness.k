requires "verification.k"

module SUMMARY-HARNESS
  imports MPY-VERIFICATION

  syntax Program ::= "Summary" "(" Int ")"
                   | "SummaryFrom" "(" Int "," Int ")"

  rule <k> Summary(N) => .K </k>
       <result> .K => chooseVal(isPrime(N), 1, 0) </result>

  rule <k> SummaryFrom(N, D) => .K </k>
       <result> .K => chooseVal(primeFrom(N, D), 1, 0) </result>
endmodule
