requires "semantic.k"

module BRIDGE-CHECK
  imports SEMANTIC

  claim [slash-split-connection]:
    <simplify>
      <k>
        slashSplit(Int2String(A) +String "/" +String Int2String(B))
        => pairList(strVal(Int2String(A)), strVal(Int2String(B)))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [decimal-value-connection]:
    <simplify>
      <k> decimalValue(Int2String(I)) => I </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>

  claim [string-int-inverse]:
    <simplify>
      <k> String2Int(Int2String(I)) => I </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </simplify>
endmodule
