# Exhaustive K declaration and rule inventory

files=26
raw_rule_starts=705 parsed_rule_blocks=705
raw_syntax_starts=233 parsed_syntax_blocks=233
raw_claim_starts=6 parsed_claim_blocks=6
coverage_ok=True
category_counts={'claim': 6, 'configuration': 1, 'context': 5, 'endmodule': 28, 'imports': 91, 'module': 28, 'requires': 25, 'rule:equational': 467, 'rule:operational': 193, 'rule:priority': 45, 'syntax': 233}

attribute_occurrences[function]=160
attribute_occurrences[total]=118
attribute_occurrences[functional]=0
attribute_occurrences[no-evaluators]=22
attribute_occurrences[priority]=45
attribute_occurrences[simplification]=0
attribute_occurrences[macro]=9
attribute_occurrences[macro-rec]=1
attribute_occurrences[owise]=26
attribute_occurrences[concrete]=36

## 0001 reference-semantics/semantics.k:34 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/syntax.k"
```

## 0002 reference-semantics/semantics.k:35 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/core.k"
```

## 0003 reference-semantics/semantics.k:36 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/iter.k"
```

## 0004 reference-semantics/semantics.k:37 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/range.k"
```

## 0005 reference-semantics/semantics.k:38 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/operators.k"
```

## 0006 reference-semantics/semantics.k:39 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/int.k"
```

## 0007 reference-semantics/semantics.k:40 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/bool.k"
```

## 0008 reference-semantics/semantics.k:41 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/float.k"
```

## 0009 reference-semantics/semantics.k:42 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/str.k"
```

## 0010 reference-semantics/semantics.k:43 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/set.k"
```

## 0011 reference-semantics/semantics.k:44 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/list.k"
```

## 0012 reference-semantics/semantics.k:45 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/tuple.k"
```

## 0013 reference-semantics/semantics.k:46 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/subscript.k"
```

## 0014 reference-semantics/semantics.k:47 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/comprehension.k"
```

## 0015 reference-semantics/semantics.k:48 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/methods.k"
```

## 0016 reference-semantics/semantics.k:49 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/controls.k"
```

## 0017 reference-semantics/semantics.k:50 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/functions.k"
```

## 0018 reference-semantics/semantics.k:51 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/builtins.k"
```

## 0019 reference-semantics/semantics.k:52 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/call.k"
```

## 0020 reference-semantics/semantics.k:53 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/sort.k"
```

## 0021 reference-semantics/semantics.k:54 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/assert.k"
```

## 0022 reference-semantics/semantics.k:55 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/dict.k"
```

## 0023 reference-semantics/semantics.k:56 [requires]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
requires "semantics/concrete.k"
```

## 0024 reference-semantics/semantics.k:58 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY
```

## 0025 reference-semantics/semantics.k:59 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0026 reference-semantics/semantics.k:60 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0027 reference-semantics/semantics.k:61 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-RANGE
```

## 0028 reference-semantics/semantics.k:62 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-OPERATORS
```

## 0029 reference-semantics/semantics.k:63 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-INT
```

## 0030 reference-semantics/semantics.k:64 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-BOOL
```

## 0031 reference-semantics/semantics.k:65 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-FLOAT
```

## 0032 reference-semantics/semantics.k:66 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-STR
```

## 0033 reference-semantics/semantics.k:67 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SET
```

## 0034 reference-semantics/semantics.k:68 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-LIST
```

## 0035 reference-semantics/semantics.k:69 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-TUPLE
```

## 0036 reference-semantics/semantics.k:70 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SUBSCRIPT
```

## 0037 reference-semantics/semantics.k:71 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-COMPREHENSION
```

## 0038 reference-semantics/semantics.k:72 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-METHODS
```

## 0039 reference-semantics/semantics.k:73 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CONTROLS
```

## 0040 reference-semantics/semantics.k:74 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-FUNCTIONS
```

## 0041 reference-semantics/semantics.k:75 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-BUILTINS
```

## 0042 reference-semantics/semantics.k:76 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CALL
```

## 0043 reference-semantics/semantics.k:77 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SORT
```

## 0044 reference-semantics/semantics.k:78 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ASSERT
```

## 0045 reference-semantics/semantics.k:79 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-DICT
```

## 0046 reference-semantics/semantics.k:80 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0047 reference-semantics/semantics.k:87 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-KRUN
```

## 0048 reference-semantics/semantics.k:88 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY
```

## 0049 reference-semantics/semantics.k:89 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CONCRETE
```

## 0050 reference-semantics/semantics.k:90 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0051 reference-semantics/semantics/assert.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-ASSERT
```

## 0052 reference-semantics/semantics/assert.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0053 reference-semantics/semantics/assert.k:6 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assert(V:Val) => .K ... </k>
       requires truthy(V)
```

## 0054 reference-semantics/semantics/assert.k:8 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assert(V:Val) ~> _ => .K </k>
       <exc> NoExc => AssertionError </exc>
       <exit-code> _ => 1 </exit-code>
       requires notBool truthy(V)
```

## 0055 reference-semantics/semantics/assert.k:13 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assert(ref(H:Int)) => Assert(V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0056 reference-semantics/semantics/assert.k:16 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0057 reference-semantics/semantics/bool.k:5 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-BOOL
```

## 0058 reference-semantics/semantics/bool.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0059 reference-semantics/semantics/bool.k:8 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyUn("not", V:Val) => notBool truthy(V)
```

## 0060 reference-semantics/semantics/bool.k:10 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", B1:Bool, B2:Bool) => B1 ==Bool B2
```

## 0061 reference-semantics/semantics/bool.k:11 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", B1:Bool, B2:Bool) => B1 =/=Bool B2
```

## 0062 reference-semantics/semantics/bool.k:16 [context]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  context BoolOp(_, (HOLE:Expr, _:Exprs))
```

## 0063 reference-semantics/semantics/bool.k:17 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp(_:String, (V:Val, .Exprs)) => V ... </k>
```

## 0064 reference-semantics/semantics/bool.k:18 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("and", (V:Val, A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       requires truthy(V)
```

## 0065 reference-semantics/semantics/bool.k:20 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("and", (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires notBool truthy(V)
```

## 0066 reference-semantics/semantics/bool.k:22 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("or",  (V:Val, _:Expr, _:Exprs)) => V ... </k>
       requires truthy(V)
```

## 0067 reference-semantics/semantics/bool.k:24 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("or",  (V:Val, A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       requires notBool truthy(V)
```

## 0068 reference-semantics/semantics/bool.k:29 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp(_:String, (ref(H:Int), .Exprs)) => ref(H) ... </k>
       [priority(40)]
```

## 0069 reference-semantics/semantics/bool.k:31 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("and", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("and", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 0070 reference-semantics/semantics/bool.k:35 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("and", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 0071 reference-semantics/semantics/bool.k:39 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("or", (ref(H:Int), _:Expr, _:Exprs)) => ref(H) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires truthy(V)
       [priority(40)]
```

## 0072 reference-semantics/semantics/bool.k:43 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BoolOp("or", (ref(H:Int), A:Expr, REST:Exprs)) => BoolOp("or", (A, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool truthy(V)
       [priority(40)]
```

## 0073 reference-semantics/semantics/bool.k:47 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0074 reference-semantics/semantics/builtins.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-BUILTINS
```

## 0075 reference-semantics/semantics/builtins.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0076 reference-semantics/semantics/builtins.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-STR
```

## 0077 reference-semantics/semantics/builtins.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SET
```

## 0078 reference-semantics/semantics/builtins.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0079 reference-semantics/semantics/builtins.k:8 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-RANGE
```

## 0080 reference-semantics/semantics/builtins.k:9 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-INT
```

## 0081 reference-semantics/semantics/builtins.k:10 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-METHODS
```

## 0082 reference-semantics/semantics/builtins.k:17 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= applyBuiltin(String, Vals) [function]
```

## 0083 reference-semantics/semantics/builtins.k:20 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= seqLen(Val) [function]
```

## 0084 reference-semantics/semantics/builtins.k:21 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("len", OBJ:Val, .Vals) => seqLen(OBJ)
```

## 0085 reference-semantics/semantics/builtins.k:22 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqLen(list(VS:ValSeq))                  => vsLen(VS)
```

## 0086 reference-semantics/semantics/builtins.k:23 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqLen(tuple(VS:ValSeq))                 => vsLen(VS)
```

## 0087 reference-semantics/semantics/builtins.k:24 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqLen(str(IS:IntSeq))                   => isLen(IS)
```

## 0088 reference-semantics/semantics/builtins.k:25 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqLen(setV(DS:IntSeq))                  => isLen(DS)
```

## 0089 reference-semantics/semantics/builtins.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqLen(rangeObj(LO:Int, HI:Int, ST:Int)) => rangeLen(LO, HI, ST)
```

## 0090 reference-semantics/semantics/builtins.k:32 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("list")), (list(VS:ValSeq),  .Vals)) => #alloc(list(VS)) ... </k>
```

## 0091 reference-semantics/semantics/builtins.k:33 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("list")), (tuple(VS:ValSeq), .Vals)) => #alloc(list(VS)) ... </k>
```

## 0092 reference-semantics/semantics/builtins.k:34 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("list")), .Vals)                     => #alloc(list(.ValSeq)) ... </k>
```

## 0093 reference-semantics/semantics/builtins.k:35 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("list")), (str(CS:IntSeq), .Vals))   => #alloc(list(charsOf(CS))) ... </k>
```

## 0094 reference-semantics/semantics/builtins.k:36 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= charsOf(IntSeq) [function, total]
```

## 0095 reference-semantics/semantics/builtins.k:37 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule charsOf(.IntSeq)                => .ValSeq
```

## 0096 reference-semantics/semantics/builtins.k:38 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule charsOf(iCons(C:Int, R:IntSeq)) => vCons(str(iCons(C, .IntSeq)), charsOf(R))
```

## 0097 reference-semantics/semantics/builtins.k:41 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("set", str(CS:IntSeq), .Vals) => setV(dedupCodes(CS))
```

## 0098 reference-semantics/semantics/builtins.k:44 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("abs", I:Int, .Vals) => absInt(I)
```

## 0099 reference-semantics/semantics/builtins.k:47 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #sumAcc(Iterable, Int) | #sumCont(Int)
```

## 0100 reference-semantics/semantics/builtins.k:48 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #sumAcc(IT:Iterable, ACC:Int) => #iterNext(IT) ~> #sumCont(ACC) ... </k>
```

## 0101 reference-semantics/semantics/builtins.k:49 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #sumCont(ACC:Int) => ACC ... </k>
```

## 0102 reference-semantics/semantics/builtins.k:50 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAcc(R, ACC +Int intOf(V)) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 0103 reference-semantics/semantics/builtins.k:54 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= intOf(Val) [function]
```

## 0104 reference-semantics/semantics/builtins.k:55 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intOf(I:Int)  => I
```

## 0105 reference-semantics/semantics/builtins.k:56 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intOf(B:Bool) => #if B #then 1 #else 0 #fi
```

## 0106 reference-semantics/semantics/builtins.k:59 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #allAcc(Iterable) | "#allCont"
```

## 0107 reference-semantics/semantics/builtins.k:60 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #allAcc(IT:Iterable) => #iterNext(IT) ~> #allCont ... </k>
```

## 0108 reference-semantics/semantics/builtins.k:61 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #allCont => true ... </k>
```

## 0109 reference-semantics/semantics/builtins.k:62 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #allCont => #allAcc(R) ... </k>
       requires truthy(V)
```

## 0110 reference-semantics/semantics/builtins.k:64 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #allCont => false ... </k>
       requires notBool truthy(V)
```

## 0111 reference-semantics/semantics/builtins.k:67 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #anyAcc(Iterable) | "#anyCont"
```

## 0112 reference-semantics/semantics/builtins.k:68 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #anyAcc(IT:Iterable) => #iterNext(IT) ~> #anyCont ... </k>
```

## 0113 reference-semantics/semantics/builtins.k:69 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #anyCont => false ... </k>
```

## 0114 reference-semantics/semantics/builtins.k:70 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, _:Iterable) ~> #anyCont => true ... </k>
       requires truthy(V)
```

## 0115 reference-semantics/semantics/builtins.k:72 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #anyCont => #anyAcc(R) ... </k>
       requires notBool truthy(V)
```

## 0116 reference-semantics/semantics/builtins.k:76 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #maxAcc0(Iterable) | "#maxCont0" | #maxAcc(Iterable, Int) | #maxCont(Int)
```

## 0117 reference-semantics/semantics/builtins.k:77 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #maxAcc0(IT:Iterable) => #iterNext(IT) ~> #maxCont0 ... </k>
```

## 0118 reference-semantics/semantics/builtins.k:78 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 0119 reference-semantics/semantics/builtins.k:80 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #maxAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #maxCont(M) ... </k>
```

## 0120 reference-semantics/semantics/builtins.k:81 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #maxCont(M:Int) => M ... </k>
```

## 0121 reference-semantics/semantics/builtins.k:82 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont(M:Int)
        => #maxAcc(R, maxInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 0122 reference-semantics/semantics/builtins.k:86 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #minAcc0(Iterable) | "#minCont0" | #minAcc(Iterable, Int) | #minCont(Int)
```

## 0123 reference-semantics/semantics/builtins.k:87 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #minAcc0(IT:Iterable) => #iterNext(IT) ~> #minCont0 ... </k>
```

## 0124 reference-semantics/semantics/builtins.k:88 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAcc(R, {V}:>Int) ... </k>
       requires isInt(V)
```

## 0125 reference-semantics/semantics/builtins.k:90 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #minAcc(IT:Iterable, M:Int) => #iterNext(IT) ~> #minCont(M) ... </k>
```

## 0126 reference-semantics/semantics/builtins.k:91 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #minCont(M:Int) => M ... </k>
```

## 0127 reference-semantics/semantics/builtins.k:92 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont(M:Int)
        => #minAcc(R, minInt(M, {V}:>Int)) ... </k>
       requires isInt(V)
```

## 0128 reference-semantics/semantics/builtins.k:97 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= maxVals(Int, Vals) [function]
```

## 0129 reference-semantics/semantics/builtins.k:98 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("max", I:Int, REST:Vals) => maxVals(I, REST)
```

## 0130 reference-semantics/semantics/builtins.k:99 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule maxVals(M:Int, .Vals)           => M
```

## 0131 reference-semantics/semantics/builtins.k:100 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule maxVals(M:Int, (I:Int, R:Vals)) => maxVals(maxInt(M, I), R)
```

## 0132 reference-semantics/semantics/builtins.k:102 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= minVals(Int, Vals) [function]
```

## 0133 reference-semantics/semantics/builtins.k:103 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("min", I:Int, REST:Vals) => minVals(I, REST)
```

## 0134 reference-semantics/semantics/builtins.k:104 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule minVals(M:Int, .Vals)           => M
```

## 0135 reference-semantics/semantics/builtins.k:105 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule minVals(M:Int, (I:Int, R:Vals)) => minVals(minInt(M, I), R)
```

## 0136 reference-semantics/semantics/builtins.k:108 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("bin", N:Int, .Vals) => str(iCons(48, iCons(98, binCodes(N))))
       requires N >=Int 0
```

## 0137 reference-semantics/semantics/builtins.k:111 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("bin", N:Int, .Vals)
    => str(iCons(45, iCons(48, iCons(98, binCodes(0 -Int N)))))
       requires N <Int 0
```

## 0138 reference-semantics/semantics/builtins.k:114 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= binCodes(Int) [function, total]
```

## 0139 reference-semantics/semantics/builtins.k:115 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule binCodes(0) => iCons(48, .IntSeq)
```

## 0140 reference-semantics/semantics/builtins.k:116 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule binCodes(N:Int) => binAcc(N, .IntSeq) requires N >Int 0
```

## 0141 reference-semantics/semantics/builtins.k:117 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= binAcc(Int, IntSeq) [function, total]
```

## 0142 reference-semantics/semantics/builtins.k:118 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule binAcc(0, ACC:IntSeq) => ACC
```

## 0143 reference-semantics/semantics/builtins.k:119 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule binAcc(N:Int, ACC:IntSeq)
    => binAcc((N -Int pyMod(N, 2)) /Int 2, iCons(48 +Int pyMod(N, 2), ACC))
       requires N >Int 0
```

## 0144 reference-semantics/semantics/builtins.k:124 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("enumerate")), (list(VS:ValSeq), .Vals))
        => #alloc(list(enumVS(VS, 0))) ... </k>
```

## 0145 reference-semantics/semantics/builtins.k:126 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= enumVS(ValSeq, Int) [function, total]
```

## 0146 reference-semantics/semantics/builtins.k:127 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule enumVS(.ValSeq, _:Int) => .ValSeq
```

## 0147 reference-semantics/semantics/builtins.k:128 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule enumVS(vCons(V:Val, R:ValSeq), I:Int)
    => vCons(tuple(vCons(I, vCons(V, .ValSeq))), enumVS(R, I +Int 1))
```

## 0148 reference-semantics/semantics/builtins.k:132 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("map")), (typeV("str"), list(VS:ValSeq), .Vals))
        => #alloc(list(mapStrVS(VS))) ... </k>
```

## 0149 reference-semantics/semantics/builtins.k:134 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= mapStrVS(ValSeq) [function, total]
```

## 0150 reference-semantics/semantics/builtins.k:135 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapStrVS(.ValSeq) => .ValSeq
```

## 0151 reference-semantics/semantics/builtins.k:136 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapStrVS(vCons(I:Int, R:ValSeq)) => vCons(str(strToCodes(Int2String(I))), mapStrVS(R))
```

## 0152 reference-semantics/semantics/builtins.k:137 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapStrVS(vCons(str(CS:IntSeq), R:ValSeq)) => vCons(str(CS), mapStrVS(R))
```

## 0153 reference-semantics/semantics/builtins.k:140 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("int", I:Int, .Vals) => I
```

## 0154 reference-semantics/semantics/builtins.k:143 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("ord", str(iCons(C:Int, .IntSeq)), .Vals) => C
```

## 0155 reference-semantics/semantics/builtins.k:144 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("chr", I:Int, .Vals) => str(iCons(I, .IntSeq))
       requires 0 <=Int I andBool I <Int 128
```

## 0156 reference-semantics/semantics/builtins.k:148 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("str", I:Int, .Vals)       => str(strToCodes(Int2String(I)))
```

## 0157 reference-semantics/semantics/builtins.k:149 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("str", str(CS:IntSeq), .Vals) => str(CS)
```

## 0158 reference-semantics/semantics/builtins.k:152 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("int", str(iCons(C:Int, .IntSeq)), .Vals) => C -Int 48
       requires 48 <=Int C andBool C <=Int 57
```

## 0159 reference-semantics/semantics/builtins.k:156 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("int", str(CS:IntSeq), .Vals) => intDigAcc(CS, 0)
       requires isLen(CS) >=Int 2
```

## 0160 reference-semantics/semantics/builtins.k:158 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= intDigAcc(IntSeq, Int) [function, total]
```

## 0161 reference-semantics/semantics/builtins.k:159 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intDigAcc(.IntSeq, ACC:Int)             => ACC
```

## 0162 reference-semantics/semantics/builtins.k:160 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intDigAcc(iCons(C:Int, R:IntSeq), ACC:Int) => intDigAcc(R, (ACC *Int 10) +Int (C -Int 48))
```

## 0163 reference-semantics/semantics/builtins.k:163 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("zip", list(A:ValSeq), list(B:ValSeq), .Vals) => zipObj(A, B)
```

## 0164 reference-semantics/semantics/builtins.k:164 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("zip", str(A:IntSeq), str(B:IntSeq), .Vals)   => zipObjS(A, B)
```

## 0165 reference-semantics/semantics/builtins.k:167 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObj(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq)))
        => #iterYield(tuple(vCons(A, vCons(B, .ValSeq))), zipObj(As, Bs)) ... </k>
```

## 0166 reference-semantics/semantics/builtins.k:169 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObj(.ValSeq, _:ValSeq))               => #iterDone ... </k>
```

## 0167 reference-semantics/semantics/builtins.k:170 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObj(vCons(_:Val, _:ValSeq), .ValSeq)) => #iterDone ... </k>
```

## 0168 reference-semantics/semantics/builtins.k:171 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObjS(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)))
        => #iterYield(tuple(vCons(str(iCons(A, .IntSeq)), vCons(str(iCons(B, .IntSeq)), .ValSeq))), zipObjS(As, Bs)) ... </k>
```

