requires "../source/semantic.k"

module CONNECTION-BASE
  imports SEMANTIC

  claim [split-universal]:
    <simplify>
      <k> slashSplit(Int2String(A) +String "/" +String Int2String(B))
           => pairList(strVal(Int2String(A)), strVal(Int2String(B))) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [decimal-universal]:
    <simplify>
      <k> decimalValue(Int2String(I)) => I </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [builtin-universal]:
    <simplify>
      <k> String2Int(Int2String(I)) => I </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [split-ground-positive]:
    <simplify>
      <k> slashSplit(Int2String(123) +String "/" +String Int2String(456))
           => pairList(strVal(Int2String(123)), strVal(Int2String(456))) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [split-ground-negative-zero]:
    <simplify>
      <k> slashSplit(Int2String(-12) +String "/" +String Int2String(0))
           => pairList(strVal(Int2String(-12)), strVal(Int2String(0))) </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [decimal-ground-negative]:
    <simplify>
      <k> decimalValue(Int2String(-123456789)) => -123456789 </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [builtin-ground-negative]:
    <simplify>
      <k> String2Int(Int2String(-123456789)) => -123456789 </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>
endmodule
