requires "verification.k"

module AUDIT-SPEC-FALSE
  imports VERIFICATION

  // Structural invariant for the inner character loop.  PREV is the code of
  // the last character already visited (48 before the first iteration).
  claim [digit-loop]:
    <k>
      #loop(
        str(CS:IntSeq),
        Name("char"),
        Assign(Name("digit"), Call(Name("int"), Name("char")))
        If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
          Assign(Name("first_digit"), Name("digit")) .Stmts,
          .Stmts)
        AugAssign(Name("digit_sum"), "+", Name("digit"))
        .Stmts)
      => .K ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope("count_nums" |-> FN:Val, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(ARR:ValSeq)
        "count" |-> COUNT:Int
        "num" |-> NUM:Val
        "n" |-> NN:Val
        "digit_sum" |->
          (SUM:Int => SUM +Int codeDigitSum(CS))
        "first_digit" |->
          (FIRST:Int => chooseFirst(FIRST, CS))
        "char" |->
          (str(iCons(PREV:Int, .IntSeq))
            => str(iCons(lastCode(PREV, CS), .IntSeq)))
        "digit" |->
          (PREV -Int 48 => lastCode(PREV, CS) -Int 48),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allDigitCodes(CS)
      andBool 48 <=Int PREV
      andBool PREV <=Int 57

  // Recurrent outer-loop base case.  The source return and fixed frame-pop
  // behavior are part of this claim.
  claim [outer-loop-empty]:
    <k>
      #loop(
        list(.ValSeq),
        Name("num"),
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
          Assign(Name("n"), Name("num")) .Stmts)
        Assign(Name("digit_sum"), Int(0))
        Assign(Name("first_digit"), Int(0))
        Assign(Name("char"), Str("0"))
        Assign(Name("digit"), Int(0))
        For(
          Name("char"),
          Call(Name("str"), Name("n")),
          Assign(Name("digit"), Call(Name("int"), Name("char")))
          If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
            Assign(Name("first_digit"), Name("digit")) .Stmts,
            .Stmts)
          AugAssign(Name("digit_sum"), "+", Name("digit"))
          .Stmts)
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          AugAssign(
            Name("digit_sum"),
            "-",
            BinOp("*", Int(2), Name("first_digit")))
          .Stmts,
          .Stmts)
        If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts)
        .Stmts)
      ~> (Return(Name("count")) .Stmts):Stmts
      ~> #endcall
      => C:Int
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope("count_nums" |-> FN:Val, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(ORIGINAL:ValSeq)
        "count" |-> C:Int
        "num" |-> OLDNUM:Val
        "n" |-> OLDN:Val
        "digit_sum" |-> OLDSUM:Int
        "first_digit" |-> OLDFIRST:Int
        "char" |-> str(iCons(OLDCODE:Int, .IntSeq))
        "digit" |-> OLDCODE -Int 48,
        parent(0))
      =>
      0 |-> scope("count_nums" |-> FN, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Recurrent outer-loop inductive case over one integer head and an
  // arbitrary all-integer tail.
  claim [outer-loop-step]:
    <k>
      #loop(
        list(vCons(I:Val, R:ValSeq)),
        Name("num"),
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
          Assign(Name("n"), Name("num")) .Stmts)
        Assign(Name("digit_sum"), Int(0))
        Assign(Name("first_digit"), Int(0))
        Assign(Name("char"), Str("0"))
        Assign(Name("digit"), Int(0))
        For(
          Name("char"),
          Call(Name("str"), Name("n")),
          Assign(Name("digit"), Call(Name("int"), Name("char")))
          If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
            Assign(Name("first_digit"), Name("digit")) .Stmts,
            .Stmts)
          AugAssign(Name("digit_sum"), "+", Name("digit"))
          .Stmts)
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          AugAssign(
            Name("digit_sum"),
            "-",
            BinOp("*", Int(2), Name("first_digit")))
          .Stmts,
          .Stmts)
        If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts)
        .Stmts)
      ~> (Return(Name("count")) .Stmts):Stmts
      ~> #endcall
      => C:Int +Int countNumsSpec(vCons(I, R))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope("count_nums" |-> FN:Val, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(ORIGINAL:ValSeq)
        "count" |-> C:Int
        "num" |-> OLDNUM:Val
        "n" |-> OLDN:Val
        "digit_sum" |-> OLDSUM:Int
        "first_digit" |-> OLDFIRST:Int
        "char" |-> str(iCons(OLDCODE:Int, .IntSeq))
        "digit" |-> OLDCODE -Int 48,
        parent(0))
      =>
      0 |-> scope("count_nums" |-> FN, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires isInt(I) andBool allInts(R)

  // Exact call setup through parameter binding, count initialization, and
  // evaluation of the outer iterable.  No program result is summarized here.
  claim [call-setup-nonempty]:
    <k>
      Call(Name("count_nums"), list(vCons(I:Int, R:ValSeq)))
      =>
      #loop(
        list(vCons(I, R)),
        Name("num"),
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
          Assign(Name("n"), Name("num")) .Stmts)
        Assign(Name("digit_sum"), Int(0))
        Assign(Name("first_digit"), Int(0))
        Assign(Name("char"), Str("0"))
        Assign(Name("digit"), Int(0))
        For(
          Name("char"),
          Call(Name("str"), Name("n")),
          Assign(Name("digit"), Call(Name("int"), Name("char")))
          If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
            Assign(Name("first_digit"), Name("digit")) .Stmts,
            .Stmts)
          AugAssign(Name("digit_sum"), "+", Name("digit"))
          .Stmts)
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          AugAssign(
            Name("digit_sum"),
            "-",
            BinOp("*", Int(2), Name("first_digit")))
          .Stmts,
          .Stmts)
        If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts)
        .Stmts)
      ~> (Return(Name("count")) .Stmts):Stmts
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      0 |-> scope(
        "count_nums" |->
          closureVal(
            "arr" , .ParamNames,
            Assign(Name("count"), Int(0))
            For(
              Name("num"),
              Name("arr"),
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
                Assign(Name("n"), Name("num")) .Stmts)
              Assign(Name("digit_sum"), Int(0))
              Assign(Name("first_digit"), Int(0))
              Assign(Name("char"), Str("0"))
              Assign(Name("digit"), Int(0))
              For(
                Name("char"),
                Call(Name("str"), Name("n")),
                Assign(Name("digit"), Call(Name("int"), Name("char")))
                If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
                  Assign(Name("first_digit"), Name("digit")) .Stmts,
                  .Stmts)
                AugAssign(Name("digit_sum"), "+", Name("digit"))
                .Stmts)
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                AugAssign(
                  Name("digit_sum"),
                  "-",
                  BinOp("*", Int(2), Name("first_digit")))
                .Stmts,
                .Stmts)
              If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
                AugAssign(Name("count"), "+", Int(1)) .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("count"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "count_nums" |->
          closureVal(
            "arr" , .ParamNames,
            Assign(Name("count"), Int(0))
            For(
              Name("num"),
              Name("arr"),
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
                Assign(Name("n"), Name("num")) .Stmts)
              Assign(Name("digit_sum"), Int(0))
              Assign(Name("first_digit"), Int(0))
              Assign(Name("char"), Str("0"))
              Assign(Name("digit"), Int(0))
              For(
                Name("char"),
                Call(Name("str"), Name("n")),
                Assign(Name("digit"), Call(Name("int"), Name("char")))
                If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
                  Assign(Name("first_digit"), Name("digit")) .Stmts,
                  .Stmts)
                AugAssign(Name("digit_sum"), "+", Name("digit"))
                .Stmts)
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                AugAssign(
                  Name("digit_sum"),
                  "-",
                  BinOp("*", Int(2), Name("first_digit")))
                .Stmts,
                .Stmts)
              If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
                AugAssign(Name("count"), "+", Int(1)) .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("count"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(vCons(I, R))
        "count" |-> 0,
        parent(0))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(R)

  // First outer iteration, before the loop body has created its temporary
  // locals.  This connects function entry to the recurrent loop claims.
  claim [outer-loop-initial]:
    <k>
      #loop(
        list(vCons(I:Int, R:ValSeq)),
        Name("num"),
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
          Assign(Name("n"), Name("num")) .Stmts)
        Assign(Name("digit_sum"), Int(0))
        Assign(Name("first_digit"), Int(0))
        Assign(Name("char"), Str("0"))
        Assign(Name("digit"), Int(0))
        For(
          Name("char"),
          Call(Name("str"), Name("n")),
          Assign(Name("digit"), Call(Name("int"), Name("char")))
          If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
            Assign(Name("first_digit"), Name("digit")) .Stmts,
            .Stmts)
          AugAssign(Name("digit_sum"), "+", Name("digit"))
          .Stmts)
        If(Compare(Name("num"), CmpOp("<", Int(0))),
          AugAssign(
            Name("digit_sum"),
            "-",
            BinOp("*", Int(2), Name("first_digit")))
          .Stmts,
          .Stmts)
        If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
          AugAssign(Name("count"), "+", Int(1)) .Stmts,
          .Stmts)
        .Stmts)
      ~> (Return(Name("count")) .Stmts):Stmts
      ~> #endcall
      => C:Int +Int countNumsSpec(vCons(I, R))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope("count_nums" |-> FN:Val, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(vCons(I, R))
        "count" |-> C:Int,
        parent(0))
      =>
      0 |-> scope("count_nums" |-> FN, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1)) => .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(R)

  // Exact translated function call on the empty list.
  claim [count-nums-empty]:
    <k>
      Call(Name("count_nums"), list(.ValSeq))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_nums" |->
          closureVal(
            "arr" , .ParamNames,
            Assign(Name("count"), Int(0))
            For(
              Name("num"),
              Name("arr"),
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
                Assign(Name("n"), Name("num")) .Stmts)
              Assign(Name("digit_sum"), Int(0))
              Assign(Name("first_digit"), Int(0))
              Assign(Name("char"), Str("0"))
              Assign(Name("digit"), Int(0))
              For(
                Name("char"),
                Call(Name("str"), Name("n")),
                Assign(Name("digit"), Call(Name("int"), Name("char")))
                If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
                  Assign(Name("first_digit"), Name("digit")) .Stmts,
                  .Stmts)
                AugAssign(Name("digit_sum"), "+", Name("digit"))
                .Stmts)
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                AugAssign(
                  Name("digit_sum"),
                  "-",
                  BinOp("*", Int(2), Name("first_digit")))
                .Stmts,
                .Stmts)
              If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
                AugAssign(Name("count"), "+", Int(1)) .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("count"))
            .Stmts,
            0),
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

  // Exact translated function call on every nonempty finite integer list.
  claim [count-nums-nonempty]:
    <k>
      Call(Name("count_nums"), list(vCons(I:Int, R:ValSeq)))
      => ?RESULT:Int
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "count_nums" |->
          closureVal(
            "arr" , .ParamNames,
            Assign(Name("count"), Int(0))
            For(
              Name("num"),
              Name("arr"),
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                Assign(Name("n"), UnaryOp("-", Name("num"))) .Stmts,
                Assign(Name("n"), Name("num")) .Stmts)
              Assign(Name("digit_sum"), Int(0))
              Assign(Name("first_digit"), Int(0))
              Assign(Name("char"), Str("0"))
              Assign(Name("digit"), Int(0))
              For(
                Name("char"),
                Call(Name("str"), Name("n")),
                Assign(Name("digit"), Call(Name("int"), Name("char")))
                If(Compare(Name("first_digit"), CmpOp("==", Int(0))),
                  Assign(Name("first_digit"), Name("digit")) .Stmts,
                  .Stmts)
                AugAssign(Name("digit_sum"), "+", Name("digit"))
                .Stmts)
              If(Compare(Name("num"), CmpOp("<", Int(0))),
                AugAssign(
                  Name("digit_sum"),
                  "-",
                  BinOp("*", Int(2), Name("first_digit")))
                .Stmts,
                .Stmts)
              If(Compare(Name("digit_sum"), CmpOp(">", Int(0))),
                AugAssign(Name("count"), "+", Int(1)) .Stmts,
                .Stmts)
              .Stmts)
            Return(Name("count"))
            .Stmts,
            0),
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
    requires allInts(R)
    ensures ?RESULT ==Int countNumsSpec(vCons(I, R)) +Int 1
endmodule