## 0169 reference-semantics/semantics/builtins.k:173 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObjS(.IntSeq, _:IntSeq))              => #iterDone ... </k>
```

## 0170 reference-semantics/semantics/builtins.k:174 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(zipObjS(iCons(_:Int, _:IntSeq), .IntSeq)) => #iterDone ... </k>
```

## 0171 reference-semantics/semantics/builtins.k:177 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("range", I:Int, .Vals)               => rangeObj(0, I, 1)
```

## 0172 reference-semantics/semantics/builtins.k:178 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("range", A:Int, B:Int, .Vals)        => rangeObj(A, B, 1)
```

## 0173 reference-semantics/semantics/builtins.k:179 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("range", A:Int, B:Int, S:Int, .Vals) => rangeObj(A, B, S)
       requires S =/=Int 0
```

## 0174 reference-semantics/semantics/builtins.k:187 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("eval", str(CS:IntSeq), .Vals) => evalArith(CS)
```

## 0175 reference-semantics/semantics/builtins.k:188 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= evalArith(IntSeq) [function]
```

## 0176 reference-semantics/semantics/builtins.k:189 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evalArith(CS:IntSeq)
    => firstNdE(passAddE(passMulE(passPowE(tokOps(CS), tokNds(CS)))))
```

## 0177 reference-semantics/semantics/builtins.k:192 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax OpSeq ::= ".OpSeq" | oCons(String, OpSeq)
```

## 0178 reference-semantics/semantics/builtins.k:194 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= evDigit(Int) [function, total]
```

## 0179 reference-semantics/semantics/builtins.k:195 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evDigit(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 0180 reference-semantics/semantics/builtins.k:196 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= evHead42(IntSeq) [function, total]
```

## 0181 reference-semantics/semantics/builtins.k:197 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evHead42(iCons(42, _:IntSeq)) => true
```

## 0182 reference-semantics/semantics/builtins.k:198 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evHead42(_:IntSeq)            => false [owise]
```

## 0183 reference-semantics/semantics/builtins.k:199 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= evHead47(IntSeq) [function, total]
```

## 0184 reference-semantics/semantics/builtins.k:200 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evHead47(iCons(47, _:IntSeq)) => true
```

## 0185 reference-semantics/semantics/builtins.k:201 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule evHead47(_:IntSeq)            => false [owise]
```

## 0186 reference-semantics/semantics/builtins.k:203 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax OpSeq ::= tokOps(IntSeq) [function, total]
```

## 0187 reference-semantics/semantics/builtins.k:204 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(.IntSeq)                 => .OpSeq
```

## 0188 reference-semantics/semantics/builtins.k:205 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(32, R:IntSeq))     => tokOps(R)
```

## 0189 reference-semantics/semantics/builtins.k:206 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(C:Int, R:IntSeq))  => tokOps(R) requires evDigit(C)
```

## 0190 reference-semantics/semantics/builtins.k:207 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(42, iCons(42, R:IntSeq))) => oCons("**", tokOps(R))
```

## 0191 reference-semantics/semantics/builtins.k:208 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(42, R:IntSeq))     => oCons("*", tokOps(R)) requires notBool evHead42(R)
```

## 0192 reference-semantics/semantics/builtins.k:209 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(47, iCons(47, R:IntSeq))) => oCons("//", tokOps(R))
```

## 0193 reference-semantics/semantics/builtins.k:210 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(47, R:IntSeq))     => oCons("/", tokOps(R)) requires notBool evHead47(R)
```

## 0194 reference-semantics/semantics/builtins.k:211 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(43, R:IntSeq))     => oCons("+", tokOps(R))
```

## 0195 reference-semantics/semantics/builtins.k:212 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokOps(iCons(45, R:IntSeq))     => oCons("-", tokOps(R))
```

## 0196 reference-semantics/semantics/builtins.k:214 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= tokNds(IntSeq) [function, total]
                  | tokNdAcc(Int, IntSeq) [function, total]
```

## 0197 reference-semantics/semantics/builtins.k:216 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNds(.IntSeq)                => .IntSeq
```

## 0198 reference-semantics/semantics/builtins.k:217 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNds(iCons(32, R:IntSeq))    => tokNds(R)
```

## 0199 reference-semantics/semantics/builtins.k:218 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNdAcc(C -Int 48, R) requires evDigit(C)
```

## 0200 reference-semantics/semantics/builtins.k:219 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNds(iCons(C:Int, R:IntSeq)) => tokNds(R)
       requires notBool evDigit(C) andBool C =/=Int 32
```

## 0201 reference-semantics/semantics/builtins.k:221 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNdAcc(A:Int, iCons(C:Int, R:IntSeq)) => tokNdAcc(A *Int 10 +Int (C -Int 48), R)
       requires evDigit(C)
```

## 0202 reference-semantics/semantics/builtins.k:223 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule tokNdAcc(A:Int, S:IntSeq) => iCons(A, tokNds(S)) [owise]
```

## 0203 reference-semantics/semantics/builtins.k:225 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= evp(OpSeq, IntSeq)
```

## 0204 reference-semantics/semantics/builtins.k:226 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= firstNdE(EvPair) [function, total]
```

## 0205 reference-semantics/semantics/builtins.k:227 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule firstNdE(evp(_:OpSeq, iCons(N:Int, _:IntSeq))) => N
```

## 0206 reference-semantics/semantics/builtins.k:228 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule firstNdE(_:EvPair) => 0 [owise]
```

## 0207 reference-semantics/semantics/builtins.k:230 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= applyOpE(String, Int, Int) [function, total]
```

## 0208 reference-semantics/semantics/builtins.k:231 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE("+",  A:Int, B:Int) => A +Int B
```

## 0209 reference-semantics/semantics/builtins.k:232 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE("-",  A:Int, B:Int) => A -Int B
```

## 0210 reference-semantics/semantics/builtins.k:233 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE("*",  A:Int, B:Int) => A *Int B
```

## 0211 reference-semantics/semantics/builtins.k:234 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE("//", A:Int, B:Int) => A divInt B
```

## 0212 reference-semantics/semantics/builtins.k:235 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE("**", A:Int, B:Int) => A ^Int B
```

## 0213 reference-semantics/semantics/builtins.k:236 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyOpE(_:String, A:Int, _:Int) => A [owise]
```

## 0214 reference-semantics/semantics/builtins.k:238 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= passPowE(OpSeq, IntSeq) [function, total]
```

## 0215 reference-semantics/semantics/builtins.k:239 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passPowE(.OpSeq, NDS:IntSeq) => evp(.OpSeq, NDS)
```

## 0216 reference-semantics/semantics/builtins.k:240 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passPowE(oCons("**", OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCombE(N, passPowE(OPS, NDS))
```

## 0217 reference-semantics/semantics/builtins.k:241 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passPowE(oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq)) => powCarryE(O, N, passPowE(OPS, NDS))
       requires O =/=String "**"
```

## 0218 reference-semantics/semantics/builtins.k:243 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passPowE(_:OpSeq, .IntSeq) => evp(.OpSeq, .IntSeq) [owise]
```

## 0219 reference-semantics/semantics/builtins.k:244 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= powCombE(Int, EvPair) [function, total]
```

## 0220 reference-semantics/semantics/builtins.k:245 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule powCombE(N:Int, evp(OPS:OpSeq, iCons(M:Int, REST:IntSeq))) => evp(OPS, iCons(N ^Int M, REST))
```

## 0221 reference-semantics/semantics/builtins.k:246 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule powCombE(N:Int, evp(OPS:OpSeq, .IntSeq)) => evp(OPS, iCons(N, .IntSeq))
```

## 0222 reference-semantics/semantics/builtins.k:247 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= powCarryE(String, Int, EvPair) [function, total]
```

## 0223 reference-semantics/semantics/builtins.k:248 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule powCarryE(O:String, N:Int, evp(OPS:OpSeq, NDS:IntSeq)) => evp(oCons(O, OPS), iCons(N, NDS))
```

## 0224 reference-semantics/semantics/builtins.k:250 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= passMulE(EvPair) [function, total] | passAddE(EvPair) [function, total]
```

## 0225 reference-semantics/semantics/builtins.k:251 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passMulE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("mul", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 0226 reference-semantics/semantics/builtins.k:252 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passMulE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 0227 reference-semantics/semantics/builtins.k:253 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passAddE(evp(OPS:OpSeq, iCons(N0:Int, NDS:IntSeq))) => passLGoE("add", N0, OPS, NDS, .OpSeq, .IntSeq)
```

## 0228 reference-semantics/semantics/builtins.k:254 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passAddE(evp(OPS:OpSeq, .IntSeq)) => evp(OPS, .IntSeq)
```

## 0229 reference-semantics/semantics/builtins.k:255 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax EvPair ::= passLGoE(String, Int, OpSeq, IntSeq, OpSeq, IntSeq) [function, total]
```

## 0230 reference-semantics/semantics/builtins.k:256 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passLGoE(_:String, CUR:Int, .OpSeq, _:IntSeq, OO:OpSeq, ON:IntSeq) => evp(OO, appendIE(ON, CUR))
```

## 0231 reference-semantics/semantics/builtins.k:257 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, applyOpE(O, CUR, N), OPS, NDS, OO, ON)
       requires inLevelE(L, O)
```

## 0232 reference-semantics/semantics/builtins.k:260 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passLGoE(L:String, CUR:Int, oCons(O:String, OPS:OpSeq), iCons(N:Int, NDS:IntSeq), OO:OpSeq, ON:IntSeq)
    => passLGoE(L, N, OPS, NDS, appendOpE(OO, O), appendIE(ON, CUR))
       requires notBool inLevelE(L, O)
```

## 0233 reference-semantics/semantics/builtins.k:263 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule passLGoE(_:String, CUR:Int, oCons(_:String, _:OpSeq), .IntSeq, OO:OpSeq, ON:IntSeq)
    => evp(OO, appendIE(ON, CUR)) [owise]
```

## 0234 reference-semantics/semantics/builtins.k:265 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= inLevelE(String, String) [function, total]
```

## 0235 reference-semantics/semantics/builtins.k:266 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule inLevelE("mul", O:String) => O ==String "*" orBool O ==String "//" orBool O ==String "/"
```

## 0236 reference-semantics/semantics/builtins.k:267 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule inLevelE("add", O:String) => O ==String "+" orBool O ==String "-"
```

## 0237 reference-semantics/semantics/builtins.k:268 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule inLevelE(_:String, _:String) => false [owise]
```

## 0238 reference-semantics/semantics/builtins.k:269 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax OpSeq ::= appendOpE(OpSeq, String) [function, total]
```

## 0239 reference-semantics/semantics/builtins.k:270 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendOpE(.OpSeq, O:String) => oCons(O, .OpSeq)
```

## 0240 reference-semantics/semantics/builtins.k:271 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendOpE(oCons(H:String, T:OpSeq), O:String) => oCons(H, appendOpE(T, O))
```

## 0241 reference-semantics/semantics/builtins.k:272 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= appendIE(IntSeq, Int) [function, total]
```

## 0242 reference-semantics/semantics/builtins.k:273 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendIE(.IntSeq, N:Int) => iCons(N, .IntSeq)
```

## 0243 reference-semantics/semantics/builtins.k:274 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendIE(iCons(H:Int, T:IntSeq), N:Int) => iCons(H, appendIE(T, N))
```

## 0244 reference-semantics/semantics/builtins.k:279 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= "#md5"
```

## 0245 reference-semantics/semantics/builtins.k:280 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Attribute(Name("hashlib"), "md5"), (E:Expr, .Exprs)) => E ~> #md5 ... </k>
       [priority(40)]
```

## 0246 reference-semantics/semantics/builtins.k:282 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> str(CS:IntSeq) ~> #md5 => md5Obj(CS) ... </k>
```

## 0247 reference-semantics/semantics/builtins.k:283 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= md5Obj(IntSeq)
```

## 0248 reference-semantics/semantics/builtins.k:284 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(md5Obj(CS:IntSeq), "hexdigest", .Vals) => str(md5hexCodes(CS))
```

## 0249 reference-semantics/semantics/builtins.k:285 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax IntSeq ::= md5hexCodes(IntSeq) [function, total, symbol(md5hexCodes), no-evaluators]
```

## 0250 reference-semantics/semantics/builtins.k:291 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("isinstance", V:Val, typeV("int"), .Vals) => isIntV(V)
```

## 0251 reference-semantics/semantics/builtins.k:292 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("isinstance", V:Val, typeV("str"), .Vals) => isStrV(V)
```

## 0252 reference-semantics/semantics/builtins.k:293 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isIntV(Val) [function] | isStrV(Val) [function]
```

## 0253 reference-semantics/semantics/builtins.k:294 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isIntV(_:Int)         => true
```

## 0254 reference-semantics/semantics/builtins.k:295 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isIntV(_:Val)         => false [owise]
```

## 0255 reference-semantics/semantics/builtins.k:296 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isStrV(str(_:IntSeq)) => true
```

## 0256 reference-semantics/semantics/builtins.k:297 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isStrV(_:Val)         => false [owise]
```

## 0257 reference-semantics/semantics/builtins.k:298 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0258 reference-semantics/semantics/call.k:10 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-CALL
```

## 0259 reference-semantics/semantics/call.k:11 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-METHODS
```

## 0260 reference-semantics/semantics/call.k:12 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-BUILTINS
```

## 0261 reference-semantics/semantics/call.k:13 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-FUNCTIONS
```

## 0262 reference-semantics/semantics/call.k:16 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Attribute(V:Val, M:String) => boundMethodV(V, M) ... </k>
```

## 0263 reference-semantics/semantics/call.k:19 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #callee(Exprs)
```

## 0264 reference-semantics/semantics/call.k:20 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Fe:Expr, ARGS:Exprs) => Fe ~> #callee(ARGS) ... </k> [owise]
```

## 0265 reference-semantics/semantics/call.k:21 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> CV:Val ~> #callee(ARGS:Exprs) => #evalArgs(ARGS, .Vals, toCall(CV)) ... </k>
```

## 0266 reference-semantics/semantics/call.k:24 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), ACC:Vals) => applyMethod(OBJ, M, ACC) ... </k>
```

## 0267 reference-semantics/semantics/call.k:26 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sum")), (OBJ:Iterable, .Vals)) => #sumAcc(OBJ, 0) ... </k>
```

## 0268 reference-semantics/semantics/call.k:27 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("all")), (OBJ:Iterable, .Vals)) => #allAcc(OBJ)    ... </k>
```

## 0269 reference-semantics/semantics/call.k:28 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("any")), (OBJ:Iterable, .Vals)) => #anyAcc(OBJ)    ... </k>
```

## 0270 reference-semantics/semantics/call.k:29 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("max")), (OBJ:Iterable, .Vals)) => #maxAcc0(OBJ)   ... </k>
```

## 0271 reference-semantics/semantics/call.k:30 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("min")), (OBJ:Iterable, .Vals)) => #minAcc0(OBJ)   ... </k>
```

## 0272 reference-semantics/semantics/call.k:31 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV(BN:String)), ACC:Vals) => applyBuiltin(BN, ACC) ... </k> [owise]
```

## 0273 reference-semantics/semantics/call.k:32 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(typeV(T:String)),     ACC:Vals) => applyBuiltin(T, ACC)  ... </k>
```

## 0274 reference-semantics/semantics/call.k:38 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0275 reference-semantics/semantics/call.k:42 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV(BN:String)), (A:Val, ref(H:Int), REST:Vals))
        => #applyK(toCall(builtinV(BN)), (A, V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(A)
       [priority(40)]
```

## 0276 reference-semantics/semantics/call.k:47 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(typeV(T:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(typeV(T)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0277 reference-semantics/semantics/call.k:52 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isMutMethod(String) [function, total]
```

## 0278 reference-semantics/semantics/call.k:53 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isMutMethod(M:String)
    => M ==String "append" orBool M ==String "sort" orBool M ==String "extend"
       orBool M ==String "insert" orBool M ==String "pop" orBool M ==String "remove"
```

## 0279 reference-semantics/semantics/call.k:56 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), M:String)), ACC:Vals)
        => #applyK(toCall(boundMethodV(V, M)), ACC) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M)
       [priority(40)]
```

## 0280 reference-semantics/semantics/call.k:63 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(OBJ:Val, M:String)), (ref(H:Int), REST:Vals))
        => #applyK(toCall(boundMethodV(OBJ, M)), (V, REST)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isMutMethod(M) andBool notBool isRefV(OBJ)
       [priority(40)]
```

## 0281 reference-semantics/semantics/call.k:69 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals) ~> CONT
        => #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(.Map, parent(DEFL)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 0282 reference-semantics/semantics/call.k:80 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(closureValC(PNS:ParamNames, CVS:ParamNames, BODY:Stmts, CM:Map)), ACC:Vals) ~> CONT
        => #allocCells(CVS) ~> #bindP(PNS, ACC) ~> BODY ~> #endcall </k>
       <env>     CALLERL:Int => NEWL </env>
       <scopes>   STORE:Map => STORE [ NEWL <- scope(CM [ "$cells" <- cellsMark(CVS) ], parent(0)) ] </scopes>
       <scopeLoc> NEWL:Int => NEWL +Int 1 </scopeLoc>
       <stack>   .List => ListItem(frame(CONT, CALLERL, NEWL)) ... </stack>
```

## 0283 reference-semantics/semantics/call.k:87 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #allocCells(ParamNames)
```

## 0284 reference-semantics/semantics/call.k:88 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #allocCells(.ParamNames) => .K ... </k>
```

## 0285 reference-semantics/semantics/call.k:89 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #allocCells((CV:String, R:ParamNames)) => #allocCells(R) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ CV <- cellRef(N) ], _) ... </scopes>
       <heap>    H:Map => (N |-> cellV(noneV)) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 0286 reference-semantics/semantics/call.k:95 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0287 reference-semantics/semantics/comprehension.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-COMPREHENSION
```

## 0288 reference-semantics/semantics/comprehension.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0289 reference-semantics/semantics/comprehension.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-OPERATORS
```

## 0290 reference-semantics/semantics/comprehension.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-LIST
```

## 0291 reference-semantics/semantics/comprehension.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CONTROLS
```

## 0292 reference-semantics/semantics/comprehension.k:8 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-FUNCTIONS
```

## 0293 reference-semantics/semantics/comprehension.k:11 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule ListComp(ELT:Expr, Gs:CompFors) => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 0294 reference-semantics/semantics/comprehension.k:12 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule GenExp(ELT:Expr, Gs:CompFors)   => Call(closureExpr(.ParamNames, compBody(Gs, ELT)), .Exprs)
```

## 0295 reference-semantics/semantics/comprehension.k:14 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Stmts ::= compBody(CompFors, Expr) [macro]
```

## 0296 reference-semantics/semantics/comprehension.k:15 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule compBody(Gs:CompFors, ELT:Expr)
    => Assign(Name("$acc"), ListExpr(.Exprs)) compNest(Gs, ELT) Return(Name("$acc"))
```

## 0297 reference-semantics/semantics/comprehension.k:18 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Stmt ::= compNest(CompFors, Expr) [macro-rec]
```

## 0298 reference-semantics/semantics/comprehension.k:19 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule compNest(.CompFors, ELT:Expr)
    => Assign(Name("$acc"), BinOp("+", Name("$acc"), ListExpr(ELT)))
```

## 0299 reference-semantics/semantics/comprehension.k:21 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule compNest((CompFor(T:Expr, ITER:Expr, Fs:Exprs) GRest:CompFors), ELT:Expr)
    => For(T, ITER, If(compGuard(Fs), compNest(GRest, ELT), .Stmts))
```

## 0300 reference-semantics/semantics/comprehension.k:24 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Expr ::= compGuard(Exprs) [macro]
```

## 0301 reference-semantics/semantics/comprehension.k:25 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule compGuard(.Exprs)             => Bool(true)
```

## 0302 reference-semantics/semantics/comprehension.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule compGuard((F:Expr, Fs:Exprs)) => BoolOp("and", (F, Fs))
```

## 0303 reference-semantics/semantics/comprehension.k:27 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0304 reference-semantics/semantics/concrete.k:8 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-CONCRETE
```

