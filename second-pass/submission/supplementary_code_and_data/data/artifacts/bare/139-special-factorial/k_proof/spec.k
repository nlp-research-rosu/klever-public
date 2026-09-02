requires "semantic.k"

module SPEC
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

  claim [program-correct]:
    <k> init(solutionProgram, N) => .K </k>
    <functions> .Map => solutionFunctions </functions>
    <env> .Map </env>
    <stack> .CallStack </stack>
    <result> noResult => result(specialFactorialSpec(N)) </result>
    requires N >Int 0
endmodule
