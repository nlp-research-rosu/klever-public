requires "/tmp/audit-work/candidate/verification.k"

// Each "_roman_*" binding is deliberately a real closure that returns "z".
// With fixed ROMAN-BASE execution the result is therefore "z".  The four
// ROMAN-VERIFICATION bridges fail to check the selected binding and instead
// fabricate the normal numeral-place value from the caller's "number".

module BRIDGE-FALSE-WITNESSES
  imports ROMAN-VERIFICATION

  claim [thousandsBridgeFalse]:
    <k>
      Call(
        Name("_roman_thousands"),
        BinOp("//", Name("number"), Int(1000)))
      => str(iCons(109, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1000,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [hundredsBridgeFalse]:
    <k>
      Call(
        Name("_roman_hundreds"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(1000)),
          Int(100)))
      => str(iCons(99, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_hundreds"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 100,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [tensBridgeFalse]:
    <k>
      Call(
        Name("_roman_tens"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(100)),
          Int(10)))
      => str(iCons(120, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_tens"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 10,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [onesBridgeFalse]:
    <k>
      Call(Name("_roman_ones"), BinOp("%", Name("number"), Int(10)))
      => str(iCons(105, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_ones"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BASE-FALSE-WITNESSES
  imports ROMAN-BASE

  claim [thousandsBaseRejectsFalse]:
    <k>
      Call(
        Name("_roman_thousands"),
        BinOp("//", Name("number"), Int(1000)))
      => str(iCons(109, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1000,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [hundredsBaseRejectsFalse]:
    <k>
      Call(
        Name("_roman_hundreds"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(1000)),
          Int(100)))
      => str(iCons(99, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_hundreds"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 100,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [tensBaseRejectsFalse]:
    <k>
      Call(
        Name("_roman_tens"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(100)),
          Int(10)))
      => str(iCons(120, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_tens"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 10,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [onesBaseRejectsFalse]:
    <k>
      Call(Name("_roman_ones"), BinOp("%", Name("number"), Int(10)))
      => str(iCons(105, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_ones"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BASE-CORRECT-WITNESSES
  imports ROMAN-BASE

  claim [thousandsBaseReturnsZ]:
    <k>
      Call(
        Name("_roman_thousands"),
        BinOp("//", Name("number"), Int(1000)))
      => str(iCons(122, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_thousands"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1000,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [hundredsBaseReturnsZ]:
    <k>
      Call(
        Name("_roman_hundreds"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(1000)),
          Int(100)))
      => str(iCons(122, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_hundreds"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 100,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [tensBaseReturnsZ]:
    <k>
      Call(
        Name("_roman_tens"),
        BinOp(
          "//",
          BinOp("%", Name("number"), Int(100)),
          Int(10)))
      => str(iCons(122, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_tens"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 10,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [onesBaseReturnsZ]:
    <k>
      Call(Name("_roman_ones"), BinOp("%", Name("number"), Int(10)))
      => str(iCons(122, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_roman_ones"
          |-> closureVal("digit", Return(Str("z")) .Stmts, 0)
        "number" |-> 1,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
