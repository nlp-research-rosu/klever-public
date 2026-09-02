requires "semantic.k"

module SPEC-VACUITY-AUDIT
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

  // Deliberately false mutation: the original YES precondition is unchanged,
  // but the result-constraining postcondition is changed from "YES" to "NO".
  // Ground witness: L1=Cons(0,Nil), L2=Cons(1,Nil).
  claim [exchange-yes-wrong-result]:
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
endmodule
