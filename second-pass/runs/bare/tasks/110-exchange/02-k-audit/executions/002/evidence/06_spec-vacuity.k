requires "semantic.k"

module SPEC-VACUITY
  imports SEMANTIC

  claim [loop-counts-even]:
    <exchange>
      <k> loop("value", L, countBody) ~> CONT => CONT </k>
      <env>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> N
        "value" |-> OLD
      =>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> (N +Int countEven(L))
        "value" |-> lastValue(L, OLD)
      </env>
      <result> noResult </result>
    </exchange>

  claim [exchange-yes-false]:
    <exchange>
      <k> init(solutionProgram, L1, L2) => .K </k>
      <env> .Map
      =>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> (countEven(L1) +Int countEven(L2))
        "value" |-> lastValue(L2, lastValue(L1, 0))
      </env>
      <result> noResult => "NO" </result>
    </exchange>
    requires countEven(L1) +Int countEven(L2) >=Int length(L1)

  claim [exchange-no]:
    <exchange>
      <k> init(solutionProgram, L1, L2) => .K </k>
      <env> .Map
      =>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> (countEven(L1) +Int countEven(L2))
        "value" |-> lastValue(L2, lastValue(L1, 0))
      </env>
      <result> noResult => "NO" </result>
    </exchange>
    requires countEven(L1) +Int countEven(L2) <Int length(L1)
endmodule