## 0305 reference-semantics/semantics/concrete.k:9 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY
```

## 0306 reference-semantics/semantics/concrete.k:13 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq))) => deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 0307 reference-semantics/semantics/concrete.k:16 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(list(A:ValSeq), CmpOp("!=", list(B:ValSeq))) => notBool deepEqVS(A, B, HP) ... </k>
       <heap> HP:Map </heap>
       requires hasRefVS(A) orBool hasRefVS(B)
```

## 0308 reference-semantics/semantics/concrete.k:25 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= kvP(Val, Val)
```

## 0309 reference-semantics/semantics/concrete.k:26 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #ksort(ValSeq, Val, ValSeq, Bool)
                 | #ksIns(Val, ValSeq, Val, ValSeq, Bool)
```

## 0310 reference-semantics/semantics/concrete.k:28 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #ksort(VS, KV, .ValSeq, false) ... </k>
       [priority(40)]
```

## 0311 reference-semantics/semantics/concrete.k:31 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #ksort(VS, KV, .ValSeq, RB) ... </k>
       [priority(40)]
```

## 0312 reference-semantics/semantics/concrete.k:34 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #ksort(.ValSeq, _:Val, ACC:ValSeq, RB:Bool)
        => #alloc(list(condRev(unpairVS(ACC), RB))) ... </k>
```

## 0313 reference-semantics/semantics/concrete.k:36 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #ksort(vCons(V:Val, R:ValSeq), KV:Val, ACC:ValSeq, RB:Bool)
        => KV ~> #callee((V, .Exprs)) ~> #ksIns(V, R, KV, ACC, RB) ... </k>
```

## 0314 reference-semantics/semantics/concrete.k:38 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> K:Val ~> #ksIns(V:Val, R:ValSeq, KV:Val, ACC:ValSeq, RB:Bool)
        => #ksort(R, KV, insPair(ACC, K, V), RB) ... </k>
       requires notBool isKwV(K)
```

## 0315 reference-semantics/semantics/concrete.k:42 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= insPair(ValSeq, Val, Val) [function]
```

## 0316 reference-semantics/semantics/concrete.k:43 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule insPair(.ValSeq, K:Val, V:Val) => vCons(kvP(K, V), .ValSeq)
```

## 0317 reference-semantics/semantics/concrete.k:44 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K, V), vCons(kvP(K2, V2), R))
       requires kLt(K, K2)
```

## 0318 reference-semantics/semantics/concrete.k:47 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule insPair(vCons(kvP(K2:Val, V2:Val), R:ValSeq), K:Val, V:Val)
    => vCons(kvP(K2, V2), insPair(R, K, V))
       requires notBool kLt(K, K2)
```

## 0319 reference-semantics/semantics/concrete.k:51 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= kLt(Val, Val) [function]
```

## 0320 reference-semantics/semantics/concrete.k:52 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule kLt(I1:Int, I2:Int)             => I1 <Int I2
```

## 0321 reference-semantics/semantics/concrete.k:53 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule kLt(F1:Float, F2:Float)         => F1 <Float F2
```

## 0322 reference-semantics/semantics/concrete.k:54 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule kLt(str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 0323 reference-semantics/semantics/concrete.k:56 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= unpairVS(ValSeq) [function, total]
```

## 0324 reference-semantics/semantics/concrete.k:57 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule unpairVS(.ValSeq) => .ValSeq
```

## 0325 reference-semantics/semantics/concrete.k:58 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule unpairVS(vCons(kvP(_:Val, V:Val), R:ValSeq)) => vCons(V, unpairVS(R))
```

## 0326 reference-semantics/semantics/concrete.k:59 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule unpairVS(vCons(V:Val, R:ValSeq)) => vCons(V, unpairVS(R)) [owise]
```

## 0327 reference-semantics/semantics/concrete.k:60 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0328 reference-semantics/semantics/controls.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-CONTROLS
```

## 0329 reference-semantics/semantics/controls.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0330 reference-semantics/semantics/controls.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-TUPLE
```

## 0331 reference-semantics/semantics/controls.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0332 reference-semantics/semantics/controls.k:9 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 0333 reference-semantics/semantics/controls.k:12 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 0334 reference-semantics/semantics/controls.k:20 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- applyBin(OP, {M[X]}:>Val, V) ], _) ... </scopes>
       requires X in_keys(M)
```

## 0335 reference-semantics/semantics/controls.k:27 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> AugAssign(Name(X:String), OP:String, V:Val) => Assign(Name(X), BinOp(OP, Name(X), V)) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
       [priority(40)]
```

## 0336 reference-semantics/semantics/controls.k:35 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ImportFrom("math", NS:ParamNames) => #bindImports(NS) ... </k>
```

## 0337 reference-semantics/semantics/controls.k:36 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ImportFrom(_:String, _:ParamNames) => .K ... </k> [owise]
```

## 0338 reference-semantics/semantics/controls.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #bindImports(ParamNames)
```

## 0339 reference-semantics/semantics/controls.k:38 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindImports(.ParamNames) => .K ... </k>
```

## 0340 reference-semantics/semantics/controls.k:39 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ N <- builtinV(N) ], _) ... </scopes>
       requires N ==String "floor" orBool N ==String "ceil"
```

## 0341 reference-semantics/semantics/controls.k:43 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindImports((N:String, NS:ParamNames)) => #bindImports(NS) ... </k>
       requires notBool (N ==String "floor" orBool N ==String "ceil")
```

## 0342 reference-semantics/semantics/controls.k:48 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Expr(_:Val) => .K ... </k>
```

## 0343 reference-semantics/semantics/controls.k:51 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #branch(Bool, Stmts, Stmts)
```

## 0344 reference-semantics/semantics/controls.k:52 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> If(C:Val, T:Stmts, E:Stmts) => #branch(truthy(C), T, E) ... </k>
```

## 0345 reference-semantics/semantics/controls.k:53 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #branch(true,  T:Stmts, _:Stmts) => T ... </k>
```

## 0346 reference-semantics/semantics/controls.k:54 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #branch(false, _:Stmts, E:Stmts) => E ... </k>
```

## 0347 reference-semantics/semantics/controls.k:57 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> IfExp(V:Val, T:Expr, _:Expr) => T ... </k>
       requires truthy(V)
```

## 0348 reference-semantics/semantics/controls.k:59 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> IfExp(V:Val, _:Expr, E:Expr) => E ... </k>
       requires notBool truthy(V)
```

## 0349 reference-semantics/semantics/controls.k:65 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #loop(Val, Expr, Stmts) | #loopStep(Expr, Stmts)
                 | #while(Expr, Stmts) | #whileCond(Expr, Stmts)
                 | #loopLbl(K) | "#cont" | "#brk"
```

## 0350 reference-semantics/semantics/controls.k:69 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> For(T:Expr, OBJ:Val, B:Stmts) => #loop(OBJ, T, B) ... </k>
```

## 0351 reference-semantics/semantics/controls.k:71 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #loop(IT:Iterable, T:Expr, B:Stmts) => #iterNext(IT) ~> #loopStep(T, B) ... </k>
```

## 0352 reference-semantics/semantics/controls.k:72 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #loopStep(_:Expr, _:Stmts) => .K ... </k>
```

## 0353 reference-semantics/semantics/controls.k:73 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, REST:Iterable) ~> #loopStep(T:Expr, B:Stmts)
        => #bindTgt(T, V) ~> B ~> #loopLbl(#loop(REST, T, B)) ... </k>
```

## 0354 reference-semantics/semantics/controls.k:77 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> While(C:Expr, B:Stmts) => #while(C, B) ... </k>
```

## 0355 reference-semantics/semantics/controls.k:78 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #while(C:Expr, B:Stmts) => C ~> #whileCond(C, B) ... </k>
```

## 0356 reference-semantics/semantics/controls.k:79 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #whileCond(C:Expr, B:Stmts) => B ~> #loopLbl(#while(C, B)) ... </k>
       requires truthy(V)
```

## 0357 reference-semantics/semantics/controls.k:81 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #whileCond(_C:Expr, _B:Stmts) => .K ... </k>
       requires notBool truthy(V)
```

## 0358 reference-semantics/semantics/controls.k:85 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 0359 reference-semantics/semantics/controls.k:86 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Continue => #cont ... </k>
```

## 0360 reference-semantics/semantics/controls.k:87 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Break => #brk ... </k>
```

## 0361 reference-semantics/semantics/controls.k:88 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #cont ~> #loopLbl(NEXT:K) => NEXT ... </k>
```

## 0362 reference-semantics/semantics/controls.k:89 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #cont ~> (_:KItem => .K) ... </k> [owise]
```

## 0363 reference-semantics/semantics/controls.k:90 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #brk ~> #loopLbl(_:K) => .K ... </k>
```

## 0364 reference-semantics/semantics/controls.k:91 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #brk ~> (_:KItem => .K) ... </k> [owise]
```

## 0365 reference-semantics/semantics/controls.k:95 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> If(ref(H:Int), T:Stmts, E:Stmts) => If(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0366 reference-semantics/semantics/controls.k:98 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> IfExp(ref(H:Int), T:Expr, E:Expr) => IfExp(V, T, E) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0367 reference-semantics/semantics/controls.k:101 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ref(H:Int) ~> #whileCond(C:Expr, B:Stmts) => V ~> #whileCond(C, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0368 reference-semantics/semantics/controls.k:106 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> For(T:Expr, ref(H:Int), B:Stmts) => For(T, V, B) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0369 reference-semantics/semantics/controls.k:109 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0370 reference-semantics/semantics/core.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-CORE
```

## 0371 reference-semantics/semantics/core.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SYNTAX
```

## 0372 reference-semantics/semantics/core.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports INT
```

## 0373 reference-semantics/semantics/core.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports BOOL
```

## 0374 reference-semantics/semantics/core.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports STRING
```

## 0375 reference-semantics/semantics/core.k:8 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MAP
```

## 0376 reference-semantics/semantics/core.k:9 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports LIST
```

## 0377 reference-semantics/semantics/core.k:10 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports K-EQUAL
```

## 0378 reference-semantics/semantics/core.k:13 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
```

## 0379 reference-semantics/semantics/core.k:14 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)
```

## 0380 reference-semantics/semantics/core.k:15 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Str    ::= str(IntSeq)
```

## 0381 reference-semantics/semantics/core.k:18 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Iterable ::= list(ValSeq)
                    | tuple(ValSeq)
                    | Str
                    | rangeObj(Int, Int, Int)
                    | zipObj(ValSeq, ValSeq)
                    | zipObjS(IntSeq, IntSeq)
```

## 0382 reference-semantics/semantics/core.k:25 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val      ::= Int
                    | Bool
                    | "noneV"
                    | Iterable
                    | ref(Int)          // a heap object: <heap> holds its list(VS)
                    | cellRef(Int)      // a closure cell: <heap> holds cellV(V)
                    | closureVal(ParamNames, Stmts, Int)
                    | typeV(String)     // a type object (int/str), resolved from the builtins frame
                    | builtinV(String)  // a builtin function, resolved like any name (LEGB fallthrough)
                    | boundMethodV(Val, String)   // a cooled Attribute: obj.method
```

## 0383 reference-semantics/semantics/core.k:36 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Parent   ::= "root" | parent(Int)
```

## 0384 reference-semantics/semantics/core.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Scope    ::= scope(Map, Parent)
```

## 0385 reference-semantics/semantics/core.k:38 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KResult  ::= Val
```

## 0386 reference-semantics/semantics/core.k:39 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Expr     ::= Val   // cooling puts results back into expression holes
```

## 0387 reference-semantics/semantics/core.k:40 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Vals     ::= List{Val, ","}
```

## 0388 reference-semantics/semantics/core.k:41 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Exc      ::= "NoExc" | "AssertionError"
```

## 0389 reference-semantics/semantics/core.k:42 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax RetState ::= "noRet" | retV(Val)
```

## 0390 reference-semantics/semantics/core.k:49 [configuration]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  configuration
    <k>       #loadAll($PGM:Module) </k>
    <env>     0 </env>
    <scopes>   0     |-> scope(.Map, parent(-1))
              -1    |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>    .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>   .List </stack>
    <ret>     noRet </ret>
    <exc>     NoExc </exc>
    <exit-code exit=""> 0 </exit-code>
```

## 0391 reference-semantics/semantics/core.k:68 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isRefV(Val) [function, total]
```

## 0392 reference-semantics/semantics/core.k:69 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isRefV(ref(_:Int)) => true
```

## 0393 reference-semantics/semantics/core.k:70 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isRefV(_:Val)      => false [owise]
```

## 0394 reference-semantics/semantics/core.k:75 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax HeapVal ::= cellV(Val)
```

## 0395 reference-semantics/semantics/core.k:76 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isCellRef(Val) [function, total]
```

## 0396 reference-semantics/semantics/core.k:77 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isCellRef(cellRef(_:Int)) => true
```

## 0397 reference-semantics/semantics/core.k:78 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isCellRef(_:Val)          => false [owise]
```

## 0398 reference-semantics/semantics/core.k:85 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> cellRef(H:Int) => V ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires "$cells" in_keys(M)
       [priority(40)]
```

## 0399 reference-semantics/semantics/core.k:95 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= kwV(String, Val)
```

## 0400 reference-semantics/semantics/core.k:96 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #kwTag(String)
```

## 0401 reference-semantics/semantics/core.k:97 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> KwArg(N:String, E:Expr) => E ~> #kwTag(N) ... </k>
```

## 0402 reference-semantics/semantics/core.k:98 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #kwTag(N:String) => kwV(N, V) ... </k>
       requires notBool isKwV(V)
```

## 0403 reference-semantics/semantics/core.k:100 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isKwV(Val) [function, total]
```

## 0404 reference-semantics/semantics/core.k:101 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isKwV(kwV(_:String, _:Val)) => true
```

## 0405 reference-semantics/semantics/core.k:102 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isKwV(_:Val)                => false [owise]
```

## 0406 reference-semantics/semantics/core.k:106 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= cellsMark(ParamNames)
```

## 0407 reference-semantics/semantics/core.k:107 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ParamNames ::= cellsOf(Val) [function]
```

## 0408 reference-semantics/semantics/core.k:108 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cellsOf(cellsMark(CVS:ParamNames)) => CVS
```

## 0409 reference-semantics/semantics/core.k:109 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= pnMember(String, ParamNames) [function, total]
```

## 0410 reference-semantics/semantics/core.k:110 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule pnMember(_:String, .ParamNames) => false
```

## 0411 reference-semantics/semantics/core.k:111 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule pnMember(X:String, (P:String, R:ParamNames)) => X ==String P orBool pnMember(X, R)
```

## 0412 reference-semantics/semantics/core.k:113 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #cellW(Val, Val)
```

## 0413 reference-semantics/semantics/core.k:114 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #cellW(cellRef(H:Int), V:Val) => .K ... </k>
       <heap> ... H |-> cellV(_:Val => V) ... </heap>
```

## 0414 reference-semantics/semantics/core.k:117 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #alloc(Val)
```

## 0415 reference-semantics/semantics/core.k:118 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #alloc(V:Val) => ref(N) ... </k>
       <heap>    H:Map => (N |-> V) H </heap>
       <heapLoc> N:Int => N +Int 1 </heapLoc>
       requires notBool N in_keys(H)
```

## 0416 reference-semantics/semantics/core.k:124 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #loadAll(Module)
```

## 0417 reference-semantics/semantics/core.k:125 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #loadAll(Module(SS:Stmts)) => SS ... </k>
```

## 0418 reference-semantics/semantics/core.k:126 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> (S:Stmt SS:Stmts):Stmts => S ~> SS ... </k>
```

## 0419 reference-semantics/semantics/core.k:127 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> .Stmts => .K ... </k>
```

## 0420 reference-semantics/semantics/core.k:130 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #look(String, Int)
```

## 0421 reference-semantics/semantics/core.k:131 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Name(X:String) => #look(X, L) ... </k> <env> L:Int </env>
```

## 0422 reference-semantics/semantics/core.k:132 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #look(X:String, L:Int) => {M[X]}:>Val ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires X in_keys(M)
```

## 0423 reference-semantics/semantics/core.k:145 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #look(X:String, L:Int) => V ... </k>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       <heap> ... H |-> cellV(V:Val) ... </heap>
       requires X in_keys(M) andBool "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool {M[X]}:>Val ==K cellRef(H)
       [priority(40)]
```

## 0424 reference-semantics/semantics/core.k:152 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #look(X:String, L:Int) => #look(X, P) ... </k>
       <scopes> ... L |-> scope(M:Map, parent(P:Int)) ... </scopes>
       requires notBool (X in_keys(M))
```

## 0425 reference-semantics/semantics/core.k:157 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Scope ::= "builtinsScope" [function, total]
```

## 0426 reference-semantics/semantics/core.k:158 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule builtinsScope
    => scope(.Map [ "len"    <- builtinV("len")    ]
                  [ "set"    <- builtinV("set")    ]
                  [ "sum"    <- builtinV("sum")    ]
                  [ "abs"    <- builtinV("abs")    ]
                  [ "min"    <- builtinV("min")    ]
                  [ "max"    <- builtinV("max")    ]
                  [ "ord"    <- builtinV("ord")    ]
                  [ "chr"    <- builtinV("chr")    ]
                  [ "range"  <- builtinV("range")  ]
                  [ "all"    <- builtinV("all")    ]
                  [ "any"    <- builtinV("any")    ]
                  [ "zip"    <- builtinV("zip")    ]
                  [ "isinstance" <- builtinV("isinstance") ]
                  [ "sorted" <- builtinV("sorted") ]
                  [ "list"   <- builtinV("list")   ]
                  [ "round"  <- builtinV("round")  ]
                  [ "bin"    <- builtinV("bin")    ]
                  [ "enumerate" <- builtinV("enumerate") ]
                  [ "map"    <- builtinV("map")    ]
                  [ "eval"   <- builtinV("eval")   ]
                  [ "int"    <- typeV("int")       ]
                  [ "str"    <- typeV("str")       ]
                  [ "float"  <- typeV("float")     ], root)
```

## 0427 reference-semantics/semantics/core.k:185 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ApplyK ::= toCall(Val)
```

## 0428 reference-semantics/semantics/core.k:186 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem  ::= #evalArgs(Exprs, Vals, ApplyK)
                  | #evalArgCont(Exprs, Vals, ApplyK)
                  | #applyK(ApplyK, Vals)
```

## 0429 reference-semantics/semantics/core.k:189 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #evalArgs((A:Expr, REST:Exprs), ACC:Vals, K:ApplyK) => A ~> #evalArgCont(REST, ACC, K) ... </k>
```

## 0430 reference-semantics/semantics/core.k:190 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #evalArgCont(REST:Exprs, ACC:Vals, K:ApplyK) => #evalArgs(REST, appendVal(ACC, V), K) ... </k>
```

## 0431 reference-semantics/semantics/core.k:191 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #evalArgs(.Exprs, ACC:Vals, K:ApplyK) => #applyK(K, ACC) ... </k>
```

## 0432 reference-semantics/semantics/core.k:194 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Int(I:Int)   => I ... </k>
```

## 0433 reference-semantics/semantics/core.k:195 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Bool(B:Bool) => B ... </k>
```

## 0434 reference-semantics/semantics/core.k:196 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> NoneVal      => noneV ... </k>
```

## 0435 reference-semantics/semantics/core.k:199 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= truthy(Val) [function]
```

## 0436 reference-semantics/semantics/core.k:200 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(B:Bool)          => B
```

## 0437 reference-semantics/semantics/core.k:201 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(noneV)           => false
```

## 0438 reference-semantics/semantics/core.k:202 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(I:Int)           => I =/=Int 0
```

## 0439 reference-semantics/semantics/core.k:203 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(str(S:IntSeq))   => notBool (S ==K .IntSeq)
```

## 0440 reference-semantics/semantics/core.k:204 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(list(V:ValSeq))  => notBool (V ==K .ValSeq)
```

## 0441 reference-semantics/semantics/core.k:205 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule truthy(tuple(V:ValSeq)) => notBool (V ==K .ValSeq)
```

## 0442 reference-semantics/semantics/core.k:208 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val  ::= applyUn(String, Val) [function]
```

## 0443 reference-semantics/semantics/core.k:209 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val  ::= applyBin(String, Val, Val) [function]
```

