requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A proof-domain sequence containing only strings.  stringVals embeds it
  // into the ValSeq used by the supplied Python semantics.
  syntax StringSeq ::= ".StringSeq"
                     | sCons(IntSeq, StringSeq)

  syntax ValSeq ::= stringVals(StringSeq)
  rule stringVals(.StringSeq) => .ValSeq
  rule stringVals(sCons(CS:IntSeq, REST:StringSeq))
    => vCons(str(CS), stringVals(REST))

  // Symbolic iterator equations for the embedded sequence.  They are the two
  // MPY-LIST iterator rules composed with the stringVals equations above.
  rule <k> #iterNext(list(stringVals(.StringSeq))) => #iterDone ... </k>
       [priority(40)]
  rule <k> #iterNext(list(stringVals(sCons(CS:IntSeq, REST:StringSeq))))
        => #iterYield(str(CS), list(stringVals(REST))) ... </k>
       [priority(40)]

  // Mathematical left fold for the contract.  Strict comparison is
  // deliberate: on a tie the existing (earlier) result is retained.
  syntax Val ::= longestAcc(Val, StringSeq) [function, total]
  rule longestAcc(BEST:Val, .StringSeq) => BEST
  rule longestAcc(noneV, sCons(CS:IntSeq, REST:StringSeq))
    => longestAcc(str(CS), REST)
  rule longestAcc(str(BEST:IntSeq), sCons(CS:IntSeq, REST:StringSeq))
    => longestAcc(str(CS), REST)
    requires isLen(CS) >Int isLen(BEST)
  rule longestAcc(str(BEST:IntSeq), sCons(CS:IntSeq, REST:StringSeq))
    => longestAcc(str(BEST), REST)
    requires isLen(CS) <=Int isLen(BEST)

  // Exact closure produced by loading solution.mpy; used to keep the call
  // theorems compact while still tying them to the translated program.
  syntax Val ::= "longestSolution" [macro]
  rule longestSolution
    => closureVal("strings",
         Assign(Name("result"), NoneVal)
         Assign(Name("string"), NoneVal)
         For(Name("string"), Name("strings"),
           If(Compare(Name("result"), CmpOp("is", NoneVal)),
             Assign(Name("result"), Name("string")),
             If(Compare(
               Call(Name("len"), Name("string")),
               CmpOp("<=", Call(Name("len"), Name("result")))),
               Assign(Name("result"), Name("result")),
               If(Compare(
                 Call(Name("len"), Name("string")),
                 CmpOp(">", Call(Name("len"), Name("result")))),
                 Assign(Name("result"), Name("string")),
                 .Stmts))))
         Return(Name("result")),
         0)
endmodule
