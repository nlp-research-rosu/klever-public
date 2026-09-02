requires "verification.k"

module SPEC
  imports VERIFICATION

  // Circularity for the one source while-loop. At a loop head, the heap list
  // is an arbitrary prefix P. On exit it is P extended with values I through N.
  claim [tri-loop]:
    <k> #while(triLoopCondition, triLoopBody) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope("i" |-> (I:Int => N +Int 1)
                       "n" |-> N:Int
                       "values" |-> ref(H:Int),
                       parent(0))
      ...
    </scopes>
    <heap>
      ... H |-> (list(P:ValSeq) => list(triComplete(P, I, N))) ...
    </heap>
    requires N >=Int 0
     andBool I >=Int 0
     andBool I <=Int N +Int 1

  // Exact entry: load the translated definition into an empty module scope,
  // resolve its binding normally, call it, and observe the returned heap list.
  claim [tri-entry]:
    <k> #loadAll(Module(triDefinition))
         ~> Call(Name("tri"), Int(N:Int))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "tri" |-> closureVal(
                ("n", .ParamNames),
                triFunctionBody,
                0),
              parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(triResult(N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0

  // The proof-side sequence definition matches every clause of the prompt.
  claim [tri-at-zero]:
    <k> triValue(0) => 1 </k>

  claim [tri-at-one]:
    <k> triValue(1) => 3 </k>

  claim [tri-at-even]:
    <k> triValue(N:Int) => 1 +Int N /Int 2 </k>
    requires N >=Int 2 andBool pyMod(N, 2) ==Int 0

  claim [tri-at-odd-recurrence]:
    <k> triValue(N:Int)
      => triValue(N -Int 1)
         +Int triValue(N -Int 2)
         +Int triValue(N +Int 1)
    </k>
    requires N >=Int 3 andBool pyMod(N, 2) ==Int 1
endmodule
