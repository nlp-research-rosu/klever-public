// verif-klist.k — probe: K's BUILTIN hooked List as the proof container (no subsorting —
// that dead end is notes/klist-probe). Three questions, one leg each:
//   consume: does a circularity narrow a SYMBOLIC L:List against `ListItem(I) L'`?
//   build:   does builtin assoc/unit flattening replace our concat lemmas?
//   cast:    does the guarded element-cast trick ({V}:>Int under isInt) work on ListItem payloads?
module VERIF-KLIST
  imports INT
  imports BOOL
  imports LIST
  imports K-EQUAL

  configuration <k> $PGM:K </k> <acc> 0 </acc> <out> .List </out>

  // ---- consume leg: k-cell fold over a List of Ints ----
  syntax KItem ::= #sum(List)
  rule <k> #sum(.List) => .K ... </k>
  rule <k> #sum(ListItem(I:Int) L:List) => #sum(L) ... </k>
       <acc> A:Int => A +Int I </acc>

  syntax Int ::= sumL(List) [function, total]
  rule sumL(.List) => 0 [simplification]
  rule sumL(ListItem(I:Int) L:List) => I +Int sumL(L) [simplification]

  // ---- build leg: append accumulation, summary is a recursive List builder ----
  syntax KItem ::= #build(Int)
  rule <k> #build(0) => .K ... </k>
  rule <k> #build(N:Int) => #build(N -Int 1) ... </k>
       <out> L:List => L ListItem(N) </out>
       requires N >Int 0

  syntax List ::= buildL(Int) [function, total]
  rule buildL(N:Int) => .List requires N <=Int 0 [simplification]
  rule buildL(N:Int) => ListItem(N) buildL(N -Int 1) requires N >Int 0 [simplification]

  // ---- cast leg: elements are Vals; guarded cast in the fold ----
  syntax Val ::= Int | "other"
  syntax KItem ::= #sumV(List)
  rule <k> #sumV(.List) => .K ... </k>
  rule <k> #sumV(ListItem(V:Val) L:List) => #sumV(L) ... </k>
       <acc> A:Int => A +Int {V}:>Int </acc>
       requires isInt(V)

  syntax Bool ::= allIntL(List) [function, total]
  rule allIntL(.List) => true [simplification]
  rule allIntL(ListItem(V:KItem) L:List) => isInt(V) andBool allIntL(L) [simplification]

  syntax Int ::= sumVL(List) [function, total]
  rule sumVL(.List) => 0 [simplification]
  rule sumVL(ListItem(V:KItem) L:List) => {V}:>Int +Int sumVL(L)
       requires isInt(V) [simplification]
endmodule
