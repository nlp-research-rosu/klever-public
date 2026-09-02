requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [inner]:
        <k> INNER-LOOP ~> REST => REST </k>
        <env>
          "count" |-> (C => C +Int digitSevens(X))
          "i" |-> _I
          "n" |-> _N
          "x" |-> (X => 0)
        </env>
    requires X >=Int 0

  claim [outer]:
        <k> OUTER-LOOP ~> REST => REST </k>
        <env>
          "count" |-> (C => C +Int fizzFrom(I, N))
          "i" |-> (I => N)
          "n" |-> N
          "x" |-> 0
        </env>
    requires I >=Int 0 andBool I <=Int N

  claim [entry]:
        <fizz>
          <k>
            Module(
              FuncDef("fizz_buzz", Params("n"),
                Assign(Name("count"), Int(0))
                Assign(Name("i"), Int(0))
                OUTER-LOOP
                Return(Name("count"))))
            => .K
          </k>
          <input> N </input>
          <env> .Map =>
            "count" |-> fizzFrom(0, N)
            "i" |-> fizzEnd(N)
            "n" |-> N
            "x" |-> 0
          </env>
          <result> 0 => fizzFrom(0, N) </result>
        </fizz>
endmodule

