module BF-PROBE3
  imports INT
  imports BOOL
  imports STRING
  imports K-EQUAL
  imports MAP
  syntax IntSeq ::= ".IntSeq" | iCons(Int, IntSeq)
  syntax IntSeq ::= strToCodes(String) [function]
  rule strToCodes("") => .IntSeq
  rule strToCodes(S:String) => iCons(ordChar(substrString(S,0,1)), strToCodes(substrString(S,1,lengthString(S)))) requires S =/=String ""
  syntax Int ::= idx8(IntSeq) [function, total]
  rule idx8(P:IntSeq) =>
    #if P ==K strToCodes("Mercury") #then 0 #else #if P ==K strToCodes("Venus") #then 1
    #else #if P ==K strToCodes("Earth") #then 2 #else #if P ==K strToCodes("Mars") #then 3
    #else #if P ==K strToCodes("Jupiter") #then 4 #else #if P ==K strToCodes("Saturn") #then 5
    #else #if P ==K strToCodes("Uranus") #then 6 #else #if P ==K strToCodes("Neptune") #then 7
    #else -1 #fi #fi #fi #fi #fi #fi #fi #fi [simplification]
  syntax KItem ::= d8(IntSeq) | res(Int) | sel(Bool, Int, KItem)
  rule <k> d8(P:IntSeq) => sel(P==K strToCodes("Mercury"),0, sel(P==K strToCodes("Venus"),1,
    sel(P==K strToCodes("Earth"),2, sel(P==K strToCodes("Mars"),3, sel(P==K strToCodes("Jupiter"),4,
    sel(P==K strToCodes("Saturn"),5, sel(P==K strToCodes("Uranus"),6, sel(P==K strToCodes("Neptune"),7,
    res(-1))))))))) ... </k>
  rule <k> sel(true,  N:Int, _:KItem) => res(N) ... </k>
  rule <k> sel(false, _:Int, K:KItem) => K ... </k>
  configuration <k> $PGM:K </k>
endmodule