## 0444 reference-semantics/semantics/core.k:210 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= applyCmp(String, Val, Val) [function]
```

## 0445 reference-semantics/semantics/core.k:213 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Vals ::= appendVal(Vals, Val) [function, total]
```

## 0446 reference-semantics/semantics/core.k:214 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendVal(.Vals, V:Val)              => V , .Vals
```

## 0447 reference-semantics/semantics/core.k:215 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule appendVal((V0:Val, VS:Vals), V:Val)  => V0 , appendVal(VS, V)
```

## 0448 reference-semantics/semantics/core.k:217 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= vals2valSeq(Vals) [function, total]
```

## 0449 reference-semantics/semantics/core.k:218 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule vals2valSeq(.Vals)            => .ValSeq
```

## 0450 reference-semantics/semantics/core.k:219 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule vals2valSeq((V:Val, VS:Vals)) => vCons(V, vals2valSeq(VS))
```

## 0451 reference-semantics/semantics/core.k:223 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= vsLen(ValSeq) [function, total]
```

## 0452 reference-semantics/semantics/core.k:224 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule vsLen(.ValSeq)                => 0
```

## 0453 reference-semantics/semantics/core.k:225 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule vsLen(vCons(_:Val, S:ValSeq)) => 1 +Int vsLen(S)
```

## 0454 reference-semantics/semantics/core.k:227 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= isLen(IntSeq) [function, total]
```

## 0455 reference-semantics/semantics/core.k:228 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isLen(.IntSeq)                => 0
```

## 0456 reference-semantics/semantics/core.k:229 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isLen(iCons(_:Int, S:IntSeq)) => 1 +Int isLen(S)
```

## 0457 reference-semantics/semantics/core.k:233 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= setVSAt(ValSeq, Int, Val) [function, total]
```

## 0458 reference-semantics/semantics/core.k:234 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule setVSAt(.ValSeq, _:Int, _:Val)               => .ValSeq
```

## 0459 reference-semantics/semantics/core.k:235 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule setVSAt(vCons(_:Val, S:ValSeq), 0, V:Val)    => vCons(V, S)
```

## 0460 reference-semantics/semantics/core.k:236 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule setVSAt(vCons(W:Val, S:ValSeq), I:Int, V:Val) => vCons(W, setVSAt(S, I -Int 1, V))
       requires I >Int 0
```

## 0461 reference-semantics/semantics/core.k:238 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule setVSAt(VS:ValSeq, I:Int, _:Val)             => VS
       requires I <Int 0
```

## 0462 reference-semantics/semantics/core.k:240 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0463 reference-semantics/semantics/dict.k:13 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-DICT
```

## 0464 reference-semantics/semantics/dict.k:14 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0465 reference-semantics/semantics/dict.k:15 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0466 reference-semantics/semantics/dict.k:16 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-METHODS
```

## 0467 reference-semantics/semantics/dict.k:17 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-LIST
```

## 0468 reference-semantics/semantics/dict.k:20 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= dictV(ValSeq, ValSeq)
```

## 0469 reference-semantics/semantics/dict.k:23 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #dictAcc(Entries, ValSeq, ValSeq)
                 | #dictKey(Expr, Entries, ValSeq, ValSeq)
                 | #dictVal(Val, Entries, ValSeq, ValSeq)
```

## 0470 reference-semantics/semantics/dict.k:26 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> DictExpr(ES:Entries) => #dictAcc(ES, .ValSeq, .ValSeq) ... </k>
```

## 0471 reference-semantics/semantics/dict.k:27 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #dictAcc(.Entries, KS:ValSeq, VS:ValSeq) => dictV(KS, VS) ... </k>
```

## 0472 reference-semantics/semantics/dict.k:28 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #dictAcc((Entry(K:Expr, V:Expr), REST:Entries), KS:ValSeq, VS:ValSeq)
        => K ~> #dictKey(V, REST, KS, VS) ... </k>
```

## 0473 reference-semantics/semantics/dict.k:30 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> KV:Val ~> #dictKey(V:Expr, REST:Entries, KS:ValSeq, VS:ValSeq)
        => V ~> #dictVal(KV, REST, KS, VS) ... </k>
```

## 0474 reference-semantics/semantics/dict.k:32 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> VV:Val ~> #dictVal(KV:Val, REST:Entries, KS:ValSeq, VS:ValSeq)
        => #dictAcc(REST, dPutK(KS, KV), dPutV(KS, VS, KV, VV)) ... </k>
```

## 0475 reference-semantics/semantics/dict.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= dHasKey(ValSeq, Val) [function, total]
```

## 0476 reference-semantics/semantics/dict.k:38 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dHasKey(.ValSeq, _:Val)                => false
```

## 0477 reference-semantics/semantics/dict.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dHasKey(vCons(A:Val, _:ValSeq), K:Val) => true          requires A ==K K
```

## 0478 reference-semantics/semantics/dict.k:40 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dHasKey(vCons(A:Val, R:ValSeq), K:Val) => dHasKey(R, K) requires notBool (A ==K K)
```

## 0479 reference-semantics/semantics/dict.k:43 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= dPutK(ValSeq, Val) [function, total]
```

## 0480 reference-semantics/semantics/dict.k:44 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dPutK(KS:ValSeq, K:Val) => KS                                  requires dHasKey(KS, K)
```

## 0481 reference-semantics/semantics/dict.k:45 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dPutK(KS:ValSeq, K:Val) => valSeqConcat(KS, vCons(K, .ValSeq)) requires notBool dHasKey(KS, K)
```

## 0482 reference-semantics/semantics/dict.k:49 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= dPutV(ValSeq, ValSeq, Val, Val) [function, total]
```

## 0483 reference-semantics/semantics/dict.k:50 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dPutV(vCons(A:Val, _:ValSeq), vCons(_:Val, VR:ValSeq), K:Val, V:Val)  => vCons(V, VR)
       requires A ==K K
```

## 0484 reference-semantics/semantics/dict.k:52 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dPutV(vCons(A:Val, KR:ValSeq), vCons(B:Val, VR:ValSeq), K:Val, V:Val) => vCons(B, dPutV(KR, VR, K, V))
       requires notBool (A ==K K)
```

## 0485 reference-semantics/semantics/dict.k:54 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dPutV(_KS:ValSeq, VS:ValSeq, _K:Val, V:Val) => valSeqConcat(VS, vCons(V, .ValSeq)) [owise]
```

## 0486 reference-semantics/semantics/dict.k:58 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(dictV(KS:ValSeq, _:ValSeq), "keys")), .Vals)
        => #alloc(list(KS)) ... </k>
       [priority(40)]
```

## 0487 reference-semantics/semantics/dict.k:63 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyIndexD(dictV(KS:ValSeq, VS:ValSeq), K:Val) => dGet(KS, VS, K)
```

## 0488 reference-semantics/semantics/dict.k:64 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= applyIndexD(Val, Val) [function]
```

## 0489 reference-semantics/semantics/dict.k:65 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Subscript(dictV(KS:ValSeq, VS:ValSeq), K:Val) => applyIndexD(dictV(KS, VS), K) ... </k>
       [priority(45)]
```

## 0490 reference-semantics/semantics/dict.k:70 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= dictSet(Val, Val, Val) [function]
```

## 0491 reference-semantics/semantics/dict.k:71 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dictSet(dictV(KS:ValSeq, VS:ValSeq), K:Val, V:Val) => dictV(dPutK(KS, K), dPutV(KS, VS, K, V))
```

## 0492 reference-semantics/semantics/dict.k:76 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #dsetK(String, Val)
```

## 0493 reference-semantics/semantics/dict.k:77 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(Subscript(Name(X:String), K:Expr), VV:Val) => K ~> #dsetK(X, VV) ... </k>
```

## 0494 reference-semantics/semantics/dict.k:78 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- dictSet({M[X]}:>Val, KV, VV) ], _) ... </scopes>
       requires X in_keys(M) andBool notBool isRefV({M[X]}:>Val)
```

## 0495 reference-semantics/semantics/dict.k:82 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> KV:Val ~> #dsetK(X:String, VV:Val) => #dsetV({M[X]}:>Val, KV, VV) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires X in_keys(M) andBool isRefV({M[X]}:>Val)
```

## 0496 reference-semantics/semantics/dict.k:86 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #dsetV(Val, Val, Val)
```

## 0497 reference-semantics/semantics/dict.k:87 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #dsetV(ref(H:Int), I:Int, VV:Val) => .K ... </k>
       <heap> ... H |-> list(VS:ValSeq => setVSAt(VS, normIdxD(I, vsLen(VS)), VV)) ... </heap>
```

## 0498 reference-semantics/semantics/dict.k:90 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= normIdxD(Int, Int) [function, total]
```

## 0499 reference-semantics/semantics/dict.k:91 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule normIdxD(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 0500 reference-semantics/semantics/dict.k:92 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule normIdxD(I:Int, _:Int)   => I          requires I >=Int 0
```

## 0501 reference-semantics/semantics/dict.k:95 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", dictV(KS1:ValSeq, VS1:ValSeq), dictV(KS2:ValSeq, VS2:ValSeq))
    => (vsLen(KS1) ==Int vsLen(KS2)) andBool dSubset(KS1, VS1, KS2, VS2)
```

## 0502 reference-semantics/semantics/dict.k:97 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= dSubset(ValSeq, ValSeq, ValSeq, ValSeq) [function]
```

## 0503 reference-semantics/semantics/dict.k:98 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dSubset(.ValSeq, .ValSeq, _:ValSeq, _:ValSeq) => true
```

## 0504 reference-semantics/semantics/dict.k:99 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dSubset(vCons(K:Val, KR:ValSeq), vCons(V:Val, VR:ValSeq), KS2:ValSeq, VS2:ValSeq)
    => dHasKey(KS2, K) andBool (dGet(KS2, VS2, K) ==K V) andBool dSubset(KR, VR, KS2, VS2)
```

## 0505 reference-semantics/semantics/dict.k:101 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= dGet(ValSeq, ValSeq, Val) [function]
```

## 0506 reference-semantics/semantics/dict.k:102 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dGet(vCons(A:Val, _:ValSeq), vCons(B:Val, _:ValSeq), K:Val) => B                requires A ==K K
```

## 0507 reference-semantics/semantics/dict.k:103 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dGet(vCons(A:Val, KR:ValSeq), vCons(_:Val, VR:ValSeq), K:Val) => dGet(KR, VR, K) requires notBool (A ==K K)
```

## 0508 reference-semantics/semantics/dict.k:104 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0509 reference-semantics/semantics/float.k:14 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-FLOAT
```

## 0510 reference-semantics/semantics/float.k:15 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-OPERATORS
```

## 0511 reference-semantics/semantics/float.k:16 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-BUILTINS
```

## 0512 reference-semantics/semantics/float.k:17 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports FLOAT
```

## 0513 reference-semantics/semantics/float.k:20 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= Float
```

## 0514 reference-semantics/semantics/float.k:21 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Float(F:Float) => F ... </k>
```

## 0515 reference-semantics/semantics/float.k:24 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= intFloatDiv(Int, Float) [function, total, symbol(intFloatDiv), no-evaluators]
```

## 0516 reference-semantics/semantics/float.k:25 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule intFloatDiv(I:Int, F:Float) => Int2Float(I, 53, 11) /Float F [concrete]
```

## 0517 reference-semantics/semantics/float.k:27 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("/", I:Int, F:Float) => intFloatDiv(I, F)
```

## 0518 reference-semantics/semantics/float.k:30 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= divII(Int, Int) [function, total, symbol(divII), no-evaluators]
```

## 0519 reference-semantics/semantics/float.k:31 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule divII(I1:Int, I2:Int) => Int2Float(I1, 53, 11) /Float Int2Float(I2, 53, 11) [concrete]
```

## 0520 reference-semantics/semantics/float.k:32 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("/", I1:Int, I2:Int) => divII(I1, I2)
```

## 0521 reference-semantics/semantics/float.k:37 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= floatMod(Float, Float) [function, total, symbol(floatMod), no-evaluators]
```

## 0522 reference-semantics/semantics/float.k:38 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule floatMod(F1:Float, F2:Float) => F1 -Float (floorFloat(F1 /Float F2) *Float F2) [concrete]
```

## 0523 reference-semantics/semantics/float.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("%", F1:Float, F2:Float) => floatMod(F1, F2)
```

## 0524 reference-semantics/semantics/float.k:43 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", F1:Float, F2:Float) => F1 ==Float F2
```

## 0525 reference-semantics/semantics/float.k:44 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", F1:Float, F2:Float) => notBool (F1 ==Float F2)
```

## 0526 reference-semantics/semantics/float.k:50 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Bool ::= floatLt(Float, Float) [function, total, symbol(floatLt), no-evaluators]
```

## 0527 reference-semantics/semantics/float.k:51 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule floatLt(F1:Float, F2:Float) => F1 <Float F2 [concrete]
```

## 0528 reference-semantics/semantics/float.k:52 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<", F1:Float, F2:Float) => floatLt(F1, F2)
```

## 0529 reference-semantics/semantics/float.k:54 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= absF(Float) [function, total, symbol(absF), no-evaluators]
```

## 0530 reference-semantics/semantics/float.k:55 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule absF(F:Float) => absFloat(F) [concrete]
```

## 0531 reference-semantics/semantics/float.k:56 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("abs", F:Float, .Vals) => absF(F)
```

## 0532 reference-semantics/semantics/float.k:61 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Import(_:String) => .K ... </k>
```

## 0533 reference-semantics/semantics/float.k:65 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= "#mathCeil"
```

## 0534 reference-semantics/semantics/float.k:66 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Attribute(Name("math"), "ceil"), (E:Expr, .Exprs)) => E ~> #mathCeil ... </k> [priority(40)]
```

## 0535 reference-semantics/semantics/float.k:67 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #mathCeil => ceilF(V) ... </k>
```

## 0536 reference-semantics/semantics/float.k:70 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= "#mathFloor"
```

## 0537 reference-semantics/semantics/float.k:71 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Attribute(Name("math"), "floor"), (E:Expr, .Exprs)) => E ~> #mathFloor ... </k> [priority(40)]
```

## 0538 reference-semantics/semantics/float.k:72 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V:Val ~> #mathFloor => floorFI(V) ... </k>
```

## 0539 reference-semantics/semantics/float.k:73 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= floorFI(Val) [function, total, symbol(floorFI)]
```

## 0540 reference-semantics/semantics/float.k:74 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule floorFI(I:Int)   => I                        [concrete]
```

## 0541 reference-semantics/semantics/float.k:75 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule floorFI(F:Float) => Float2Int(floorFloat(F)) [concrete]
```

## 0542 reference-semantics/semantics/float.k:78 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("floor", V:Val, .Vals) => floorFI(V)
```

## 0543 reference-semantics/semantics/float.k:79 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("ceil",  V:Val, .Vals) => ceilF(V)
```

## 0544 reference-semantics/semantics/float.k:82 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #mathPow1(Expr) | #mathPow2(Val)
```

## 0545 reference-semantics/semantics/float.k:83 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Attribute(Name("math"), "pow"), (E1:Expr, E2:Expr, .Exprs)) => E1 ~> #mathPow1(E2) ... </k> [priority(40)]
```

## 0546 reference-semantics/semantics/float.k:84 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V1:Val ~> #mathPow1(E2:Expr) => E2 ~> #mathPow2(V1) ... </k>
```

## 0547 reference-semantics/semantics/float.k:85 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> V2:Val ~> #mathPow2(V1:Val) => powF(toF(V1), toF(V2)) ... </k>
```

## 0548 reference-semantics/semantics/float.k:86 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Float ::= toF(Val) [function, total, symbol(toF)]
```

## 0549 reference-semantics/semantics/float.k:87 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule toF(F:Float) => F        [concrete]
```

## 0550 reference-semantics/semantics/float.k:88 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule toF(I:Int)   => intToF(I) [concrete]
```

## 0551 reference-semantics/semantics/float.k:93 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= ceilF(Val) [function, total, symbol(ceilF)]
```

## 0552 reference-semantics/semantics/float.k:94 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule ceilF(I:Int)   => I                       [concrete]
```

## 0553 reference-semantics/semantics/float.k:95 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule ceilF(F:Float) => Float2Int(ceilFloat(F)) [concrete]
```

## 0554 reference-semantics/semantics/float.k:99 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyUn("-", F:Float) => 0.0 -Float F
```

## 0555 reference-semantics/semantics/float.k:103 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= subF(Float, Float) [function, total, symbol(subF), no-evaluators]
```

## 0556 reference-semantics/semantics/float.k:104 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule subF(F1:Float, F2:Float) => F1 -Float F2 [concrete]
```

## 0557 reference-semantics/semantics/float.k:105 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-", F1:Float, F2:Float) => subF(F1, F2)
```

## 0558 reference-semantics/semantics/float.k:107 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= divF(Float, Float) [function, total, symbol(divF), no-evaluators]
```

## 0559 reference-semantics/semantics/float.k:108 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule divF(F1:Float, F2:Float) => F1 /Float F2 [concrete]
```

## 0560 reference-semantics/semantics/float.k:109 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("/", F1:Float, F2:Float) => divF(F1, F2)
```

## 0561 reference-semantics/semantics/float.k:111 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= addF(Float, Float) [function, total, symbol(addF), no-evaluators]
```

## 0562 reference-semantics/semantics/float.k:112 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule addF(F1:Float, F2:Float) => F1 +Float F2 [concrete]
```

## 0563 reference-semantics/semantics/float.k:113 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+", F1:Float, F2:Float) => addF(F1, F2)
```

## 0564 reference-semantics/semantics/float.k:115 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= mulF(Float, Float) [function, total, symbol(mulF), no-evaluators]
```

## 0565 reference-semantics/semantics/float.k:116 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule mulF(F1:Float, F2:Float) => F1 *Float F2 [concrete]
```

## 0566 reference-semantics/semantics/float.k:117 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*", F1:Float, F2:Float) => mulF(F1, F2)
```

## 0567 reference-semantics/semantics/float.k:119 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= powF(Float, Float) [function, total, symbol(powF), no-evaluators]
```

## 0568 reference-semantics/semantics/float.k:120 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule powF(F1:Float, F2:Float) => F1 ^Float F2 [concrete]
```

## 0569 reference-semantics/semantics/float.k:121 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("**", F1:Float, F2:Float) => powF(F1, F2)
```

## 0570 reference-semantics/semantics/float.k:125 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Bool ::= gtF(Float, Float) [function, total, symbol(gtF), no-evaluators]
```

## 0571 reference-semantics/semantics/float.k:126 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule gtF(F1:Float, F2:Float) => F1 >Float F2 [concrete]
```

## 0572 reference-semantics/semantics/float.k:127 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">",  F1:Float, F2:Float) => gtF(F1, F2)
```

## 0573 reference-semantics/semantics/float.k:128 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">=", F1:Float, F2:Float) => notBool floatLt(F1, F2)
```

## 0574 reference-semantics/semantics/float.k:129 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<=", F1:Float, F2:Float) => notBool gtF(F1, F2)
```

## 0575 reference-semantics/semantics/float.k:132 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("**", I:Int, F:Float) => powF(intToF(I), F)
```

## 0576 reference-semantics/semantics/float.k:133 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("**", F:Float, I:Int) => powF(F, intToF(I))
```

## 0577 reference-semantics/semantics/float.k:134 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-",  I:Int, F:Float) => subF(intToF(I), F)
```

## 0578 reference-semantics/semantics/float.k:135 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-",  F:Float, I:Int) => subF(F, intToF(I))
```

## 0579 reference-semantics/semantics/float.k:136 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  I:Int, F:Float) => addF(intToF(I), F)
```

## 0580 reference-semantics/semantics/float.k:137 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  F:Float, I:Int) => addF(F, intToF(I))
```

## 0581 reference-semantics/semantics/float.k:138 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*",  I:Int, F:Float) => mulF(intToF(I), F)
```

## 0582 reference-semantics/semantics/float.k:139 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*",  F:Float, I:Int) => mulF(F, intToF(I))
```

## 0583 reference-semantics/semantics/float.k:142 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Bool ::= eqF(Float, Float) [function, total, symbol(eqF), no-evaluators]
```

## 0584 reference-semantics/semantics/float.k:143 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule eqF(F1:Float, F2:Float) => F1 ==Float F2 [concrete]
```

