requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  // Exact source-body macros. They only avoid duplicating the translated AST
  // in the claims; macro expansion happens before execution.
  syntax Stmts ::= "sortEvenBody" [macro]
  syntax Stmts ::= "sortEvenLoopBody" [macro]

  // Number of even positions in a sequence of length N.
  syntax Int ::= evenCount(Int) [function, total]

  // Apply consecutive writes for counters I through STOP - 1.
  syntax ValSeq ::= fillEven(ValSeq, ValSeq, Int, Int)
                    [function, total]

  // The result specified by the source contract: the input sequence with its
  // even-position projection replaced by the ascending sort of that projection.
  syntax ValSeq ::= sortEvenResult(ValSeq) [function, total]
endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  rule sortEvenLoopBody
    => Assign(
         Subscript(Name("result"), BinOp("*", Int(2), Name("i"))),
         Subscript(Name("evens"), Name("i")))

  rule sortEvenBody
    => Assign(Name("result"), Call(Name("list"), Name("l")))
       Assign(
         Name("evens"),
         Call(
           Name("sorted"),
           Subscript(Name("l"), Slice(NoBound, NoBound, Int(2)))))
       Assign(Name("i"), Int(0))
       For(
         Name("i"),
         Call(
           Name("range"),
           BinOp(
             "//",
             BinOp("+", Call(Name("len"), Name("l")), Int(1)),
             Int(2))),
         sortEvenLoopBody)
       Return(Name("result"))

  rule evenCount(N)
    => (N +Int 1 -Int pyMod(N +Int 1, 2)) /Int 2

  rule fillEven(VS, _SORTED, I, STOP) => VS
    requires I >=Int STOP

  rule fillEven(VS, SORTED, I, STOP)
    => fillEven(
         setVSAt(VS, 2 *Int I, valSeqAt(SORTED, I)),
         SORTED,
         I +Int 1,
         STOP)
    requires I <Int STOP

  rule sortEvenResult(VS)
    => fillEven(
         VS,
         sortVS(buildVS(VS, 0, vsLen(VS), 2)),
         0,
         evenCount(vsLen(VS)))
endmodule

// Used to prove the loop connection theorem without the operational bridge.
module VERIFICATION-NO-BRIDGE
  imports VERIFICATION-BASE
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact operational bridge justified by SPEC-CONNECTION.loop-connection,
  // which is proved under VERIFICATION-NO-BRIDGE.  The rule deliberately
  // accepts no continuation, binding, heap, stack, return, exception, or exit
  // context beyond the universally quantified context of that theorem.
  rule
    <k>
      #loop(
        rangeObj(I, C, 1),
        Name("i"),
        sortEvenLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        1 |-> scope(
          ( "l"      |-> list(VS)
            "result" |-> ref(0)
            "evens"  |-> ref(2)
            "i"      |-> _J ),
          parent(0))
        -1 |-> B:Scope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> B )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      ( 0 |-> list(
          CUR
          => fillEven(
               CUR,
               SORTED,
               I,
               C))
        1 |-> list(SLICE)
        2 |-> list(SORTED) )
    </heap>
    <heapLoc> 3 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0
    [priority(40)]
endmodule
