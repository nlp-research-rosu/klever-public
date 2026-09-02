requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim [loop-invariant]:
    <k>
      solutionLoop ~> exec(Return(Name("result")) .Stmts)
      => .K
    </k>
    <input> N </input>
    <env>
      "factorial" |-> intVal(F:Int)
      "i"         |-> intVal(I)
      "n"         |-> intVal(N)
      "result"    |-> listVal(L:List)
      "total"     |-> intVal(T:Int)
      =>
      "factorial" |-> intVal(?_FOUT:Int)
      "i"         |-> intVal(?_IOUT:Int)
      "n"         |-> intVal(N)
      "result"    |-> listVal(expectedCompletion(I, N, F, T, L))
      "total"     |-> intVal(?_TOUT:Int)
    </env>
    <result> noResult => done(listVal(expectedCompletion(I, N, F, T, L))) </result>
    requires N >=Int 0 andBool I >=Int 1

  claim [main-correct]:
    <k> solution => .K </k>
    <input> N </input>
    <env>
      .Map
      =>
      "factorial" |-> intVal(?_FOUT:Int)
      "i"         |-> intVal(?_IOUT:Int)
      "n"         |-> intVal(N)
      "result"    |-> listVal(expected(N))
      "total"     |-> intVal(?_TOUT:Int)
    </env>
    <result> noResult => done(listVal(expected(N))) </result>
    requires N >=Int 0
endmodule