## 0585 reference-semantics/semantics/float.k:144 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", I:Int, F:Float) => eqF(intToF(I), F)
```

## 0586 reference-semantics/semantics/float.k:145 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", F:Float, I:Int) => eqF(F, intToF(I))
```

## 0587 reference-semantics/semantics/float.k:146 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", I:Int, F:Float) => notBool eqF(intToF(I), F)
```

## 0588 reference-semantics/semantics/float.k:147 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", F:Float, I:Int) => notBool eqF(F, intToF(I))
```

## 0589 reference-semantics/semantics/float.k:148 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<",  I:Int, F:Float) => floatLt(intToF(I), F)
```

## 0590 reference-semantics/semantics/float.k:149 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<",  F:Float, I:Int) => floatLt(F, intToF(I))
```

## 0591 reference-semantics/semantics/float.k:150 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">",  I:Int, F:Float) => gtF(intToF(I), F)
```

## 0592 reference-semantics/semantics/float.k:151 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">",  F:Float, I:Int) => gtF(F, intToF(I))
```

## 0593 reference-semantics/semantics/float.k:154 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", V:Val, noneV) => V ==K noneV
```

## 0594 reference-semantics/semantics/float.k:155 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", V:Val, noneV) => notBool (V ==K noneV)
```

## 0595 reference-semantics/semantics/float.k:160 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= decStrToF(IntSeq) [function, total, symbol(decStrToF), no-evaluators]
```

## 0596 reference-semantics/semantics/float.k:161 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule decStrToF(iCons(45, CS:IntSeq)) => 0.0 -Float decStrToF(CS) [concrete]
```

## 0597 reference-semantics/semantics/float.k:162 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule decStrToF(CS:IntSeq)
    => intToF(intPart(CS)) +Float (intToF(fracPart(CS)) /Float intToF(fracScale(CS)))
       requires isLen(CS) >Int 0 andBool headIS(CS) =/=Int 45 [concrete]
```

## 0598 reference-semantics/semantics/float.k:165 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= headIS(IntSeq) [function]
```

## 0599 reference-semantics/semantics/float.k:166 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule headIS(iCons(C:Int, _:IntSeq)) => C
```

## 0600 reference-semantics/semantics/float.k:167 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= intPart(IntSeq) [function, total] | intPartAcc(IntSeq, Int) [function, total]
```

## 0601 reference-semantics/semantics/float.k:168 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intPart(CS:IntSeq) => intPartAcc(CS, 0)
```

## 0602 reference-semantics/semantics/float.k:169 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intPartAcc(.IntSeq, A:Int) => A
```

## 0603 reference-semantics/semantics/float.k:170 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intPartAcc(iCons(46, _:IntSeq), A:Int) => A
```

## 0604 reference-semantics/semantics/float.k:171 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intPartAcc(iCons(C:Int, R:IntSeq), A:Int) => intPartAcc(R, A *Int 10 +Int (C -Int 48))
       requires C =/=Int 46
```

## 0605 reference-semantics/semantics/float.k:173 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= fracPart(IntSeq) [function, total] | fracAcc(IntSeq, Int) [function, total]
```

## 0606 reference-semantics/semantics/float.k:174 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracPart(.IntSeq) => 0
```

## 0607 reference-semantics/semantics/float.k:175 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracPart(iCons(46, R:IntSeq)) => fracAcc(R, 0)
```

## 0608 reference-semantics/semantics/float.k:176 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracPart(iCons(C:Int, R:IntSeq)) => fracPart(R) requires C =/=Int 46
```

## 0609 reference-semantics/semantics/float.k:177 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracAcc(.IntSeq, A:Int) => A
```

## 0610 reference-semantics/semantics/float.k:178 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracAcc(iCons(C:Int, R:IntSeq), A:Int) => fracAcc(R, A *Int 10 +Int (C -Int 48))
```

## 0611 reference-semantics/semantics/float.k:179 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= fracScale(IntSeq) [function, total] | fscAcc(IntSeq, Int) [function, total]
```

## 0612 reference-semantics/semantics/float.k:180 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracScale(.IntSeq) => 1
```

## 0613 reference-semantics/semantics/float.k:181 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracScale(iCons(46, R:IntSeq)) => fscAcc(R, 1)
```

## 0614 reference-semantics/semantics/float.k:182 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fracScale(iCons(C:Int, R:IntSeq)) => fracScale(R) requires C =/=Int 46
```

## 0615 reference-semantics/semantics/float.k:183 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fscAcc(.IntSeq, A:Int) => A
```

## 0616 reference-semantics/semantics/float.k:184 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule fscAcc(iCons(_:Int, R:IntSeq), A:Int) => fscAcc(R, A *Int 10)
```

## 0617 reference-semantics/semantics/float.k:185 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("float", str(CS:IntSeq), .Vals) => decStrToF(CS)
```

## 0618 reference-semantics/semantics/float.k:186 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("float", I:Int, .Vals)          => intToF(I)
```

## 0619 reference-semantics/semantics/float.k:187 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("float", F:Float, .Vals)        => F
```

## 0620 reference-semantics/semantics/float.k:190 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= divFloatIntV(Float, Int) [function, total, symbol(divFloatIntV), no-evaluators]
```

## 0621 reference-semantics/semantics/float.k:191 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule divFloatIntV(F:Float, I:Int) => F /Float Int2Float(I, 53, 11) [concrete]
```

## 0622 reference-semantics/semantics/float.k:192 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("/", F:Float, I:Int) => divFloatIntV(F, I)
```

## 0623 reference-semantics/semantics/float.k:195 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= intToF(Int) [function, total, symbol(intToF), no-evaluators]
```

## 0624 reference-semantics/semantics/float.k:196 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule intToF(I:Int) => Int2Float(I, 53, 11) [concrete]
```

## 0625 reference-semantics/semantics/float.k:197 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+", I:Int, F:Float) => addF(intToF(I), F)
```

## 0626 reference-semantics/semantics/float.k:198 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+", F:Float, I:Int) => addF(F, intToF(I))
```

## 0627 reference-semantics/semantics/float.k:199 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-", I:Int, F:Float) => subF(intToF(I), F)
```

## 0628 reference-semantics/semantics/float.k:200 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-", F:Float, I:Int) => subF(F, intToF(I))
```

## 0629 reference-semantics/semantics/float.k:201 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*", I:Int, F:Float) => mulF(intToF(I), F)
```

## 0630 reference-semantics/semantics/float.k:202 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*", F:Float, I:Int) => mulF(F, intToF(I))
```

## 0631 reference-semantics/semantics/float.k:203 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<", I:Int, F:Float) => floatLt(intToF(I), F)
```

## 0632 reference-semantics/semantics/float.k:204 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<", F:Float, I:Int) => floatLt(F, intToF(I))
```

## 0633 reference-semantics/semantics/float.k:205 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">", I:Int, F:Float) => gtF(intToF(I), F)
```

## 0634 reference-semantics/semantics/float.k:206 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">", F:Float, I:Int) => gtF(F, intToF(I))
```

## 0635 reference-semantics/semantics/float.k:209 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Int ::= truncF(Float) [function, total, symbol(truncF), no-evaluators]
```

## 0636 reference-semantics/semantics/float.k:210 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule truncF(F:Float) => #if F >=Float 0.0 #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi [concrete]
```

## 0637 reference-semantics/semantics/float.k:211 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("int", F:Float, .Vals) => truncF(F)
```

## 0638 reference-semantics/semantics/float.k:213 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("float", I:Int, .Vals)   => intToF(I)
```

## 0639 reference-semantics/semantics/float.k:214 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("float", F:Float, .Vals) => F
```

## 0640 reference-semantics/semantics/float.k:217 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Int ::= roundF(Float) [function, total, symbol(roundF), no-evaluators]
```

## 0641 reference-semantics/semantics/float.k:218 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule roundF(F:Float)
    => #if (F -Float floorFloat(F)) ==Float 0.5
       #then (#if Float2Int(floorFloat(F)) %Int 2 ==Int 0
              #then Float2Int(floorFloat(F)) #else Float2Int(ceilFloat(F)) #fi)
       #else Float2Int(floorFloat(F +Float 0.5)) #fi [concrete]
```

## 0642 reference-semantics/semantics/float.k:223 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= roundFN(Float, Int) [function, total, symbol(roundFN), no-evaluators]
```

## 0643 reference-semantics/semantics/float.k:224 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule roundFN(F:Float, N:Int)
    => Int2Float(roundF(F *Float Int2Float(10 ^Int N, 53, 11)), 53, 11)
       /Float Int2Float(10 ^Int N, 53, 11) [concrete]
```

## 0644 reference-semantics/semantics/float.k:227 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("round", F:Float, .Vals)        => roundF(F)
```

## 0645 reference-semantics/semantics/float.k:228 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBuiltin("round", F:Float, N:Int, .Vals) => roundFN(F, N)
```

## 0646 reference-semantics/semantics/float.k:230 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax Float ::= sqrtF(Float) [function, total, symbol(sqrtF), no-evaluators]
```

## 0647 reference-semantics/semantics/float.k:231 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule sqrtF(F:Float) => sqrtFloat(F) [concrete]
```

## 0648 reference-semantics/semantics/float.k:232 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= "#mathSqrt"
```

## 0649 reference-semantics/semantics/float.k:233 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Call(Attribute(Name("math"), "sqrt"), (E:Expr, .Exprs)) => E ~> #mathSqrt ... </k> [priority(40)]
```

## 0650 reference-semantics/semantics/float.k:234 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> F:Float ~> #mathSqrt => sqrtF(F) ... </k>
```

## 0651 reference-semantics/semantics/float.k:235 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> I:Int ~> #mathSqrt => sqrtF(intToF(I)) ... </k>
```

## 0652 reference-semantics/semantics/float.k:243 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #maxAccF(Iterable, Float) | #maxContF(Float)
```

## 0653 reference-semantics/semantics/float.k:244 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxCont0 => #maxAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 0654 reference-semantics/semantics/float.k:245 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #maxAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #maxContF(M) ... </k>
```

## 0655 reference-semantics/semantics/float.k:246 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #maxContF(M:Float) => M ... </k>
```

## 0656 reference-semantics/semantics/float.k:247 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #maxContF(M:Float) => #maxAccF(R, maxFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 0657 reference-semantics/semantics/float.k:250 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #minAccF(Iterable, Float) | #minContF(Float)
```

## 0658 reference-semantics/semantics/float.k:251 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minCont0 => #minAccF(R, {V}:>Float) ... </k> requires isFloat(V)
```

## 0659 reference-semantics/semantics/float.k:252 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #minAccF(IT:Iterable, M:Float) => #iterNext(IT) ~> #minContF(M) ... </k>
```

## 0660 reference-semantics/semantics/float.k:253 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #minContF(M:Float) => M ... </k>
```

## 0661 reference-semantics/semantics/float.k:254 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #minContF(M:Float) => #minAccF(R, minFloat(M, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 0662 reference-semantics/semantics/float.k:261 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #sumAccF(Iterable, Float) | #sumContF(Float)
```

## 0663 reference-semantics/semantics/float.k:262 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumCont(ACC:Int)
        => #sumAccF(R, addF(intToF(ACC), {V}:>Float)) ... </k>
       requires isFloat(V) andBool notBool (isInt(V) orBool isBool(V))
```

## 0664 reference-semantics/semantics/float.k:265 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #sumAccF(IT:Iterable, ACC:Float) => #iterNext(IT) ~> #sumContF(ACC) ... </k>
```

## 0665 reference-semantics/semantics/float.k:266 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #sumContF(ACC:Float) => ACC ... </k>
```

## 0666 reference-semantics/semantics/float.k:267 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, {V}:>Float)) ... </k>
       requires isFloat(V)
```

## 0667 reference-semantics/semantics/float.k:270 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(V:Val, R:Iterable) ~> #sumContF(ACC:Float)
        => #sumAccF(R, addF(ACC, intToF(intOf(V)))) ... </k>
       requires isInt(V) orBool isBool(V)
```

## 0668 reference-semantics/semantics/float.k:273 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0669 reference-semantics/semantics/functions.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-FUNCTIONS
```

## 0670 reference-semantics/semantics/functions.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0671 reference-semantics/semantics/functions.k:8 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= frame(continuation: K, callerEnv: Int, savedLoc: Int)
                 | #bindP(ParamNames, Vals)
                 | "#pop"
                 | "#endcall"
```

## 0672 reference-semantics/semantics/functions.k:14 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureVal(PNS, BODY, L) ], _) ... </scopes>
```

## 0673 reference-semantics/semantics/functions.k:18 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Expr ::= closureExpr(ParamNames, Stmts)
```

## 0674 reference-semantics/semantics/functions.k:19 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> closureExpr(PNS:ParamNames, BODY:Stmts) => closureVal(PNS, BODY, L) ... </k>
       <env> L:Int </env>
```

## 0675 reference-semantics/semantics/functions.k:27 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= closureValC(ParamNames, ParamNames, Stmts, Map)
```

## 0676 reference-semantics/semantics/functions.k:31 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #mkClosure(String, ParamNames, ParamNames, ParamNames, Stmts, Map)
                 | #mkLambda(ParamNames, ParamNames, ParamNames, Stmts, Map)
```

## 0677 reference-semantics/semantics/functions.k:33 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> FuncDef(F:String, Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                   FreeVars(FVS:ParamNames), BODY:Stmts)
        => #mkClosure(F, PNS, CVS, FVS, BODY, .Map) ... </k>
```

## 0678 reference-semantics/semantics/functions.k:36 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkClosure(F, PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 0679 reference-semantics/semantics/functions.k:42 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #mkClosure(F:String, PNS:ParamNames, CVS:ParamNames,
                      .ParamNames, BODY:Stmts, CM:Map) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ F <- closureValC(PNS, CVS, BODY, CM) ], _) ... </scopes>
```

## 0680 reference-semantics/semantics/functions.k:47 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Lambda(Params(PNS:ParamNames), E:Expr)
        => closureVal(PNS, Return(E) .Stmts, L) ... </k>
       <env> L:Int </env>
```

## 0681 reference-semantics/semantics/functions.k:50 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Lambda(Params(PNS:ParamNames), CellVars(CVS:ParamNames),
                  FreeVars(FVS:ParamNames), E:Expr)
        => #mkLambda(PNS, CVS, FVS, Return(E) .Stmts, .Map) ... </k>
```

## 0682 reference-semantics/semantics/functions.k:53 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames,
                     (FV:String, FVR:ParamNames), BODY:Stmts, CM:Map)
        => #mkLambda(PNS, CVS, FVR, BODY, CM [ FV <- {M[FV]}:>Val ]) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires FV in_keys(M)
```

## 0683 reference-semantics/semantics/functions.k:59 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #mkLambda(PNS:ParamNames, CVS:ParamNames, .ParamNames, BODY:Stmts, CM:Map)
        => closureValC(PNS, CVS, BODY, CM) ... </k>
```

## 0684 reference-semantics/semantics/functions.k:63 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindP(.ParamNames, .Vals) => .K ... </k>
```

## 0685 reference-semantics/semantics/functions.k:64 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals)) => #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ P <- V ], _) ... </scopes>
```

## 0686 reference-semantics/semantics/functions.k:68 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))
        => #cellW({M[P]}:>Val, V) ~> #bindP(PS, VS) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(P, cellsOf({M["$cells"]}:>Val))
        andBool P in_keys(M) andBool isCellRef({M[P]}:>Val)
       [priority(40)]
```

## 0687 reference-semantics/semantics/functions.k:78 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Return(V:Val) ~> _ => #pop </k>
       <ret> noRet => retV(V) </ret>
```

## 0688 reference-semantics/semantics/functions.k:80 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #endcall => #pop ... </k>
       <ret> noRet => retV(noneV) </ret>
```

## 0689 reference-semantics/semantics/functions.k:85 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #pop => V ~> CONT </k>
       <ret>   retV(V) => noRet </ret>
       <stack> ListItem(frame(CONT:K, CALLERL:Int, SAVEDL:Int)) => .List ... </stack>
       <env>   L:Int => CALLERL </env>
       <scopes> SC:Map => SC [ L <- undef ] </scopes>
       <scopeLoc> _ => SAVEDL </scopeLoc>
```

## 0690 reference-semantics/semantics/functions.k:91 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0691 reference-semantics/semantics/int.k:4 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-INT
```

## 0692 reference-semantics/semantics/int.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0693 reference-semantics/semantics/int.k:7 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyUn("-", I:Int) => 0 -Int I
```

## 0694 reference-semantics/semantics/int.k:9 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  I1:Int, I2:Int) => I1 +Int I2
```

## 0695 reference-semantics/semantics/int.k:11 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  I:Int, B:Bool) => I +Int #if B #then 1 #else 0 #fi
```

## 0696 reference-semantics/semantics/int.k:12 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  B:Bool, I:Int) => #if B #then 1 #else 0 #fi +Int I
```

## 0697 reference-semantics/semantics/int.k:13 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("-",  I1:Int, I2:Int) => I1 -Int I2
```

## 0698 reference-semantics/semantics/int.k:14 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("*",  I1:Int, I2:Int) => I1 *Int I2
```

## 0699 reference-semantics/semantics/int.k:15 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("%",  I1:Int, I2:Int) => pyMod(I1, I2)
```

## 0700 reference-semantics/semantics/int.k:16 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("//", I1:Int, I2:Int) => (I1 -Int pyMod(I1, I2)) /Int I2
```

## 0701 reference-semantics/semantics/int.k:17 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("**", I1:Int, I2:Int) => I1 ^Int I2 requires I2 >=Int 0
```

## 0702 reference-semantics/semantics/int.k:19 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= pyMod(Int, Int) [function]
```

## 0703 reference-semantics/semantics/int.k:20 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule pyMod(I1:Int, I2:Int) => ((I1 %Int I2) +Int I2) %Int I2
```

## 0704 reference-semantics/semantics/int.k:22 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<",  I1:Int, I2:Int)   => I1 <Int  I2
```

## 0705 reference-semantics/semantics/int.k:23 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<=", I1:Int, I2:Int)   => I1 <=Int I2
```

## 0706 reference-semantics/semantics/int.k:24 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">",  I1:Int, I2:Int)   => I1 >Int  I2
```

## 0707 reference-semantics/semantics/int.k:25 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">=", I1:Int, I2:Int)   => I1 >=Int I2
```

## 0708 reference-semantics/semantics/int.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", I1:Int, I2:Int)   => I1 ==Int I2
```

## 0709 reference-semantics/semantics/int.k:27 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", I1:Int, I2:Int)   => I1 =/=Int I2
```

## 0710 reference-semantics/semantics/int.k:28 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0711 reference-semantics/semantics/iter.k:6 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-ITER
```

## 0712 reference-semantics/semantics/iter.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0713 reference-semantics/semantics/iter.k:8 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #iterNext(Iterable) | "#iterDone" | #iterYield(Val, Iterable)
```

## 0714 reference-semantics/semantics/iter.k:9 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0715 reference-semantics/semantics/list.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-LIST
```

## 0716 reference-semantics/semantics/list.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0717 reference-semantics/semantics/list.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0718 reference-semantics/semantics/list.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-OPERATORS
```

## 0719 reference-semantics/semantics/list.k:9 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(list(.ValSeq))                => #iterDone ... </k>
```

## 0720 reference-semantics/semantics/list.k:10 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(list(vCons(V:Val, R:ValSeq))) => #iterYield(V, list(R)) ... </k>
```

## 0721 reference-semantics/semantics/list.k:13 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ApplyK ::= "toList"
```

## 0722 reference-semantics/semantics/list.k:14 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ListExpr(ES:Exprs) => #evalArgs(ES, .Vals, toList) ... </k>
```

## 0723 reference-semantics/semantics/list.k:15 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toList, ACC:Vals) => #alloc(list(vals2valSeq(ACC))) ... </k>
```

## 0724 reference-semantics/semantics/list.k:18 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= valSeqConcat(ValSeq, ValSeq) [function, total]
```

## 0725 reference-semantics/semantics/list.k:19 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule valSeqConcat(.ValSeq, T:ValSeq)                => T
```

