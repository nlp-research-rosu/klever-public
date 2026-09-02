// spec.k — make_palindrome, TRAP-FREE (P10): the call-in-loop rung on the real
// code. Claim A = is_palindrome's two-pointer while (frame-generic; fires as a
// circularity inside the callee frame each search step). Claim B = the search
// while with the REAL call (fixed store shape per Probe A: the callee frame
// allocates at the pinned scopeLoc and deallocation restores it; co-inductive
// firstPal case-split per step). Claim C = entry over both FuncDefs.
//
//   kompile verification.k --backend haskell --main-module MAKE-PALINDROME-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module MAKE-PALINDROME-SPEC

requires "verification.k"

module MAKE-PALINDROME-SPEC
  imports MAKE-PALINDROME-VERIFICATION

  // ---- Claim A: the two-pointer scan folds to the sticky palFold
  claim
    <k>
      #while(Compare(Name("lo"), CmpOp("<", Name("hi"))),
        If(Compare(Subscript(Name("string"), Name("lo")), CmpOp("!=", Subscript(Name("string"), Name("hi")))),
          Assign(Name("ok"), Bool(false)),
          .Stmts)
        Assign(Name("lo"), BinOp("+", Name("lo"), Int(1)))
        Assign(Name("hi"), BinOp("-", Name("hi"), Int(1))))
    => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> ( scope(.Map [ "string" <- str(CS2:IntSeq) ] [ "lo" <- LO:Int ] [ "hi" <- HI:Int ] [ "ok" <- OK:Bool ], PR:Parent)
               => scope(.Map [ "string" <- str(CS2) ] [ "lo" <- ?_:Val ] [ "hi" <- ?_:Val ] [ "ok" <- palFold(CS2, LO, HI, OK) ], PR) ) ...
    </scopes>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires LO >=Int 0 andBool HI <Int isLen(CS2)
    [all-path]

  // ---- Claim B: the search while with the REAL call (fixed store shape)
  claim
    <k>
      #while(UnaryOp("not",
          Call(Name("is_palindrome"),
            Subscript(Name("string"), Slice(Name("beginning_of_suffix"), NoBound, NoBound)))),
        AugAssign(Name("beginning_of_suffix"), "+", Int(1)))
    => .K ... </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map
              [ "is_palindrome" <- closureVal("string",
            Assign(Name("lo"), Int(0))
            Assign(Name("hi"), BinOp("-", Call(Name("len"), Name("string")), Int(1)))
            Assign(Name("ok"), Bool(true))
            While(Compare(Name("lo"), CmpOp("<", Name("hi"))),
              If(Compare(Subscript(Name("string"), Name("lo")), CmpOp("!=", Subscript(Name("string"), Name("hi")))),
                Assign(Name("ok"), Bool(false)),
                .Stmts)
              Assign(Name("lo"), BinOp("+", Name("lo"), Int(1)))
              Assign(Name("hi"), BinOp("-", Name("hi"), Int(1))))
            Return(Name("ok")), 0) ]
              [ "make_palindrome" <- MPV:Val ], parent(-1))
      1 |-> ( scope(.Map [ "string" <- str(CS:IntSeq) ] [ "beginning_of_suffix" <- B:Int ], parent(0))
           => scope(.Map [ "string" <- str(CS) ] [ "beginning_of_suffix" <- firstPal(CS, B) ], parent(0)) )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HRST:Map => ?_:Map </heap>
    <heapLoc> HL:Int => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> _STK:List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int B
    [all-path]

  // ---- Claim C: entry
  claim
    <k>
      FuncDef("is_palindrome", Params("string"),
        Assign(Name("lo"), Int(0))
        Assign(Name("hi"), BinOp("-", Call(Name("len"), Name("string")), Int(1)))
        Assign(Name("ok"), Bool(true))
        While(Compare(Name("lo"), CmpOp("<", Name("hi"))),
          If(Compare(Subscript(Name("string"), Name("lo")), CmpOp("!=", Subscript(Name("string"), Name("hi")))),
            Assign(Name("ok"), Bool(false)),
            .Stmts)
          Assign(Name("lo"), BinOp("+", Name("lo"), Int(1)))
          Assign(Name("hi"), BinOp("-", Name("hi"), Int(1))))
        Return(Name("ok")))
      FuncDef("make_palindrome", Params("string"),
        If(UnaryOp("not", Name("string")),
          Return(Str("")),
          .Stmts)
        Assign(Name("beginning_of_suffix"), Int(0))
        While(UnaryOp("not",
            Call(Name("is_palindrome"),
              Subscript(Name("string"), Slice(Name("beginning_of_suffix"), NoBound, NoBound)))),
          AugAssign(Name("beginning_of_suffix"), "+", Int(1)))
        Return(BinOp("+", Name("string"),
          Subscript(
            Subscript(Name("string"), Slice(NoBound, Name("beginning_of_suffix"), NoBound)),
            Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))
      Assign(Name("result"), Call(Name("make_palindrome"), str(CS:IntSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "is_palindrome" <- ?_:Val ] [ "make_palindrome" <- ?_:Val ]
                       [ "result" <- mpRes(CS) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
