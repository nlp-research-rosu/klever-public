requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-CORE

  syntax Int ::= oddDigitCount(IntSeq) [function, total]
               | oddDigitCountValue(Val) [function, total]
  syntax IntSeq ::= oddCountMessage(Int) [function, total]
                  | prefixOddCount(IntSeq) [function, total]
  syntax ValSeq ::= oddCountResults(ValSeq) [function, total]
                  | appendOddCountResults(ValSeq, ValSeq) [function, total]
  syntax Val ::= oddCountResult(Val) [function, total]
  syntax Bool ::= digitCodes(IntSeq) [function, total]
                | digitStrings(ValSeq) [function, total]
                | digitString(Val) [function, total]

  // Exact notation for the translated target.  These are compile-time macros;
  // they expose, rather than replace, the fixed-semantics execution.
  syntax Stmts ::= "oddCountLoopBody" [macro]
                 | "oddCountBody" [macro]
  syntax Module ::= "oddCountModule" [macro]
endmodule

module VERIFICATION-BASE
  imports MPY
  imports VERIFICATION-SYNTAX

  // Number of occurrences of the five odd decimal digits.  The equation is
  // deliberately the same left-associated sum computed by solution.py.
  rule oddDigitCount(CS:IntSeq)
    => ((((cntSub(CS, iCons(49, .IntSeq))
           +Int cntSub(CS, iCons(51, .IntSeq)))
          +Int cntSub(CS, iCons(53, .IntSeq)))
         +Int cntSub(CS, iCons(55, .IntSeq)))
        +Int cntSub(CS, iCons(57, .IntSeq)))

  rule oddDigitCountValue(str(CS:IntSeq)) => oddDigitCount(CS)
  rule oddDigitCountValue(_:Val) => 0 [owise]

  rule oddCountResult(V:Val)
    => str(oddCountMessage(oddDigitCountValue(V)))

  // Exact code sequence produced by the source's left-associated string
  // concatenations.  Int2String is left symbolic when its argument is symbolic,
  // exactly as it is in the fixed semantics for str(count).
  rule oddCountMessage(N:Int)
    => prefixOddCount(
         seqConcat(
           seqConcat(
             seqConcat(
               seqConcat(
                 seqConcat(
                   seqConcat(
                     seqConcat(
                       strToCodes(Int2String(N)),
                       strToCodes("n the str")),
                     strToCodes(Int2String(N))),
                   strToCodes("ng ")),
                 strToCodes(Int2String(N))),
               strToCodes(" of the ")),
             strToCodes(Int2String(N))),
           strToCodes("nput.")))

  rule prefixOddCount(T:IntSeq)
    => iCons(116, iCons(104, iCons(101, iCons(32, iCons(110,
       iCons(117, iCons(109, iCons(98, iCons(101, iCons(114,
       iCons(32, iCons(111, iCons(102, iCons(32, iCons(111,
       iCons(100, iCons(100, iCons(32, iCons(101, iCons(108,
       iCons(101, iCons(109, iCons(101, iCons(110, iCons(116,
       iCons(115, iCons(32, T)))))))))))))))))))))))))))

  rule oddCountResults(VS:ValSeq) => appendOddCountResults(.ValSeq, VS)

  rule appendOddCountResults(ACC:ValSeq, .ValSeq) => ACC
  rule appendOddCountResults(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => appendOddCountResults(
         valSeqConcat(
           ACC,
           vCons(oddCountResult(V), .ValSeq)),
         REST)

  rule digitCodes(.IntSeq) => true
  rule digitCodes(iCons(C:Int, REST:IntSeq))
    => (48 <=Int C andBool C <=Int 57) andBool digitCodes(REST)

  rule digitString(str(CS:IntSeq))
    => digitCodes(CS)
       andBool #Ceil(strToCodes(Int2String(oddDigitCount(CS))))
  rule digitString(_:Val) => false [owise]

  rule digitStrings(.ValSeq) => true
  rule digitStrings(vCons(V:Val, REST:ValSeq))
    => digitString(V) andBool digitStrings(REST)

  rule oddCountLoopBody
    => Assign(
         Name("count"),
         BinOp(
           "+",
           BinOp(
             "+",
             BinOp(
               "+",
               BinOp(
                 "+",
                 Call(Attribute(Name("digits"), "count"), Str("1")),
                 Call(Attribute(Name("digits"), "count"), Str("3"))),
               Call(Attribute(Name("digits"), "count"), Str("5"))),
             Call(Attribute(Name("digits"), "count"), Str("7"))),
          Call(Attribute(Name("digits"), "count"), Str("8"))))
       Assign(Name("count_text"), Call(Name("str"), Name("count")))
       Expr(
         Call(
           Attribute(Name("result"), "append"),
           BinOp(
             "+",
             BinOp(
               "+",
               BinOp(
                 "+",
                 BinOp(
                   "+",
                   BinOp(
                     "+",
                     BinOp(
                       "+",
                       BinOp(
                         "+",
                         BinOp(
                           "+",
                           Str("the number of odd elements "),
                           Name("count_text")),
                         Str("n the str")),
                       Name("count_text")),
                     Str("ng ")),
                   Name("count_text")),
                 Str(" of the ")),
               Name("count_text")),
             Str("nput."))))

  rule oddCountBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("digits"), Name("lst"), oddCountLoopBody)
       Return(Name("result"))

  rule oddCountModule
    => Module(FuncDef("odd_count", Params("lst"), oddCountBody))