## 0726 reference-semantics/semantics/list.k:20 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule valSeqConcat(vCons(V:Val, S:ValSeq), T:ValSeq) => vCons(V, valSeqConcat(S, T))
```

## 0727 reference-semantics/semantics/list.k:24 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BinOp("+", list(A:ValSeq), list(B:ValSeq)) => #alloc(list(valSeqConcat(A, B))) ... </k>
       [priority(45)]
```

## 0728 reference-semantics/semantics/list.k:27 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", list(A:ValSeq), list(B:ValSeq)) => A ==K B
```

## 0729 reference-semantics/semantics/list.k:28 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", list(A:ValSeq), list(B:ValSeq)) => notBool (A ==K B)
```

## 0730 reference-semantics/semantics/list.k:33 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= hasRefVS(ValSeq) [function, total]
```

## 0731 reference-semantics/semantics/list.k:34 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasRefVS(.ValSeq)                => false
```

## 0732 reference-semantics/semantics/list.k:35 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasRefVS(vCons(V:Val, R:ValSeq)) => isRefV(V) orBool hasRefVS(R)
```

## 0733 reference-semantics/semantics/list.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= deepEqVS(ValSeq, ValSeq, Map) [function]
                | deepEqV(Val, Val, Map)        [function]
```

## 0734 reference-semantics/semantics/list.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqVS(.ValSeq, .ValSeq, _:Map)                   => true
```

## 0735 reference-semantics/semantics/list.k:40 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqVS(.ValSeq, vCons(_:Val, _:ValSeq), _:Map)    => false
```

## 0736 reference-semantics/semantics/list.k:41 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqVS(vCons(_:Val, _:ValSeq), .ValSeq, _:Map)    => false
```

## 0737 reference-semantics/semantics/list.k:42 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqVS(vCons(A:Val, As:ValSeq), vCons(B:Val, Bs:ValSeq), HP:Map)
    => deepEqV(A, B, HP) andBool deepEqVS(As, Bs, HP)
```

## 0738 reference-semantics/semantics/list.k:45 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqV(ref(H:Int), B:Val, HP:Map) => deepEqV({HP[H]}:>Val, B, HP)
       requires H in_keys(HP)
```

## 0739 reference-semantics/semantics/list.k:47 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqV(A:Val, ref(H:Int), HP:Map) => deepEqV(A, {HP[H]}:>Val, HP)
       requires notBool isRefV(A) andBool H in_keys(HP)
```

## 0740 reference-semantics/semantics/list.k:49 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqV(list(A:ValSeq), list(B:ValSeq), HP:Map) => deepEqVS(A, B, HP)
```

## 0741 reference-semantics/semantics/list.k:50 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule deepEqV(A:Val, B:Val, _:Map) => A ==K B [owise]
```

## 0742 reference-semantics/semantics/list.k:53 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "append")), (V:Val, .Vals)) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => valSeqConcat(VS, vCons(V, .ValSeq))) ... </heap>
       [priority(40)]
```

## 0743 reference-semantics/semantics/list.k:58 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #memberAcc(Val, Iterable) | #memberCont(Val) | "#notB"
```

## 0744 reference-semantics/semantics/list.k:59 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(LV:Val, CmpOp("in",     list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ... </k>
```

## 0745 reference-semantics/semantics/list.k:60 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(LV:Val, CmpOp("not in", list(VS:ValSeq))) => #memberAcc(LV, list(VS)) ~> #notB ... </k>
```

## 0746 reference-semantics/semantics/list.k:61 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #memberAcc(V:Val, IT:Iterable) => #iterNext(IT) ~> #memberCont(V) ... </k>
```

## 0747 reference-semantics/semantics/list.k:62 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterDone ~> #memberCont(_V:Val) => false ... </k>
```

## 0748 reference-semantics/semantics/list.k:63 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(E:Val, _:Iterable) ~> #memberCont(V:Val) => true ... </k>
       requires E ==K V
```

## 0749 reference-semantics/semantics/list.k:65 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterYield(E:Val, R:Iterable) ~> #memberCont(V:Val) => #memberAcc(V, R) ... </k>
       requires notBool (E ==K V)
```

## 0750 reference-semantics/semantics/list.k:67 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> B:Bool ~> #notB => notBool B ... </k>
```

## 0751 reference-semantics/semantics/list.k:68 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0752 reference-semantics/semantics/methods.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-METHODS
```

## 0753 reference-semantics/semantics/methods.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0754 reference-semantics/semantics/methods.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports K-EQUAL
```

## 0755 reference-semantics/semantics/methods.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-STR
```

## 0756 reference-semantics/semantics/methods.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-LIST
```

## 0757 reference-semantics/semantics/methods.k:10 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= applyMethod(Val, String, Vals) [function]
```

## 0758 reference-semantics/semantics/methods.k:13 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "isupper", .Vals) => hasUpper(CS) andBool notBool hasLower(CS)
```

## 0759 reference-semantics/semantics/methods.k:14 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "islower", .Vals) => hasLower(CS) andBool notBool hasUpper(CS)
```

## 0760 reference-semantics/semantics/methods.k:15 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "isalpha", .Vals) => notBool (CS ==K .IntSeq) andBool allAlpha(CS)
```

## 0761 reference-semantics/semantics/methods.k:16 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "isdigit", .Vals) => notBool (CS ==K .IntSeq) andBool allDigit(CS)
```

## 0762 reference-semantics/semantics/methods.k:19 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "lower",    .Vals) => str(mapLower(CS))
```

## 0763 reference-semantics/semantics/methods.k:20 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "upper",    .Vals) => str(mapUpper(CS))
```

## 0764 reference-semantics/semantics/methods.k:21 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "swapcase", .Vals) => str(mapSwap(CS))
```

## 0765 reference-semantics/semantics/methods.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(SEP:IntSeq), "join", list(VS:ValSeq), .Vals) => str(joinCodes(SEP, VS))
```

## 0766 reference-semantics/semantics/methods.k:27 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= joinCodes(IntSeq, ValSeq) [function, total]
```

## 0767 reference-semantics/semantics/methods.k:28 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule joinCodes(_:IntSeq, .ValSeq) => .IntSeq
```

## 0768 reference-semantics/semantics/methods.k:29 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule joinCodes(_:IntSeq, vCons(str(CS:IntSeq), .ValSeq)) => CS
```

## 0769 reference-semantics/semantics/methods.k:30 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule joinCodes(SEP:IntSeq, vCons(str(CS:IntSeq), vCons(V:Val, R:ValSeq)))
    => seqConcat(CS, seqConcat(SEP, joinCodes(SEP, vCons(V, R))))
```

## 0770 reference-semantics/semantics/methods.k:34 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "count", str(PC:IntSeq), .Vals) => cntSub(CS, PC)
```

## 0771 reference-semantics/semantics/methods.k:35 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= cntSub(IntSeq, IntSeq) [function]
```

## 0772 reference-semantics/semantics/methods.k:36 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntSub(.IntSeq, _:IntSeq) => 0
```

## 0773 reference-semantics/semantics/methods.k:37 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => 1 +Int cntSub(dropIS(iCons(C, R), isLen(PC)), PC)
       requires strPrefix(PC, iCons(C, R)) andBool isLen(PC) >Int 0
```

## 0774 reference-semantics/semantics/methods.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntSub(iCons(C:Int, R:IntSeq), PC:IntSeq) => cntSub(R, PC)
       requires notBool strPrefix(PC, iCons(C, R)) orBool isLen(PC) <=Int 0
```

## 0775 reference-semantics/semantics/methods.k:41 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= dropIS(IntSeq, Int) [function, total]
```

## 0776 reference-semantics/semantics/methods.k:42 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dropIS(S:IntSeq, N:Int) => S requires N <=Int 0
```

## 0777 reference-semantics/semantics/methods.k:43 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dropIS(.IntSeq, _:Int) => .IntSeq [owise]
```

## 0778 reference-semantics/semantics/methods.k:44 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dropIS(iCons(_:Int, R:IntSeq), N:Int) => dropIS(R, N -Int 1) requires N >Int 0
```

## 0779 reference-semantics/semantics/methods.k:47 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "strip", .Vals) => str(revIS(trimWS(revIS(trimWS(CS)))))
```

## 0780 reference-semantics/semantics/methods.k:48 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= trimWS(IntSeq) [function, total]
```

## 0781 reference-semantics/semantics/methods.k:49 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule trimWS(.IntSeq) => .IntSeq
```

## 0782 reference-semantics/semantics/methods.k:50 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => trimWS(R) requires isWSC(C)
```

## 0783 reference-semantics/semantics/methods.k:51 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule trimWS(iCons(C:Int, R:IntSeq)) => iCons(C, R) requires notBool isWSC(C)
```

## 0784 reference-semantics/semantics/methods.k:52 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= revIS(IntSeq) [function, total] | revISAcc(IntSeq, IntSeq) [function, total]
```

## 0785 reference-semantics/semantics/methods.k:53 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revIS(S:IntSeq) => revISAcc(S, .IntSeq)
```

## 0786 reference-semantics/semantics/methods.k:54 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revISAcc(.IntSeq, A:IntSeq) => A
```

## 0787 reference-semantics/semantics/methods.k:55 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revISAcc(iCons(C:Int, R:IntSeq), A:IntSeq) => revISAcc(R, iCons(C, A))
```

## 0788 reference-semantics/semantics/methods.k:58 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

## 0789 reference-semantics/semantics/methods.k:61 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(XC:IntSeq), "startswith", str(PC:IntSeq), .Vals) => startsWith(PC, XC)
```

## 0790 reference-semantics/semantics/methods.k:64 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(list(VS:ValSeq), "count", V:Val, .Vals) => cntOccVS(VS, V)
```

## 0791 reference-semantics/semantics/methods.k:65 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= cntOccVS(ValSeq, Val) [function, total]
```

## 0792 reference-semantics/semantics/methods.k:66 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntOccVS(.ValSeq, _:Val)                => 0
```

## 0793 reference-semantics/semantics/methods.k:67 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => 1 +Int cntOccVS(R, V) requires A ==K V
```

## 0794 reference-semantics/semantics/methods.k:68 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule cntOccVS(vCons(A:Val, R:ValSeq), V:Val) => cntOccVS(R, V)        requires notBool (A ==K V)
```

## 0795 reference-semantics/semantics/methods.k:72 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), .Vals)
        => #alloc(list(splitWS(CS, .IntSeq, .ValSeq))) ... </k>
       [priority(40)]
```

## 0796 reference-semantics/semantics/methods.k:75 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= splitWS(IntSeq, IntSeq, ValSeq) [function]  // remaining, current token, result
```

## 0797 reference-semantics/semantics/methods.k:76 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitWS(.IntSeq, CUR:IntSeq, ACC:ValSeq) => flushTok(ACC, CUR)
```

## 0798 reference-semantics/semantics/methods.k:77 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, .IntSeq, flushTok(ACC, CUR))
       requires isWSC(C)
```

## 0799 reference-semantics/semantics/methods.k:79 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitWS(iCons(C:Int, R:IntSeq), CUR:IntSeq, ACC:ValSeq) => splitWS(R, seqConcat(CUR, iCons(C, .IntSeq)), ACC)
       requires notBool isWSC(C)
```

## 0800 reference-semantics/semantics/methods.k:82 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= flushTok(ValSeq, IntSeq) [function]
```

## 0801 reference-semantics/semantics/methods.k:83 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule flushTok(ACC:ValSeq, .IntSeq)            => ACC
```

## 0802 reference-semantics/semantics/methods.k:84 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule flushTok(ACC:ValSeq, iCons(C:Int, T:IntSeq)) => valSeqConcat(ACC, vCons(str(iCons(C, T)), .ValSeq))
```

## 0803 reference-semantics/semantics/methods.k:85 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isWSC(Int) [function, total]
```

## 0804 reference-semantics/semantics/methods.k:86 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isWSC(C:Int) => C ==Int 32 orBool C ==Int 9 orBool C ==Int 10 orBool C ==Int 13
```

## 0805 reference-semantics/semantics/methods.k:89 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (kwV("sep", str(S:IntSeq)), .Vals))
        => #applyK(toCall(boundMethodV(str(CS), "split")), (str(S), .Vals)) ... </k>
       [priority(39)]
```

## 0806 reference-semantics/semantics/methods.k:94 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(str(CS:IntSeq), "split")), (str(iCons(SEP:Int, .IntSeq)), .Vals))
        => #alloc(list(splitSep(CS, SEP, .IntSeq))) ... </k>
       [priority(40)]
```

## 0807 reference-semantics/semantics/methods.k:97 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= splitSep(IntSeq, Int, IntSeq) [function]  // remaining, sep code, current token
```

## 0808 reference-semantics/semantics/methods.k:98 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitSep(.IntSeq, _SEP:Int, CUR:IntSeq)              => vCons(str(CUR), .ValSeq)
```

## 0809 reference-semantics/semantics/methods.k:99 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => vCons(str(CUR), splitSep(R, SEP, .IntSeq))
       requires C ==Int SEP
```

## 0810 reference-semantics/semantics/methods.k:101 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule splitSep(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq) => splitSep(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
       requires notBool (C ==Int SEP)
```

## 0811 reference-semantics/semantics/methods.k:104 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(str(CS:IntSeq), "replace", str(iCons(A:Int, .IntSeq)), str(iCons(B:Int, .IntSeq)), .Vals)
    => str(replaceC(CS, A, B))
```

## 0812 reference-semantics/semantics/methods.k:106 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= replaceC(IntSeq, Int, Int) [function, total]
```

## 0813 reference-semantics/semantics/methods.k:107 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule replaceC(.IntSeq, _:Int, _:Int)             => .IntSeq
```

## 0814 reference-semantics/semantics/methods.k:108 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(B, replaceC(R, A, B)) requires C ==Int A
```

## 0815 reference-semantics/semantics/methods.k:109 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule replaceC(iCons(C:Int, R:IntSeq), A:Int, B:Int) => iCons(C, replaceC(R, A, B)) requires notBool (C ==Int A)
```

## 0816 reference-semantics/semantics/methods.k:112 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isUpperC(Int) [function, total]
```

## 0817 reference-semantics/semantics/methods.k:113 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isUpperC(C:Int) => C >=Int 65 andBool C <=Int 90
```

## 0818 reference-semantics/semantics/methods.k:115 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isLowerC(Int) [function, total]
```

## 0819 reference-semantics/semantics/methods.k:116 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isLowerC(C:Int) => C >=Int 97 andBool C <=Int 122
```

## 0820 reference-semantics/semantics/methods.k:118 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isAlphaC(Int) [function, total]
```

## 0821 reference-semantics/semantics/methods.k:119 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isAlphaC(C:Int) => isUpperC(C) orBool isLowerC(C)
```

## 0822 reference-semantics/semantics/methods.k:121 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= isDigitC(Int) [function, total]
```

## 0823 reference-semantics/semantics/methods.k:122 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule isDigitC(C:Int) => C >=Int 48 andBool C <=Int 57
```

## 0824 reference-semantics/semantics/methods.k:124 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= hasUpper(IntSeq) [function, total]
```

## 0825 reference-semantics/semantics/methods.k:125 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasUpper(.IntSeq) => false
```

## 0826 reference-semantics/semantics/methods.k:126 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasUpper(iCons(C:Int, S:IntSeq)) => isUpperC(C) orBool hasUpper(S)
```

## 0827 reference-semantics/semantics/methods.k:128 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= hasLower(IntSeq) [function, total]
```

## 0828 reference-semantics/semantics/methods.k:129 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasLower(.IntSeq) => false
```

## 0829 reference-semantics/semantics/methods.k:130 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule hasLower(iCons(C:Int, S:IntSeq)) => isLowerC(C) orBool hasLower(S)
```

## 0830 reference-semantics/semantics/methods.k:132 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= allAlpha(IntSeq) [function, total]
```

## 0831 reference-semantics/semantics/methods.k:133 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule allAlpha(.IntSeq) => true
```

## 0832 reference-semantics/semantics/methods.k:134 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule allAlpha(iCons(C:Int, S:IntSeq)) => isAlphaC(C) andBool allAlpha(S)
```

## 0833 reference-semantics/semantics/methods.k:136 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= allDigit(IntSeq) [function, total]
```

## 0834 reference-semantics/semantics/methods.k:137 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule allDigit(.IntSeq) => true
```

## 0835 reference-semantics/semantics/methods.k:138 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule allDigit(iCons(C:Int, S:IntSeq)) => isDigitC(C) andBool allDigit(S)
```

## 0836 reference-semantics/semantics/methods.k:140 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= lowerC(Int) [function, total]
```

## 0837 reference-semantics/semantics/methods.k:142 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule lowerC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 0838 reference-semantics/semantics/methods.k:143 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule lowerC(C:Int) => C         [owise]
```

## 0839 reference-semantics/semantics/methods.k:145 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= upperC(Int) [function, total]
```

## 0840 reference-semantics/semantics/methods.k:146 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule upperC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 0841 reference-semantics/semantics/methods.k:147 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule upperC(C:Int) => C         [owise]
```

## 0842 reference-semantics/semantics/methods.k:149 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= swapC(Int) [function, total]
```

## 0843 reference-semantics/semantics/methods.k:150 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule swapC(C:Int) => C +Int 32 requires isUpperC(C)
```

## 0844 reference-semantics/semantics/methods.k:151 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule swapC(C:Int) => C -Int 32 requires isLowerC(C)
```

## 0845 reference-semantics/semantics/methods.k:152 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule swapC(C:Int) => C         [owise]
```

## 0846 reference-semantics/semantics/methods.k:154 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= mapLower(IntSeq) [function, total]
```

## 0847 reference-semantics/semantics/methods.k:155 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapLower(.IntSeq) => .IntSeq
```

## 0848 reference-semantics/semantics/methods.k:156 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapLower(iCons(C:Int, S:IntSeq)) => iCons(lowerC(C), mapLower(S))
```

## 0849 reference-semantics/semantics/methods.k:158 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= mapUpper(IntSeq) [function, total]
```

## 0850 reference-semantics/semantics/methods.k:159 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapUpper(.IntSeq) => .IntSeq
```

## 0851 reference-semantics/semantics/methods.k:160 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapUpper(iCons(C:Int, S:IntSeq)) => iCons(upperC(C), mapUpper(S))
```

## 0852 reference-semantics/semantics/methods.k:162 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= mapSwap(IntSeq) [function, total]
```

## 0853 reference-semantics/semantics/methods.k:163 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapSwap(.IntSeq) => .IntSeq
```

## 0854 reference-semantics/semantics/methods.k:164 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule mapSwap(iCons(C:Int, S:IntSeq)) => iCons(swapC(C), mapSwap(S))
```

## 0855 reference-semantics/semantics/methods.k:166 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= startsWith(IntSeq, IntSeq) [function, total]
```

## 0856 reference-semantics/semantics/methods.k:167 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule startsWith(.IntSeq, _:IntSeq)               => true
```

## 0857 reference-semantics/semantics/methods.k:168 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule startsWith(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 0858 reference-semantics/semantics/methods.k:169 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule startsWith(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool startsWith(As, Bs)
```

## 0859 reference-semantics/semantics/methods.k:170 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0860 reference-semantics/semantics/operators.k:6 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-OPERATORS
```

## 0861 reference-semantics/semantics/operators.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0862 reference-semantics/semantics/operators.k:8 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0863 reference-semantics/semantics/operators.k:10 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> UnaryOp(OP:String, V:Val) => applyUn(OP, V) ... </k>
```

## 0864 reference-semantics/semantics/operators.k:12 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BinOp(OP:String, L:Val, R:Val) => applyBin(OP, L, R) ... </k>
```

## 0865 reference-semantics/semantics/operators.k:15 [context]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  context Compare(HOLE, _)
```

## 0866 reference-semantics/semantics/operators.k:16 [context]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  context Compare(_:Val, CmpOp(_, HOLE))
```

## 0867 reference-semantics/semantics/operators.k:17 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(LV:Val, CmpOp(OP:String, RV:Val)) => applyCmp(OP, LV, RV) ... </k> [owise]
```

## 0868 reference-semantics/semantics/operators.k:19 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("is",     V:Val, noneV) => V ==K noneV
```

