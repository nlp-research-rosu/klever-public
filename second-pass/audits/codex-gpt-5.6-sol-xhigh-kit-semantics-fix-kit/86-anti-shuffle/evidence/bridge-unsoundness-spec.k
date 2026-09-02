requires "verification.k"

module AUDIT-HELPER-FALSE-BRIDGE
  imports VERIFICATION

  claim [false-helper-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("current"),
        If(
          Compare(Name("char"), CmpOp("<", Name("current"))),
          Return(BinOp("+", BinOp("+", Name("prefix"), Name("char")), Name("suffix"))),
          Assign(Name("prefix"), BinOp("+", Name("prefix"), Name("current")))
          Assign(Name("suffix"), Subscript(Name("suffix"), Slice(Int(1), NoBound, NoBound)))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(iCons(97, .IntSeq)) ~> CONT:K
    </k>
    <env> 2 => 1 </env>
    <scopes>
      ( BASE:Map
        2 |-> scope(
          "word" |-> str(.IntSeq)
          "char" |-> str(iCons(97, .IntSeq))
          "prefix" |-> str(.IntSeq)
          "suffix" |-> str(.IntSeq)
          "current" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 3 => 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 1, 2)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-HELPER-FALSE-BASE
  imports VERIFICATION-BASE

  claim [false-helper-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("current"),
        If(
          Compare(Name("char"), CmpOp("<", Name("current"))),
          Return(BinOp("+", BinOp("+", Name("prefix"), Name("char")), Name("suffix"))),
          Assign(Name("prefix"), BinOp("+", Name("prefix"), Name("current")))
          Assign(Name("suffix"), Subscript(Name("suffix"), Slice(Int(1), NoBound, NoBound)))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(iCons(97, .IntSeq)) ~> CONT:K
    </k>
    <env> 2 => 1 </env>
    <scopes>
      ( BASE:Map
        2 |-> scope(
          "word" |-> str(.IntSeq)
          "char" |-> str(iCons(97, .IntSeq))
          "prefix" |-> str(.IntSeq)
          "suffix" |-> str(.IntSeq)
          "current" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 3 => 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 1, 2)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-HELPER-TRUE-BASE
  imports VERIFICATION-BASE

  claim [true-helper-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("current"),
        If(
          Compare(Name("char"), CmpOp("<", Name("current"))),
          Return(BinOp("+", BinOp("+", Name("prefix"), Name("char")), Name("suffix"))),
          Assign(Name("prefix"), BinOp("+", Name("prefix"), Name("current")))
          Assign(Name("suffix"), Subscript(Name("suffix"), Slice(Int(1), NoBound, NoBound)))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(iCons(120, .IntSeq)) ~> CONT:K
    </k>
    <env> 2 => 1 </env>
    <scopes>
      ( BASE:Map
        2 |-> scope(
          "word" |-> str(.IntSeq)
          "char" |-> str(iCons(97, .IntSeq))
          "prefix" |-> str(.IntSeq)
          "suffix" |-> str(.IntSeq)
          "current" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 3 => 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 1, 2)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-OUTER-FALSE-BRIDGE
  imports VERIFICATION-FULL

  claim [false-outer-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("char"),
        If(
          Compare(Name("char"), CmpOp("==", Str(" "))),
          Assign(Name("result"), BinOp("+", BinOp("+", Name("result"), Name("word")), Str(" ")))
          Assign(Name("word"), Str("")),
          Assign(Name("word"), Call(Name("insert_char"), Name("word"), Name("char")))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(.IntSeq) ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( BASE:Map
        1 |-> scope(
          "s" |-> str(.IntSeq)
          "result" |-> str(.IntSeq)
          "word" |-> str(.IntSeq)
          "char" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-OUTER-FALSE-BASE
  imports VERIFICATION

  claim [false-outer-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("char"),
        If(
          Compare(Name("char"), CmpOp("==", Str(" "))),
          Assign(Name("result"), BinOp("+", BinOp("+", Name("result"), Name("word")), Str(" ")))
          Assign(Name("word"), Str("")),
          Assign(Name("word"), Call(Name("insert_char"), Name("word"), Name("char")))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(.IntSeq) ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( BASE:Map
        1 |-> scope(
          "s" |-> str(.IntSeq)
          "result" |-> str(.IntSeq)
          "word" |-> str(.IntSeq)
          "char" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module AUDIT-OUTER-TRUE-BASE
  imports VERIFICATION

  claim [true-outer-return]:
    <k>
      #loop(
        str(.IntSeq),
        Name("char"),
        If(
          Compare(Name("char"), CmpOp("==", Str(" "))),
          Assign(Name("result"), BinOp("+", BinOp("+", Name("result"), Name("word")), Str(" ")))
          Assign(Name("word"), Str("")),
          Assign(Name("word"), Call(Name("insert_char"), Name("word"), Name("char")))))
      ~> Return(Str("x"))
      ~> #endcall
      => str(iCons(120, .IntSeq)) ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( BASE:Map
        1 |-> scope(
          "s" |-> str(.IntSeq)
          "result" |-> str(.IntSeq)
          "word" |-> str(.IntSeq)
          "char" |-> str(.IntSeq),
          parent(0)) )
      => BASE
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> NEXT:Int </heapLoc>
    <stack> ListItem(frame(CONT, 0, 1)) REST:List => REST </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