endmodule

module VERIFICATION-BODY
  imports VERIFICATION-BASE

  // Initial-iteration variant: count/count_text have not been bound yet.
  // CONNECTION-SPEC.initial-body-step proves this exact transition without
  // importing module VERIFICATION.
  rule <k> oddCountLoopBody
            ~> #loopLbl(#loop(list(REST:ValSeq), Name("digits"), oddCountLoopBody))
            ~> (Return(Name("result")) .Stmts) ~> #endcall
        => #loop(list(REST), Name("digits"), oddCountLoopBody)
            ~> (Return(Name("result")) .Stmts) ~> #endcall </k>
       <env> 1 </env>
       <scopes>
          -1 |-> BUILTINS:Scope
          0  |-> scope("odd_count" |-> closureVal("lst", oddCountBody, 0), parent(-1))
          1  |-> (scope("lst"    |-> list(ORIGINAL:ValSeq)
                         "result" |-> ref(0)
                         "digits" |-> V:Val,
                       parent(0))
                  => scope("lst"        |-> list(ORIGINAL)
                           "result"     |-> ref(0)
                           "digits"     |-> V
                           "count"      |-> oddDigitCountValue(V)
                           "count_text" |-> str(strToCodes(Int2String(oddDigitCountValue(V)))),
                         parent(0)))
       </scopes>
       <scopeLoc> 2 </scopeLoc>
       <heap>
         0 |-> list(ACC:ValSeq
                    => valSeqConcat(ACC, vCons(oddCountResult(V), .ValSeq)))
       </heap>
       <heapLoc> 1 </heapLoc>
       <stack> ListItem(frame(.K, 0, 1)) </stack>
       <ret> noRet </ret>
       <exc> NoExc </exc>
       <exit-code> 0 </exit-code>
    requires BUILTINS ==K builtinsScope
     andBool digitString(V)
    [priority(40)]

  // Exact one-body operational bridge.  connection-spec.k proves the same
  // transition with this module excluded (main module VERIFICATION-BASE).
  rule <k> oddCountLoopBody
            ~> #loopLbl(#loop(list(REST:ValSeq), Name("digits"), oddCountLoopBody))
            ~> (Return(Name("result")) .Stmts) ~> #endcall
        => #loop(list(REST), Name("digits"), oddCountLoopBody)
            ~> (Return(Name("result")) .Stmts) ~> #endcall </k>
       <env> 1 </env>
       <scopes>
          -1 |-> BUILTINS:Scope
          0  |-> scope("odd_count" |-> closureVal("lst", oddCountBody, 0), parent(-1))
          1  |-> scope("lst"        |-> list(ORIGINAL:ValSeq)
                       "result"     |-> ref(0)
                       "digits"     |-> V:Val
                       "count"      |-> (OLD_COUNT:Val => oddDigitCountValue(V))
                       "count_text" |-> (OLD_TEXT:Val => str(strToCodes(Int2String(oddDigitCountValue(V))))),
                      parent(0))
       </scopes>
       <scopeLoc> 2 </scopeLoc>
       <heap>
         0 |-> list(ACC:ValSeq
                    => valSeqConcat(
                         ACC,
                         vCons(oddCountResult(V), .ValSeq)))
       </heap>
       <heapLoc> 1 </heapLoc>
       <stack> ListItem(frame(.K, 0, 1)) </stack>
       <ret> noRet </ret>
       <exc> NoExc </exc>
       <exit-code> 0 </exit-code>
    requires BUILTINS ==K builtinsScope
     andBool digitString(V)
    [priority(40)]
endmodule

module VERIFICATION
  imports VERIFICATION-BODY

  // Exact loop summary used only after loop-spec.k proves this transition
  // under VERIFICATION-BODY, where this rule is absent.
  rule <k> #loop(list(VS:ValSeq), Name("digits"), oddCountLoopBody)
            ~> (Return(Name("result")) .Stmts) ~> #endcall
        => ref(0) </k>
       <env> 1 => 0 </env>
       <scopes>
          -1 |-> BUILTINS:Scope
          0  |-> scope("odd_count" |-> closureVal("lst", oddCountBody, 0), parent(-1))
          1  |-> scope("lst"        |-> list(ORIGINAL:ValSeq)
                       "result"     |-> ref(0)
                       "digits"     |-> OLD_DIGITS:Val
                       "count"      |-> OLD_COUNT:Val
                       "count_text" |-> OLD_TEXT:Val,
                      parent(0))
       => -1 |-> BUILTINS
          0  |-> scope("odd_count" |-> closureVal("lst", oddCountBody, 0), parent(-1))
       </scopes>
       <scopeLoc> 2 => 1 </scopeLoc>
       <heap>
         0 |-> list(ACC:ValSeq => appendOddCountResults(ACC, VS))
       </heap>
       <heapLoc> 1 </heapLoc>
       <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
       <ret> noRet </ret>
       <exc> NoExc </exc>
       <exit-code> 0 </exit-code>
    requires BUILTINS ==K builtinsScope
     andBool digitStrings(VS)
    [priority(40)]
endmodule