## 0869 reference-semantics/semantics/operators.k:20 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("is not", V:Val, noneV) => notBool (V ==K noneV)
```

## 0870 reference-semantics/semantics/operators.k:25 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BinOp(OP:String, ref(H:Int), R:Expr) => BinOp(OP, V, R) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0871 reference-semantics/semantics/operators.k:28 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> BinOp(OP:String, L:Val, ref(H:Int)) => BinOp(OP, L, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
       [priority(40)]
```

## 0872 reference-semantics/semantics/operators.k:34 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(ref(H:Int), CmpOp(OP:String, R:Expr)) => Compare(V, CmpOp(OP, R)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires OP =/=String "in" andBool OP =/=String "not in"
       [priority(40)]
```

## 0873 reference-semantics/semantics/operators.k:38 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(L:Val, CmpOp(OP:String, ref(H:Int))) => Compare(L, CmpOp(OP, V)) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       requires notBool isRefV(L)
        orBool OP ==String "in" orBool OP ==String "not in"
       [priority(40)]
```

## 0874 reference-semantics/semantics/operators.k:44 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> UnaryOp(OP:String, ref(H:Int)) => UnaryOp(OP, V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0875 reference-semantics/semantics/operators.k:47 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0876 reference-semantics/semantics/range.k:5 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-RANGE
```

## 0877 reference-semantics/semantics/range.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0878 reference-semantics/semantics/range.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0879 reference-semantics/semantics/range.k:9 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= inRange(Int, Int, Int) [function, total]
```

## 0880 reference-semantics/semantics/range.k:10 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule inRange(I:Int, HI:Int, ST:Int) => (ST >Int 0 andBool I <Int HI) orBool (ST <Int 0 andBool I >Int HI)
```

## 0881 reference-semantics/semantics/range.k:12 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= rangeLen(Int, Int, Int) [function]
```

## 0882 reference-semantics/semantics/range.k:13 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (HI -Int LO +Int ST -Int 1) /Int ST
       requires ST >Int 0 andBool HI >Int LO
```

## 0883 reference-semantics/semantics/range.k:15 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => (LO -Int HI -Int ST -Int 1) /Int (0 -Int ST)
       requires ST <Int 0 andBool HI <Int LO
```

## 0884 reference-semantics/semantics/range.k:17 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule rangeLen(LO:Int, HI:Int, ST:Int) => 0
       requires (ST >Int 0 andBool HI <=Int LO) orBool (ST <Int 0 andBool HI >=Int LO)
```

## 0885 reference-semantics/semantics/range.k:20 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int))
        => #iterYield(I, rangeObj(I +Int ST, HI, ST)) ... </k>
       requires inRange(I, HI, ST)
```

## 0886 reference-semantics/semantics/range.k:23 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(rangeObj(I:Int, HI:Int, ST:Int)) => #iterDone ... </k>
       requires notBool inRange(I, HI, ST)
```

## 0887 reference-semantics/semantics/range.k:25 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0888 reference-semantics/semantics/set.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-SET
```

## 0889 reference-semantics/semantics/set.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0890 reference-semantics/semantics/set.k:8 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= setV(IntSeq)
```

## 0891 reference-semantics/semantics/set.k:11 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= codeIn(Int, IntSeq) [function, total]
```

## 0892 reference-semantics/semantics/set.k:12 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule codeIn(_:Int, .IntSeq)                => false
```

## 0893 reference-semantics/semantics/set.k:13 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule codeIn(C:Int, iCons(H:Int, T:IntSeq)) => C ==Int H orBool codeIn(C, T)
```

## 0894 reference-semantics/semantics/set.k:16 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= dedupCodes(IntSeq)         [function, total]
                  | dedupFrom(IntSeq, IntSeq)  [function, total]
```

## 0895 reference-semantics/semantics/set.k:18 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dedupCodes(CS:IntSeq) => dedupFrom(CS, .IntSeq)
```

## 0896 reference-semantics/semantics/set.k:19 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dedupFrom(.IntSeq, ACC:IntSeq) => ACC
```

## 0897 reference-semantics/semantics/set.k:20 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, ACC)
       requires codeIn(C, ACC)
```

## 0898 reference-semantics/semantics/set.k:22 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule dedupFrom(iCons(C:Int, S:IntSeq), ACC:IntSeq) => dedupFrom(S, snocCode(ACC, C))
       requires notBool codeIn(C, ACC)
```

## 0899 reference-semantics/semantics/set.k:25 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= snocCode(IntSeq, Int) [function, total]
```

## 0900 reference-semantics/semantics/set.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule snocCode(.IntSeq, C:Int)                => iCons(C, .IntSeq)
```

## 0901 reference-semantics/semantics/set.k:27 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule snocCode(iCons(H:Int, T:IntSeq), C:Int) => iCons(H, snocCode(T, C))
```

## 0902 reference-semantics/semantics/set.k:31 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= subsetCodes(IntSeq, IntSeq) [function, total]
```

## 0903 reference-semantics/semantics/set.k:32 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule subsetCodes(.IntSeq, _:IntSeq)                => true
```

## 0904 reference-semantics/semantics/set.k:33 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule subsetCodes(iCons(C:Int, S:IntSeq), B:IntSeq) => codeIn(C, B) andBool subsetCodes(S, B)
```

## 0905 reference-semantics/semantics/set.k:35 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= sameSet(IntSeq, IntSeq) [function, total]
```

## 0906 reference-semantics/semantics/set.k:36 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule sameSet(A:IntSeq, B:IntSeq) => subsetCodes(A, B) andBool subsetCodes(B, A)
```

## 0907 reference-semantics/semantics/set.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", setV(A:IntSeq), setV(B:IntSeq)) => sameSet(A, B)
```

## 0908 reference-semantics/semantics/set.k:40 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0909 reference-semantics/semantics/sort.k:10 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-SORT
```

## 0910 reference-semantics/semantics/sort.k:11 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-BUILTINS
```

## 0911 reference-semantics/semantics/sort.k:12 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-SUBSCRIPT
```

## 0912 reference-semantics/semantics/sort.k:18 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax ValSeq ::= sortVS(ValSeq) [function, total, symbol(sortVS), no-evaluators]
```

## 0913 reference-semantics/semantics/sort.k:19 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= insVS(Int, ValSeq) [function]
```

## 0914 reference-semantics/semantics/sort.k:20 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule sortVS(.ValSeq)                => .ValSeq          [concrete]
```

## 0915 reference-semantics/semantics/sort.k:21 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule sortVS(vCons(X:Int, R:ValSeq)) => insVS(X, sortVS(R)) [concrete]
```

## 0916 reference-semantics/semantics/sort.k:22 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVS(X:Int, .ValSeq)                => vCons(X, .ValSeq) [concrete]
```

## 0917 reference-semantics/semantics/sort.k:23 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(X, vCons(Y, R)) requires X <=Int Y [concrete]
```

## 0918 reference-semantics/semantics/sort.k:24 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVS(X:Int, vCons(Y:Int, R:ValSeq)) => vCons(Y, insVS(X, R)) requires X  >Int Y [concrete]
```

## 0919 reference-semantics/semantics/sort.k:26 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= insVSs(IntSeq, ValSeq) [function]
```

## 0920 reference-semantics/semantics/sort.k:27 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule sortVS(vCons(str(CS:IntSeq), R:ValSeq)) => insVSs(CS, sortVS(R)) [concrete]
```

## 0921 reference-semantics/semantics/sort.k:28 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVSs(A:IntSeq, .ValSeq) => vCons(str(A), .ValSeq) [concrete]
```

## 0922 reference-semantics/semantics/sort.k:29 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(A), vCons(str(B), R))
       requires strLt(A, B) orBool A ==K B [concrete]
```

## 0923 reference-semantics/semantics/sort.k:31 [rule:equational]
DISPOSITION: ACCEPT: concrete-only supplied-semantics equation; absent from the Haskell proof theory unless attached to a function evaluator
```k
  rule insVSs(A:IntSeq, vCons(str(B:IntSeq), R:ValSeq)) => vCons(str(B), insVSs(A, R))
       requires notBool (strLt(A, B) orBool A ==K B) [concrete]
```

## 0924 reference-semantics/semantics/sort.k:36 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))
        => #alloc(list(sortVS(VS))) ... </k>
```

## 0925 reference-semantics/semantics/sort.k:40 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(boundMethodV(ref(H:Int), "sort")), .Vals) => noneV ... </k>
       <heap> ... H |-> list(VS:ValSeq => sortVS(VS)) ... </heap>
       [priority(40)]
```

## 0926 reference-semantics/semantics/sort.k:49 [syntax]
DISPOSITION: BOUNDARY: supplied opaque/trusted symbol declaration
```k
  syntax ValSeq ::= sortKeyVS(ValSeq, Val) [function, total, symbol(sortKeyVS), no-evaluators]
```

## 0927 reference-semantics/semantics/sort.k:51 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= revVS(ValSeq) [function, total]
                  | revVSAcc(ValSeq, ValSeq) [function, total]
```

## 0928 reference-semantics/semantics/sort.k:53 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revVS(S:ValSeq) => revVSAcc(S, .ValSeq)
```

## 0929 reference-semantics/semantics/sort.k:54 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revVSAcc(.ValSeq, A:ValSeq) => A
```

## 0930 reference-semantics/semantics/sort.k:55 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule revVSAcc(vCons(V:Val, R:ValSeq), A:ValSeq) => revVSAcc(R, vCons(V, A))
```

## 0931 reference-semantics/semantics/sort.k:57 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= condRev(ValSeq, Bool) [function, total]
```

## 0932 reference-semantics/semantics/sort.k:58 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule condRev(S:ValSeq, false) => S
```

## 0933 reference-semantics/semantics/sort.k:59 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule condRev(S:ValSeq, true)  => revVS(S)
```

## 0934 reference-semantics/semantics/sort.k:61 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), .Vals))
        => #alloc(list(sortKeyVS(VS, KV))) ... </k>
```

## 0935 reference-semantics/semantics/sort.k:63 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("key", KV:Val), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortKeyVS(VS, KV), RB))) ... </k>
```

## 0936 reference-semantics/semantics/sort.k:65 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), kwV("reverse", RB:Bool), .Vals))
        => #alloc(list(condRev(sortVS(VS), RB))) ... </k>
```

## 0937 reference-semantics/semantics/sort.k:72 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0938 reference-semantics/semantics/str.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-STR
```

## 0939 reference-semantics/semantics/str.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0940 reference-semantics/semantics/str.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 0941 reference-semantics/semantics/str.k:8 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(str(.IntSeq))                 => #iterDone ... </k>
```

## 0942 reference-semantics/semantics/str.k:9 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(str(iCons(C:Int, R:IntSeq)))
        => #iterYield(str(iCons(C, .IntSeq)), str(R)) ... </k>
```

## 0943 reference-semantics/semantics/str.k:13 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= strToCodes(String) [function]
```

## 0944 reference-semantics/semantics/str.k:14 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Str(S:String) => str(strToCodes(S)) ... </k>
```

## 0945 reference-semantics/semantics/str.k:15 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strToCodes("") => .IntSeq
```

## 0946 reference-semantics/semantics/str.k:16 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strToCodes(S:String) => iCons(ordChar(substrString(S, 0, 1)), strToCodes(substrString(S, 1, lengthString(S))))
    requires S =/=String "" andBool ordChar(substrString(S, 0, 1)) <Int 128
```

## 0947 reference-semantics/semantics/str.k:20 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= seqConcat(IntSeq, IntSeq) [function, total]
```

## 0948 reference-semantics/semantics/str.k:21 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqConcat(.IntSeq, T:IntSeq)                => T
```

## 0949 reference-semantics/semantics/str.k:22 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule seqConcat(iCons(I:Int, S:IntSeq), T:IntSeq) => iCons(I, seqConcat(S, T))
```

## 0950 reference-semantics/semantics/str.k:24 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyBin("+",  str(A:IntSeq), str(B:IntSeq)) => str(seqConcat(A, B))
```

## 0951 reference-semantics/semantics/str.k:25 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", str(A:IntSeq), str(B:IntSeq)) => A ==K B
```

## 0952 reference-semantics/semantics/str.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", str(A:IntSeq), str(B:IntSeq)) => notBool (A ==K B)
```

## 0953 reference-semantics/semantics/str.k:29 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("in",     str(P:IntSeq), str(X:IntSeq)) => strContains(P, X)
```

## 0954 reference-semantics/semantics/str.k:30 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("not in", str(P:IntSeq), str(X:IntSeq)) => notBool strContains(P, X)
```

## 0955 reference-semantics/semantics/str.k:32 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= strPrefix(IntSeq, IntSeq) [function, total]
```

## 0956 reference-semantics/semantics/str.k:33 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strPrefix(.IntSeq, _:IntSeq)               => true
```

## 0957 reference-semantics/semantics/str.k:34 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strPrefix(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 0958 reference-semantics/semantics/str.k:35 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strPrefix(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => A ==Int B andBool strPrefix(As, Bs)
```

## 0959 reference-semantics/semantics/str.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= strContains(IntSeq, IntSeq) [function, total]
```

## 0960 reference-semantics/semantics/str.k:38 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strContains(P:IntSeq, X:IntSeq) => true  requires strPrefix(P, X)
```

## 0961 reference-semantics/semantics/str.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strContains(P:IntSeq, .IntSeq)  => false requires notBool strPrefix(P, .IntSeq)
```

## 0962 reference-semantics/semantics/str.k:40 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strContains(P:IntSeq, iCons(C:Int, Xs:IntSeq)) => strContains(P, Xs)
       requires notBool strPrefix(P, iCons(C, Xs))
```

## 0963 reference-semantics/semantics/str.k:48 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bool ::= strLt(IntSeq, IntSeq) [function, total]
```

## 0964 reference-semantics/semantics/str.k:49 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(.IntSeq, .IntSeq)                => false
```

## 0965 reference-semantics/semantics/str.k:50 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(.IntSeq, iCons(_:Int, _:IntSeq)) => true
```

## 0966 reference-semantics/semantics/str.k:51 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(iCons(_:Int, _:IntSeq), .IntSeq) => false
```

## 0967 reference-semantics/semantics/str.k:52 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => true          requires A  <Int B
```

## 0968 reference-semantics/semantics/str.k:53 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => false         requires A  >Int B
```

## 0969 reference-semantics/semantics/str.k:54 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule strLt(iCons(A:Int, As:IntSeq), iCons(B:Int, Bs:IntSeq)) => strLt(As, Bs) requires A ==Int B
```

## 0970 reference-semantics/semantics/str.k:56 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<",  str(A:IntSeq), str(B:IntSeq)) => strLt(A, B)
```

## 0971 reference-semantics/semantics/str.k:57 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">",  str(A:IntSeq), str(B:IntSeq)) => strLt(B, A)
```

## 0972 reference-semantics/semantics/str.k:58 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("<=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(B, A)
```

## 0973 reference-semantics/semantics/str.k:59 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp(">=", str(A:IntSeq), str(B:IntSeq)) => notBool strLt(A, B)
```

## 0974 reference-semantics/semantics/str.k:60 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 0975 reference-semantics/semantics/subscript.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-SUBSCRIPT
```

## 0976 reference-semantics/semantics/subscript.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 0977 reference-semantics/semantics/subscript.k:11 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= valSeqAt(ValSeq, Int) [function, total]
```

## 0978 reference-semantics/semantics/subscript.k:12 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule valSeqAt(vCons(V:Val, _:ValSeq), 0)     => V
```

## 0979 reference-semantics/semantics/subscript.k:13 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule valSeqAt(vCons(_:Val, S:ValSeq), I:Int) => valSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 0980 reference-semantics/semantics/subscript.k:16 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= intSeqAt(IntSeq, Int) [function]
```

## 0981 reference-semantics/semantics/subscript.k:17 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intSeqAt(iCons(C:Int, _:IntSeq), 0)     => C
```

## 0982 reference-semantics/semantics/subscript.k:18 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule intSeqAt(iCons(_:Int, S:IntSeq), I:Int) => intSeqAt(S, I -Int 1)
       requires I >Int 0
```

## 0983 reference-semantics/semantics/subscript.k:21 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= normIdx(Int, Int) [function, total]
```

## 0984 reference-semantics/semantics/subscript.k:22 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule normIdx(I:Int, LEN:Int) => I +Int LEN requires I  <Int 0
```

## 0985 reference-semantics/semantics/subscript.k:23 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule normIdx(I:Int, _:Int)   => I          requires I >=Int 0
```

## 0986 reference-semantics/semantics/subscript.k:27 [context]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  context Subscript(HOLE, _)
```

## 0987 reference-semantics/semantics/subscript.k:28 [context]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  context Subscript(_:Val, HOLE:Expr)
```

## 0988 reference-semantics/semantics/subscript.k:31 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Subscript(ref(H:Int), IX:Index) => Subscript(V, IX) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 0989 reference-semantics/semantics/subscript.k:35 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Subscript(OBJ:Val, I:Int) => applyIndex(OBJ, I) ... </k>
```

## 0990 reference-semantics/semantics/subscript.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= applyIndex(Val, Int) [function]
```

## 0991 reference-semantics/semantics/subscript.k:38 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyIndex(list(VS:ValSeq),  I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 0992 reference-semantics/semantics/subscript.k:39 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyIndex(tuple(VS:ValSeq), I:Int) => valSeqAt(VS, normIdx(I, vsLen(VS)))
```

## 0993 reference-semantics/semantics/subscript.k:40 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyIndex(str(IS:IntSeq),   I:Int)
    => str(iCons(intSeqAt(IS, normIdx(I, isLen(IS))), .IntSeq))
```

## 0994 reference-semantics/semantics/subscript.k:44 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #evalB(Bound) | "#toSome"
                 | #slLo(Val, Bound, Bound)
                 | #slHi(Val, OptInt, Bound)
                 | #slStep(Val, OptInt, OptInt)
```

## 0995 reference-semantics/semantics/subscript.k:49 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax OptInt ::= "noB" | someB(Int)
```

## 0996 reference-semantics/semantics/subscript.k:50 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #evalB(NoBound)  => noB ... </k>
```

## 0997 reference-semantics/semantics/subscript.k:51 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #evalB(E:Expr)   => E ~> #toSome ... </k>
```

## 0998 reference-semantics/semantics/subscript.k:52 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> I:Int ~> #toSome => someB(I) ... </k>
```

## 0999 reference-semantics/semantics/subscript.k:54 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Subscript(OBJ:Val, Slice(LO:Bound, HI:Bound, ST:Bound)) => #evalB(LO) ~> #slLo(OBJ, HI, ST) ... </k>
```

## 1000 reference-semantics/semantics/subscript.k:55 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> LO:OptInt ~> #slLo(OBJ:Val, HI:Bound, ST:Bound)   => #evalB(HI) ~> #slHi(OBJ, LO, ST) ... </k>
```

## 1001 reference-semantics/semantics/subscript.k:56 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> HI:OptInt ~> #slHi(OBJ:Val, LO:OptInt, ST:Bound)  => #evalB(ST) ~> #slStep(OBJ, LO, HI) ... </k>
```

## 1002 reference-semantics/semantics/subscript.k:58 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ST:OptInt ~> #slStep(list(VS:ValSeq), LO:OptInt, HI:OptInt)
        => #alloc(doSlice(list(VS), LO, HI, ST)) ... </k>
       [priority(45)]
```

## 1003 reference-semantics/semantics/subscript.k:61 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> ST:OptInt ~> #slStep(OBJ:Val, LO:OptInt, HI:OptInt) => doSlice(OBJ, LO, HI, ST) ... </k>
```

## 1004 reference-semantics/semantics/subscript.k:63 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Val ::= doSlice(Val, OptInt, OptInt, OptInt) [function]
```

## 1005 reference-semantics/semantics/subscript.k:64 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule doSlice(list(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => list(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 1006 reference-semantics/semantics/subscript.k:66 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule doSlice(tuple(VS:ValSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => tuple(buildVS(VS, slStart(LO, ST, vsLen(VS)), slStop(HI, ST, vsLen(VS)), slStep(ST)))
```

## 1007 reference-semantics/semantics/subscript.k:68 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule doSlice(str(IS:IntSeq), LO:OptInt, HI:OptInt, ST:OptInt)
    => str(buildIS(IS, slStart(LO, ST, isLen(IS)), slStop(HI, ST, isLen(IS)), slStep(ST)))
```

## 1008 reference-semantics/semantics/subscript.k:72 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= slStep(OptInt) [function, total]
```

