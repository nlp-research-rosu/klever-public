requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately wrong body: the orange count is added instead of subtracted.
  claim [wrong-body]:
    <k>
      Call(
        closureVal(
          ("s", "n"),
          Return(
            BinOp(
              "+",
              BinOp(
                "-",
                Name("n"),
                Call(
                  Name("int"),
                  Subscript(
                    Call(Attribute(Name("s"), "split"), .Exprs),
                    Int(0)),
                  .Exprs)),
              Call(
                Name("int"),
                Subscript(
                  Call(Attribute(Name("s"), "split"), .Exprs),
                  Int(3)),
                .Exprs)))
          .Stmts,
          0),
        str(CS:IntSeq),
        N:Int)
      => N -Int APPLES -Int ORANGES
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      splitWS(CS, .IntSeq, .ValSeq)
        ==K vCons(
              str(APPLECODES:IntSeq),
              vCons(
                str(strToCodes("apples")),
                vCons(
                  str(strToCodes("and")),
                  vCons(
                    str(ORANGECODES:IntSeq),
                    vCons(str(strToCodes("oranges")), .ValSeq)))))
      andBool
      applyBuiltin("int", str(APPLECODES), .Vals) ==K APPLES:Int
      andBool
      applyBuiltin("int", str(ORANGECODES), .Vals) ==K ORANGES:Int
      andBool allDigit(APPLECODES)
      andBool allDigit(ORANGECODES)
      andBool isLen(APPLECODES) >Int 0
      andBool isLen(ORANGECODES) >Int 0
      andBool APPLES >=Int 0
      andBool ORANGES >=Int 0
      andBool N >=Int APPLES +Int ORANGES
endmodule
