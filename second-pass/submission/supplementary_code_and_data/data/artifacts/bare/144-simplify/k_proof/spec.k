requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [simplify-general]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify",
            strVal(Int2String(A) +String "/" +String Int2String(B)),
            strVal(Int2String(C) +String "/" +String Int2String(D)))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult =>
        result(boolVal(((A *Int C) %Int (B *Int D)) ==Int 0))
      </result>
    </simplify>
    requires A >Int 0 andBool B >Int 0
     andBool C >Int 0 andBool D >Int 0

  claim [example-true]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify", strVal("1/5"), strVal("5/1"))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult => result(boolVal(true)) </result>
    </simplify>

  claim [example-false-one]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify", strVal("1/6"), strVal("2/1"))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult => result(boolVal(false)) </result>
    </simplify>

  claim [example-false-two]:
    <simplify>
      <k> simplifyProgram ~>
          invoke("simplify", strVal("7/10"), strVal("10/2"))
          => .K </k>
      <functions> .Map => ?FS:Map </functions>
      <env> .Map => ?RHO:Map </env>
      <result> noResult => result(boolVal(false)) </result>
    </simplify>
endmodule
