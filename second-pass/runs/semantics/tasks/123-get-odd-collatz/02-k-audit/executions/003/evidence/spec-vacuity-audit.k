requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // One arbitrary odd loop step: append the current odd value and apply 3n+1.
  claim
    <k>
      #while(
        Compare(Name("n"), CmpOp("!=", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2)))))
      =>
      #loopLbl(#while(
        Compare(Name("n"), CmpOp("!=", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2))))))
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        .Map [ "n" <- N ] [ "odd_numbers" <- ref(0) ],
        parent(0))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      1 |-> scope(
        .Map [ "n" <- 3 *Int N +Int 1 ] [ "odd_numbers" <- ref(0) ],
        parent(0))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <heap>
      0 |-> list(A)
      =>
      0 |-> list(valSeqConcat(A, vCons(N, .ValSeq)))
    </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1 andBool pyMod(N, 2) ==Int 1
    [label(odd-step)]

  // One arbitrary even loop step: do not append and apply Python floor division.
  claim
    <k>
      #while(
        Compare(Name("n"), CmpOp("!=", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2)))))
      =>
      #loopLbl(#while(
        Compare(Name("n"), CmpOp("!=", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2))))))
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        .Map [ "n" <- N ] [ "odd_numbers" <- ref(0) ],
        parent(0))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      1 |-> scope(
        .Map [
          "n" <- (N -Int pyMod(N, 2)) /Int 2
        ] [ "odd_numbers" <- ref(0) ],
        parent(0))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <heap> 0 |-> list(A) </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1 andBool notBool (pyMod(N, 2) ==Int 1)
    [label(even-step)]

  // Symbolic exit: for any accumulated sequence, append 1 and return its
  // trusted ascending sort.
  claim
    <k>
      #while(
        Compare(Name("n"), CmpOp("!=", Int(1))),
        If(Compare(BinOp("%", Name("n"), Int(2)), CmpOp("==", Int(1))),
          Expr(Call(Attribute(Name("odd_numbers"), "append"), Name("n")))
          Assign(
            Name("n"),
            BinOp("+", BinOp("*", Int(3), Name("n")), Int(1))),
          Assign(Name("n"), BinOp("//", Name("n"), Int(2)))))
      ~> Expr(Call(Attribute(Name("odd_numbers"), "append"), Int(1)))
      ~> Return(Call(Name("sorted"), Name("odd_numbers")))
      ~> #endcall
      =>
      ref(1)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      1 |-> scope(
        .Map [ "n" <- 1 ] [ "odd_numbers" <- ref(0) ],
        parent(0))
      0 |-> scope(M:Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(M, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(A)
      =>
      0 |-> list(valSeqConcat(A, vCons(1, .ValSeq)))
      1 |-> list(sortVS(valSeqConcat(A, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 1 => 2 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool ("sorted" in_keys(M))
    [label(exit-step)]

  // End-to-end base case.
  claim
    <k> #getOddCollatz(1) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map [ "get_odd_collatz" <- getOddCollatzClosure ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(sortVS(vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(case-1)]

  // End-to-end examples covering both transition branches and nontrivial sort.
  claim
    <k> #getOddCollatz(5) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map [ "get_odd_collatz" <- getOddCollatzClosure ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(5, vCons(1, .ValSeq)))
      1 |-> list(sortVS(vCons(5, vCons(3, vCons(1, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(case-5)]

  claim
    <k> #getOddCollatz(6) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map [ "get_odd_collatz" <- getOddCollatzClosure ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(3, vCons(5, vCons(1, .ValSeq))))
      1 |-> list(sortVS(vCons(3, vCons(5, vCons(1, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(case-6)]

  claim
    <k> #getOddCollatz(7) => ref(1) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        .Map [ "get_odd_collatz" <- getOddCollatzClosure ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(7,
          vCons(11,
            vCons(17,
              vCons(13,
                vCons(5,
                  vCons(1, .ValSeq)))))))
      1 |-> list(sortVS(
        vCons(7,
          vCons(11,
            vCons(17,
              vCons(13,
                vCons(5,
                  vCons(1, .ValSeq))))))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(case-7)]
endmodule
