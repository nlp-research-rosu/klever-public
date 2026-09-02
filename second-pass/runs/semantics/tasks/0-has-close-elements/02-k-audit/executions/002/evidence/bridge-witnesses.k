requires "verification.k"

// The inner-loop bridge accepts an arbitrary body.  With START=2 and one
// element, its summary is false, while this body writes found=true.
module WITNESS-INNER-BODY
  imports VERIFICATION-BASE

  claim <k> For(Name("other"),
                list(fCons(0.0, .FloatSeq)),
                Assign(Name("found"), Bool(true)) .Stmts)
         => .K ... </k>
        <env> 2 </env>
        <scopes> ... 2 |-> scope(M:Map => M
                                  [ "found" <- closeSkip(0.0,
                                                         fCons(0.0, .FloatSeq),
                                                         1.0, 0, 2) ]
                                  [ "index" <- 0 ]
                                  [ "other" <- 0.0 ],
                                parent(0)) ... </scopes>
        <ret> noRet </ret>
    requires {M["number"]}:>Val ==K 0.0
     andBool {M["numbers"]}:>Val ==K list(fCons(0.0, .FloatSeq))
     andBool {M["threshold"]}:>Val ==K 1.0
     andBool {M["start"]}:>Val ==K 2
     andBool {M["found"]}:>Val ==K false
     andBool {M["index"]}:>Val ==K 0
endmodule

// The helper #applyK bridge accepts an arbitrary closure body.  The submitted
// summary is false for an empty list, while this closure returns true.
module WITNESS-HELPER-APPLY-BODY
  imports VERIFICATION-BASE

  claim <k> #applyK(toCall(closureVal(
                     ("number", "numbers", "threshold", "start"),
                     Return(Bool(true)) .Stmts, 0)),
                   (0.0, list(.FloatSeq), 1.0, 0, .Vals))
              ~> #proofDone ~> #proofDone
         => closeSkip(0.0, .FloatSeq, 1.0, 0, 0)
              ~> #proofDone ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(.Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
endmodule

// The helper textual-Call bridge does not pin the selected binding.  Here the
// name is bound to a closure returning true, but the empty-list summary is false.
module WITNESS-HELPER-CALL-BINDING
  imports VERIFICATION-BASE

  claim <k> Call(Name("is_close_to_any"),
                 Name("number"), Name("numbers"), Name("threshold"),
                 Name("start"), .Exprs)
              ~> #proofDone
         => closeSkip(0.0, .FloatSeq, 1.0, 0, 0)
              ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0 |-> scope(.Map
                       [ "is_close_to_any" <- closureVal(
                           ("number", "numbers", "threshold", "start"),
                           Return(Bool(true)) .Stmts, 0) ],
                     parent(-1))
          1 |-> scope(.Map
                       [ "number" <- 0.0 ]
                       [ "numbers" <- list(.FloatSeq) ]
                       [ "threshold" <- 1.0 ]
                       [ "start" <- 0 ],
                     parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
endmodule

// The outer-loop bridge accepts an arbitrary body.  A singleton has no pair,
// so hasPairs is false, while this body writes found=true.
module WITNESS-OUTER-BODY
  imports VERIFICATION-BASE

  claim <k> For(Name("number"),
                list(fCons(0.0, .FloatSeq)),
                Assign(Name("found"), Bool(true)) .Stmts)
         => .K ... </k>
        <env> 1 </env>
        <scopes> ... 1 |-> scope(M:Map => M
                                  [ "found" <- hasPairs(
                                      fCons(0.0, .FloatSeq),
                                      fCons(0.0, .FloatSeq), 0.0, 1) ]
                                  [ "start" <- 1 ]
                                  [ "number" <- 0.0 ],
                                parent(0)) ... </scopes>
        <ret> noRet </ret>
    requires {M["numbers"]}:>Val ==K list(fCons(0.0, .FloatSeq))
     andBool {M["threshold"]}:>Val ==K 0.0
     andBool {M["found"]}:>Val ==K false
     andBool {M["start"]}:>Val ==K 1
endmodule

// The entry textual-Call bridge also does not pin the selected binding.  The
// singleton summary is false, while the bound closure returns true.
module WITNESS-ENTRY-CALL-BINDING
  imports VERIFICATION-BASE

  claim <k> Call(Name("has_close_elements"),
                 list(fCons(0.0, .FloatSeq)), 0.0, .Exprs)
              ~> #proofDone
         => hasPairs(fCons(0.0, .FloatSeq),
                     fCons(0.0, .FloatSeq), 0.0, 1)
              ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map
                       [ "has_close_elements" <- closureVal(
                           ("numbers", "threshold"),
                           Return(Bool(true)) .Stmts, 0) ],
                     parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
endmodule
