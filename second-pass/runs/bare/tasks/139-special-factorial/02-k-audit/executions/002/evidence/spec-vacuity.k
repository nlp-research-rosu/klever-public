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

  // Deliberately false at every satisfying input, including N = 1:
  // the real result is specialFactorialSpec(N), not that value plus one.
  claim [program-off-by-one]:
    <k> init(solutionProgram, N) => .K </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
    <stack> .CallStack </stack>
    <result>
      noResult => result(specialFactorialSpec(N) +Int 1)
    </result>
    requires N >Int 0
endmodule