## 1009 reference-semantics/semantics/subscript.k:73 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStep(noB)          => 1
```

## 1010 reference-semantics/semantics/subscript.k:74 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStep(someB(S:Int)) => S
```

## 1011 reference-semantics/semantics/subscript.k:76 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= slStart(OptInt, OptInt, Int) [function]
```

## 1012 reference-semantics/semantics/subscript.k:77 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStart(noB,          ST:OptInt, _LEN:Int) => 0
       requires slStep(ST) >Int 0
```

## 1013 reference-semantics/semantics/subscript.k:79 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStart(noB,          ST:OptInt, LEN:Int)  => LEN -Int 1
       requires slStep(ST) <Int 0
```

## 1014 reference-semantics/semantics/subscript.k:81 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStart(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 1015 reference-semantics/semantics/subscript.k:83 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= slStop(OptInt, OptInt, Int) [function]
```

## 1016 reference-semantics/semantics/subscript.k:84 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStop(noB,          ST:OptInt, LEN:Int)  => LEN
       requires slStep(ST) >Int 0
```

## 1017 reference-semantics/semantics/subscript.k:86 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStop(noB,          ST:OptInt, _LEN:Int) => -1
       requires slStep(ST) <Int 0
```

## 1018 reference-semantics/semantics/subscript.k:88 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slStop(someB(I:Int), ST:OptInt, LEN:Int)  => slAdjust(I, LEN, slStep(ST))
```

## 1019 reference-semantics/semantics/subscript.k:90 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= slAdjust(Int, Int, Int) [function, total]
```

## 1020 reference-semantics/semantics/subscript.k:91 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampLo(I +Int LEN, STEP)
       requires I  <Int 0
```

## 1021 reference-semantics/semantics/subscript.k:93 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule slAdjust(I:Int, LEN:Int, STEP:Int) => clampHi(I, LEN, STEP)
       requires I >=Int 0
```

## 1022 reference-semantics/semantics/subscript.k:96 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= clampLo(Int, Int) [function, total]
```

## 1023 reference-semantics/semantics/subscript.k:97 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule clampLo(J:Int, _STEP:Int) => J
       requires J >=Int 0
```

## 1024 reference-semantics/semantics/subscript.k:99 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule clampLo(J:Int, STEP:Int)  => #if STEP <Int 0 #then -1 #else 0 #fi
       requires J <Int 0
```

## 1025 reference-semantics/semantics/subscript.k:102 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= clampHi(Int, Int, Int) [function, total]
```

## 1026 reference-semantics/semantics/subscript.k:103 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule clampHi(I:Int, LEN:Int, _STEP:Int) => I
       requires I  <Int LEN
```

## 1027 reference-semantics/semantics/subscript.k:105 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule clampHi(I:Int, LEN:Int, STEP:Int)  => #if STEP <Int 0 #then LEN -Int 1 #else LEN #fi
       requires I >=Int LEN
```

## 1028 reference-semantics/semantics/subscript.k:109 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ValSeq ::= buildVS(ValSeq, Int, Int, Int) [function]
```

## 1029 reference-semantics/semantics/subscript.k:110 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule buildVS(VS:ValSeq, I:Int, STOP:Int, STEP:Int)
    => vCons(valSeqAt(VS, I), buildVS(VS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 1030 reference-semantics/semantics/subscript.k:113 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule buildVS(_:ValSeq, I:Int, STOP:Int, STEP:Int) => .ValSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 1031 reference-semantics/semantics/subscript.k:116 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax IntSeq ::= buildIS(IntSeq, Int, Int, Int) [function]
```

## 1032 reference-semantics/semantics/subscript.k:117 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule buildIS(IS:IntSeq, I:Int, STOP:Int, STEP:Int)
    => iCons(intSeqAt(IS, I), buildIS(IS, I +Int STEP, STOP, STEP))
       requires (STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP)
```

## 1033 reference-semantics/semantics/subscript.k:120 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule buildIS(_:IntSeq, I:Int, STOP:Int, STEP:Int) => .IntSeq
       requires notBool ((STEP >Int 0 andBool I <Int STOP) orBool (STEP <Int 0 andBool I >Int STOP))
```

## 1034 reference-semantics/semantics/subscript.k:122 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 1035 reference-semantics/semantics/syntax.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-SYNTAX
```

## 1036 reference-semantics/semantics/syntax.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports INT-SYNTAX
```

## 1037 reference-semantics/semantics/syntax.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports FLOAT-SYNTAX
```

## 1038 reference-semantics/semantics/syntax.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports BOOL-SYNTAX
```

## 1039 reference-semantics/semantics/syntax.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports STRING-SYNTAX
```

## 1040 reference-semantics/semantics/syntax.k:9 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Expr ::= "Int"      "(" Int ")"
                | "Float"    "(" Float ")"
                | "Bool"     "(" Bool ")"
                | "Name"     "(" String ")"
                | "Str"      "(" String ")"
                | "UnaryOp"  "(" String "," Expr ")" [strict(2)]
                | "BinOp"    "(" String "," Expr "," Expr ")" [seqstrict(2, 3)]
                | "BoolOp"    "(" String "," Exprs ")"
                | "ListExpr"  "(" Exprs ")"
                | "DictExpr"  "(" Entries ")"
                | "ListComp"  "(" Expr "," CompFors ")" [macro]
                | "GenExp"    "(" Expr "," CompFors ")" [macro]
                | "TupleExpr" "(" Exprs ")"
                | "Subscript" "(" Expr "," Index ")"
                | "IfExp"     "(" Expr "," Expr "," Expr ")" [strict(1)]
                | "Lambda"    "(" Params "," Expr ")"
                | "KwArg"     "(" String "," Expr ")"
                | "Lambda"    "(" Params "," CellVars "," FreeVars "," Expr ")"
                | "NoneVal"
                | "Call"      "(" Expr "," Exprs ")"
                | "Attribute" "(" Expr "," String ")" [strict(1)]
                | "Compare"   "(" Expr "," CmpOp ")"
```

## 1041 reference-semantics/semantics/syntax.k:32 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax CmpOp    ::= "CmpOp" "(" String "," Expr ")"
```

## 1042 reference-semantics/semantics/syntax.k:33 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Entry    ::= "Entry" "(" Expr "," Expr ")"
```

## 1043 reference-semantics/semantics/syntax.k:34 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Entries  ::= List{Entry, ","}
```

## 1044 reference-semantics/semantics/syntax.k:35 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax CompFor  ::= "CompFor" "(" Expr "," Expr "," Exprs ")"
```

## 1045 reference-semantics/semantics/syntax.k:36 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax CompFors ::= List{CompFor, ""}
```

## 1046 reference-semantics/semantics/syntax.k:37 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Exprs    ::= List{Expr, ","}
```

## 1047 reference-semantics/semantics/syntax.k:38 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Index    ::= Expr | "Slice" "(" Bound "," Bound "," Bound ")"
```

## 1048 reference-semantics/semantics/syntax.k:39 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Bound    ::= Expr | "NoBound"
```

## 1049 reference-semantics/semantics/syntax.k:41 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Stmt ::= "Assign"    "(" Expr "," Expr ")" [strict(2)]
                | "Import"    "(" String ")"
                | "ImportFrom" "(" String "," ParamNames ")"
                | "AugAssign" "(" Expr "," String "," Expr ")" [strict(3)]
                | "For"       "(" Expr "," Expr "," Stmts ")" [strict(2)]
                | "While"     "(" Expr "," Stmts ")"
                | "Break"
                | "Continue"
                | "If"        "(" Expr "," Stmts "," Stmts ")" [strict(1)]
                | "Return"    "(" Expr ")" [strict]
                | "Assert"    "(" Expr ")" [strict]
                | "Expr"      "(" Expr ")" [strict]
                | "FuncDef"   "(" String "," Params "," Stmts ")"
                | "FuncDef"   "(" String "," Params "," CellVars "," FreeVars "," Stmts ")"
```

## 1050 reference-semantics/semantics/syntax.k:56 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Stmts      ::= List{Stmt, ""}
```

## 1051 reference-semantics/semantics/syntax.k:57 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Params     ::= "Params" "(" ParamNames ")"
```

## 1052 reference-semantics/semantics/syntax.k:58 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax CellVars   ::= "CellVars" "(" ParamNames ")"
```

## 1053 reference-semantics/semantics/syntax.k:59 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax FreeVars   ::= "FreeVars" "(" ParamNames ")"
```

## 1054 reference-semantics/semantics/syntax.k:60 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ParamNames ::= List{String, ","}
```

## 1055 reference-semantics/semantics/syntax.k:61 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Module     ::= "Module" "(" Stmts ")"
```

## 1056 reference-semantics/semantics/syntax.k:62 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 1057 reference-semantics/semantics/tuple.k:3 [module]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
module MPY-TUPLE
```

## 1058 reference-semantics/semantics/tuple.k:4 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-CORE
```

## 1059 reference-semantics/semantics/tuple.k:5 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-ITER
```

## 1060 reference-semantics/semantics/tuple.k:6 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-LIST
```

## 1061 reference-semantics/semantics/tuple.k:7 [imports]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  imports MPY-METHODS
```

## 1062 reference-semantics/semantics/tuple.k:10 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(tuple(.ValSeq))                => #iterDone ... </k>
```

## 1063 reference-semantics/semantics/tuple.k:11 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #iterNext(tuple(vCons(V:Val, R:ValSeq))) => #iterYield(V, tuple(R)) ... </k>
```

## 1064 reference-semantics/semantics/tuple.k:14 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax ApplyK ::= "toTuple"
```

## 1065 reference-semantics/semantics/tuple.k:15 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> TupleExpr(ES:Exprs) => #evalArgs(ES, .Vals, toTuple) ... </k>
```

## 1066 reference-semantics/semantics/tuple.k:16 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #applyK(toTuple, ACC:Vals) => tuple(vals2valSeq(ACC)) ... </k>
```

## 1067 reference-semantics/semantics/tuple.k:18 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("==", tuple(A:ValSeq), tuple(B:ValSeq)) => A ==K B
```

## 1068 reference-semantics/semantics/tuple.k:20 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(LV:Val, CmpOp("in",     tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ... </k>
```

## 1069 reference-semantics/semantics/tuple.k:21 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Compare(LV:Val, CmpOp("not in", tuple(VS:ValSeq))) => #memberAcc(LV, tuple(VS)) ~> #notB ... </k>
```

## 1070 reference-semantics/semantics/tuple.k:23 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyMethod(tuple(VS:ValSeq), "index", V:Val, .Vals) => idxOfVS(VS, V, 0)
```

## 1071 reference-semantics/semantics/tuple.k:24 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax Int ::= idxOfVS(ValSeq, Val, Int) [function]
```

## 1072 reference-semantics/semantics/tuple.k:25 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule idxOfVS(vCons(A:Val, _:ValSeq), V:Val, I:Int) => I requires A ==K V
```

## 1073 reference-semantics/semantics/tuple.k:26 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule idxOfVS(vCons(A:Val, R:ValSeq), V:Val, I:Int) => idxOfVS(R, V, I +Int 1)
       requires notBool (A ==K V)
```

## 1074 reference-semantics/semantics/tuple.k:28 [rule:equational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule applyCmp("!=", tuple(A:ValSeq), tuple(B:ValSeq)) => notBool (A ==K B)
```

## 1075 reference-semantics/semantics/tuple.k:31 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #bindTgt(Expr, Val)
```

## 1076 reference-semantics/semantics/tuple.k:32 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindTgt(Name(X:String), V:Val) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map => M [ X <- V ], _) ... </scopes>
```

## 1077 reference-semantics/semantics/tuple.k:35 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindTgt(Name(X:String), V:Val) => #cellW({M[X]}:>Val, V) ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _) ... </scopes>
       requires "$cells" in_keys(M)
        andBool pnMember(X, cellsOf({M["$cells"]}:>Val))
        andBool X in_keys(M) andBool isCellRef({M[X]}:>Val)
       [priority(40)]
```

## 1078 reference-semantics/semantics/tuple.k:42 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 1079 reference-semantics/semantics/tuple.k:43 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 1080 reference-semantics/semantics/tuple.k:44 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #bindTgt(TupleExpr(TS:Exprs), ref(H:Int)) => #bindTgt(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 1081 reference-semantics/semantics/tuple.k:49 [syntax]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
  syntax KItem ::= #unpackSeq(Exprs, ValSeq)
```

## 1082 reference-semantics/semantics/tuple.k:50 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(TupleExpr(TS:Exprs), tuple(VS:ValSeq)) => #unpackSeq(TS, VS) ... </k>
```

## 1083 reference-semantics/semantics/tuple.k:51 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(TupleExpr(TS:Exprs), list(VS:ValSeq))  => #unpackSeq(TS, VS) ... </k>
```

## 1084 reference-semantics/semantics/tuple.k:52 [rule:priority]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> Assign(TupleExpr(TS:Exprs), ref(H:Int)) => Assign(TupleExpr(TS), V) ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
```

## 1085 reference-semantics/semantics/tuple.k:55 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #unpackSeq((T:Expr, TS:Exprs), vCons(V:Val, VS:ValSeq))
        => #bindTgt(T, V) ~> #unpackSeq(TS, VS) ... </k>
```

## 1086 reference-semantics/semantics/tuple.k:57 [rule:operational]
DISPOSITION: ACCEPT: supplied-semantics rule/equation; no task-answer rule and no false conclusion witness found; target-path analysis in REVIEW.md
```k
  rule <k> #unpackSeq(.Exprs, .ValSeq) => .K ... </k>
```

## 1087 reference-semantics/semantics/tuple.k:58 [endmodule]
DISPOSITION: ACCEPT: supplied-semantics structure/declaration
```k
endmodule
```

## 1088 verification.k:1 [requires]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
requires "reference-semantics/semantics.k"
```

## 1089 verification.k:3 [module]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
module VERIFICATION-SYNTAX
```

## 1090 verification.k:4 [imports]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  imports MPY-SYNTAX
```

## 1091 verification.k:5 [imports]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  imports INT-SYNTAX
```

## 1092 verification.k:7 [syntax]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  syntax Int ::= triValue(Int) [function, total]
```

## 1093 verification.k:8 [syntax]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  syntax ValSeq ::= triComplete(ValSeq, Int, Int) [function, total]
                  | triResult(Int) [function, total]
```

## 1094 verification.k:12 [syntax]
DISPOSITION: ACCEPT: syntax-only exact-AST macro declaration
```k
  syntax Expr ::= "triLoopCondition" [macro]
```

## 1095 verification.k:13 [rule:equational]
DISPOSITION: ACCEPT: parse-time exact-AST macro expansion
```k
  rule triLoopCondition
    => Compare(Name("i"), CmpOp("<=", Name("n")))
```

## 1096 verification.k:16 [syntax]
DISPOSITION: ACCEPT: syntax-only exact-AST macro declaration
```k
  syntax Stmts ::= "triLoopBody" [macro]
```

## 1097 verification.k:17 [rule:equational]
DISPOSITION: ACCEPT: parse-time exact-AST macro expansion
```k
  rule triLoopBody
    => If(Compare(Name("i"), CmpOp("==", Int(0))),
          Expr(Call(Attribute(Name("values"), "append"), Int(1))),
          If(Compare(Name("i"), CmpOp("==", Int(1))),
            Expr(Call(Attribute(Name("values"), "append"), Int(3))),
            If(Compare(BinOp("%", Name("i"), Int(2)),
                       CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("values"), "append"),
                        BinOp("+", Int(1),
                                   BinOp("//", Name("i"), Int(2))))),
              Expr(Call(Attribute(Name("values"), "append"),
                        BinOp("*",
                          BinOp("+", BinOp("//", Name("i"), Int(2)), Int(1)),
                          BinOp("+", BinOp("//", Name("i"), Int(2)), Int(3))))))))
       AugAssign(Name("i"), "+", Int(1))
```

## 1098 verification.k:33 [syntax]
DISPOSITION: ACCEPT: syntax-only exact-AST macro declaration
```k
  syntax Stmts ::= "triFunctionBody" [macro]
```

## 1099 verification.k:34 [rule:equational]
DISPOSITION: ACCEPT: parse-time exact-AST macro expansion
```k
  rule triFunctionBody
    => Assign(Name("values"), ListExpr(.Exprs))
       Assign(Name("i"), Int(0))
       While(triLoopCondition, triLoopBody)
       Return(Name("values"))
```

## 1100 verification.k:40 [syntax]
DISPOSITION: ACCEPT: syntax-only exact-AST macro declaration
```k
  syntax Stmts ::= "triDefinition" [macro]
```

## 1101 verification.k:41 [rule:equational]
DISPOSITION: ACCEPT: parse-time exact-AST macro expansion
```k
  rule triDefinition
    => FuncDef("tri", Params("n"), triFunctionBody)
```

## 1102 verification.k:43 [endmodule]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
endmodule
```

## 1103 verification.k:45 [module]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
module VERIFICATION
```

## 1104 verification.k:46 [imports]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  imports VERIFICATION-SYNTAX
```

## 1105 verification.k:47 [imports]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
  imports MPY
```

## 1106 verification.k:51 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triValue(I:Int) => 0
    requires I <Int 0
```

## 1107 verification.k:53 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triValue(I:Int)
    => ((I -Int pyMod(I, 2)) /Int 2 +Int 1)
       *Int ((I -Int pyMod(I, 2)) /Int 2 +Int 3)
    requires I >=Int 0 andBool pyMod(I, 2) ==Int 1
```

## 1108 verification.k:57 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triValue(I:Int)
    => 1 +Int (I -Int pyMod(I, 2)) /Int 2
    requires I >=Int 0 andBool pyMod(I, 2) ==Int 0
```

## 1109 verification.k:64 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triComplete(P:ValSeq, I:Int, N:Int) => P
    requires I >Int N
```

## 1110 verification.k:66 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triComplete(P:ValSeq, I:Int, N:Int)
    => triComplete(
         valSeqConcat(P, vCons(triValue(I), .ValSeq)),
         I +Int 1,
         N)
    requires I <=Int N
```

## 1111 verification.k:73 [rule:equational]
DISPOSITION: ACCEPT: proof-local total mathematical definition
```k
  rule triResult(N:Int) => triComplete(.ValSeq, 0, N)
```

## 1112 verification.k:74 [endmodule]
DISPOSITION: ACCEPT: verification module structure/declaration
```k
endmodule
```

## 1113 spec.k:1 [requires]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
requires "verification.k"
```

## 1114 spec.k:3 [module]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
module SPEC
```

## 1115 spec.k:4 [imports]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  imports VERIFICATION
```

## 1116 spec.k:8 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-loop]:
    <k> #while(triLoopCondition, triLoopBody) => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope("i" |-> (I:Int => N +Int 1)
                       "n" |-> N:Int
                       "values" |-> ref(H:Int),
                       parent(0))
      ...
    </scopes>
    <heap>
      ... H |-> (list(P:ValSeq) => list(triComplete(P, I, N))) ...
    </heap>
    requires N >=Int 0
     andBool I >=Int 0
     andBool I <=Int N +Int 1
```

## 1117 spec.k:27 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-entry]:
    <k> #loadAll(Module(triDefinition))
         ~> Call(Name("tri"), Int(N:Int))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
              "tri" |-> closureVal(
                ("n", .ParamNames),
                triFunctionBody,
                0),
              parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(triResult(N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
```

## 1118 spec.k:55 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-at-zero]:
    <k> triValue(0) => 1 </k>
```

## 1119 spec.k:58 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-at-one]:
    <k> triValue(1) => 3 </k>
```

## 1120 spec.k:61 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-at-even]:
    <k> triValue(N:Int) => 1 +Int N /Int 2 </k>
    requires N >=Int 2 andBool pyMod(N, 2) ==Int 0
```

## 1121 spec.k:65 [claim]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
  claim [tri-at-odd-recurrence]:
    <k> triValue(N:Int)
      => triValue(N -Int 1)
         +Int triValue(N -Int 2)
         +Int triValue(N +Int 1)
    </k>
    requires N >=Int 3 andBool pyMod(N, 2) ==Int 1
```

## 1122 spec.k:72 [endmodule]
DISPOSITION: TARGET: reachability target/lemma; adequacy addressed in REVIEW.md stage 4
```k
endmodule
```

