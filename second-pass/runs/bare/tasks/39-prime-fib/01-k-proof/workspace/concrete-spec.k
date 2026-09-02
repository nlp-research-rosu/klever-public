requires "verification.k"

module CONCRETE-SPEC
  imports PRIME-FIB-PROGRAM

  // These claims execute the ordinary small-step semantics.  This module does
  // not import VERIFICATION, so the general loop-summary rule is unavailable.
  claim [concrete-1]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 1 "b" |-> 2 "c" |-> 2 "count" |-> 1
      "divisor" |-> 2 "n" |-> 1 "prime" |-> true
    </env>
    <n> 1 </n>
    <result> noResult => 2 </result>

  claim [concrete-2]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 2 "b" |-> 3 "c" |-> 3 "count" |-> 2
      "divisor" |-> 2 "n" |-> 2 "prime" |-> true
    </env>
    <n> 2 </n>
    <result> noResult => 3 </result>

  claim [concrete-3]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 3 "b" |-> 5 "c" |-> 5 "count" |-> 3
      "divisor" |-> 3 "n" |-> 3 "prime" |-> true
    </env>
    <n> 3 </n>
    <result> noResult => 5 </result>

  claim [concrete-4]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 8 "b" |-> 13 "c" |-> 13 "count" |-> 4
      "divisor" |-> 4 "n" |-> 4 "prime" |-> true
    </env>
    <n> 4 </n>
    <result> noResult => 13 </result>

  claim [concrete-5]:
    <k> primeFibProgram => .K </k>
    <env> .Map =>
      "a" |-> 55 "b" |-> 89 "c" |-> 89 "count" |-> 5
      "divisor" |-> 10 "n" |-> 5 "prime" |-> true
    </env>
    <n> 5 </n>
    <result> noResult => 89 </result>
endmodule
