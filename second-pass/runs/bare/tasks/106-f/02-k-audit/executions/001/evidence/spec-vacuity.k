requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Deliberately false: every returned list is required to have an extra 0.
  // Witness N=0 satisfies the precondition; real execution returns [].
  claim [main-false-extra-zero]:
    <k> solution => .K </k>
    <input> N </input>
    <env>
      .Map
      =>
      "factorial" |-> intVal(?_FOUT:Int)
      "i"         |-> intVal(?_IOUT:Int)
      "n"         |-> intVal(N)
      "result"    |-> listVal(expected(N) ListItem(0))
      "total"     |-> intVal(?_TOUT:Int)
    </env>
    <result> noResult => done(listVal(expected(N) ListItem(0))) </result>
    requires N >=Int 0
endmodule
