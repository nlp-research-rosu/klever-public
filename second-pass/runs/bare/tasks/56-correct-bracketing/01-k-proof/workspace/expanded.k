module SORT-K 
  syntax K [hook(K.K)]
endmodule

module BASIC-K 
  imports public ML-SYNTAX
  imports public SORT-BOOL
  syntax KItem [hook(K.KItem)]
  syntax K  ::=
    KItem 
  syntax KConfigVar [token]
  syntax KItem  ::=
    KConfigVar 
endmodule

module KSTRING 
  syntax KString  ::=
    r"[\\\"](([^\\\"\\n\\r\\\\])|([\\\\][nrtf\\\"\\\\])|([\\\\][x][0-9a-fA-F]{2})|([\\\\][u][0-9a-fA-F]{4})|([\\\\][U][0-9a-fA-F]{8}))*[\\\"]" [token]
endmodule

module BUILTIN-ID-TOKENS 
  syntax #LowerId  ::=
    r"[a-z][a-zA-Z0-9]*" [prec(2), token]
  syntax #UpperId  ::=
    r"[A-Z][a-zA-Z0-9]*" [prec(2), token]
endmodule

module SORT-KBOTT 
  imports public SORT-K
  syntax KBott 
endmodule

module KAST 
  imports public BASIC-K
  imports public SORT-KBOTT
  imports public KSTRING
  imports public BUILTIN-ID-TOKENS
  syntax KBott  ::=
    "#token" "(" KString "," KString ")" [symbol(#KToken)]
  | "#klabel" "(" KLabel ")" [symbol(#WrappedKLabel)]
  | KLabel "(" KList ")" [symbol(#KApply)]
  syntax KItem  ::=
    KBott 
  syntax KLabel  ::=
    r"`(\\\\`|\\\\\\\\|[^`\\\\\\n\\r])+`" [token]
  | #LowerId [token]
  | r"[#a-z][a-zA-Z0-9]*" [prec(1), token]
  syntax KList  ::=
    K 
  | ".KList" [symbol(#EmptyKList)]
  | KList "," KList [assoc, left, prefer, symbol(#KList), unit(#EmptyKList)]
endmodule

module KSEQ 
  imports public KAST
  imports public K-TOP-SORT
  syntax K  ::=
    ".K" [symbol(#EmptyK)]
  | "." [deprecated, symbol(#EmptyK), unparseAvoid]
  syntax K  ::=
    K "~>" K [assoc, left, symbol(#KSequence), unit(#EmptyK)]
  syntax left #KSequence 
  syntax {Sort} Sort  ::=
    "(" Sort ")" [applyPriority(1), bracket, group(defaultBracket)]
endmodule

module ML-SYNTAX [not-lr1]
  imports public SORT-K
  syntax {Sort} Sort  ::=
    "#Top" [group(mlUnary), symbol(#Top)]
  | "#Bottom" [group(mlUnary), symbol(#Bottom)]
  | "#Not" "(" Sort ")" [group(mlUnary, mlOp), mlOp, symbol(#Not)]
  syntax {Sort1, Sort2} Sort2  ::=
    "#Ceil" "(" Sort1 ")" [group(mlUnary, mlOp), mlOp, symbol(#Ceil)]
  | "#Floor" "(" Sort1 ")" [group(mlUnary, mlOp), mlOp, symbol(#Floor)]
  | "{" Sort1 "#Equals" Sort1 "}" [comm, format(%1%i%n%2%d%n%3%i%n%4%d%n%5), group(mlEquals, mlOp), mlOp, symbol(#Equals)]
  syntax priority mlUnary  > mlEquals  > mlAnd  
  syntax {Sort} Sort  ::=
    Sort "#And" Sort [assoc, comm, format(%i%1%d%n%2%n%i%3%d), group(mlAnd, mlOp), left, mlOp, symbol(#And), unit(#Top)]
  > Sort "#Or" Sort [assoc, comm, format(%i%1%d%n%2%n%i%3%d), group(mlOp), left, mlOp, symbol(#Or), unit(#Bottom)]
  > Sort "#Implies" Sort [format(%i%1%d%n%2%n%i%3%d), group(mlImplies, mlOp), mlOp, symbol(#Implies)]
  syntax priority mlImplies  > mlQuantifier  
  syntax {Sort1, Sort2} Sort2  ::=
    "#Exists" Sort1 "." Sort2 [group(mlQuantifier, mlOp), mlBinder, mlOp, symbol(#Exists)]
  | "#Forall" Sort1 "." Sort2 [group(mlQuantifier, mlOp), mlBinder, mlOp, symbol(#Forall)]
  syntax {Sort} Sort  ::=
    "#AG" "(" Sort ")" [group(mlOp), mlOp, symbol(#AG)]
  | "#wEF" "(" Sort ")" [group(mlOp), mlOp, symbol(weakExistsFinally)]
  | "#wAF" "(" Sort ")" [group(mlOp), mlOp, symbol(weakAlwaysFinally)]
endmodule

module KVARIABLE-SYNTAX 
  syntax #KVariable 
endmodule

module KSEQ-SYMBOLIC 
  imports public KSEQ
  imports public ML-SYNTAX
  imports public KVARIABLE-SYNTAX
  syntax #KVariable  ::=
    r"(\\!|\\?|@)?([A-Z][A-Za-z0-9'_]*|_|_[A-Z][A-Za-z0-9'_]*)" [prec(1), token]
  | #UpperId [token]
  syntax KConfigVar  ::=
    r"(\\$)([A-Z][A-Za-z0-9'_]*)" [token]
  syntax KBott  ::=
    #KVariable 
  syntax KBott  ::=
    KConfigVar 
endmodule

module KCELLS 
  imports public KAST
  syntax Cell 
  syntax Bag  ::=
    Bag Bag [assoc, left, symbol(#cells), unit(#cells)]
  | ".Bag" [symbol(#cells)]
  | ".::Bag" [symbol(#cells)]
  | Cell 
  syntax Bag  ::=
    "(" Bag ")" [bracket]
  syntax KItem  ::=
    Bag 
  syntax #RuleBody  ::=
    "[" "[" K "]" "]" Bag [avoid, symbol(#withConfig)]
  syntax non-assoc #withConfig 
  syntax Bag  ::=
    KBott 
endmodule

module RULE-CELLS 
  imports public KCELLS
  imports public RULE-LISTS
  syntax #OptionalDots  ::=
    "..." [symbol(#dots)]
  | "" [symbol(#noDots)]
  syntax Int 
  syntax GeneratedCounterCell  ::=
    "<generatedCounter>" Int "</generatedCounter>" [cell, internal, symbol(<generatedCounter>)]
endmodule

module CONFIG-CELLS 
  imports public KCELLS
  imports public RULE-LISTS
  syntax #CellName  ::=
    r"[a-zA-Z][a-zA-Z0-9\\-]*" [prec(1), token]
  | #LowerId [token]
  | #UpperId [token]
  syntax Cell  ::=
    "<" #CellName #CellProperties ">" K "</" #CellName ">" [symbol(#configCell)]
  syntax Cell  ::=
    "<" #CellName "/>" [symbol(#externalCell)]
  syntax #CellProperties  ::=
    #CellProperty #CellProperties [symbol(#cellPropertyList)]
  | "" [symbol(#cellPropertyListTerminator)]
  syntax #CellProperty  ::=
    #CellName "=" KString [symbol(#cellProperty)]
endmodule

module REQUIRES-ENSURES 
  imports public BASIC-K
  syntax #RuleBody  ::=
    K 
  syntax #RuleContent  ::=
    #RuleBody [symbol(#ruleNoConditions)]
  | #RuleBody "requires" Bool [symbol(#ruleRequires)]
  | #RuleBody "ensures" Bool [symbol(#ruleEnsures)]
  | #RuleBody "requires" Bool "ensures" Bool [symbol(#ruleRequiresEnsures)]
endmodule

module K-TOP-SORT 
  imports public SORT-KBOTT
  syntax KItem  ::=
    KBott 
  syntax {Sort} KItem  ::=
    Sort 
endmodule

module K-BOTTOM-SORT 
  imports public SORT-KBOTT
  syntax KItem  ::=
    KBott 
  syntax {Sort} Sort  ::=
    KBott 
endmodule

module K-SORT-LATTICE 
  imports public K-TOP-SORT
  imports public K-BOTTOM-SORT
endmodule

module AUTO-CASTS 
endmodule

module AUTO-FOLLOW 
endmodule

module PROGRAM-LISTS 
  imports public SORT-K
endmodule

module RULE-LISTS 
endmodule

module RECORD-PRODUCTIONS 
endmodule

module SORT-PREDICATES 
endmodule

module KREWRITE 
  syntax {Sort} Sort  ::=
    Sort "=>" Sort [symbol(#KRewrite)]
  syntax non-assoc #KRewrite 
  syntax priority #KRewrite  > #withConfig  
endmodule

module K 
  imports public KSEQ-SYMBOLIC
  imports public REQUIRES-ENSURES
  imports public RECORD-PRODUCTIONS
  imports public SORT-PREDICATES
  imports public K-SORT-LATTICE
  imports public AUTO-CASTS
  imports public AUTO-FOLLOW
  imports public KREWRITE
  syntax {Sort} Sort  ::=
    Sort "#as" Sort [symbol(#KAs)]
  syntax {Sort} Sort  ::=
    "#fun" "(" Sort ")" "(" Sort ")" [prefer, symbol(#fun2)]
  syntax {Sort1, Sort2} Sort1  ::=
    "#fun" "(" Sort2 "=>" Sort1 ")" "(" Sort2 ")" [symbol(#fun3)]
  syntax {Sort1, Sort2} Sort1  ::=
    "#let" Sort2 "=" Sort2 "#in" Sort1 [symbol(#let)]
  syntax Bool  ::=
    left: 
    K ":=K" K [function, group(equalEqualK), symbol(_:=K_), total]
  | K ":/=K" K [function, group(notEqualEqualK), symbol(_:/=K_), total]
endmodule

module K-TERM 
  imports public KSEQ-SYMBOLIC
  imports public RECORD-PRODUCTIONS
  imports public SORT-PREDICATES
  imports public K-SORT-LATTICE
  imports public AUTO-CASTS
  imports public AUTO-FOLLOW
  imports public KREWRITE
endmodule

module DEFAULT-LAYOUT 
  syntax #Layout  ::=
    r"(\\/\\*([^\\*]|(\\*+([^\\*\\/])))*\\*+\\/)" 
  | r"(\\/\\/[^\\n\\r]*)" 
  | r"([\\ \\n\\r\\t])" 
endmodule

module DEFAULT-CONFIGURATION 
  imports public BASIC-K
  configuration <k> $PGM:K </k> 
endmodule

module K-AMBIGUITIES 
  syntax {Sort} Sort  ::=
    "amb" "(" Sort "," Sort ")" [symbol(amb)]
endmodule

module K-LOCATIONS 
  imports public STRING-SYNTAX
  imports public INT-SYNTAX
  syntax {Sort} Sort  ::=
    "#location" "(" Sort "," String "," Int "," Int "," Int "," Int ")" [format(%3), symbol(#location)]
endmodule

module DOMAINS-SYNTAX 
  imports public SORT-K
  imports public ID-SYNTAX
  imports public UNSIGNED-INT-SYNTAX
  imports public BOOL-SYNTAX
  imports public STRING-SYNTAX
endmodule

module DOMAINS 
  imports public DOMAINS-SYNTAX
  imports public INT
  imports public BOOL
  imports public STRING
  imports public BASIC-K
  imports public LIST
  imports public K-IO
  imports public MAP
  imports public SET
  imports public ID
  imports public K-EQUAL
endmodule

module ARRAY-SYNTAX 
  imports private LIST
  syntax Array 
  syntax KItem  ::=
    Array "[" Int "]" [function]
  syntax Array  ::=
    Array "[" key: Int "<-" value: KItem "]" [function, symbol(_[_<-_])]
  syntax Array  ::=
    Array "[" Int "<-" "undef" "]" [function]
  syntax Array  ::=
    "updateArray" "(" Array "," index: Int "," List ")" [function]
  syntax Array  ::=
    "fillArray" "(" Array "," index: Int "," length: Int "," value: KItem ")" [function]
  syntax Bool  ::=
    Int "in_keys" "(" Array ")" [function, total]
endmodule

module ARRAY-IN-K [private]
  imports public ARRAY-SYNTAX
  imports private LIST
  imports private K-EQUAL
  imports private INT
  imports private BOOL
  syntax Array  ::=
    "makeArray" "(" length: Int "," value: KItem ")" [function, public]
  syntax Array  ::=
    "arr" "(" List "," Int "," KItem ")" 
  rule makeArray(I::Int, D::KItem) => arr(.List, I, D) 
  rule arr(L::List, _, _       ) [ IDX::Int ] => L[IDX] requires 0 <=Int IDX andBool IDX  <Int size(L) 
  rule arr(_      , _, D::KItem) [ _        ] => D       [owise]
  syntax List  ::=
    "ensureOffsetList" "(" List "," Int "," KItem ")" [function]
  rule ensureOffsetList(L::List, IDX::Int, D::KItem) => L makeList(IDX +Int 1 -Int size(L), D) requires         IDX >=Int size(L) 
  rule ensureOffsetList(L::List, IDX::Int, _::KItem) => L                                      requires notBool IDX >=Int size(L) 
  rule arr(L::List, I::Int, D::KItem) [ IDX::Int <- VAL::KItem ] => arr(ensureOffsetList(L, IDX, D) [ IDX <- VAL ], I, D) 
  rule arr(L::List, I::Int, D::KItem) [ IDX::Int <- undef ] => arr(L, I, D) [ IDX <- D ] 
  rule updateArray(arr(L::List, I::Int, D::KItem), IDX::Int, L2::List) => arr(updateList(ensureOffsetList(L, IDX +Int size(L2) -Int 1, D), IDX, L2), I, D) 
  rule fillArray(arr(L::List, I::Int, D::KItem), IDX::Int, LEN::Int, VAL::KItem) => arr(fillList(ensureOffsetList(L, IDX +Int LEN -Int 1, D), IDX, LEN, VAL), I, D) 
  rule IDX::Int in_keys(arr(_, I::Int, _)) => IDX >=Int 0 andBool IDX <Int I 
endmodule

module ARRAY-SYMBOLIC [symbolic]
  imports public ARRAY-IN-K
endmodule

module ARRAY-KORE 
  imports public ARRAY-IN-K
endmodule

module ARRAY 
  imports public ARRAY-SYMBOLIC
  imports public ARRAY-KORE
endmodule

module MAP 
  imports private BOOL-SYNTAX
  imports private INT-SYNTAX
  imports private LIST
  imports private SET
  syntax Map [hook(MAP.Map)]
  syntax Map  ::=
    Map Map [assoc, comm, element(_|->_), format(%1%n%2), function, hook(MAP.concat), index(0), left, symbol(_Map_), unit(.Map)]
  syntax Map  ::=
    ".Map" [function, hook(MAP.unit), symbol(.Map), total]
  syntax Map  ::=
    KItem "|->" KItem [function, hook(MAP.element), injective, symbol(_|->_), total]
  syntax priority _|->_  > _Map_ .Map  
  syntax non-assoc _|->_ 
  syntax KItem  ::=
    Map "[" KItem "]" [function, hook(MAP.lookup), symbol(Map:lookup)]
  syntax KItem  ::=
    Map "[" KItem "]" "orDefault" KItem [function, hook(MAP.lookupOrDefault), symbol(Map:lookupOrDefault), total]
  syntax Map  ::=
    Map "[" key: KItem "<-" value: KItem "]" [function, hook(MAP.update), prefer, symbol(Map:update), total]
  syntax Map  ::=
    Map "[" KItem "<-" "undef" "]" [function, hook(MAP.remove), symbol(_[_<-undef]), total]
  syntax Map  ::=
    Map "-Map" Map [function, hook(MAP.difference), total]
  syntax Map  ::=
    "updateMap" "(" Map "," Map ")" [function, hook(MAP.updateAll), total]
  syntax Map  ::=
    "removeAll" "(" Map "," Set ")" [function, hook(MAP.removeAll), total]
  syntax Set  ::=
    "keys" "(" Map ")" [function, hook(MAP.keys), total]
  syntax List  ::=
    "keys_list" "(" Map ")" [function, hook(MAP.keys_list)]
  syntax Bool  ::=
    KItem "in_keys" "(" Map ")" [function, hook(MAP.in_keys), total]
  syntax List  ::=
    "values" "(" Map ")" [function, hook(MAP.values)]
  syntax Int  ::=
    "size" "(" Map ")" [function, hook(MAP.size), symbol(sizeMap), total]
  syntax Bool  ::=
    Map "<=Map" Map [function, hook(MAP.inclusion), total]
  syntax KItem  ::=
    "choice" "(" Map ")" [function, hook(MAP.choice), symbol(Map:choice)]
endmodule

module MAP-KORE-SYMBOLIC [haskell, symbolic]
  imports public MAP
  imports private K-EQUAL
  imports private BOOL
  rule #Ceil(@M:Map [@K:KItem]) => {(@K in_keys(@M)) #Equals true} #And #Ceil(@M) #And #Ceil(@K)  [simplification]
  rule (K |-> _ M:Map) [ K <- V ] => (K |-> V M)  [simplification]
  rule M:Map [ K <- V ] => (K |-> V M) requires notBool (K in_keys(M))  [simplification]
  rule M:Map [ K <- _ ] [ K <- V ] => M [ K <- V ]  [simplification]
  rule (K1 |-> V1 M:Map) [ K2 <- V2 ] => (K1 |-> V1 (M [ K2 <- V2 ])) requires K1 =/=K K2  [simplification]
  rule (K |-> _ M:Map) [ K <- undef ] => M ensures notBool (K in_keys(M))  [simplification]
  rule M:Map [ K <- undef ] => M requires notBool (K in_keys(M))  [simplification]
  rule (K1 |-> V1 M:Map) [ K2 <- undef ] => (K1 |-> V1 (M [ K2 <- undef ])) requires K1 =/=K K2  [simplification]
  rule (K  |->  V M:Map) [ K ]  => V ensures notBool (K in_keys(M))  [simplification]
  rule (K1 |-> _V M:Map) [ K2 ] => M [K2] requires K1 =/=K K2 ensures notBool (K1 in_keys(M))  [simplification]
  rule (_MAP:Map [ K  <-  V1 ]) [ K ]  => V1  [simplification]
  rule ( MAP:Map [ K1 <- _V1 ]) [ K2 ] => MAP [ K2 ] requires K1 =/=K K2  [simplification]
  rule (K  |->  V M:Map) [  K ] orDefault _ => V ensures notBool (K in_keys(M))  [simplification]
  rule (K1 |-> _V M:Map) [ K2 ] orDefault D => M [K2] orDefault D requires K1 =/=K K2 ensures notBool (K1 in_keys(M))  [simplification]
  rule (_MAP:Map [ K  <-  V1 ]) [ K ] orDefault _ => V1  [simplification]
  rule ( MAP:Map [ K1 <- _V1 ]) [ K2 ] orDefault D => MAP [ K2 ] orDefault D requires K1 =/=K K2  [simplification]
  rule .Map [ _ ] orDefault D => D  [simplification]
  rule K in_keys(_M [ K <- undef ]) => false  [simplification]
  rule K in_keys(_M [ K <- _ ]) => true  [simplification]
  rule K1 in_keys(M [ K2 <- _ ]) => true requires K1 ==K K2 orBool K1 in_keys(M)  [simplification]
  rule K1 in_keys(M [ K2 <- _ ]) => K1 in_keys(M) requires K1 =/=K K2  [simplification]
  rule {false #Equals @Key in_keys(.Map)} => #Ceil(@Key)  [simplification]
  rule {@Key in_keys(.Map) #Equals false} => #Ceil(@Key)  [simplification]
  rule {false #Equals @Key in_keys(Key' |-> Val @M)} => #Ceil(@Key) #And #Ceil(Key' |-> Val @M) #And #Not({@Key #Equals Key'}) #And {false #Equals @Key in_keys(@M)}  [simplification]
  rule {@Key in_keys(Key' |-> Val @M) #Equals false} => #Ceil(@Key) #And #Ceil(Key' |-> Val @M) #And #Not({@Key #Equals Key'}) #And {@Key in_keys(@M) #Equals false}  [simplification]
endmodule

module MAP-SYMBOLIC 
  imports public MAP-KORE-SYMBOLIC
endmodule

module RANGEMAP 
  imports private BOOL-SYNTAX
  imports private INT-SYNTAX
  imports private LIST
  imports private SET
  syntax Range  ::=
    "[" KItem "," KItem ")" [symbol(RangeMap:Range)]
  syntax RangeMap [hook(RANGEMAP.RangeMap)]
  syntax RangeMap  ::=
    RangeMap RangeMap [assoc, comm, element(_r|->_), format(%1%n%2), function, hook(RANGEMAP.concat), index(0), left, symbol(_RangeMap_), unit(.RangeMap)]
  syntax RangeMap  ::=
    ".RangeMap" [function, hook(RANGEMAP.unit), symbol(.RangeMap), total]
  syntax RangeMap  ::=
    Range "r|->" KItem [function, hook(RANGEMAP.elementRng), injective, symbol(_r|->_)]
  syntax priority _r|->_  > _RangeMap_ .RangeMap  
  syntax non-assoc _r|->_ 
  syntax KItem  ::=
    RangeMap "[" KItem "]" [function, hook(RANGEMAP.lookup), symbol(RangeMap:lookup)]
  syntax KItem  ::=
    RangeMap "[" KItem "]" "orDefault" KItem [function, hook(RANGEMAP.lookupOrDefault), symbol(RangeMap:lookupOrDefault), total]
  syntax Range  ::=
    "find_range" "(" RangeMap "," KItem ")" [function, hook(RANGEMAP.find_range), symbol(RangeMap:find_range)]
  syntax RangeMap  ::=
    RangeMap "[" keyRange: Range "<-" value: KItem "]" [function, hook(RANGEMAP.updateRng), prefer, symbol(RangeMap:update)]
  syntax RangeMap  ::=
    RangeMap "[" Range "<-" "undef" "]" [function, hook(RANGEMAP.removeRng), symbol(_r[_<-undef])]
  syntax RangeMap  ::=
    RangeMap "-RangeMap" RangeMap [function, hook(RANGEMAP.difference), total]
  syntax RangeMap  ::=
    "updateRangeMap" "(" RangeMap "," RangeMap ")" [function, hook(RANGEMAP.updateAll), total]
  syntax RangeMap  ::=
    "removeAll" "(" RangeMap "," Set ")" [function, hook(RANGEMAP.removeAll)]
  syntax Set  ::=
    "keys" "(" RangeMap ")" [function, hook(RANGEMAP.keys), total]
  syntax List  ::=
    "keys_list" "(" RangeMap ")" [function, hook(RANGEMAP.keys_list)]
  syntax Bool  ::=
    KItem "in_keys" "(" RangeMap ")" [function, hook(RANGEMAP.in_keys), total]
  syntax List  ::=
    "values" "(" RangeMap ")" [function, hook(RANGEMAP.values)]
  syntax Int  ::=
    "size" "(" RangeMap ")" [function, hook(RANGEMAP.size), symbol(sizeRangeMap), total]
  syntax Bool  ::=
    RangeMap "<=RangeMap" RangeMap [function, hook(RANGEMAP.inclusion), total]
  syntax KItem  ::=
    "choice" "(" RangeMap ")" [function, hook(RANGEMAP.choice), symbol(RangeMap:choice)]
endmodule

module SET 
  imports private INT-SYNTAX
  imports private BASIC-K
  syntax Set [hook(SET.Set)]
  syntax Set  ::=
    Set Set [assoc, comm, element(SetItem), format(%1%n%2), function, hook(SET.concat), idem, left, symbol(_Set_), unit(.Set)]
  syntax Set  ::=
    ".Set" [function, hook(SET.unit), symbol(.Set), total]
  syntax Set  ::=
    "SetItem" "(" KItem ")" [function, hook(SET.element), injective, symbol(SetItem), total]
  syntax Set  ::=
    Set "|Set" Set [comm, function, hook(SET.union), left, total]
  rule S1:Set |Set S2:Set => S1 (S2 -Set S1)  [concrete]
  syntax Set  ::=
    "intersectSet" "(" Set "," Set ")" [comm, function, hook(SET.intersection), total]
  syntax Set  ::=
    Set "-Set" Set [function, hook(SET.difference), symbol(Set:difference), total]
  syntax Bool  ::=
    KItem "in" Set [function, hook(SET.in), symbol(Set:in), total]
  syntax Bool  ::=
    Set "<=Set" Set [function, hook(SET.inclusion), total]
  syntax Int  ::=
    "size" "(" Set ")" [function, hook(SET.size), total]
  syntax KItem  ::=
    "choice" "(" Set ")" [function, hook(SET.choice), symbol(Set:choice)]
endmodule

module SET-KORE-SYMBOLIC [haskell, symbolic]
  imports public SET
  imports private K-EQUAL
  imports private BOOL
  rule #Ceil(@S:Set SetItem(@E:KItem)) =>
         {(@E in @S) #Equals false} #And #Ceil(@S) #And #Ceil(@E)
     [simplification]
  rule S              -Set .Set           => S           [simplification]
  rule .Set           -Set  _             => .Set        [simplification]
  rule SetItem(X)     -Set (S SetItem(X)) => .Set
                               ensures notBool (X in S)  [simplification]
  rule S              -Set (S SetItem(X)) => .Set
                               ensures notBool (X in S)  [simplification]
  rule (S SetItem(X)) -Set S              => SetItem(X)
                               ensures notBool (X in S)  [simplification]
  rule (S SetItem(X)) -Set SetItem(X)     => S
                               ensures notBool (X in S)  [simplification]
  rule S    |Set .Set => S     [comm, simplification]
  rule S    |Set S    => S     [simplification]
  rule (S SetItem(X)) |Set SetItem(X) => S SetItem(X)
                             ensures notBool (X in S)  [comm, simplification]
  rule intersectSet(.Set, _   ) => .Set     [comm, simplification]
  rule intersectSet( S  , S   ) =>  S       [simplification]
  rule intersectSet( S SetItem(X), SetItem(X))     => SetItem(X)
                                                        ensures notBool (X in S)       [comm, simplification]
  rule intersectSet( S1 SetItem(X), S2 SetItem(X)) => intersectSet(S1, S2) SetItem(X)
                                                        ensures notBool (X in S1)
                                                        andBool notBool (X in S2)      [simplification]
  rule _E in .Set           => false    [simplification]
  rule E  in (S SetItem(E)) => true
              ensures notBool (E in S)  [simplification]
  rule X in ((SetItem(X) S) |Set  _            ) => true
                                    ensures notBool (X in S)  [simplification]
  rule X in ( _             |Set (SetItem(X) S)) => true
                                    ensures notBool (X in S)  [simplification]
endmodule

module SET-SYMBOLIC 
  imports public SET-KORE-SYMBOLIC
endmodule

module LIST 
  imports private INT-SYNTAX
  imports private MINT-SYNTAX
  imports private BASIC-K
  syntax List [hook(LIST.List)]
  syntax List  ::=
    List List [assoc, element(ListItem), format(%1%n%2), function, hook(LIST.concat), left, smtlib(smt_seq_concat), symbol(_List_), total, unit(.List), update(List:set)]
  syntax List  ::=
    ".List" [function, hook(LIST.unit), smtlib(smt_seq_nil), symbol(.List), total]
  syntax List  ::=
    "ListItem" "(" KItem ")" [function, hook(LIST.element), smtlib(smt_seq_elem), symbol(ListItem), total]
  syntax List  ::=
    "pushList" "(" KItem "," List ")" [function, hook(LIST.push), symbol(pushList), total]
  rule pushList(K::KItem, L1::List) => ListItem(K) L1 
  syntax KItem  ::=
    List "[" Int "]" [function, hook(LIST.get), symbol(List:get)]
  syntax {Width} KItem  ::=
    List "[" MInt{Width} "]" [function, hook(LIST.getMInt), symbol(List:getMInt)]
  syntax List  ::=
    List "[" index: Int "<-" value: KItem "]" [function, hook(LIST.update), symbol(List:set)]
  syntax {Width} List  ::=
    List "[" index: MInt{Width} "<-" value: KItem "]" [function, hook(LIST.updateMInt), symbol(List:setMInt)]
  syntax List  ::=
    "makeList" "(" length: Int "," value: KItem ")" [function, hook(LIST.make)]
  syntax List  ::=
    "updateList" "(" dest: List "," index: Int "," src: List ")" [function, hook(LIST.updateAll)]
  syntax List  ::=
    "fillList" "(" List "," index: Int "," length: Int "," value: KItem ")" [function, hook(LIST.fill)]
  syntax List  ::=
    "range" "(" List "," fromFront: Int "," fromBack: Int ")" [function, hook(LIST.range), symbol(List:range)]
  syntax Bool  ::=
    KItem "in" List [function, hook(LIST.in), symbol(_inList_), total]
  syntax Int  ::=
    "size" "(" List ")" [function, hook(LIST.size), smtlib(smt_seq_len), symbol(sizeList), total]
  syntax {Width} MInt{Width}  ::=
    "size" "(" List ")" [function, hook(LIST.sizeMInt), symbol(sizeMInt)]
endmodule

module COLLECTIONS 
  imports public LIST
  imports public SET
  imports public MAP
  syntax List  ::=
    "Set2List" "(" Set ")" [function, hook(SET.set2list), total]
  syntax Set  ::=
    "List2Set" "(" List ")" [function, hook(SET.list2set), total]
endmodule

module SORT-BOOL 
  syntax Bool [hook(BOOL.Bool)]
endmodule

module BOOL-SYNTAX 
  imports public SORT-BOOL
  syntax Bool  ::=
    "true" [token]
  syntax Bool  ::=
    "false" [token]
endmodule

module BOOL-COMMON 
  imports private BASIC-K
  imports public BOOL-SYNTAX
  syntax Bool  ::=
    "notBool" Bool [function, group(boolOperation), hook(BOOL.not), smt-hook(not), symbol(notBool_), total]
  > Bool "andBool" Bool [function, group(boolOperation), hook(BOOL.and), left, smt-hook(and), symbol(_andBool_), total]
  | Bool "andThenBool" Bool [function, group(boolOperation), hook(BOOL.andThen), left, smt-hook(and), symbol(_andThenBool_), total]
  | Bool "xorBool" Bool [function, group(boolOperation), hook(BOOL.xor), left, smt-hook(xor), symbol(_xorBool_), total]
  | Bool "orBool" Bool [function, group(boolOperation), hook(BOOL.or), left, smt-hook(or), symbol(_orBool_), total]
  | Bool "orElseBool" Bool [function, group(boolOperation), hook(BOOL.orElse), left, smt-hook(or), symbol(_orElseBool_), total]
  | Bool "impliesBool" Bool [function, group(boolOperation), hook(BOOL.implies), left, smt-hook(=>), symbol(_impliesBool_), total]
  > left: 
    Bool "==Bool" Bool [comm, function, hook(BOOL.eq), left, smt-hook(=), symbol(_==Bool_), total]
  | Bool "=/=Bool" Bool [comm, function, hook(BOOL.ne), left, smt-hook(distinct), symbol(_=/=Bool_), total]
  rule notBool true => false 
  rule notBool false => true 
  rule true andBool B:Bool => B:Bool 
  rule B:Bool andBool true => B:Bool  [simplification]
  rule false andBool _:Bool => false 
  rule _:Bool andBool false => false  [simplification]
  rule true andThenBool K::Bool => K 
  rule K::Bool andThenBool true => K  [simplification]
  rule false andThenBool _ => false 
  rule _ andThenBool false => false   [simplification]
  rule false xorBool B:Bool => B:Bool 
  rule B:Bool xorBool false => B:Bool  [simplification]
  rule B:Bool xorBool B:Bool => false 
  rule true orBool _:Bool => true 
  rule _:Bool orBool true => true  [simplification]
  rule false orBool B:Bool => B 
  rule B:Bool orBool false => B    [simplification]
  rule true orElseBool _ => true 
  rule _ orElseBool true => true      [simplification]
  rule false orElseBool K::Bool => K 
  rule K::Bool orElseBool false => K  [simplification]
  rule true impliesBool B:Bool => B 
  rule false impliesBool _:Bool => true 
  rule _:Bool impliesBool true => true        [simplification]
  rule B:Bool impliesBool false => notBool B  [simplification]
  rule B1:Bool =/=Bool B2:Bool => notBool (B1 ==Bool B2) 
endmodule

module BOOL-KORE [symbolic]
  imports public BOOL-COMMON
  rule {true #Equals notBool @B} => {false #Equals @B}  [simplification]
  rule {notBool @B #Equals true} => {@B #Equals false}  [simplification]
  rule {false #Equals notBool @B} => {true #Equals @B}  [simplification]
  rule {notBool @B #Equals false} => {@B #Equals true}  [simplification]
  rule {true #Equals @B1 andBool @B2} => {true #Equals @B1} #And {true #Equals @B2}  [simplification]
  rule {@B1 andBool @B2 #Equals true} => {@B1 #Equals true} #And {@B2 #Equals true}  [simplification]
  rule {false #Equals @B1 orBool @B2} => {false #Equals @B1} #And {false #Equals @B2}  [simplification]
  rule {@B1 orBool @B2 #Equals false} => {@B1 #Equals false} #And {@B2 #Equals false}  [simplification]
endmodule

module BOOL 
  imports public BOOL-COMMON
  imports public BOOL-KORE
endmodule

module UNSIGNED-INT-SYNTAX 
  syntax Int [hook(INT.Int)]
  syntax Int  ::=
    r"[0-9]+" [prec(2), prefer, token]
endmodule

module INT-SYNTAX 
  imports public UNSIGNED-INT-SYNTAX
  syntax Int  ::=
    r"[\\+\\-]?[0-9]+" [prec(2), prefer, token]
endmodule

module INT-COMMON 
  imports public INT-SYNTAX
  imports private BOOL
  syntax Int  ::=
    "~Int" Int [function, hook(INT.not), smtlib(notInt), symbol(~Int_), total]
  > left: 
    Int "^Int" Int [function, hook(INT.pow), left, smt-hook(^), symbol(_^Int_)]
  | Int "^%Int" Int Int [function, hook(INT.powmod), left, smt-hook((mod (^ #1 #2) #3)), symbol(_^%Int__)]
  > left: 
    Int "*Int" Int [comm, function, hook(INT.mul), left, smt-hook(*), symbol(_*Int_), total]
  | Int "/Int" Int [function, hook(INT.tdiv), left, smt-hook((ite (or (= 0 (mod #1 #2)) (>= #1 0)) (div #1 #2) (ite (> #2 0) (+ (div #1 #2) 1) (- (div #1 #2) 1)))), symbol(_/Int_)]
  | Int "%Int" Int [function, hook(INT.tmod), left, smt-hook((ite (or (= 0 (mod #1 #2)) (>= #1 0)) (mod #1 #2) (ite (> #2 0) (- (mod #1 #2) #2) (+ (mod #1 #2) #2)))), symbol(_%Int_)]
  | Int "divInt" Int [function, hook(INT.ediv), left, smt-hook(div), symbol(_divInt_)]
  | Int "modInt" Int [function, hook(INT.emod), left, smt-hook(mod), symbol(_modInt_)]
  > left: 
    Int "+Int" Int [comm, function, hook(INT.add), left, smt-hook(+), symbol(_+Int_), total]
  | Int "-Int" Int [function, hook(INT.sub), left, smt-hook(-), symbol(_-Int_), total]
  > left: 
    Int ">>Int" Int [function, hook(INT.shr), left, smtlib(shrInt), symbol(_>>Int_)]
  | Int "<<Int" Int [function, hook(INT.shl), left, smtlib(shlInt), symbol(_<<Int_)]
  > left: 
    Int "&Int" Int [comm, function, hook(INT.and), left, smtlib(andInt), symbol(_&Int_), total]
  > left: 
    Int "xorInt" Int [comm, function, hook(INT.xor), left, smtlib(xorInt), symbol(_xorInt_), total]
  > left: 
    Int "|Int" Int [comm, function, hook(INT.or), left, smtlib(orInt), symbol(_|Int_), total]
  syntax Int  ::=
    "minInt" "(" Int "," Int ")" [function, hook(INT.min), smt-hook((ite (< #1 #2) #1 #2)), total]
  | "maxInt" "(" Int "," Int ")" [function, hook(INT.max), smt-hook((ite (< #1 #2) #2 #1)), total]
  syntax Int  ::=
    "absInt" "(" Int ")" [function, hook(INT.abs), smt-hook((ite (< #1 0) (- 0 #1) #1)), total]
  syntax Int  ::=
    "log2Int" "(" Int ")" [function, hook(INT.log2)]
  syntax Int  ::=
    "bitRangeInt" "(" Int "," index: Int "," length: Int ")" [function, hook(INT.bitRange)]
  | "signExtendBitRangeInt" "(" Int "," index: Int "," length: Int ")" [function, hook(INT.signExtendBitRange)]
  syntax Bool  ::=
    Int "<=Int" Int [function, hook(INT.le), smt-hook(<=), symbol(_<=Int_), total]
  | Int "<Int" Int [function, hook(INT.lt), smt-hook(<), symbol(_<Int_), total]
  | Int ">=Int" Int [function, hook(INT.ge), smt-hook(>=), symbol(_>=Int_), total]
  | Int ">Int" Int [function, hook(INT.gt), smt-hook(>), symbol(_>Int_), total]
  | Int "==Int" Int [comm, function, hook(INT.eq), smt-hook(=), symbol(_==Int_), total]
  | Int "=/=Int" Int [comm, function, hook(INT.ne), smt-hook(distinct), symbol(_=/=Int_), total]
  syntax Bool  ::=
    Int "dividesInt" Int [function]
  syntax Int  ::=
    "randInt" "(" Int ")" [function, hook(INT.rand), impure]
  syntax K  ::=
    "srandInt" "(" Int ")" [function, hook(INT.srand), impure]
endmodule

module INT-SYMBOLIC [symbolic]
  imports public INT-COMMON
  imports public INT-SYMBOLIC-KORE
  imports private BOOL
  rule I +Int 0 => I  [simplification]
  rule I -Int 0 => I  [simplification]
  rule X modInt N => X requires 0 <=Int X andBool X <Int N  [simplification]
  rule X   %Int N => X requires 0 <=Int X andBool X <Int N  [simplification]
  rule X <<Int 0 => X                     [preserves-definedness, simplification]
  rule 0 <<Int Y => 0 requires 0 <=Int Y  [preserves-definedness, simplification]
  rule X >>Int 0 => X                     [preserves-definedness, simplification]
  rule 0 >>Int Y => 0 requires 0 <=Int Y  [preserves-definedness, simplification]
endmodule

module INT-SYMBOLIC-KORE [haskell, symbolic]
  imports public INT-COMMON
  imports public ML-SYNTAX
  imports private BOOL
  rule #Ceil(@I1:Int /Int   @I2:Int) => {(@I2 =/=Int 0) #Equals true} #And #Ceil(@I1) #And #Ceil(@I2)  [simplification]
  rule #Ceil(@I1:Int %Int   @I2:Int) => {(@I2 =/=Int 0) #Equals true} #And #Ceil(@I1) #And #Ceil(@I2)  [simplification]
  rule #Ceil(@I1:Int modInt @I2:Int) => {(@I2 =/=Int 0) #Equals true} #And #Ceil(@I1) #And #Ceil(@I2)  [simplification]
  rule #Ceil(@I1:Int >>Int  @I2:Int) => {(@I2 >=Int 0)  #Equals true} #And #Ceil(@I1) #And #Ceil(@I2)  [simplification]
  rule #Ceil(@I1:Int <<Int  @I2:Int) => {(@I2 >=Int 0)  #Equals true} #And #Ceil(@I1) #And #Ceil(@I2)  [simplification]
endmodule

module INT-KORE [symbolic]
  imports private K-EQUAL
  imports private BOOL
  imports public INT-COMMON
  rule [eq-k-to-eq-int]: I1:Int ==K I2:Int            => I1 ==Int I2            [simplification]
  rule [eq-int-true-left]: {K1 ==Int K2 #Equals true}   => {K1 #Equals K2}        [simplification]
  rule [eq-int-true-rigth]: {true #Equals K1 ==Int K2}   => {K1 #Equals K2}        [simplification]
  rule [eq-int-false-left]: {K1 ==Int K2 #Equals false}  => #Not({K1 #Equals K2})  [simplification]
  rule [eq-int-false-rigth]: {false #Equals K1 ==Int K2}  => #Not({K1 #Equals K2})  [simplification]
  rule [neq-int-true-left]: {K1 =/=Int K2 #Equals true}  => #Not({K1 #Equals K2})  [simplification]
  rule [neq-int-true-right]: {true #Equals K1 =/=Int K2}  => #Not({K1 #Equals K2})  [simplification]
  rule [neq-int-false-left]: {K1 =/=Int K2 #Equals false} => {K1 #Equals K2}        [simplification]
  rule [neq-int-false-right]: {false #Equals K1 =/=Int K2} => {K1 #Equals K2}        [simplification]
  rule I +Int B => B +Int I           [concrete(I), simplification(51), symbolic(B)]
  rule A -Int I => A +Int (0 -Int I)  [concrete(I), simplification(51), symbolic(A)]
  rule (A +Int I2) +Int I3 => A +Int (I2 +Int I3)  [concrete(I2, I3), simplification, symbolic(A)]
  rule I1 +Int (B +Int I3) => B +Int (I1 +Int I3)  [concrete(I1, I3), simplification, symbolic(B)]
  rule I1 -Int (B +Int I3) => (I1 -Int I3) -Int B  [concrete(I1, I3), simplification, symbolic(B)]
  rule I1 +Int (I2 +Int C) => (I1 +Int I2) +Int C  [concrete(I1, I2), simplification, symbolic(C)]
  rule I1 +Int (I2 -Int C) => (I1 +Int I2) -Int C  [concrete(I1, I2), simplification, symbolic(C)]
  rule (I1 -Int B) +Int I3 => (I1 +Int I3) -Int B  [concrete(I1, I3), simplification, symbolic(B)]
  rule I1 -Int (I2 +Int C) => (I1 -Int I2) -Int C  [concrete(I1, I2), simplification, symbolic(C)]
  rule I1 -Int (I2 -Int C) => (I1 -Int I2) +Int C  [concrete(I1, I2), simplification, symbolic(C)]
  rule (C -Int I2) -Int I3 => C -Int (I2 +Int I3)  [concrete(I2, I3), simplification, symbolic(C)]
  rule I1 &Int (I2 &Int C) => (I1 &Int I2) &Int C  [concrete(I1, I2), simplification, symbolic(C)]
endmodule

module INT 
  imports public INT-COMMON
  imports public INT-SYMBOLIC
  imports public INT-KORE
  imports private K-EQUAL
  imports private BOOL
  rule bitRangeInt(I::Int, IDX::Int, LEN::Int) => (I >>Int IDX) modInt (1 <<Int LEN) 
  rule signExtendBitRangeInt(I::Int, IDX::Int, LEN::Int) => (bitRangeInt(I, IDX, LEN) +Int (1 <<Int (LEN -Int 1))) modInt (1 <<Int LEN) -Int (1 <<Int (LEN -Int 1)) 
  rule I1:Int divInt I2:Int => (I1 -Int (I1 modInt I2)) /Int I2
  requires I2 =/=Int 0 
  rule I1:Int modInt I2:Int
  =>
    ((I1 %Int absInt(I2)) +Int absInt(I2)) %Int absInt(I2)
  requires I2 =/=Int 0     [concrete, simplification]
  rule minInt(I1:Int, I2:Int) => I1 requires I1 <Int  I2 
  rule minInt(I1:Int, I2:Int) => I2 requires I1 >=Int I2 
  rule I1:Int =/=Int I2:Int => notBool (I1 ==Int I2) 
  rule (I1:Int dividesInt I2:Int) => (I2 %Int I1) ==Int 0 
  syntax Int  ::=
    "freshInt" "(" Int ")" [freshGenerator, function, private, total]
  rule freshInt(I:Int) => I 
endmodule

module FLOAT-SYNTAX 
  syntax Float [hook(FLOAT.Float)]
  syntax Float  ::=
    r"([\\+\\-]?[0-9]+(\\.[0-9]*)?|\\.[0-9]+)([eE][\\+\\-]?[0-9]+)?([fFdD]|([pP][0-9]+[xX][0-9]+))?" [prec(1), token]
  syntax Float  ::=
    r"[\\+\\-]?Infinity([fFdD]|([pP][0-9]+[xX][0-9]+))?" [prec(3), token]
  syntax Float  ::=
    r"NaN([fFdD]|([pP][0-9]+[xX][0-9]+))?" [prec(3), token]
endmodule

module FLOAT 
  imports public FLOAT-SYNTAX
  imports private BOOL
  imports private INT-SYNTAX
  syntax Int  ::=
    "precisionFloat" "(" Float ")" [function, hook(FLOAT.precision), total]
  syntax Int  ::=
    "exponentBitsFloat" "(" Float ")" [function, hook(FLOAT.exponentBits), total]
  syntax Int  ::=
    "exponentFloat" "(" Float ")" [function, hook(FLOAT.exponent), total]
  syntax Bool  ::=
    "signFloat" "(" Float ")" [function, hook(FLOAT.sign), total]
  syntax Bool  ::=
    "isNaN" "(" Float ")" [function, hook(FLOAT.isNaN), smt-hook(fp.isNaN), total]
  | "isInfinite" "(" Float ")" [function, total]
  syntax Float  ::=
    "--Float" Float [function, hook(FLOAT.neg), smt-hook(fp.neg), total]
  > Float "^Float" Float [function, hook(FLOAT.pow), left]
  > left: 
    Float "*Float" Float [function, hook(FLOAT.mul), left, smt-hook((fp.mul roundNearestTiesToEven #1 #2))]
  | Float "/Float" Float [function, hook(FLOAT.div), left, smt-hook((fp.div roundNearestTiesToEven #1 #2))]
  | Float "%Float" Float [function, hook(FLOAT.rem), left, smt-hook((fp.rem roundNearestTiesToEven #1 #2))]
  > left: 
    Float "+Float" Float [function, hook(FLOAT.add), left, smt-hook((fp.add roundNearestTiesToEven #1 #2))]
  | Float "-Float" Float [function, hook(FLOAT.sub), left, smt-hook((fp.sub roundNearestTiesToEven #1 #2))]
  syntax Float  ::=
    "rootFloat" "(" Float "," Int ")" [function, hook(FLOAT.root)]
  | "absFloat" "(" Float ")" [function, hook(FLOAT.abs), smt-hook(fp.abs), total]
  | "roundFloat" "(" Float "," precision: Int "," exponentBits: Int ")" [function, hook(FLOAT.round)]
  | "floorFloat" "(" Float ")" [function, hook(FLOAT.floor), total]
  | "ceilFloat" "(" Float ")" [function, hook(FLOAT.ceil), total]
  | "truncFloat" "(" Float ")" [function, hook(FLOAT.trunc), total]
  | "expFloat" "(" Float ")" [function, hook(FLOAT.exp), total]
  | "logFloat" "(" Float ")" [function, hook(FLOAT.log)]
  | "sinFloat" "(" Float ")" [function, hook(FLOAT.sin), total]
  | "cosFloat" "(" Float ")" [function, hook(FLOAT.cos), total]
  | "tanFloat" "(" Float ")" [function, hook(FLOAT.tan)]
  | "asinFloat" "(" Float ")" [function, hook(FLOAT.asin)]
  | "acosFloat" "(" Float ")" [function, hook(FLOAT.acos)]
  | "atanFloat" "(" Float ")" [function, hook(FLOAT.atan), total]
  | "atan2Float" "(" Float "," Float ")" [function, hook(FLOAT.atan2)]
  | "maxFloat" "(" Float "," Float ")" [function, hook(FLOAT.max), smt-hook(fp.max)]
  | "minFloat" "(" Float "," Float ")" [function, hook(FLOAT.min), smt-hook(fp.min)]
  | "sqrtFloat" "(" Float ")" [function]
  | "maxValueFloat" "(" precision: Int "," exponentBits: Int ")" [function, hook(FLOAT.maxValue)]
  | "minValueFloat" "(" precision: Int "," exponentBits: Int ")" [function, hook(FLOAT.minValue)]
  syntax Bool  ::=
    Float "<=Float" Float [function, hook(FLOAT.le), smt-hook(fp.leq)]
  | Float "<Float" Float [function, hook(FLOAT.lt), smt-hook(fp.lt)]
  | Float ">=Float" Float [function, hook(FLOAT.ge), smt-hook(fp.geq)]
  | Float ">Float" Float [function, hook(FLOAT.gt), smt-hook(fg.gt)]
  | Float "==Float" Float [comm, function, hook(FLOAT.eq), smt-hook(fp.eq), symbol(_==Float_)]
  | Float "=/=Float" Float [comm, function, smt-hook((not (fp.eq #1 #2)))]
  rule F1:Float =/=Float F2:Float => notBool (F1 ==Float F2) 
  syntax Float  ::=
    "Int2Float" "(" Int "," precision: Int "," exponentBits: Int ")" [function, hook(FLOAT.int2float)]
  syntax Int  ::=
    "Float2Int" "(" Float ")" [function, hook(FLOAT.float2int), total]
  rule sqrtFloat(F:Float) => rootFloat(F, 2) 
  rule isInfinite(F:Float) => F >Float maxValueFloat(precisionFloat(F), exponentBitsFloat(F)) orBool F <Float --Float maxValueFloat(precisionFloat(F), exponentBitsFloat(F)) 
endmodule

module STRING-SYNTAX 
  syntax String [hook(STRING.String)]
  syntax String  ::=
    r"[\\\"](([^\\\"\\n\\r\\\\])|([\\\\][nrtf\\\"\\\\])|([\\\\][x][0-9a-fA-F]{2})|([\\\\][u][0-9a-fA-F]{4})|([\\\\][U][0-9a-fA-F]{8}))*[\\\"]" [token]
endmodule

module STRING-COMMON 
  imports public STRING-SYNTAX
  imports private INT
  imports private FLOAT-SYNTAX
  imports private K-EQUAL
  imports private BOOL
  syntax String  ::=
    String "+String" String [function, hook(STRING.concat), left, total]
  syntax Int  ::=
    "lengthString" "(" String ")" [function, hook(STRING.length), total]
  syntax String  ::=
    "chrChar" "(" Int ")" [function, hook(STRING.chr)]
  syntax Int  ::=
    "ordChar" "(" String ")" [function, hook(STRING.ord)]
  syntax String  ::=
    "substrString" "(" String "," startIndex: Int "," endIndex: Int ")" [function, hook(STRING.substr), total]
  syntax Int  ::=
    "findString" "(" haystack: String "," needle: String "," index: Int ")" [function, hook(STRING.find)]
  syntax Int  ::=
    "rfindString" "(" haystack: String "," needle: String "," index: Int ")" [function, hook(STRING.rfind)]
  syntax Int  ::=
    "findChar" "(" haystack: String "," needles: String "," index: Int ")" [function, hook(STRING.findChar)]
  syntax Int  ::=
    "rfindChar" "(" haystack: String "," needles: String "," index: Int ")" [function, hook(STRING.rfindChar)]
  syntax String  ::=
    "Bool2String" "(" Bool ")" [function, total]
  rule Bool2String(true)  => "true" 
  rule Bool2String(false) => "false" 
  syntax Bool  ::=
    "String2Bool" "(" String ")" [function]
  rule String2Bool("true")  => true 
  rule String2Bool("false") => false 
  syntax String  ::=
    "Float2String" "(" Float ")" [function, hook(STRING.float2string), total]
  syntax String  ::=
    "Float2String" "(" Float "," format: String ")" [function, hook(STRING.floatFormat), symbol(FloatFormat)]
  syntax Float  ::=
    "String2Float" "(" String ")" [function, hook(STRING.string2float)]
  syntax Int  ::=
    "String2Int" "(" String ")" [function, hook(STRING.string2int)]
  syntax String  ::=
    "Int2String" "(" Int ")" [function, hook(STRING.int2string), total]
  syntax String  ::=
    "Base2String" "(" Int "," base: Int ")" [function, hook(STRING.base2string)]
  syntax Int  ::=
    "String2Base" "(" String "," base: Int ")" [function, hook(STRING.string2base)]
  syntax String  ::=
    "replaceAll" "(" haystack: String "," needle: String "," replacement: String ")" [function, hook(STRING.replaceAll), total]
  syntax String  ::=
    "replace" "(" haystack: String "," needle: String "," replacement: String "," times: Int ")" [function, hook(STRING.replace)]
  syntax String  ::=
    "replaceFirst" "(" haystack: String "," needle: String "," replacement: String ")" [function, hook(STRING.replaceFirst), total]
  syntax Int  ::=
    "countAllOccurrences" "(" haystack: String "," needle: String ")" [function, hook(STRING.countAllOccurrences), total]
  syntax Bool  ::=
    String "==String" String [comm, function, hook(STRING.eq), total]
  | String "=/=String" String [comm, function, hook(STRING.ne), total]
  rule S1:String =/=String S2:String => notBool (S1 ==String S2) 
  syntax Bool  ::=
    String "<String" String [function, hook(STRING.lt), total]
  | String "<=String" String [function, hook(STRING.le), total]
  | String ">String" String [function, hook(STRING.gt), total]
  | String ">=String" String [function, hook(STRING.ge), total]
  syntax String  ::=
    "categoryChar" "(" String ")" [function, hook(STRING.category)]
  | "directionalityChar" "(" String ")" [function, hook(STRING.directionality)]
  syntax String  ::=
    "newUUID" [function, hook(STRING.uuid), impure]
  rule S1:String <=String S2:String => notBool (S2 <String S1) 
  rule S1:String >String S2:String => S2 <String S1 
  rule S1:String >=String S2:String => notBool (S1 <String S2) 
  rule findChar(S1:String, S2:String, I:Int) => #if findString(S1, substrString(S2, 0, 1), I) ==Int -1 #then findChar(S1, substrString(S2, 1, lengthString(S2)), I) #else #if findChar(S1, substrString(S2, 1, lengthString(S2)), I) ==Int -1 #then findString(S1, substrString(S2, 0, 1), I) #else minInt(findString(S1, substrString(S2, 0, 1), I), findChar(S1, substrString(S2, 1, lengthString(S2)), I)) #fi #fi requires S2 =/=String "" 
  rule findChar(_, "", _) => -1 
  rule rfindChar(S1:String, S2:String, I:Int) => maxInt(rfindString(S1, substrString(S2, 0, 1), I), rfindChar(S1, substrString(S2, 1, lengthString(S2)), I)) requires S2 =/=String "" 
  rule rfindChar(_, "", _) => -1 
  rule countAllOccurrences(Source:String, ToCount:String) => 0
            requires findString(Source, ToCount, 0) <Int 0 
  rule countAllOccurrences(Source:String, ToCount:String) => 1 +Int countAllOccurrences(substrString(Source, findString(Source, ToCount, 0) +Int lengthString(ToCount), lengthString(Source)), ToCount)
            requires findString(Source, ToCount, 0) >=Int 0 
  rule replaceFirst(Source:String, ToReplace:String, Replacement:String) => substrString(Source, 0, findString(Source, ToReplace, 0))
                +String Replacement +String substrString(Source, findString(Source, ToReplace, 0) +Int lengthString(ToReplace), lengthString(Source))
                requires findString(Source, ToReplace, 0) >=Int 0 
  rule replaceFirst(Source:String, ToReplace:String, _:String) => Source
        requires findString(Source, ToReplace, 0) <Int 0 
  rule replace(Source:String, ToReplace:String, Replacement:String, Count:Int) =>
       substrString(Source, 0, findString(Source, ToReplace, 0)) +String Replacement +String
       replace(substrString(Source, findString(Source, ToReplace, 0) +Int lengthString(ToReplace), lengthString(Source)), ToReplace, Replacement, Count -Int 1)
        requires Count >Int 0 andBool findString(Source, ToReplace, 0) >=Int 0 
  rule replace(Source:String, _, _, Count) => Source
        requires Count >=Int 0  [owise]
  rule replaceAll(Source:String, ToReplace:String, Replacement:String) => replace(Source, ToReplace, Replacement, countAllOccurrences(Source, ToReplace)) 
endmodule

module STRING-KORE [symbolic]
  imports private K-EQUAL
  imports public STRING-COMMON
  rule S1:String ==K S2:String => S1 ==String S2  [simplification]
endmodule

module STRING 
  imports public STRING-COMMON
  imports public STRING-KORE
endmodule

module STRING-BUFFER-IN-K [symbolic]
  imports private BASIC-K
  imports public STRING
  syntax StringBuffer  ::=
    ".StringBuffer" [function, total]
  syntax StringBuffer  ::=
    StringBuffer "+String" String [avoid, function, total]
  syntax StringBuffer  ::=
    String 
  syntax String  ::=
    "StringBuffer2String" "(" StringBuffer ")" [function, total]
  rule {SB:String +String S:String}::StringBuffer => (SB +String S)::String 
  rule .StringBuffer => "" 
  rule StringBuffer2String(S:String) => S 
endmodule

module STRING-BUFFER-HOOKED [concrete]
  imports private BASIC-K
  imports public STRING
  syntax StringBuffer [hook(BUFFER.StringBuffer)]
  syntax StringBuffer  ::=
    ".StringBuffer" [function, hook(BUFFER.empty), impure, total]
  syntax StringBuffer  ::=
    StringBuffer "+String" String [avoid, function, hook(BUFFER.concat), total]
  syntax String  ::=
    "StringBuffer2String" "(" StringBuffer ")" [function, hook(BUFFER.toString), total]
endmodule

module STRING-BUFFER 
  imports public STRING-BUFFER-HOOKED
  imports public STRING-BUFFER-IN-K
endmodule

module BYTES-SYNTAX 
  imports private STRING-SYNTAX
  syntax Bytes [hook(BYTES.Bytes)]
  syntax Bytes  ::=
    r"b[\\\"](([ !#-\\[\\]-~])|([\\\\][tnfr\\\"\\\\])|([\\\\][x][0-9a-fA-F]{2}))*[\\\"]" [token]
endmodule

module BYTES-STRING-ENCODE [symbolic]
  imports public BYTES-SYNTAX
  syntax String  ::=
    "decodeBytes" "(" encoding: String "," contents: Bytes ")" [function, hook(BYTES.decodeBytes)]
  syntax Bytes  ::=
    "encodeBytes" "(" encoding: String "," contents: String ")" [function, hook(BYTES.encodeBytes)]
endmodule

module BYTES-HOOKED 
  imports public STRING-SYNTAX
  imports public BYTES-SYNTAX
  imports public MINT-SYNTAX
  imports public BYTES-STRING-ENCODE
  syntax Bytes  ::=
    ".Bytes" [function, hook(BYTES.empty), total]
  syntax Endianness  ::=
    "LE" [symbol(littleEndianBytes)]
  | "BE" [symbol(bigEndianBytes)]
  syntax Signedness  ::=
    "Signed" [symbol(signedBytes)]
  | "Unsigned" [symbol(unsignedBytes)]
  syntax Int  ::=
    "Bytes2Int" "(" Bytes "," Endianness "," Signedness ")" [function, hook(BYTES.bytes2int), total]
  syntax Bytes  ::=
    "Int2Bytes" "(" length: Int "," Int "," Endianness ")" [function, hook(BYTES.int2bytes), total]
  | "Int2Bytes" "(" Int "," Endianness "," Signedness ")" [function, symbol(Int2BytesNoLen), total]
  syntax String  ::=
    "Bytes2String" "(" Bytes ")" [function, hook(BYTES.bytes2string), total]
  | "Bytes2Hex" "(" Bytes ")" [function, hook(BYTES.bytes2hex), total]
  syntax Bytes  ::=
    "String2Bytes" "(" String ")" [function, hook(BYTES.string2bytes), total]
  syntax Bytes  ::=
    Bytes "[" index: Int "<-" value: Int "]" [function, hook(BYTES.update)]
  syntax {Width} Bytes  ::=
    Bytes "[" index: MInt{Width} "<-" value: MInt{Width} "]" [function, hook(BYTES.updateMInt)]
  syntax Int  ::=
    Bytes "[" Int "]" [function, hook(BYTES.get)]
  syntax {Width} MInt{Width}  ::=
    Bytes "[" MInt{Width} "]" [function, hook(BYTES.getMInt)]
  syntax Bytes  ::=
    "substrBytes" "(" Bytes "," startIndex: Int "," endIndex: Int ")" [function, hook(BYTES.substr)]
  syntax {Width} Bytes  ::=
    "substrBytes" "(" Bytes "," startIndex: MInt{Width} "," endIndex: MInt{Width} ")" [function, hook(BYTES.substrMInt)]
  syntax Bytes  ::=
    "replaceAtBytes" "(" dest: Bytes "," index: Int "," src: Bytes ")" [function, hook(BYTES.replaceAt)]
  syntax {Width} Bytes  ::=
    "replaceAtBytes" "(" dest: Bytes "," index: MInt{Width} "," src: Bytes ")" [function, hook(BYTES.replaceAtMInt)]
  syntax Bytes  ::=
    "memsetBytes" "(" dest: Bytes "," index: Int "," count: Int "," v: Int ")" [function, hook(BYTES.memset)]
  syntax Bytes  ::=
    "padRightBytes" "(" Bytes "," length: Int "," value: Int ")" [function, hook(BYTES.padRight)]
  | "padLeftBytes" "(" Bytes "," length: Int "," value: Int ")" [function, hook(BYTES.padLeft)]
  syntax {Width} Bytes  ::=
    "padRightBytes" "(" Bytes "," length: MInt{Width} "," value: MInt{Width} ")" [function, hook(BYTES.padRightMInt)]
  | "padLeftBytes" "(" Bytes "," length: MInt{Width} "," value: MInt{Width} ")" [function, hook(BYTES.padLeftMInt)]
  syntax Bytes  ::=
    "reverseBytes" "(" Bytes ")" [function, hook(BYTES.reverse), total]
  syntax Int  ::=
    "lengthBytes" "(" Bytes ")" [function, hook(BYTES.length), smtlib(lengthBytes), total]
  syntax {Width} MInt{Width}  ::=
    "lengthBytes" "(" Bytes ")" [function, hook(BYTES.lengthMInt), total]
  syntax Bytes  ::=
    Bytes "+Bytes" Bytes [function, hook(BYTES.concat), right, total]
endmodule

module BYTES-CONCRETE [concrete]
  imports public BYTES-HOOKED
endmodule

module BYTES-KORE 
  imports public BYTES-HOOKED
  imports public BYTES-SYMBOLIC-CEIL
endmodule

module BYTES-SYMBOLIC-CEIL [symbolic]
  imports public BYTES-HOOKED
  imports private INT
  imports private BOOL
  rule #Ceil(padRightBytes(_, LEN, VAL)) => {(0 <=Int LEN andBool 0 <=Int VAL andBool VAL <Int 256) #Equals true}  [simplification]
  rule #Ceil(padLeftBytes(_, LEN, VAL))  => {(0 <=Int LEN andBool 0 <=Int VAL andBool VAL <Int 256) #Equals true}  [simplification]
endmodule

module BYTES 
  imports public BYTES-CONCRETE
  imports public BYTES-KORE
  imports private INT
  rule Int2Bytes(I::Int, _::Endianness, _)        => .Bytes
    requires I ==Int 0 
  rule Int2Bytes(I::Int, E::Endianness, Unsigned) => Int2Bytes((log2Int(I) +Int 8) /Int 8, I, E)
    requires I >Int 0  [preserves-definedness]
  rule Int2Bytes(I::Int, E::Endianness, Signed  ) => Int2Bytes((log2Int(I) +Int 9) /Int 8, I, E)
    requires I >Int 0  [preserves-definedness]
  rule Int2Bytes(I::Int, E::Endianness, Signed  ) => Int2Bytes((log2Int(~Int I) +Int 9) /Int 8, I, E)
    requires I <Int -1  [preserves-definedness]
  rule Int2Bytes(I::Int, E::Endianness, Signed  ) => Int2Bytes(1, -1, E)
    requires I ==Int -1  [preserves-definedness]
endmodule

module ID-SYNTAX-PROGRAM-PARSING 
  imports public BUILTIN-ID-TOKENS
  syntax Id  ::=
    r"[A-Za-z\\_][A-Za-z0-9\\_]*" [prec(1), token]
  | #LowerId [token]
  | #UpperId [token]
endmodule

module ID-SYNTAX 
  syntax Id [token]
endmodule

module ID-COMMON 
  imports public ID-SYNTAX
  imports private STRING
  syntax String  ::=
    "Id2String" "(" Id ")" [function, hook(STRING.token2string), total]
  syntax Id  ::=
    "String2Id" "(" String ")" [function, hook(STRING.string2token), total]
  syntax Id  ::=
    "freshId" "(" Int ")" [freshGenerator, function, private, total]
  rule freshId(I:Int) => String2Id("_" +String Int2String(I)) 
endmodule

module ID 
  imports public ID-COMMON
endmodule

module K-EQUAL-SYNTAX 
  imports private BOOL
  imports private BASIC-K
  syntax Bool  ::=
    left: 
    K "==K" K [comm, function, group(equalEqualK), hook(KEQUAL.eq), smt-hook(=), symbol(_==K_), total]
  | K "=/=K" K [comm, function, group(notEqualEqualK), hook(KEQUAL.ne), smt-hook(distinct), symbol(_=/=K_), total]
  syntax priority equalEqualK notEqualEqualK  > boolOperation mlOp  
  syntax {Sort} Sort  ::=
    "#if" Bool "#then" Sort "#else" Sort "#fi" [function, hook(KEQUAL.ite), smt-hook(ite), symbol(ite), total]
endmodule

module K-EQUAL-KORE [symbolic]
  imports private BOOL
  imports public K-EQUAL-SYNTAX
  rule K1:Bool ==K K2:Bool => K1 ==Bool K2  [simplification]
  rule {K1 ==K K2 #Equals true} => {K1 #Equals K2}  [simplification]
  rule {true #Equals K1 ==K K2} => {K1 #Equals K2}  [simplification]
  rule {K1 ==K K2 #Equals false} => #Not({K1 #Equals K2})  [simplification]
  rule {false #Equals K1 ==K K2} => #Not({K1 #Equals K2})  [simplification]
  rule {K1 =/=K K2 #Equals true} => #Not({K1 #Equals K2})  [simplification]
  rule {true #Equals K1 =/=K K2} => #Not({K1 #Equals K2})  [simplification]
  rule {K1 =/=K K2 #Equals false} => {K1 #Equals K2}  [simplification]
  rule {false #Equals K1 =/=K K2} => {K1 #Equals K2}  [simplification]
endmodule

module K-EQUAL 
  imports private BOOL
  imports public K-EQUAL-SYNTAX
  imports public K-EQUAL-KORE
  rule K1:K =/=K K2:K => notBool (K1 ==K K2) 
  rule #if C:Bool #then B1::K #else _ #fi => B1 requires C 
  rule #if C:Bool #then _ #else B2::K #fi => B2 requires notBool C 
endmodule

module K-REFLECTION 
  imports public BASIC-K
  imports public STRING
  syntax K  ::=
    "#configuration" [function, hook(KREFLECTION.configuration), impure]
  syntax String  ::=
    "#sort" "(" K ")" [function, hook(KREFLECTION.sort)]
  syntax KItem  ::=
    "#fresh" "(" String ")" [function, hook(KREFLECTION.fresh), impure]
  syntax KItem  ::=
    "getsymbol" "(" K ")" [function, hook(KREFLECTION.getKLabel)]
  syntax K  ::=
    "#getenv" "(" String ")" [function, hook(KREFLECTION.getenv), impure]
  syntax String  ::=
    "#kompiledDirectory" "(" ")" [function, hook(KREFLECTION.kompiledDir)]
  syntax List  ::=
    "#argv" "(" ")" [function, hook(KREFLECTION.argv)]
  syntax {Sort} String  ::=
    "#unparseKORE" "(" Sort ")" [function, hook(KREFLECTION.printKORE)]
  syntax IOError  ::=
    "#noParse" "(" String ")" [symbol(#noParse)]
endmodule

module K-IO 
  imports private LIST
  imports private STRING
  imports private INT
  syntax IOError  ::=
    "#EOF" [symbol(#EOF)]
  | "#unknownIOError" "(" errno: Int ")" [symbol(#unknownIOError)]
  | "#E2BIG" [symbol(#E2BIG)]
  | "#EACCES" [symbol(#EACCES)]
  | "#EAGAIN" [symbol(#EAGAIN)]
  | "#EBADF" [symbol(#EBADF)]
  | "#EBUSY" [symbol(#EBUSY)]
  | "#ECHILD" [symbol(#ECHILD)]
  | "#EDEADLK" [symbol(#EDEADLK)]
  | "#EDOM" [symbol(#EDOM)]
  | "#EEXIST" [symbol(#EEXIST)]
  | "#EFAULT" [symbol(#EFAULT)]
  | "#EFBIG" [symbol(#EFBIG)]
  | "#EINTR" [symbol(#EINTR)]
  | "#EINVAL" [symbol(#EINVAL)]
  | "#EIO" [symbol(#EIO)]
  | "#EISDIR" [symbol(#EISDIR)]
  | "#EMFILE" [symbol(#EMFILE)]
  | "#EMLINK" [symbol(#EMLINK)]
  | "#ENAMETOOLONG" [symbol(#ENAMETOOLONG)]
  | "#ENFILE" [symbol(#ENFILE)]
  | "#ENODEV" [symbol(#ENODEV)]
  | "#ENOENT" [symbol(#ENOENT)]
  | "#ENOEXEC" [symbol(#ENOEXEC)]
  | "#ENOLCK" [symbol(#ENOLCK)]
  | "#ENOMEM" [symbol(#ENOMEM)]
  | "#ENOSPC" [symbol(#ENOSPC)]
  | "#ENOSYS" [symbol(#ENOSYS)]
  | "#ENOTDIR" [symbol(#ENOTDIR)]
  | "#ENOTEMPTY" [symbol(#ENOTEMPTY)]
  | "#ENOTTY" [symbol(#ENOTTY)]
  | "#ENXIO" [symbol(#ENXIO)]
  | "#EPERM" [symbol(#EPERM)]
  | "#EPIPE" [symbol(#EPIPE)]
  | "#ERANGE" [symbol(#ERANGE)]
  | "#EROFS" [symbol(#EROFS)]
  | "#ESPIPE" [symbol(#ESPIPE)]
  | "#ESRCH" [symbol(#ESRCH)]
  | "#EXDEV" [symbol(#EXDEV)]
  | "#EWOULDBLOCK" [symbol(#EWOULDBLOCK)]
  | "#EINPROGRESS" [symbol(#EINPROGRESS)]
  | "#EALREADY" [symbol(#EALREADY)]
  | "#ENOTSOCK" [symbol(#ENOTSOCK)]
  | "#EDESTADDRREQ" [symbol(#EDESTADDRREQ)]
  | "#EMSGSIZE" [symbol(#EMSGSIZE)]
  | "#EPROTOTYPE" [symbol(#EPROTOTYPE)]
  | "#ENOPROTOOPT" [symbol(#ENOPROTOOPT)]
  | "#EPROTONOSUPPORT" [symbol(#EPROTONOSUPPORT)]
  | "#ESOCKTNOSUPPORT" [symbol(#ESOCKTNOSUPPORT)]
  | "#EOPNOTSUPP" [symbol(#EOPNOTSUPP)]
  | "#EPFNOSUPPORT" [symbol(#EPFNOSUPPORT)]
  | "#EAFNOSUPPORT" [symbol(#EAFNOSUPPORT)]
  | "#EADDRINUSE" [symbol(#EADDRINUSE)]
  | "#EADDRNOTAVAIL" [symbol(#EADDRNOTAVAIL)]
  | "#ENETDOWN" [symbol(#ENETDOWN)]
  | "#ENETUNREACH" [symbol(#ENETUNREACH)]
  | "#ENETRESET" [symbol(#ENETRESET)]
  | "#ECONNABORTED" [symbol(#ECONNABORTED)]
  | "#ECONNRESET" [symbol(#ECONNRESET)]
  | "#ENOBUFS" [symbol(#ENOBUFS)]
  | "#EISCONN" [symbol(#EISCONN)]
  | "#ENOTCONN" [symbol(#ENOTCONN)]
  | "#ESHUTDOWN" [symbol(#ESHUTDOWN)]
  | "#ETOOMANYREFS" [symbol(#ETOOMANYREFS)]
  | "#ETIMEDOUT" [symbol(#ETIMEDOUT)]
  | "#ECONNREFUSED" [symbol(#ECONNREFUSED)]
  | "#EHOSTDOWN" [symbol(#EHOSTDOWN)]
  | "#EHOSTUNREACH" [symbol(#EHOSTUNREACH)]
  | "#ELOOP" [symbol(#ELOOP)]
  | "#EOVERFLOW" [symbol(#EOVERFLOW)]
  syntax IOInt  ::=
    Int 
  | IOError 
  syntax IOString  ::=
    String 
  | IOError 
  syntax IOInt  ::=
    "#open" "(" path: String ")" [function]
  | "#open" "(" path: String "," mode: String ")" [function, hook(IO.open), impure]
  rule #open(S:String) => #open(S:String, "r+") 
  syntax IOInt  ::=
    "#tell" "(" fd: Int ")" [function, hook(IO.tell), impure]
  syntax K  ::=
    "#seek" "(" fd: Int "," index: Int ")" [function, hook(IO.seek), impure]
  | "#seekEnd" "(" fd: Int "," fromEnd: Int ")" [function, hook(IO.seekEnd), impure]
  syntax IOInt  ::=
    "#getc" "(" fd: Int ")" [function, hook(IO.getc), impure]
  syntax IOString  ::=
    "#read" "(" fd: Int "," length: Int ")" [function, hook(IO.read), impure]
  syntax K  ::=
    "#putc" "(" fd: Int "," value: Int ")" [function, hook(IO.putc), impure]
  | "#write" "(" fd: Int "," value: String ")" [function, hook(IO.write), impure]
  syntax K  ::=
    "#close" "(" fd: Int ")" [function, hook(IO.close), impure]
  syntax K  ::=
    "#lock" "(" fd: Int "," endIndex: Int ")" [function, hook(IO.lock), impure]
  | "#unlock" "(" fd: Int "," endIndex: Int ")" [function, hook(IO.unlock), impure]
  syntax IOInt  ::=
    "#accept" "(" fd: Int ")" [function, hook(IO.accept), impure]
  syntax K  ::=
    "#shutdownWrite" "(" fd: Int ")" [function, hook(IO.shutdownWrite), impure]
  syntax Int  ::=
    "#time" "(" ")" [function, hook(IO.time), impure]
  syntax Int  ::=
    "#stdin" [function, total]
  | "#stdout" [function, total]
  | "#stderr" [function, total]
  rule #stdin => 0 
  rule #stdout => 1 
  rule #stderr => 2 
  syntax KItem  ::=
    "#system" "(" String ")" [function, hook(IO.system), impure]
  | "#systemResult" "(" Int "," String "," String ")" [symbol(#systemResult)]
  syntax IOFile  ::=
    "#mkstemp" "(" template: String ")" [function, hook(IO.mkstemp), impure]
  syntax IOFile  ::=
    IOError 
  | "#tempFile" "(" path: String "," fd: Int ")" [symbol(#tempFile)]
  syntax K  ::=
    "#remove" "(" path: String ")" [function, hook(IO.remove), impure, total]
  syntax K  ::=
    "#logToFile" "(" name: String "," value: String ")" [function, hook(IO.log), impure, returnsUnit, symbol(#logToFile), total]
  syntax K  ::=
    "#log" "(" value: String ")" [function, hook(IO.logString), impure, returnsUnit, symbol(#log), total]
  syntax K  ::=
    "#trace" "(" value: KItem ")" [function, hook(IO.traceTerm), impure, returnsUnit, symbol(#trace), total]
  | "#traceK" "(" value: K ")" [function, hook(IO.traceTerm), impure, returnsUnit, symbol(#traceK), total]
  syntax Stream  ::=
    "#buffer" "(" K ")" 
  | "#istream" "(" Int ")" 
  | "#parseInput" "(" String "," String ")" 
  | "#ostream" "(" Int ")" 
endmodule

module STDIN-STREAM 
  imports public K-IO
  imports public K-REFLECTION
  imports public LIST
  imports public INT
  imports public BOOL
  configuration <stdin> ListItem(#buffer($STDIN:String)) ListItem($IO:String) ListItem(#istream(#stdin)) </stdin> 
  rule [stdinGetc]: <stdin>
       ListItem(#parseInput(_:String, Delimiters:String))
       ListItem(#buffer(S:String => S +String chrChar({#getc(N)}:>Int)))
       ListItem("on")
       ListItem(#istream(N:Int))
       </stdin>
    requires findChar(S, Delimiters, 0) ==Int -1 // [stdin]
        [priority(200), stream]
  rule [stdinParseString]: <stdin>
       (ListItem(#parseInput("String", Delimiters:String)) => ListItem(S))
       ListItem(#buffer(S:String => ""))
       _:List
       </stdin>
    requires findChar(S, Delimiters, 0) =/=Int -1 // [stdin]
        [stream]
  rule [stdinParseInt]: <stdin>
       (ListItem(#parseInput("Int", Delimiters:String))
       => ListItem(String2Int(substrString(S, 0, findChar(S, Delimiters, 0)))))
       ListItem(#buffer(S:String => substrString(S,findChar(S, Delimiters, 0) +Int 1, lengthString(S))))
       _:List
       </stdin>
    requires findChar(S, Delimiters, 0) =/=Int -1
       andBool lengthString(S) >Int 1 // [stdin]
        [stream]
  rule [stdinTrim]: <stdin>
       ListItem(#parseInput(Sort:String, Delimiters:String))
       ListItem(#buffer(S:String => substrString(S, 1, lengthString(S))))
       _:List
       </stdin>
    requires findChar(S, Delimiters, 0) =/=Int -1
       andBool Sort =/=String "String"
       andBool lengthString(S) <=Int 1 // [stdin]
        [stream]
  rule [stdinUnblock]: <stdin>
         (.List => ListItem(#parseInput(?Sort:String, ?Delimiters:String)))
         ListItem(#buffer(_:String))
         ...
       </stdin> 
endmodule

module STDOUT-STREAM 
  imports public K-IO
  imports public LIST
  imports public STRING
  configuration <stdout> ListItem(#ostream(#stdout)) ListItem($IO:String) ListItem(#buffer("")) </stdout> 
  rule [stdoutBufferFloat]: <stdout>
       ListItem(#ostream(_))
       ListItem(_)
       ListItem(#buffer(Buffer:String => Buffer +String Float2String(F)))
       (ListItem(F:Float) => .List)
       _:List
       </stdout>
       // [stdout, stderr]
        [priority(25), stream]
  rule [stdoutBufferInt]: <stdout>
       ListItem(#ostream(_))
       ListItem(_)
       ListItem(#buffer(Buffer:String => Buffer +String Int2String(I)))
       (ListItem(I:Int) => .List)
       _:List
       </stdout>
       // [stdout, stderr]
        [priority(25), stream]
  rule [stdoutBufferString]: <stdout>
       ListItem(#ostream(_))
       ListItem(_)
       ListItem(#buffer(Buffer:String => Buffer +String S))
       (ListItem(S:String) => .List)
       _:List
       </stdout>
       // [stdout, stderr]
        [priority(25), stream]
  rule [stdoutWrite]: <stdout>
       ListItem(#ostream(N:Int => {#write(N, S) ~> N:Int}:>Int))
       ListItem("on")
       ListItem(#buffer(S:String => ""))
       _:List
       </stdout>
    requires S =/=String "" // [stdout, stderr]
        [priority(30), stream]
endmodule

module MINT-SYNTAX 
  syntax {Width} MInt{Width} [hook(MINT.MInt)]
  syntax {Width} MInt{Width}  ::=
    r"[\\+\\-]?[0-9]+[pP][0-9]+" [hook(MINT.literal), prec(2), token]
endmodule

module MINT 
  imports public MINT-SYNTAX
  imports private INT
  imports private BYTES
  imports private BOOL
  syntax {Width} Int  ::=
    "bitwidthMInt" "(" MInt{Width} ")" [function, hook(MINT.bitwidth), total]
  syntax {Width} Int  ::=
    "MInt2Signed" "(" MInt{Width} ")" [function, hook(MINT.svalue), total]
  | "MInt2Unsigned" "(" MInt{Width} ")" [function, hook(MINT.uvalue), smt-hook(bv2int), total]
  syntax {Width} MInt{Width}  ::=
    "Int2MInt" "(" Int ")" [function, hook(MINT.integer), smt-hook(int2bv), total]
  syntax {Width} Bytes  ::=
    "MInt2Bytes" "(" MInt{Width} ")" [function, hook(MINT.MInt2bytes), total]
  syntax {Width} MInt{Width}  ::=
    "Bytes2MInt" "(" Bytes ")" [function, hook(MINT.bytes2MInt), total]
  syntax Int  ::=
    "sminMInt" "(" Int ")" [function]
  | "smaxMInt" "(" Int ")" [function]
  | "uminMInt" "(" Int ")" [function]
  | "umaxMInt" "(" Int ")" [function]
  rule sminMInt(N:Int) => 0 -Int (1 <<Int (N -Int 1)) 
  rule smaxMInt(N:Int) => (1 <<Int (N -Int 1)) -Int 1 
  rule uminMInt(_:Int) => 0 
  rule umaxMInt(N:Int) => (1 <<Int N) -Int 1 
  syntax Bool  ::=
    "soverflowMInt" "(" width: Int "," Int ")" [function]
  | "uoverflowMInt" "(" width: Int "," Int ")" [function]
  rule soverflowMInt(N:Int, I:Int)
  =>
    I <Int sminMInt(N) orBool I >Int smaxMInt(N) 
  rule uoverflowMInt(N:Int, I:Int)
  =>
    I <Int uminMInt(N) orBool I >Int umaxMInt(N) 
  syntax {Width} MInt{Width}  ::=
    "~MInt" MInt{Width} [function, hook(MINT.not), smt-hook(bvnot), total]
  | "--MInt" MInt{Width} [function, hook(MINT.neg), smt-hook(bvuminus), total]
  > left: 
    MInt{Width} "^MInt" MInt{Width} [function, hook(MINT.pow), total]
  | MInt{Width} "*MInt" MInt{Width} [function, hook(MINT.mul), smt-hook(bvmul), total]
  | MInt{Width} "/sMInt" MInt{Width} [function, hook(MINT.sdiv), smt-hook(bvsdiv)]
  | MInt{Width} "%sMInt" MInt{Width} [function, hook(MINT.srem), smt-hook(bvsrem)]
  | MInt{Width} "/uMInt" MInt{Width} [function, hook(MINT.udiv), smt-hook(bvudiv)]
  | MInt{Width} "%uMInt" MInt{Width} [function, hook(MINT.urem), smt-hook(bvurem)]
  > left: 
    MInt{Width} "+MInt" MInt{Width} [function, hook(MINT.add), smt-hook(bvadd), total]
  | MInt{Width} "-MInt" MInt{Width} [function, hook(MINT.sub), smt-hook(bvsub), total]
  > left: 
    MInt{Width} "<<MInt" MInt{Width} [function, hook(MINT.shl), smt-hook(bvshl)]
  | MInt{Width} ">>aMInt" MInt{Width} [function, hook(MINT.ashr), smt-hook(bvashr)]
  | MInt{Width} ">>lMInt" MInt{Width} [function, hook(MINT.lshr), smt-hook(bvlshr)]
  > left: 
    MInt{Width} "&MInt" MInt{Width} [function, hook(MINT.and), smt-hook(bvand), total]
  > left: 
    MInt{Width} "xorMInt" MInt{Width} [function, hook(MINT.xor), smt-hook(bvxor), total]
  > left: 
    MInt{Width} "|MInt" MInt{Width} [function, hook(MINT.or), smt-hook(bvor), total]
  syntax {Width} Bool  ::=
    MInt{Width} "<sMInt" MInt{Width} [function, hook(MINT.slt), smt-hook(bvslt), total]
  | MInt{Width} "<uMInt" MInt{Width} [function, hook(MINT.ult), smt-hook(bvult), total]
  | MInt{Width} "<=sMInt" MInt{Width} [function, hook(MINT.sle), smt-hook(bvsle), total]
  | MInt{Width} "<=uMInt" MInt{Width} [function, hook(MINT.ule), smt-hook(bvule), total]
  | MInt{Width} ">sMInt" MInt{Width} [function, hook(MINT.sgt), smt-hook(bvsgt), total]
  | MInt{Width} ">uMInt" MInt{Width} [function, hook(MINT.ugt), smt-hook(bvugt), total]
  | MInt{Width} ">=sMInt" MInt{Width} [function, hook(MINT.sge), smt-hook(bvsge), total]
  | MInt{Width} ">=uMInt" MInt{Width} [function, hook(MINT.uge), smt-hook(bvuge), total]
  | MInt{Width} "==MInt" MInt{Width} [function, hook(MINT.eq), smt-hook(=), total]
  | MInt{Width} "=/=MInt" MInt{Width} [function, hook(MINT.ne), smt-hook(distinct), total]
  syntax {Width} MInt{Width}  ::=
    "sMaxMInt" "(" MInt{Width} "," MInt{Width} ")" [function, hook(MINT.smax), smt-hook((ite (bvslt #1 #2) #2 #1)), total]
  | "sMinMInt" "(" MInt{Width} "," MInt{Width} ")" [function, hook(MINT.smin), smt-hook((ite (bvslt #1 #2) #1 #2)), total]
  | "uMaxMInt" "(" MInt{Width} "," MInt{Width} ")" [function, hook(MINT.umax), smt-hook((ite (bvult #1 #2) #2 #1)), total]
  | "uMinMInt" "(" MInt{Width} "," MInt{Width} ")" [function, hook(MINT.umin), smt-hook((ite (bvult #1 #2) #1 #2)), total]
  syntax {Width1, Width2} MInt{Width1}  ::=
    "roundMInt" "(" MInt{Width2} ")" [function, hook(MINT.round), total]
  syntax {Width1, Width2} MInt{Width1}  ::=
    "signExtendMInt" "(" MInt{Width2} ")" [function, hook(MINT.sext), total]
endmodule


module VERIFICATION 
  imports public INT
  imports public BOOL
  imports public STRING
  syntax Bool  ::=
    "bracketSpec" "(" String "," Int ")" [function, total]
  | "bracketEmpty" "(" Bool "," String "," Int ")" [function, total]
  | "bracketOpen" "(" Bool "," String "," Int ")" [function, total]
  | "bracketNegative" "(" Bool "," String "," Int ")" [function, total]
  rule bracketSpec(S, D) => bracketEmpty(S ==String "", S, D) 
  rule bracketEmpty(true, _, D) => D ==Int 0 
  rule bracketEmpty(false, S, D)
    => bracketOpen(substrString(S, 0, 1) ==String "<", S, D) 
  rule bracketOpen(true, S, D)
    => bracketSpec(substrString(S, 1, lengthString(S)), D +Int 1) 
  rule bracketOpen(false, S, D)
    => bracketNegative(D -Int 1 <Int 0, S, D) 
  rule bracketNegative(true, _, _) => false 
  rule bracketNegative(false, S, D)
    => bracketSpec(substrString(S, 1, lengthString(S)), D -Int 1) 
endmodule

module MPY-SYNTAX 
  imports public INT-SYNTAX
  imports public BOOL-SYNTAX
  imports public STRING-SYNTAX
  syntax Pgm  ::=
    "Module" "(" Stmts ")" 
  | "correctProgram" "(" ")" 
  syntax Stmts  ::=
    List{Stmt,""} 
  | "targetLoopBody" "(" ")" [function, total]
  | "targetTail" "(" ")" [function, total]
  syntax Strings  ::=
    List{String,","} 
  syntax Params  ::=
    "Params" "(" Strings ")" 
  syntax Stmt  ::=
    "FuncDef" "(" String "," Params "," Stmts ")" 
  | "Assign" "(" Expr "," Expr ")" 
  | "For" "(" Expr "," Expr "," Stmts ")" 
  | "If" "(" Expr "," Stmts "," Stmts ")" 
  | "Return" "(" Expr ")" 
  syntax Expr  ::=
    "Name" "(" String ")" 
  | "Int" "(" Int ")" 
  | "Bool" "(" Bool ")" 
  | "Str" "(" String ")" 
  | "BinOp" "(" String "," Expr "," Expr ")" 
  | "Compare" "(" Expr "," CmpOp ")" 
  syntax CmpOp  ::=
    "CmpOp" "(" String "," Expr ")" 
endmodule

module MPY 
  imports public MPY-SYNTAX
  imports public MAP
  imports public INT
  imports public BOOL
  imports public STRING
  imports public VERIFICATION
  syntax Value  ::=
    "IVal" "(" Int ")" 
  | "BVal" "(" Bool ")" 
  | "SVal" "(" String ")" 
  syntax Function  ::=
    "function" "(" Params "," Stmts ")" 
  syntax Store  ::=
    "emptyStore" "(" ")" 
  | "bind" "(" String "," Value "," Store ")" 
  syntax Value  ::=
    "lookup" "(" String "," Store ")" [function]
  rule lookup(X, bind(X, V, _)) => V 
  rule lookup(X, bind(Y, _, REST)) => lookup(X, REST)
    requires X =/=String Y 
  syntax KItem  ::=
    "invoke" "(" String "," Value ")" 
  | "functionBoundary" "(" ")" 
  | "assignName" "(" String ")" 
  | "binopLeft" "(" String "," Expr ")" 
  | "binopRight" "(" String "," Value ")" 
  | "compareLeft" "(" CmpOp ")" 
  | "compareRight" "(" String "," Value ")" 
  | "ifKont" "(" Stmts "," Stmts ")" 
  | "forStart" "(" Expr "," Stmts ")" 
  | "forString" "(" String "," String "," Stmts ")" 
  | "returnKont" "(" ")" 
  | "finish" "(" ")" 
  configuration <py>
      <k> $PGM:Pgm ~> invoke("correct_bracketing", SVal($INPUT:String)) </k>
      <functions> .Map </functions>
      <env> emptyStore() </env>
      <result> noResult() </result>
    </py> 
  syntax Result  ::=
    "noResult" "(" ")" 
  | "result" "(" Value ")" 
  rule <k> Module(SS) => SS ... </k> 
  rule targetLoopBody() =>
    If(Compare(Name("bracket"), CmpOp("==", Str("<"))),
      Assign(Name("depth"), BinOp("+", Name("depth"), Int(1))),
      Assign(Name("depth"), BinOp("-", Name("depth"), Int(1))))
    If(Compare(Name("depth"), CmpOp("<", Int(0))),
      Return(Bool(false)),
      .Stmts) 
  rule targetTail() =>
    Return(Compare(Name("depth"), CmpOp("==", Int(0)))) 
  rule correctProgram() =>
    Module(
      FuncDef("correct_bracketing", Params("brackets"),
        Assign(Name("depth"), Int(0))
        For(Name("bracket"), Name("brackets"),
          targetLoopBody())
        targetTail())) 
  rule <k> (S:Stmt REST:Stmts) => S ~> REST ... </k> 
  rule <k> .Stmts => . ... </k> 
  rule <k> FuncDef(F, PS, BODY) => . ... </k>
       <functions> M => M [ F <- function(PS, BODY) ] </functions> 
  rule <k> invoke(F, V) => BODY ~> functionBoundary() ... </k>
       <functions> ... F |-> function(Params(P, .Strings), BODY) ... </functions>
       <env> _ => bind(P, V, emptyStore()) </env> 
  rule <k> Int(I) => IVal(I) ... </k> 
  rule <k> Bool(B) => BVal(B) ... </k> 
  rule <k> Str(S) => SVal(S) ... </k> 
  rule <k> Name(X) => lookup(X, STORE) ... </k>
       <env> STORE </env> 
  rule <k> Assign(Name(X), E) => E ~> assignName(X) ... </k> 
  rule <k> V:Value ~> assignName(X) => . ... </k>
       <env> STORE => bind(X, V, STORE) </env> 
  rule <k> BinOp(OP, L, R) => L ~> binopLeft(OP, R) ... </k> 
  rule <k> V:Value ~> binopLeft(OP, R) => R ~> binopRight(OP, V) ... </k> 
  rule <k> IVal(J) ~> binopRight("+", IVal(I)) => IVal(I +Int J) ... </k> 
  rule <k> IVal(J) ~> binopRight("-", IVal(I)) => IVal(I -Int J) ... </k> 
  rule <k> Compare(L, C) => L ~> compareLeft(C) ... </k> 
  rule <k> V:Value ~> compareLeft(CmpOp(OP, R))
        => R ~> compareRight(OP, V) ... </k> 
  rule <k> SVal(R) ~> compareRight("==", SVal(L))
        => BVal(L ==String R) ... </k> 
  rule <k> IVal(R) ~> compareRight("==", IVal(L))
        => BVal(L ==Int R) ... </k> 
  rule <k> IVal(R) ~> compareRight("<", IVal(L))
        => BVal(L <Int R) ... </k> 
  rule <k> If(E, THEN, ELSE) => E ~> ifKont(THEN, ELSE) ... </k> 
  rule <k> BVal(true) ~> ifKont(THEN, _) => THEN ... </k> 
  rule <k> BVal(false) ~> ifKont(_, ELSE) => ELSE ... </k> 
  rule <k> For(TARGET, ITERABLE, BODY)
        => ITERABLE ~> forStart(TARGET, BODY) ... </k> 
  rule <k> SVal(S) ~> forStart(Name(X), BODY)
        => forString(S, X, BODY) ... </k> 
  rule <k> forString(S, _, _) => . ... </k>
    requires S ==String "" 
  rule <k> forString(S, X, BODY)
        => BODY ~> forString(substrString(S, 1, lengthString(S)), X, BODY) ... </k>
       <env> STORE => bind(X, SVal(substrString(S, 0, 1)), STORE) </env>
    requires S =/=String "" 
  rule <k> Return(E) => E ~> returnKont() ... </k> 
  rule <k> V:Value ~> returnKont() ~> _REST:K
        => V ~> finish() </k> 
  rule <k> V:Value ~> finish() => .K </k>
       <result> _ => result(V) </result> 
endmodule


