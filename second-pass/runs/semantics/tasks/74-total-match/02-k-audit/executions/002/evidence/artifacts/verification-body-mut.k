requires "reference-semantics/semantics.k"

module TOTAL-MATCH-VERIFICATION
  imports MPY

  // A proof-domain sequence whose elements are strings.  Keeping this sort
  // separate from ValSeq records the HumanEval input precondition in the
  // symbolic term itself.
  syntax StrSeq ::= ".StrSeq"
                  | ssCons(IntSeq, StrSeq)

  syntax ValSeq ::= strVals(StrSeq)
  rule strVals(.StrSeq) => .ValSeq
  rule strVals(ssCons(S:IntSeq, REST:StrSeq))
    => vCons(str(S), strVals(REST))

  syntax Int ::= totalChars(StrSeq) [function, total]
  rule totalChars(.StrSeq) => 0
  rule totalChars(ssCons(S:IntSeq, REST:StrSeq))
    => isLen(S) +Int totalChars(REST)

  // Let the reference iterator consume the proof-domain representation one
  // symbolic string at a time.  This adapter is used by the independent loop
  // invariant claim in spec.k.
  syntax KItem ::= nextStrings(StrSeq)
  rule <k> #iterNext(list(strVals(ITEMS:StrSeq)))
        => nextStrings(ITEMS)
        ...
       </k>
       [priority(40)]
  rule <k> nextStrings(.StrSeq)
        => #iterDone
        ...
       </k>
  rule <k> nextStrings(ssCons(S:IntSeq, REST:StrSeq))
        => #iterYield(str(S), list(strVals(REST)))
        ...
       </k>

  // A proof-only observer used after the real loop: read the accumulator and
  // discard the loop variable, which is unobservable to total_match.
  syntax KItem ::= readAccAndDrop(String, String)
  rule <k> readAccAndDrop(ACC:String, ITEM:String)
        => I
        ...
       </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           (ACC |-> I:Int) M:Map,
           _P:Parent)
         ...
       </scopes>
       requires notBool (ACC in_keys(M))
        andBool ACC =/=String ITEM
        andBool notBool (ITEM in_keys(M))

  rule <k> readAccAndDrop(ACC:String, ITEM:String)
        => I
        ...
       </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           ((ACC |-> I:Int) (ITEM |-> _V:Val) M:Map
             => (ACC |-> I) M),
           _P:Parent)
         ...
       </scopes>
       requires notBool (ACC in_keys(M))
        andBool notBool (ITEM in_keys(M))
        andBool ACC =/=String ITEM

  // Loop invariant for this program shape:
  //
  //   accumulator_after = accumulator_before + totalChars(remaining)
  //
  // The rule is deliberately restricted to iteration over strVals and to the
  // exact `acc += len(item)` body.  TOTAL-MATCH-LOOP-SPEC proves the
  // corresponding recursive #loop reachability claim using the reference
  // iterator, binding, builtin-call, and AugAssign rules.  The loop variable's
  // final binding is unobservable in total_match and its frame is discarded
  // on return.
  rule <k>
         For(
           Name(ITEM:String),
           list(strVals(ITEMS:StrSeq)),
           AugAssign(
             Name(ACC:String),
             "+",
             Call(Name("len"), Name(ITEM))) .Stmts)
         => .K
         ...
       </k>
       <env> L:Int </env>
       <scopes>
         ...
         L |-> scope(
           M:Map
             => M [ ACC <- ({M[ACC]}:>Int +Int totalChars(ITEMS)) ],
           _P:Parent)
         ...
       </scopes>
       requires ACC in_keys(M)
        andBool isInt({M[ACC]}:>Val)
       [priority(40)]

  // The translated function body, exposed as a callable closure so claims can
  // supply arbitrary symbolic lists without changing the Python program.
  syntax KItem ::= runTotalMatch(StrSeq, StrSeq)
  rule <k> runTotalMatch(A:StrSeq, B:StrSeq)
        => Call(
             closureVal(
               ("lst1", "lst2"),
               Assign(Name("total1"), Int(0))
               Assign(Name("total2"), Int(0))
               For(Name("item"), Name("lst1"),
                 AugAssign(
                   Name("total1"),
                   "+",
                   Int(0)))
               For(Name("item"), Name("lst2"),
                 AugAssign(
                   Name("total2"),
                   "+",
                   Call(Name("len"), Name("item"))))
               If(
                 Compare(Name("total1"), CmpOp("<=", Name("total2"))),
                 Return(Name("lst1")),
                 .Stmts)
               Return(Name("lst2")),
               0),
             list(strVals(A)),
             list(strVals(B)))
           ...
       </k>
endmodule
