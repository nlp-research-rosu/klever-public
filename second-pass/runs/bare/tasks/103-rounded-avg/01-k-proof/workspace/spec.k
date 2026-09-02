requires "verification.k"

module SPEC
  imports VERIFICATION

  // Invalid interval.
  claim [reversed]:
    <py>
      <k> boot(roundedAvgProgram, N, M) => .K </k>
      <env> .Map => ("n" |-> intVal(N)) ("m" |-> intVal(M)) </env>
      <result> noResult => result(intVal(-1)) </result>
    </py>
    requires N >Int 0 andBool M >Int 0 andBool N >Int M

  // Valid intervals with an integral midpoint.
  claim [integral-midpoint]:
    <py>
      <k> boot(roundedAvgProgram, N, M) => .K </k>
      <env> .Map => ("n" |-> intVal(N)) ("m" |-> intVal(M)) </env>
      <result> noResult => result(binVal((N +Int M) /Int 2)) </result>
    </py>
    requires N >Int 0 andBool M >Int 0
     andBool N <=Int M
     andBool (N +Int M) %Int 2 ==Int 0

  // Half-integral midpoint whose lower neighbor is even: ties round down.
  claim [half-even-down]:
    <py>
      <k> boot(roundedAvgProgram, N, M) => .K </k>
      <env> .Map => ("n" |-> intVal(N)) ("m" |-> intVal(M)) </env>
      <result> noResult => result(binVal((N +Int M) /Int 2)) </result>
    </py>
    requires N >Int 0 andBool M >Int 0
     andBool N <=Int M
     andBool (N +Int M) %Int 2 ==Int 1
     andBool ((N +Int M) /Int 2) %Int 2 ==Int 0

  // Half-integral midpoint whose lower neighbor is odd: ties round up.
  claim [half-even-up]:
    <py>
      <k> boot(roundedAvgProgram, N, M) => .K </k>
      <env> .Map => ("n" |-> intVal(N)) ("m" |-> intVal(M)) </env>
      <result> noResult
        => result(binVal(((N +Int M) /Int 2) +Int 1)) </result>
    </py>
    requires N >Int 0 andBool M >Int 0
     andBool N <=Int M
     andBool (N +Int M) %Int 2 ==Int 1
     andBool ((N +Int M) /Int 2) %Int 2 ==Int 1

  // The prompt's examples are also executable proof obligations.
  claim [example-1-5]:
    <py>
      <k> boot(roundedAvgProgram, 1, 5) => .K </k>
      <env> .Map => ("n" |-> intVal(1)) ("m" |-> intVal(5)) </env>
      <result> noResult => result(binVal(3)) </result>
    </py>

  claim [example-7-5]:
    <py>
      <k> boot(roundedAvgProgram, 7, 5) => .K </k>
      <env> .Map => ("n" |-> intVal(7)) ("m" |-> intVal(5)) </env>
      <result> noResult => result(intVal(-1)) </result>
    </py>

  claim [example-10-20]:
    <py>
      <k> boot(roundedAvgProgram, 10, 20) => .K </k>
      <env> .Map => ("n" |-> intVal(10)) ("m" |-> intVal(20)) </env>
      <result> noResult => result(binVal(15)) </result>
    </py>

  claim [example-20-33]:
    <py>
      <k> boot(roundedAvgProgram, 20, 33) => .K </k>
      <env> .Map => ("n" |-> intVal(20)) ("m" |-> intVal(33)) </env>
      <result> noResult => result(binVal(26)) </result>
    </py>

  claim [render-3]:
    <py>
      <k> renderBinary(binVal(3)) => "0b11" </k>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  claim [render-15]:
    <py>
      <k> renderBinary(binVal(15)) => "0b1111" </k>
      <env> .Map </env>
      <result> noResult </result>
    </py>

  claim [render-26]:
    <py>
      <k> renderBinary(binVal(26)) => "0b11010" </k>
      <env> .Map </env>
      <result> noResult </result>
    </py>
endmodule
