requires "semantic.k"

module SPEC
  imports SEMANTIC

  // The recurrence model used below has this definitional form on n >= 4.
  // This small claim makes the link used when composing initialization with
  // loop-correct explicit in the proof suite.
  claim [fib4-spec-link]:
    <fib4>
      <k> .K </k>
      <arg> N </arg>
      <env> _M:Map </env>
      <result>
        result(fib4Spec(N)) => result(advanceTo(0, 0, 2, 0, 4, N))
      </result>
    </fib4>
    requires N >=Int 4

  claim [loop-correct]:
    <fib4>
      <k>
        exec(
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            Assign(Name("e"),
              BinOp("+", BinOp("+", BinOp("+", Name("a"), Name("b")),
                                        Name("c")), Name("d")))
            Assign(Name("a"), Name("b"))
            Assign(Name("b"), Name("c"))
            Assign(Name("c"), Name("d"))
            Assign(Name("d"), Name("e"))
            Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
          Return(Name("d")))
        => .K
      </k>
      <arg> N </arg>
      <env>
          "n" |-> N
          "a" |-> A
          "b" |-> B
          "c" |-> C
          "d" |-> D
          "e" |-> _E
          "i" |-> I
        => ?_FINAL:Map
      </env>
      <result>
        noResult => result(advanceTo(A, B, C, D, I, N))
      </result>
    </fib4>
    requires N >=Int 4 andBool I >=Int 4
         andBool (I <=Int N orBool I ==Int N +Int 1)
    [circularity]

  // The finite initialization half of the n >= 4 proof.  Its target is exactly
  // the A=0,B=0,C=2,D=0,I=4 instance of loop-correct above.  Thus these two
  // reachability claims compose to result(fib4Spec(N)).
  claim [fib4-inductive-init]:
    <fib4>
      <k>
        solutionProgram
        => exec(
             While(Compare(Name("i"), CmpOp("<=", Name("n"))),
               Assign(Name("e"),
                 BinOp("+", BinOp("+", BinOp("+", Name("a"), Name("b")),
                                           Name("c")), Name("d")))
               Assign(Name("a"), Name("b"))
               Assign(Name("b"), Name("c"))
               Assign(Name("c"), Name("d"))
               Assign(Name("d"), Name("e"))
               Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
             Return(Name("d")))
      </k>
      <arg> N </arg>
      <env>
        .Map
        => "n" |-> N
           "a" |-> 0
           "b" |-> 0
           "c" |-> 2
           "d" |-> 0
           "e" |-> 0
           "i" |-> 4
      </env>
      <result> noResult </result>
    </fib4>
    requires N >=Int 4

  claim [fib4-base-0]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 0 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(fib4Spec(0)) </result>
    </fib4>

  claim [fib4-base-1]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 1 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(fib4Spec(1)) </result>
    </fib4>

  claim [fib4-base-2]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 2 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(fib4Spec(2)) </result>
    </fib4>

  claim [fib4-base-3]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 3 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(fib4Spec(3)) </result>
    </fib4>

  claim [fib4-seven]:
    <fib4>
      <k> solutionProgram => .K </k>
      <arg> 7 </arg>
      <env> .Map => ?_FINAL:Map </env>
      <result> noResult => result(14) </result>
    </fib4>
endmodule
