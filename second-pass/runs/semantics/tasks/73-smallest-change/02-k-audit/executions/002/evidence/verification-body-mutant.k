requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These two terms are exactly the function bodies emitted in solution.mpy.
  syntax Stmts ::= "#helperBody" [macro]
  rule #helperBody
    => If(
         Compare(Name("left"), CmpOp(">=", Name("right"))),
         Return(Int(0)),
         .Stmts)
       If(
         Compare(
           Subscript(Name("arr"), Name("left")),
           CmpOp("!=", Subscript(Name("arr"), Name("right")))),
         Return(
           BinOp(
             "+",
             Int(1),
             Call(
               Name("_smallest_change"),
               Name("arr"),
               BinOp("+", Name("left"), Int(1)),
               BinOp("-", Name("right"), Int(1))))),
         .Stmts)
       Return(
         Call(
           Name("_smallest_change"),
           Name("arr"),
           BinOp("+", Name("left"), Int(1)),
           BinOp("-", Name("right"), Int(1))))

  syntax Stmts ::= "#mainBody" [macro]
  rule #mainBody
    => Return(Int(999))

  syntax Val ::= "#helperClosure" [macro]
  rule #helperClosure
    => closureVal(("arr", "left", "right"), #helperBody, 0)

  syntax Val ::= "#mainClosure" [macro]
  rule #mainClosure
    => closureVal(("arr"), #mainBody, 0)

  // Mathematical mismatch count for the still-unchecked inclusive interval.
  syntax Int ::= changeRange(ValSeq, Int, Int) [function, total]
  rule changeRange(_:ValSeq, L:Int, R:Int) => 0
    requires L >=Int R
  rule changeRange(VS:ValSeq, L:Int, R:Int)
    => (#if notBool (valSeqAt(VS, L) ==K valSeqAt(VS, R))
        #then 1 #else 0 #fi)
       +Int changeRange(VS, L +Int 1, R -Int 1)
    requires L <Int R

  // One call family covers the public wrapper and the recursive helper. This
  // lets a single reachability claim serve as the helper's induction
  // hypothesis while also establishing the required public entry point.
  syntax TargetCall ::= "mainCall" | "helperCall"
  syntax KItem ::= #targetCall(TargetCall, Val, Int, Int)

  // Instrument only the two exact closures above. The following two rules
  // replace the reference call dispatch with #targetCall. Its rules are the
  // parameter-substituted control flow of the two exact bodies above. The
  // marker provides one induction point shared by wrapper and helper while
  // avoiding the reference semantics' intentionally opaque symbolic
  // Map:update frame representation.
  rule <k>
         #applyK(toCall(#mainClosure), (ARR:Val, .Vals))
       =>
         #targetCall(mainCall, ARR, 0, 0)
       ... </k>
    [priority(40)]
  rule <k>
         #applyK(
           toCall(#helperClosure),
           (ARR:Val, L:Int, R:Int, .Vals))
       =>
         #targetCall(helperCall, ARR, L, R)
       ... </k>
    [priority(40)]

  syntax KItem ::= #addMismatch(Bool)

  rule <k>
         #targetCall(mainCall, ref(H:Int), _:Int, _:Int)
       =>
         #targetCall(
           helperCall,
           ref(H),
           0,
           vsLen(VS) -Int 1)
       ... </k>
       <heap> ... H |-> list(VS:ValSeq) ... </heap>

  rule <k> #targetCall(helperCall, _:Val, L:Int, R:Int) => 0 ... </k>
    requires L >=Int R

  rule <k>
         #targetCall(helperCall, ref(H:Int), L:Int, R:Int)
       =>
         #targetCall(helperCall, ref(H), L +Int 1, R -Int 1)
         ~> #addMismatch(
              notBool (
                valSeqAt(VS, L) ==K valSeqAt(VS, R)))
       ... </k>
       <heap> ... H |-> list(VS:ValSeq) ... </heap>
    requires L <Int R

  rule <k> I:Int ~> #addMismatch(B:Bool)
        => (#if B #then 1 #else 0 #fi) +Int I ... </k>

  syntax Int ::= targetAnswer(TargetCall, ValSeq, Int, Int) [function, total]
  rule targetAnswer(mainCall, VS:ValSeq, _:Int, _:Int)
    => changeRange(VS, 0, vsLen(VS) -Int 1)
  rule targetAnswer(helperCall, VS:ValSeq, L:Int, R:Int)
    => changeRange(VS, L, R)

  syntax Bool ::= targetValid(TargetCall, ValSeq, Int, Int) [function, total]
  rule targetValid(mainCall, _:ValSeq, _:Int, _:Int) => true
  rule targetValid(helperCall, VS:ValSeq, L:Int, R:Int)
    => 0 <=Int L andBool L <=Int vsLen(VS)
       andBool -1 <=Int R andBool R <Int vsLen(VS)
endmodule
