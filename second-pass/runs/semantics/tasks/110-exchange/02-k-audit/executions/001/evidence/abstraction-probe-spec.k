requires "verification.k"

module EXCHANGE-ABSTRACTION-PROBE-SPEC
  imports EXCHANGE-VERIFICATION

  // The empty iterator extension preserves and executes a trailing observable
  // continuation rather than swallowing control.
  claim [empty-iterator-continuation]:
    <k>
      #iterNext(list(intVals(.IntSeq)))
      ~> #loopStep(Name("x"), .Stmts)
      ~> Assign(Name("x"), Int(7))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(("x" |-> 0), root)
      =>
      0 |-> scope(("x" |-> 7), root)
    </scopes>

  // intVals is faithful for the operation used by the program (iteration), but
  // it is not a globally interchangeable ValSeq representation: the fixed
  // truthiness rule recognizes only the native .ValSeq empty constructor.
  claim [native-empty-is-false]:
    <k> truthy(list(.ValSeq)) => false </k>

  claim [abstract-empty-is-true]:
    <k> truthy(list(intVals(.IntSeq))) => true </k>
endmodule
