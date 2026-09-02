requires "verification.k"

module SPEC-INNER
  imports VERIFICATION-BASE

  claim <k> #loop(list(.FloatSeq),
                   Name("other"), helperLoopBody())
              ~> Assign(Name("index"), Int(0))
              ~> Assign(Name("other"), Name("number"))
              ~> Return(Name("found")) ~> #endcall
         => Return(Name("found")) ~> #endcall </k>
        <env> 2 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(EM:Map, parent(0))
          2  |-> (scope(.Map
                        [ "number" <- A:Float ]
                        [ "numbers" <- list(ALL:FloatSeq) ]
                        [ "threshold" <- T:Float ]
                        [ "start" <- START:Int ]
                        [ "found" <- false ]
                        [ "index" <- I:Int ]
                        [ "other" <- Q:Float ],
                       parent(0))
                  => scope(.Map
                           [ "number" <- A ]
                           [ "numbers" <- list(ALL) ]
                           [ "threshold" <- T ]
                           [ "start" <- START ]
                           [ "found" <- false ]
                           [ "index" <- 0 ]
                           [ "other" <- A ],
                          parent(0)))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 3 </scopeLoc>
        <stack> ListItem(frame(K:K, 1, 2)) REST:List </stack>
        <ret> noRet </ret>

  claim <k> #loop(list(fCons(F:Float, R:FloatSeq)),
                   Name("other"), helperLoopBody())
              ~> Assign(Name("index"), Int(0))
              ~> Assign(Name("other"), Name("number"))
              ~> Return(Name("found")) ~> #endcall
         => Return(Name("found")) ~> #endcall </k>
        <env> 2 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(EM:Map, parent(0))
          2  |-> (scope(.Map
                         [ "number" <- A:Float ]
                         [ "numbers" <- list(ALL:FloatSeq) ]
                         [ "threshold" <- T:Float ]
                         [ "start" <- START:Int ]
                         [ "found" <- false ]
                         [ "index" <- I:Int ]
                         [ "other" <- Q:Float ],
                        parent(0))
                   => scope(.Map
                            [ "number" <- A ]
                            [ "numbers" <- list(ALL) ]
                            [ "threshold" <- T ]
                            [ "start" <- START ]
                            [ "found" <- closeSkip(A, R, T, I +Int 1, START) ]
                            [ "index" <- 0 ]
                            [ "other" <- A ],
                           parent(0)))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 3 </scopeLoc>
        <stack> ListItem(frame(K:K, 1, 2)) REST:List </stack>
        <ret> noRet </ret>
    requires I <Int START

  claim <k> #loop(list(fCons(F:Float, R:FloatSeq)),
                   Name("other"), helperLoopBody())
              ~> Assign(Name("index"), Int(0))
              ~> Assign(Name("other"), Name("number"))
              ~> Return(Name("found")) ~> #endcall
         => Return(Name("found")) ~> #endcall </k>
        <env> 2 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(EM:Map, parent(0))
          2  |-> (scope(.Map
                         [ "number" <- A:Float ]
                         [ "numbers" <- list(ALL:FloatSeq) ]
                         [ "threshold" <- T:Float ]
                         [ "start" <- START:Int ]
                         [ "found" <- false ]
                         [ "index" <- I:Int ]
                         [ "other" <- Q:Float ],
                        parent(0))
                   => scope(.Map
                            [ "number" <- A ]
                            [ "numbers" <- list(ALL) ]
                            [ "threshold" <- T ]
                            [ "start" <- START ]
                            [ "found" <- (near(A, F, T)
                                           orBool closeSkip(A, R, T, I +Int 1, START)) ]
                            [ "index" <- 0 ]
                            [ "other" <- A ],
                           parent(0)))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 3 </scopeLoc>
        <stack> ListItem(frame(K:K, 1, 2)) REST:List </stack>
        <ret> noRet </ret>
    requires I >=Int START
endmodule

module SPEC-HELPER
  imports VERIFICATION-WITH-INNER

  claim <k> #applyK(toCall(helperClosure()),
                    (A:Float, list(ALL:FloatSeq),
                     T:Float, START:Int, .Vals)) ~> #proofDone
         => closeSkip(A, ALL, T, 0, START) ~> #proofDone </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> scope(EM:Map, parent(0))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <ret> noRet </ret>
endmodule

module SPEC-OUTER
  imports VERIFICATION-WITH-HELPER

  claim <k> #loop(list(.FloatSeq),
                   Name("number"), outerLoopBody())
              ~> Assign(Name("start"), Int(1))
              ~> Assign(Name("number"), Name("threshold"))
              ~> Return(Name("found")) ~> #endcall
         => Return(Name("found")) ~> #endcall </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> (scope(.Map
                        [ "numbers" <- list(ALL:FloatSeq) ]
                        [ "threshold" <- T:Float ]
                        [ "found" <- false ]
                        [ "start" <- START:Int ]
                        [ "number" <- Q:Float ],
                       parent(0))
                  => scope(.Map
                           [ "numbers" <- list(ALL) ]
                           [ "threshold" <- T ]
                           [ "found" <- false ]
                           [ "start" <- 1 ]
                           [ "number" <- T ],
                          parent(0)))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <stack> ListItem(frame(K:K, 0, 1)) REST:List </stack>
        <ret> noRet </ret>

  claim <k> #loop(list(fCons(A:Float, R:FloatSeq)),
                   Name("number"), outerLoopBody())
              ~> Assign(Name("start"), Int(1))
              ~> Assign(Name("number"), Name("threshold"))
              ~> Return(Name("found")) ~> #endcall
         => Return(Name("found")) ~> #endcall </k>
        <env> 1 </env>
        <scopes>
          0  |-> solutionScope()
          1  |-> (scope(.Map
                         [ "numbers" <- list(ALL:FloatSeq) ]
                         [ "threshold" <- T:Float ]
                         [ "found" <- false ]
                         [ "start" <- START:Int ]
                         [ "number" <- Q:Float ],
                        parent(0))
                   => scope(.Map
                            [ "numbers" <- list(ALL) ]
                            [ "threshold" <- T ]
                            [ "found" <- (closeSkip(A, ALL, T, 0, START)
                                           orBool hasPairs(ALL, R, T, START +Int 1)) ]
                            [ "start" <- 1 ]
                            [ "number" <- T ],
                           parent(0)))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 2 </scopeLoc>
        <stack> ListItem(frame(K:K, 0, 1)) REST:List </stack>
        <ret> noRet </ret>
endmodule

module SPEC-ENTRY
  imports VERIFICATION-WITH-OUTER

  claim <k> #applyK(toCall(entryClosure()),
                    (list(ALL:FloatSeq), T:Float, .Vals)) ~> #proofDone
         => hasPairs(ALL, ALL, T, 1) ~> #proofDone </k>
        <env> 0 </env>
        <scopes>
          0  |-> solutionScope()
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule

module SPEC
  imports VERIFICATION-WITH-ENTRY

  claim <k> #loadAll(solutionModule())
              ~> Call(Name("has_close_elements"),
                      list(ALL:FloatSeq), T:Float, .Exprs)
         => hasPairs(ALL, ALL, T, 1) ... </k>
        <env> 0 </env>
        <scopes>
          0  |-> (scope(.Map, parent(-1)) => solutionScope())
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule
