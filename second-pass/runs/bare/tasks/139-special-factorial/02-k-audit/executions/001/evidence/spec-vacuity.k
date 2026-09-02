requires "semantic.k"

module SPEC-VACUITY
  imports MPY

  claim [factorial-call]:
    <k> eval(Call(Name("factorial"), Name("n"))) ~> KONT:K
      => returned("factorial", factorialSpec(N), KONT) </k>
    <functions> solutionFunctions </functions>
    <env> "n" |-> N _ENV:Map </env>
    <stack> _STACK:CallStack </stack>
    <result> _R:Result </result>
    requires N >Int 0

  claim [special-factorial-call]:
    <k> eval(Call(Name("special_factorial"), Name("n"))) ~> KONT:K
      => returned("special_factorial", specialFactorialSpec(N), KONT) </k>
    <functions> solutionFunctions </functions>
    <env> "n" |-> N _ENV:Map </env>
    <stack> _STACK:CallStack </stack>
    <result> _R:Result </result>
    requires N >Int 0

  // Fresh false mutation: the real result is specialFactorialSpec(N), not +1.
  // N = 1 is a satisfying witness: execution returns 1, while this asks for 2.
  claim [program-correct-off-by-one]:
    <k> init(solutionProgram, N) => .K </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
    <stack> .CallStack </stack>
    <result>
      noResult => result(specialFactorialSpec(N) +Int 1)
    </result>
    requires N >Int 0
endmodule
