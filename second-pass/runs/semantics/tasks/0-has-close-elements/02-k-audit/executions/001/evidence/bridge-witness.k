requires "verification.k"

// Same closure invocation and Float/List input in both claims.  The closure
// body deliberately returns false.  The submitted generalized bridge ignores
// that body and returns closeSkip(...).  The symbolic contrast is paired in
// REVIEW.md with the satisfying ground instance A=1.0, T=0.1, for which the
// concrete meaning of closeSkip(A,[A],T,0,0) is true.
module WITNESS-FIXED-CLOSURE-FALSE
  imports VERIFICATION-WITH-INNER

  claim <k> #applyK(toCall(closureVal(
                       ("number", "numbers", "threshold", "start"),
                       Return(Bool(false)) .Stmts,
                       0)),
                     (A:Float,
                      list(fCons(A, fCons(A, .FloatSeq))),
                      T:Float, 1, .Vals)) ~> #proofDone
         => false ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(.Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

module WITNESS-BRIDGED-CLOSURE-SUMMARY
  imports VERIFICATION-WITH-HELPER

  claim <k> #applyK(toCall(closureVal(
                       ("number", "numbers", "threshold", "start"),
                       Return(Bool(false)) .Stmts,
                       0)),
                     (A:Float,
                      list(fCons(A, fCons(A, .FloatSeq))),
                      T:Float, 1, .Vals)) ~> #proofDone
         => closeSkip(A, fCons(A, fCons(A, .FloatSeq)),
                      T, 0, 1) ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(.Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

// The direct Call bridge does not check lookup/binding.  In this state the
// current local scope deliberately shadows is_close_to_any with a closure that
// returns false.
module WITNESS-FIXED-SHADOWED-HELPER-FALSE
  imports VERIFICATION-WITH-INNER

  claim <k> Call(Name("is_close_to_any"),
                  Name("number"), Name("numbers"), Name("threshold"),
                  Name("start"), .Exprs) ~> #proofDone
         => false ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0 |-> solutionScope()
          1 |-> scope(.Map
                      [ "number" <- A:Float ]
                      [ "numbers" <-
                        list(fCons(A, fCons(A, .FloatSeq))) ]
                      [ "threshold" <- T:Float ]
                      [ "start" <- 1 ]
                      [ "is_close_to_any" <-
                        closureVal(("number", "numbers", "threshold", "start"),
                                   Return(Bool(false)) .Stmts, 0) ],
                     parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

module WITNESS-BRIDGED-SHADOWED-HELPER-SUMMARY
  imports VERIFICATION-WITH-HELPER

  claim <k> Call(Name("is_close_to_any"),
                  Name("number"), Name("numbers"), Name("threshold"),
                  Name("start"), .Exprs) ~> #proofDone
         => closeSkip(A, fCons(A, fCons(A, .FloatSeq)), T, 0, 1)
              ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0 |-> solutionScope()
          1 |-> scope(.Map
                      [ "number" <- A:Float ]
                      [ "numbers" <-
                        list(fCons(A, fCons(A, .FloatSeq))) ]
                      [ "threshold" <- T:Float ]
                      [ "start" <- 1 ]
                      [ "is_close_to_any" <-
                        closureVal(("number", "numbers", "threshold", "start"),
                                   Return(Bool(false)) .Stmts, 0) ],
                     parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

// The public-entry Call bridge likewise does not check the selected binding.
module WITNESS-FIXED-SHADOWED-ENTRY-FALSE
  imports VERIFICATION-WITH-OUTER

  claim <k> Call(Name("has_close_elements"),
                  list(ALL:FloatSeq), T:Float, .Exprs) ~> #proofDone
         => false ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map
                      [ "has_close_elements" <-
                        closureVal(("numbers", "threshold"),
                                   Return(Bool(false)) .Stmts, 0) ],
                     parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule

module WITNESS-BRIDGED-SHADOWED-ENTRY-SUMMARY
  imports VERIFICATION-WITH-ENTRY

  claim <k> Call(Name("has_close_elements"),
                  list(ALL:FloatSeq), T:Float, .Exprs) ~> #proofDone
         => hasPairs(ALL, ALL, T, 1) ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map
                      [ "has_close_elements" <-
                        closureVal(("numbers", "threshold"),
                                   Return(Bool(false)) .Stmts, 0) ],
                     parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule

// The helper-loop bridge matches any loop body and any continuation.  Here the
// body is empty, so fixed execution cannot set found to the proximity summary.
module WITNESS-FIXED-EMPTY-INNER-LOOP-FALSE
  imports VERIFICATION-BASE

  claim <k> #applyK(toCall(closureVal(
                       ("number", "numbers", "threshold", "start"),
                       Assign(Name("found"), Bool(false))
                       Assign(Name("index"), Int(0))
                       Assign(Name("other"), Name("number"))
                       For(Name("other"), Name("numbers"), .Stmts)
                       Assign(Name("index"), Int(0))
                       Assign(Name("other"), Name("number"))
                       Return(Name("found"))
                       .Stmts,
                       0)),
                     (A:Float,
                      list(fCons(A, fCons(A, .FloatSeq))),
                      T:Float, 1, .Vals)) ~> #proofDone
         => false ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(.Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

module WITNESS-BRIDGED-EMPTY-INNER-LOOP-SUMMARY
  imports VERIFICATION-WITH-INNER

  claim <k> #applyK(toCall(closureVal(
                       ("number", "numbers", "threshold", "start"),
                       Assign(Name("found"), Bool(false))
                       Assign(Name("index"), Int(0))
                       Assign(Name("other"), Name("number"))
                       For(Name("other"), Name("numbers"), .Stmts)
                       Assign(Name("index"), Int(0))
                       Assign(Name("other"), Name("number"))
                       Return(Name("found"))
                       .Stmts,
                       0)),
                     (A:Float,
                      list(fCons(A, fCons(A, .FloatSeq))),
                      T:Float, 1, .Vals)) ~> #proofDone
         => closeSkip(A, fCons(A, fCons(A, .FloatSeq)), T, 0, 1)
              ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(.Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

// The outer-loop bridge has the same arbitrary-body/context generalization.
module WITNESS-FIXED-EMPTY-OUTER-LOOP-FALSE
  imports VERIFICATION-WITH-HELPER

  claim <k> #applyK(toCall(closureVal(
                       ("numbers", "threshold"),
                       Assign(Name("found"), Bool(false))
                       Assign(Name("start"), Int(1))
                       Assign(Name("number"), Name("threshold"))
                       For(Name("number"), Name("numbers"), .Stmts)
                       Assign(Name("start"), Int(1))
                       Assign(Name("number"), Name("threshold"))
                       Return(Name("found"))
                       .Stmts,
                       0)),
                     (list(fCons(A:Float,
                                 fCons(A, .FloatSeq))),
                      T:Float, .Vals)) ~> #proofDone
         => false ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0  |-> solutionScope()
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule

module WITNESS-BRIDGED-EMPTY-OUTER-LOOP-SUMMARY
  imports VERIFICATION-WITH-OUTER

  claim <k> #applyK(toCall(closureVal(
                       ("numbers", "threshold"),
                       Assign(Name("found"), Bool(false))
                       Assign(Name("start"), Int(1))
                       Assign(Name("number"), Name("threshold"))
                       For(Name("number"), Name("numbers"), .Stmts)
                       Assign(Name("start"), Int(1))
                       Assign(Name("number"), Name("threshold"))
                       Return(Name("found"))
                       .Stmts,
                       0)),
                     (list(fCons(A:Float,
                                 fCons(A, .FloatSeq))),
                      T:Float, .Vals)) ~> #proofDone
         => hasPairs(fCons(A, fCons(A, .FloatSeq)),
                     fCons(A, fCons(A, .FloatSeq)),
                     T, 1) ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0  |-> solutionScope()
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule
