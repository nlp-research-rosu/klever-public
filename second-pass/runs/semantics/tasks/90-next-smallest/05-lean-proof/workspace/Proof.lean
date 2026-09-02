import Init.Classical
import Proof.KStep
import Klean90NextSmallest.Lemmas

namespace Proof

/- KORE symbol: Lbl'Unds'List'Unds'; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def _List_ (left right : SortList) : SortList :=
  (_root_._List_ left right).getD ⟨left.coll ++ right.coll⟩
/- KORE symbol: Lbl'Unds'Map'Unds'; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def _Map_ (left right : SortMap) : SortMap :=
  (_root_._Map_ right left).getD ⟨right.coll ++ left.coll⟩
/- KORE symbol: Lbl'Unds'in'Unds'keys'LParUndsRParUnds'MAP'Unds'Bool'Unds'KItem'Unds'Map; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def «_in_keys(_)_MAP_Bool_KItem_Map»
    (key : SortKItem) (map : SortMap) : SortBool :=
  (_root_.«_in_keys(_)_MAP_Bool_KItem_Map» key map).getD false
/- KORE symbol: Lbl'UndsLSqBUnds-LT-'-undef'RSqB'; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def «_[_<-undef]»
    (map : SortMap) (key : SortKItem) : SortMap :=
  (_root_.«_[_<-undef]» map key).getD map
/- KORE symbol: Lbl'UndsPipe'-'-GT-Unds'; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def «_|->_»
    (key value : SortKItem) : SortMap :=
  (_root_.«_|->_» key value).getD ⟨[(key, value)]⟩
/- KORE symbol: LblListItem; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def ListItem (item : SortKItem) : SortList :=
  (_root_.ListItem item).getD ⟨[item]⟩
/- KORE symbol: LblnotBool'Unds'; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
@[simp] noncomputable def notBool_ (value : SortBool) : SortBool :=
  (_root_.notBool_ value).getD (!value)

@[simp] theorem getD_if_some {α : Type} (proposition : Prop)
    [Decidable proposition] (fallback : α) :
    (if proposition then some fallback else none).getD fallback = fallback := by
  split <;> rfl

@[simp] theorem project_injected_val (value : SortVal) :
    _root_.«project:Val»
        (SortK.kseq ((@inj SortVal SortKItem) value) SortK.dotk) =
      some value := by
  cases value <;> rfl

@[simp] theorem inj_val_int (value : SortInt) :
    (@inj SortVal SortKItem) (SortVal.inj_SortInt value) =
      SortKItem.inj_SortInt value := by
  rfl

@[simp] theorem inj_val_bool (value : SortBool) :
    (@inj SortVal SortKItem) (SortVal.inj_SortBool value) =
      SortKItem.inj_SortBool value := by
  rfl

theorem applyCmp_int_ne (left right : SortInt) :
    _root_.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
        "!=" (SortVal.inj_SortInt left) (SortVal.inj_SortInt right) =
      some (Bool.not (BEq.beq left right)) := by
  simp [_root_.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»,
    _root_._03e60c5, _root_._0ae23e4, _root_._0d7d6b1,
    _root_._1c34a14, _root_._1eb1e83, _root_._21c3768,
    _root_._220c8a2, _root_._31a7ce9, _root_._3762d3f,
    _root_._41490e6, _root_._42db81d, _root_._57afa07,
    _root_._57f520f, _root_._641b30a, _root_._6b454b2,
    _root_._6b7e0d4, _root_._7031c92, _root_._758418c,
    _root_._7a57b51, _root_._87bf7c6, _root_._882c519,
    _root_._8a4564e, _root_._9a8a33a, _root_._9b4e435,
    _root_._9d30e79, _root_._9e5ad0c, _root_._9ec2057,
    _root_._9f9c54d, _root_._b076352, _root_._b37e75d,
    _root_._b558675, _root_._b69f73f, _root_._beb7b49,
    _root_._c0092c8, _root_._c91e9fa, _root_._c986c4d,
    _root_._f10cf1b, _root_._f53e67b, _root_._f5cd646,
    _root_._f64794f, _root_.retr, _root_.«_==Int_»,
    _root_.«_=/=Int_», _root_._4de6e05, _root_.notBool_,
    _root_._17ebc68, _root_._53fc758] <;>
  cases equality : left == right <;> simp

@[simp] theorem singleton_concat_of_fresh
    (key value : SortKItem) (map : SortMap)
    (fresh :
      notBool_ («_in_keys(_)_MAP_Bool_KItem_Map» key map) = true) :
    _root_._Map_ («_|->_» key value) map =
      some (_Map_ map («_|->_» key value)) := by
  have fresh_false :
      «_in_keys(_)_MAP_Bool_KItem_Map» key map = false := by
    cases found : «_in_keys(_)_MAP_Bool_KItem_Map» key map <;>
      simp_all [notBool_, _root_.notBool_, _17ebc68, _53fc758]
  rcases map with ⟨entries⟩
  induction entries with
  | nil => rfl
  | cons entry rest ih =>
      letI : DecidableEq SortKItem :=
        Classical.typeDecidableEq SortKItem
      change
        (if entry.1 = key then true
         else «_in_keys(_)_MAP_Bool_KItem_Map» key { coll := rest }) =
          false at fresh_false
      have head_ne : entry.1 ≠ key := by
        intro head_eq
        simp [head_eq] at fresh_false
      have tail_false :
          «_in_keys(_)_MAP_Bool_KItem_Map» key { coll := rest } =
            false := by
        simpa [head_ne] using fresh_false
      have tail_fresh :
          notBool_
            («_in_keys(_)_MAP_Bool_KItem_Map» key { coll := rest }) =
              true := by
        cases found :
            «_in_keys(_)_MAP_Bool_KItem_Map» key { coll := rest } <;>
          simp_all [notBool_, _root_.notBool_, _17ebc68, _53fc758]
      have tail_concat := ih tail_fresh tail_false
      simp [«_|->_», _Map_, _root_.«_|->_», _root_._Map_] at tail_concat
      simp [«_|->_», _Map_, _root_.«_|->_», _root_._Map_]
      kunfold_maps
      simp [Ne.symm head_ne, tail_concat]
      kunfold_contains
      rfl

theorem look_in_frame
    {name : SortString} {location : SortInt}
    {frame residual : SortMap} {parent : SortParent}
    {value : SortVal} {continuation : SortK}
    {envCell : SortEnvCell} {scopeLocCell : SortScopeLocCell}
    {heapCell : SortHeapCell} {heapLocCell : SortHeapLocCell}
    {stackCell : SortStackCell} {retCell : SortRetCell}
    {excCell : SortExcCell} {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell}
    (fresh :
      notBool_
        («_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt location) residual) = true)
    (present :
      _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString name) frame = some true)
    (found :
      _root_.«Map:lookup» frame (SortKItem.inj_SortString name) =
        some ((@inj SortVal SortKItem) value)) :
    Rewrites
      { k :=
          { val :=
              SortK.kseq
                (SortKItem.«#look(_,_)_MPY-CORE_KItem_String_Int»
                  name location) continuation },
        env := envCell,
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      frame parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell }
      { k :=
          { val :=
              SortK.kseq ((@inj SortVal SortKItem) value) continuation },
        env := envCell,
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      frame parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell } := by
  refine Rewrites._db779c6
    (L := location) (M := frame) (_DotVar2 := residual)
    (_Val1 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» frame parent)))
    (_Val2 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              frame parent))))
    (_Val5 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» frame parent)))
    (_Val6 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              frame parent))))
    (X := name) (_DotVar1 := continuation) (_Gen0 := parent)
    (_Gen1 := envCell) (_Gen2 := scopeLocCell) (_Gen3 := heapCell)
    (_Gen4 := heapLocCell) (_Gen5 := stackCell) (_Gen6 := retCell)
    (_Gen7 := excCell) (_Gen8 := exitCell) (_Gen9 := counterCell)
    (_Val0 := true) (_Val3 := (@inj SortVal SortKItem) value)
    (_Val4 := value)
    ?_ ?_ ?_ ?_ ?_ ?_ ?_ ?_
  · exact present
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh
  · exact found
  · exact project_injected_val value
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh
  · rfl

theorem assign_in_frame
    {name : SortString} {location : SortInt}
    {frame updated residual : SortMap} {parent : SortParent}
    {value : SortVal} {continuation : SortK}
    {scopeLocCell : SortScopeLocCell}
    {heapCell : SortHeapCell} {heapLocCell : SortHeapLocCell}
    {stackCell : SortStackCell} {retCell : SortRetCell}
    {excCell : SortExcCell} {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell}
    (fresh :
      notBool_
        («_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt location) residual) = true)
    (update :
      _root_.«Map:update» frame (SortKItem.inj_SortString name)
        ((@inj SortVal SortKItem) value) = some updated) :
    Rewrites
      { k :=
          { val :=
              SortK.kseq
                ((@inj SortStmt SortKItem)
                  (SortStmt.«Assign(_,_)_MPY-SYNTAX_Stmt_Expr_Expr»
                    (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» name)
                    ((@inj SortVal SortExpr) value))) continuation },
        env := { val := location },
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      frame parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val := continuation },
        env := { val := location },
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      updated parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell } := by
  refine Rewrites._e6f504a
    (L := location) (M := frame) (_DotVar2 := residual)
    (_Val0 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» frame parent)))
    (_Val1 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              frame parent))))
    (_Val2 := updated)
    (_Val3 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
            updated parent)))
    (_Val4 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              updated parent))))
    (V := value) (X := name) (_DotVar1 := continuation)
    (_Gen0 := parent) (_Gen1 := scopeLocCell) (_Gen2 := heapCell)
    (_Gen3 := heapLocCell) (_Gen4 := stackCell) (_Gen5 := retCell)
    (_Gen6 := excCell) (_Gen7 := exitCell) (_Gen8 := counterCell)
    ?_ ?_ ?_ ?_ ?_
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh
  · exact update
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh

theorem bind_in_frame
    {name : SortString} {location : SortInt}
    {frame updated residual : SortMap} {parent : SortParent}
    {value : SortVal} {continuation : SortK}
    {scopeLocCell : SortScopeLocCell}
    {heapCell : SortHeapCell} {heapLocCell : SortHeapLocCell}
    {stackCell : SortStackCell} {retCell : SortRetCell}
    {excCell : SortExcCell} {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell}
    (fresh :
      notBool_
        («_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt location) residual) = true)
    (update :
      _root_.«Map:update» frame (SortKItem.inj_SortString name)
        ((@inj SortVal SortKItem) value) = some updated) :
    Rewrites
      { k :=
          { val :=
              SortK.kseq
                (SortKItem.«#bindTgt(_,_)_MPY-TUPLE_KItem_Expr_Val»
                  (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» name) value)
                continuation },
        env := { val := location },
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      frame parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val := continuation },
        env := { val := location },
        scopes :=
          { val :=
              _Map_ residual
                («_|->_» (SortKItem.inj_SortInt location)
                  (SortKItem.inj_SortScope
                    (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                      updated parent))) },
        scopeLoc := scopeLocCell,
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := stackCell,
        ret := retCell,
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell } := by
  refine Rewrites._d5bec6c
    (L := location) (M := frame) (_DotVar2 := residual)
    (_Val0 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent» frame parent)))
    (_Val1 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              frame parent))))
    (_Val2 := updated)
    (_Val3 :=
      «_|->_» (SortKItem.inj_SortInt location)
        (SortKItem.inj_SortScope
          (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
            updated parent)))
    (_Val4 :=
      _Map_ residual
        («_|->_» (SortKItem.inj_SortInt location)
          (SortKItem.inj_SortScope
            (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
              updated parent))))
    (V := value) (X := name) (_DotVar1 := continuation)
    (_Gen0 := parent) (_Gen1 := scopeLocCell) (_Gen2 := heapCell)
    (_Gen3 := heapLocCell) (_Gen4 := stackCell) (_Gen5 := retCell)
    (_Gen6 := excCell) (_Gen7 := exitCell) (_Gen8 := counterCell)
    ?_ ?_ ?_ ?_ ?_
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh

  · exact update
  · rfl
  · exact singleton_concat_of_fresh _ _ _ fresh

theorem pop_frame
    {caller location saved : SortInt} {continuation : SortK}
    {scopes : SortMap} {value : SortVal} {rest : SortList}
    {currentScopeLoc : SortInt}
    {heapCell : SortHeapCell} {heapLocCell : SortHeapLocCell}
    {excCell : SortExcCell} {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell} :
    Rewrites
      { k := { val := SortK.kseq SortKItem.«#pop_MPY-FUNCTIONS_KItem» SortK.dotk },
        env := { val := location },
        scopes := { val := scopes },
        scopeLoc := { val := currentScopeLoc },
        heap := heapCell,
        heapLoc := heapLocCell,
        stack :=
          { val :=
              _List_
                (ListItem
                  (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
                    continuation caller saved))
                rest },
        ret := { val := SortRetState.«retV(_)_MPY-CORE_RetState_Val» value },
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val :=
          SortK.kseq ((@inj SortVal SortKItem) value) continuation },
        env := { val := caller },
        scopes := { val :=
          «_[_<-undef]» scopes (SortKItem.inj_SortInt location) },
        scopeLoc := { val := saved },
        heap := heapCell,
        heapLoc := heapLocCell,
        stack := { val := rest },
        ret := { val := SortRetState.«noRet_MPY-CORE_RetState» },
        exc := excCell,
        exitCode := exitCell,
        generatedCounter := counterCell } := by
  refine Rewrites._9533001
    (CALLERL := caller) (L := location) (SAVEDL := saved)
    (_Gen0 := currentScopeLoc) (CONT := continuation) (SC := scopes)
    (_Val2 := «_[_<-undef]» scopes (SortKItem.inj_SortInt location))
    (V := value) (_DotVar1 := rest)
    (_Val0 :=
      ListItem
        (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
          continuation caller saved))
    (_Val1 :=
      _List_
        (ListItem
          (SortKItem.«frame(_,_,_)_MPY-FUNCTIONS_KItem_K_Int_Int»
            continuation caller saved))
        rest)
    (_Gen1 := heapCell) (_Gen2 := heapLocCell) (_Gen3 := excCell)
    (_Gen4 := exitCell) (_Gen5 := counterCell)
    ?_ ?_ ?_
  · rfl
  · rfl
  · rfl

/- KORE symbol: LblnsScan'LParUndsCommUndsCommUndsCommUndsRParUnds'NEXT-SMALLEST-VERIFICATION'Unds'Val'Unds'Ints'Unds'Int'Unds'Int'Unds'Int; frozen source obligations: rule-24e0b061b3462f2b6e58444f2f4c1b2a9c99ebe7e02e89ff2bfabb146ab52cba. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
    : SortInts → SortInt → SortInt → SortInt → SortVal
  | SortInts.«nilInts_NEXT-SMALLEST-VERIFICATION_Ints», _, second, count =>
      if count = 2 then SortVal.inj_SortInt second
      else SortVal.«noneV_MPY-CORE_Val»
  | SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints»
        value rest, smallest, second, count =>
      if count = 0 then
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest value second 1
      else if value < smallest then
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest value smallest 2
      else if value = smallest then
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest smallest second count
      else if count = 1 then
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest smallest value 2
      else if value < second then
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest smallest value 2
      else
        «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»
          rest smallest second count

noncomputable def functionFrame
    (oldValue : SortInt) (lst : SortVal) (smallest second count : SortInt) :
    SortMap :=
  _Map_
    (_Map_
      (_Map_
        (_Map_
          («_|->_» (SortKItem.inj_SortString "value")
            (SortKItem.inj_SortInt oldValue))
          («_|->_» (SortKItem.inj_SortString "lst")
            ((@inj SortVal SortKItem) lst)))
        («_|->_» (SortKItem.inj_SortString "smallest")
          (SortKItem.inj_SortInt smallest)))
      («_|->_» (SortKItem.inj_SortString "second")
        (SortKItem.inj_SortInt second)))
    («_|->_» (SortKItem.inj_SortString "count")
      (SortKItem.inj_SortInt count))

set_option maxHeartbeats 2000000 in
@[simp] theorem functionFrame_coll
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    (functionFrame oldValue lst smallest second count).coll =
      [ (SortKItem.inj_SortString "count", SortKItem.inj_SortInt count),
        (SortKItem.inj_SortString "second", SortKItem.inj_SortInt second),
        (SortKItem.inj_SortString "smallest",
          SortKItem.inj_SortInt smallest),
        (SortKItem.inj_SortString "lst", (@inj SortVal SortKItem) lst),
        (SortKItem.inj_SortString "value",
          SortKItem.inj_SortInt oldValue) ] := by
  simp [functionFrame, _Map_, «_|->_», _root_._Map_, _root_.«_|->_»]

@[simp] theorem sortMap_eta (map : SortMap) :
    SortMap.mk map.coll = map := by
  cases map
  rfl

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_has
    (name : SortString) (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt)
    (known :
      name = "value" ∨ name = "lst" ∨ name = "smallest" ∨
      name = "second" ∨ name = "count") :
    _root_.«_in_keys(_)_MAP_Bool_KItem_Map»
        (SortKItem.inj_SortString name)
        (functionFrame oldValue lst smallest second count) =
      some true := by
  rcases known with rfl | rfl | rfl | rfl | rfl <;>
    simp [_root_.«_in_keys(_)_MAP_Bool_KItem_Map»] <;>
    kunfold_concrete_maps <;> simp

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_lookup_count
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    _root_.«Map:lookup»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "count") =
      some ((@inj SortVal SortKItem) (SortVal.inj_SortInt count)) := by
  simp [_root_.«Map:lookup»]
  kunfold_concrete_maps
  simp

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_lookup_second
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    _root_.«Map:lookup»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "second") =
      some ((@inj SortVal SortKItem) (SortVal.inj_SortInt second)) := by
  simp [_root_.«Map:lookup»]
  kunfold_concrete_maps
  simp

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_lookup_smallest
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    _root_.«Map:lookup»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "smallest") =
      some ((@inj SortVal SortKItem) (SortVal.inj_SortInt smallest)) := by
  simp [_root_.«Map:lookup»]
  kunfold_concrete_maps
  simp

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_lookup_value
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    _root_.«Map:lookup»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "value") =
      some ((@inj SortVal SortKItem) (SortVal.inj_SortInt oldValue)) := by
  simp [_root_.«Map:lookup»]
  kunfold_concrete_maps
  simp

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_update_value
    (oldValue newValue : SortInt) (lst : SortVal)
    (smallest second count : SortInt) :
    _root_.«Map:update»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "value")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newValue)) =
      some (functionFrame newValue lst smallest second count) := by
  simp [_root_.«Map:update»]
  kunfold_concrete_maps
  simp
  exact
    (congrArg SortMap.mk
      (functionFrame_coll newValue lst smallest second count)).symm.trans
        (sortMap_eta _)

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_update_smallest
    (oldValue : SortInt) (lst : SortVal)
    (smallest newSmallest second count : SortInt) :
    _root_.«Map:update»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "smallest")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newSmallest)) =
      some (functionFrame oldValue lst newSmallest second count) := by
  simp [_root_.«Map:update»]
  kunfold_concrete_maps
  simp
  exact
    (congrArg SortMap.mk
      (functionFrame_coll oldValue lst newSmallest second count)).symm.trans
        (sortMap_eta _)

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_update_second
    (oldValue : SortInt) (lst : SortVal)
    (smallest second newSecond count : SortInt) :
    _root_.«Map:update»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "second")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newSecond)) =
      some (functionFrame oldValue lst smallest newSecond count) := by
  simp [_root_.«Map:update»]
  kunfold_concrete_maps
  simp
  exact
    (congrArg SortMap.mk
      (functionFrame_coll oldValue lst smallest newSecond count)).symm.trans
        (sortMap_eta _)

set_option maxHeartbeats 2000000 in
@[simp] theorem frame_update_count
    (oldValue : SortInt) (lst : SortVal)
    (smallest second count newCount : SortInt) :
    _root_.«Map:update»
        (functionFrame oldValue lst smallest second count)
        (SortKItem.inj_SortString "count")
        ((@inj SortVal SortKItem) (SortVal.inj_SortInt newCount)) =
      some (functionFrame oldValue lst smallest second newCount) := by
  simp [_root_.«Map:update»]
  kunfold_concrete_maps
  simp
  exact
    (congrArg SortMap.mk
      (functionFrame_coll oldValue lst smallest second newCount)).symm.trans
        (sortMap_eta _)

theorem drop_empty_stmts
    {continuation : SortK}
    {envCell : SortEnvCell} {scopesCell : SortScopesCell}
    {scopeLocCell : SortScopeLocCell} {heapCell : SortHeapCell}
    {heapLocCell : SortHeapLocCell} {stackCell : SortStackCell}
    {retCell : SortRetCell} {excCell : SortExcCell}
    {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell} :
    Rewrites
      { k := { val := (SortK.kseq
          (SortKItem.inj_SortStmts
            SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
          continuation) },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val := continuation },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell } := by
  exact Rewrites._2a0ddee

theorem resume_loop
    {next continuation result : SortK}
    {envCell : SortEnvCell} {scopesCell : SortScopesCell}
    {scopeLocCell : SortScopeLocCell} {heapCell : SortHeapCell}
    {heapLocCell : SortHeapLocCell} {stackCell : SortStackCell}
    {retCell : SortRetCell} {excCell : SortExcCell}
    {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell}
    (appended : _root_.append next continuation = some result) :
    Rewrites
      { k := { val := (SortK.kseq
          (SortKItem.«#loopLbl(_)_MPY-CONTROLS_KItem_K» next)
          continuation) },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val := result },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell } := by
  exact Rewrites._d499ad9 appended

theorem continue_loop
    {next continuation result : SortK}
    {envCell : SortEnvCell} {scopesCell : SortScopesCell}
    {scopeLocCell : SortScopeLocCell} {heapCell : SortHeapCell}
    {heapLocCell : SortHeapLocCell} {stackCell : SortStackCell}
    {retCell : SortRetCell} {excCell : SortExcCell}
    {exitCell : SortExitCodeCell}
    {counterCell : SortGeneratedCounterCell}
    (appended : _root_.append next continuation = some result) :
    Rewrites
      { k := { val := (SortK.kseq
          (SortKItem.inj_SortStmts
            SortStmts.«.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts»)
          (SortK.kseq
            (SortKItem.«#loopLbl(_)_MPY-CONTROLS_KItem_K» next)
            continuation)) },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell }
      { k := { val := result },
        env := envCell, scopes := scopesCell, scopeLoc := scopeLocCell,
        heap := heapCell, heapLoc := heapLocCell, stack := stackCell,
        ret := retCell, exc := excCell, exitCode := exitCell,
        generatedCounter := counterCell } := by
  exact Rewrites.tran drop_empty_stmts (resume_loop appended)

set_option maxHeartbeats 2000000 in
@[simp] theorem discard_function_frame
    (residual frame : SortMap)
    (fresh :
      notBool_
        («_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt 1) residual) = true) :
    «_[_<-undef]»
        (_Map_ residual
          («_|->_» (SortKItem.inj_SortInt 1)
            (SortKItem.inj_SortScope
              (SortScope.«scope(_,_)_MPY-CORE_Scope_Map_Parent»
                frame (SortParent.«parent(_)_MPY-CORE_Parent_Int» 0)))))
        (SortKItem.inj_SortInt 1) =
      residual := by
  have fresh_false :
      «_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt 1) residual = false := by
    cases found :
        «_in_keys(_)_MAP_Bool_KItem_Map»
          (SortKItem.inj_SortInt 1) residual <;>
      simp_all [notBool_, _root_.notBool_, _17ebc68, _53fc758]
  rcases residual with ⟨entries⟩
  induction entries with
  | nil =>
      simp [«_[_<-undef]», _Map_, «_|->_», _root_.«_[_<-undef]»,
        _root_._Map_, _root_.«_|->_»]
      kunfold_delete
      simp
      kunfold_delete
      rfl
  | cons entry rest ih =>
      letI : DecidableEq SortKItem :=
        Classical.typeDecidableEq SortKItem
      change
        (if entry.1 = SortKItem.inj_SortInt 1 then true
         else
           «_in_keys(_)_MAP_Bool_KItem_Map»
             (SortKItem.inj_SortInt 1) { coll := rest }) =
          false at fresh_false
      have head_ne : entry.1 ≠ SortKItem.inj_SortInt 1 := by
        intro head_eq
        simp [head_eq] at fresh_false
      have tail_false :
          «_in_keys(_)_MAP_Bool_KItem_Map»
              (SortKItem.inj_SortInt 1) { coll := rest } =
            false := by
        simpa [head_ne] using fresh_false
      have tail_fresh :
          notBool_
              («_in_keys(_)_MAP_Bool_KItem_Map»
                (SortKItem.inj_SortInt 1) { coll := rest }) =
            true := by
        cases found :
            «_in_keys(_)_MAP_Bool_KItem_Map»
              (SortKItem.inj_SortInt 1) { coll := rest } <;>
          simp_all [notBool_, _root_.notBool_, _17ebc68, _53fc758]
      have tail_deleted := ih tail_fresh tail_false
      have tail_coll :=
        congrArg (fun map : SortMap => map.coll) tail_deleted
      simp [«_[_<-undef]», _Map_, «_|->_», _root_.«_[_<-undef]»,
        _root_._Map_, _root_.«_|->_»] at tail_coll
      kunfold_delete at tail_coll
      simp at tail_coll
      simp [«_[_<-undef]», _Map_, «_|->_», _root_.«_[_<-undef]»,
        _root_._Map_, _root_.«_|->_»]
      kunfold_delete
      simp
      kunfold_delete
      simp [head_ne, tail_coll]

set_option maxHeartbeats 2000000 in
theorem final :
    Klean90NextSmallest.Lemmas.targetStatement _List_ _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» ListItem notBool_ «nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int» := by
  unfold Klean90NextSmallest.Lemmas.targetStatement
  intro _DotVar0 CODE EXC REST CONT HLOC HEAP COUNT SECOND SMALLEST LST
    OLD_VALUE SC INPUT h
  revert COUNT SECOND SMALLEST OLD_VALUE
  induction INPUT with
  | «nilInts_NEXT-SMALLEST-VERIFICATION_Ints» =>
      intro COUNT SECOND SMALLEST OLD_VALUE
      rw [«nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»]
      refine Rewrites.tran Rewrites._c65b0f2 ?_
      refine Rewrites.tran
        (Rewrites._767922c
          (IS := SortInts.«nilInts_NEXT-SMALLEST-VERIFICATION_Ints»)
          (_Val0 := true) (by rfl) rfl) ?_
      refine Rewrites.tran Rewrites._8e90948 ?_
      refine Rewrites.tran Rewrites._94bd14e ?_
      refine Rewrites.tran
        (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
          (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran
        (Rewrites._1f0e78f (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran Rewrites._6d39855 ?_
      refine Rewrites.tran
        (look_in_frame
          (frame := functionFrame OLD_VALUE LST SMALLEST SECOND COUNT)
          (value := SortVal.inj_SortInt COUNT)
          (fresh := h)
          (frame_has "count" OLD_VALUE LST SMALLEST SECOND COUNT
            (by simp))
          (frame_lookup_count OLD_VALUE LST SMALLEST SECOND COUNT)) ?_
      simp only [inj_val_int]
      refine Rewrites.tran
        (Rewrites._dfb9e43
          (HOLE := SortExpr.inj_SortInt COUNT)
          (_Val0 := true) (_Val1 := true)
          (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran
        (Rewrites._e1122bd
          (HOLE := SortExpr.«Int(_)_MPY-SYNTAX_Expr_Int» 2)
          (_Gen0 := SortVal.inj_SortInt COUNT) (_Gen1 := "==")
          (_Val0 := false) (_Val1 := true) (_Val2 := true)
          (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran Rewrites._665cd53 ?_
      refine Rewrites.tran
        (Rewrites._aae3b52
          (HOLE := SortExpr.inj_SortInt 2)
          (_Gen0 := SortVal.inj_SortInt COUNT) (_Gen1 := "==")
          (_Val0 := true) (_Val1 := true)
          (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran
        (Rewrites._a00964a
          (LV := SortVal.inj_SortInt COUNT)
          (RV := SortVal.inj_SortInt 2) (OP := "==")
          (_Val0 := COUNT == 2) (by rfl)) ?_
      by_cases count_two : COUNT = 2
      · simp [count_two]
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
            (HOLE := SortExpr.inj_SortBool true)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran
          (Rewrites._c82b7aa
            (C := SortVal.inj_SortBool true) (_Val0 := true)
            (by rfl)) ?_
        refine Rewrites.tran Rewrites._0fd4639 ?_
        refine Rewrites.tran Rewrites._94bd14e ?_
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_heat»
            (HOLE := SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "second")
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran Rewrites._6d39855 ?_
        refine Rewrites.tran
          (look_in_frame
            (frame := functionFrame OLD_VALUE LST SMALLEST SECOND 2)
            (value := SortVal.inj_SortInt SECOND)
            (fresh := h)
            (frame_has "second" OLD_VALUE LST SMALLEST SECOND 2
              (by simp))
            (frame_lookup_second OLD_VALUE LST SMALLEST SECOND 2)) ?_
        simp only [inj_val_int]
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool»
            (HOLE := SortExpr.inj_SortInt SECOND)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran
          (Rewrites._b817d8b
            (V := SortVal.inj_SortInt SECOND)) ?_
        exact pop_frame
      · have count_bool : (COUNT == 2) = false := by
          simp [count_two]
        simp only [count_bool, if_neg count_two]
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_cool»
            (HOLE := SortExpr.inj_SortBool false)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran
          (Rewrites._c82b7aa
            (C := SortVal.inj_SortBool false) (_Val0 := false)
            (by rfl)) ?_
        refine Rewrites.tran Rewrites._052f78e ?_
        refine Rewrites.tran Rewrites._2a0ddee ?_
        refine Rewrites.tran Rewrites._94bd14e ?_
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_heat»
            (HOLE := SortExpr.«NoneVal_MPY-SYNTAX_Expr»)
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran Rewrites._b378664 ?_
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_Return(_)_MPY_SYNTAX_Stmt_Expr1_cool»
            (HOLE := SortExpr.inj_SortVal SortVal.«noneV_MPY-CORE_Val»)
            (_Val0 := true) (_Val1 := true)
            (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran
          (Rewrites._b817d8b
            (V := SortVal.«noneV_MPY-CORE_Val»)) ?_
        exact pop_frame
  | «consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints»
      value rest ih =>
      intro COUNT SECOND SMALLEST OLD_VALUE
      rw [«nsScan(_,_,_,_)_NEXT-SMALLEST-VERIFICATION_Val_Ints_Int_Int_Int»]
      refine Rewrites.tran Rewrites._c65b0f2 ?_
      refine Rewrites.tran
        (Rewrites._42052f2
          (IS :=
            SortInts.«consInts(_,_)_NEXT-SMALLEST-VERIFICATION_Ints_Int_Ints»
              value rest)
          (_Val0 := false) (_Val1 := true) (_Val2 := value)
          (_Val3 := rest) (by rfl) (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran Rewrites._3ff423b ?_
      refine Rewrites.tran
        (bind_in_frame
          (frame := functionFrame OLD_VALUE LST SMALLEST SECOND COUNT)
          (updated := functionFrame value LST SMALLEST SECOND COUNT)
          (value := SortVal.inj_SortInt value)
          (fresh := h)
          (frame_update_value OLD_VALUE value LST SMALLEST SECOND COUNT)) ?_
      refine Rewrites.tran Rewrites._94bd14e ?_
      refine Rewrites.tran
        (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
          (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran
        (Rewrites._1f0e78f (by rfl) (by rfl) (by rfl) rfl) ?_
      refine Rewrites.tran Rewrites._6d39855 ?_
      refine Rewrites.tran
        (look_in_frame
          (frame := functionFrame value LST SMALLEST SECOND COUNT)
          (value := SortVal.inj_SortInt COUNT)
          (fresh := h)
          (frame_has "count" value LST SMALLEST SECOND COUNT
            (by simp))
          (frame_lookup_count value LST SMALLEST SECOND COUNT)) ?_
      simp only [inj_val_int]
      finish_int_compare (COUNT, 0, "==", COUNT == 0)
      by_cases count_zero : COUNT = 0
      · simp only [count_zero]
        finish_if_true
        refine Rewrites.tran Rewrites._94bd14e ?_
        heat_assign_name ("smallest", "value")
        refine Rewrites.tran
          (look_in_frame
            (frame := functionFrame value LST SMALLEST SECOND 0)
            (value := SortVal.inj_SortInt value)
            (fresh := h)
            (frame_has "value" value LST SMALLEST SECOND 0
              (by simp))
            (frame_lookup_value value LST SMALLEST SECOND 0)) ?_
        simp only [inj_val_int]
        cool_assign_int ("smallest", value)
        refine Rewrites.tran
          (assign_in_frame
            (frame := functionFrame value LST SMALLEST SECOND 0)
            (updated := functionFrame value LST value SECOND 0)
            (value := SortVal.inj_SortInt value)
            (fresh := h)
            (frame_update_smallest value LST SMALLEST value SECOND 0)) ?_
        refine Rewrites.tran Rewrites._94bd14e ?_
        eval_assign_literal ("count", 1)
        refine Rewrites.tran
          (assign_in_frame
            (frame := functionFrame value LST value SECOND 0)
            (updated := functionFrame value LST value SECOND 1)
            (value := SortVal.inj_SortInt 1)
            (fresh := h)
            (frame_update_count value LST value SECOND 0 1)) ?_
        refine Rewrites.tran drop_empty_stmts ?_
        refine Rewrites.tran
          (continue_loop (by rfl)) ?_
        have ih' := ih 1 SECOND value value
        simp only [discard_function_frame SC _ h] at ih' ⊢
        exact ih'
      · have count_bool : (COUNT == 0) = false := by
          simp [count_zero]
        simp only [count_bool, if_neg count_zero]
        finish_if_false
        refine Rewrites.tran Rewrites._94bd14e ?_
        refine Rewrites.tran
          (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
            (HOLE :=
              SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
                (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "value")
                (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr»
                  "<" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "smallest")))
            (_Val0 := false) (_Val1 := true) (_Val2 := true)
            (by rfl) (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran
          (Rewrites._1f0e78f (by rfl) (by rfl) (by rfl) rfl) ?_
        refine Rewrites.tran Rewrites._6d39855 ?_
        refine Rewrites.tran
          (look_in_frame
            (frame := functionFrame value LST SMALLEST SECOND COUNT)
            (value := SortVal.inj_SortInt value)
            (fresh := h)
            (frame_has "value" value LST SMALLEST SECOND COUNT
              (by simp))
            (frame_lookup_value value LST SMALLEST SECOND COUNT)) ?_
        simp only [inj_val_int]
        heat_compare_name (value, "<", "smallest")
        refine Rewrites.tran
          (look_in_frame
            (frame := functionFrame value LST SMALLEST SECOND COUNT)
            (value := SortVal.inj_SortInt SMALLEST)
            (fresh := h)
            (frame_has "smallest" value LST SMALLEST SECOND COUNT
              (by simp))
            (frame_lookup_smallest value LST SMALLEST SECOND COUNT)) ?_
        simp only [inj_val_int]
        cool_compare_int (value, SMALLEST, "<", value < SMALLEST)
        by_cases value_lt : value < SMALLEST
        · simp only [value_lt]
          finish_if_true
          refine Rewrites.tran Rewrites._94bd14e ?_
          heat_assign_name ("second", "smallest")
          refine Rewrites.tran
            (look_in_frame
              (frame := functionFrame value LST SMALLEST SECOND COUNT)
              (value := SortVal.inj_SortInt SMALLEST)
              (fresh := h)
              (frame_has "smallest" value LST SMALLEST SECOND COUNT
                (by simp))
              (frame_lookup_smallest value LST SMALLEST SECOND COUNT)) ?_
          simp only [inj_val_int]
          cool_assign_int ("second", SMALLEST)
          refine Rewrites.tran
            (assign_in_frame
              (frame := functionFrame value LST SMALLEST SECOND COUNT)
              (updated := functionFrame value LST SMALLEST SMALLEST COUNT)
              (value := SortVal.inj_SortInt SMALLEST)
              (fresh := h)
              (frame_update_second
                value LST SMALLEST SECOND SMALLEST COUNT)) ?_
          refine Rewrites.tran Rewrites._94bd14e ?_
          eval_assign_literal ("count", 2)
          refine Rewrites.tran
            (assign_in_frame
              (frame := functionFrame value LST SMALLEST SMALLEST COUNT)
              (updated := functionFrame value LST SMALLEST SMALLEST 2)
              (value := SortVal.inj_SortInt 2)
              (fresh := h)
              (frame_update_count value LST SMALLEST SMALLEST COUNT 2)) ?_
          refine Rewrites.tran Rewrites._94bd14e ?_
          heat_assign_name ("smallest", "value")
          refine Rewrites.tran
            (look_in_frame
              (frame := functionFrame value LST SMALLEST SMALLEST 2)
              (value := SortVal.inj_SortInt value)
              (fresh := h)
              (frame_has "value" value LST SMALLEST SMALLEST 2
                (by simp))
              (frame_lookup_value value LST SMALLEST SMALLEST 2)) ?_
          simp only [inj_val_int]
          cool_assign_int ("smallest", value)
          refine Rewrites.tran
            (assign_in_frame
              (frame := functionFrame value LST SMALLEST SMALLEST 2)
              (updated := functionFrame value LST value SMALLEST 2)
              (value := SortVal.inj_SortInt value)
              (fresh := h)
              (frame_update_smallest
                value LST SMALLEST value SMALLEST 2)) ?_
          refine Rewrites.tran drop_empty_stmts ?_
          refine Rewrites.tran drop_empty_stmts ?_
          refine Rewrites.tran (continue_loop (by rfl)) ?_
          have ih' := ih 2 SMALLEST value value
          simp only [discard_function_frame SC _ h] at ih' ⊢
          exact ih'
        · have value_bool : decide (value < SMALLEST) = false := by
            exact decide_eq_false value_lt
          simp only [value_bool, if_neg value_lt]
          finish_if_false
          refine Rewrites.tran Rewrites._94bd14e ?_
          refine Rewrites.tran
            (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
              (HOLE :=
                SortExpr.«Compare(_,_)_MPY-SYNTAX_Expr_Expr_CmpOp»
                  (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String» "value")
                  (SortCmpOp.«CmpOp(_,_)_MPY-SYNTAX_CmpOp_String_Expr»
                    "!=" (SortExpr.«Name(_)_MPY-SYNTAX_Expr_String»
                      "smallest")))
              (_Val0 := false) (_Val1 := true) (_Val2 := true)
              (by rfl) (by rfl) (by rfl) rfl) ?_
          refine Rewrites.tran
            (Rewrites._1f0e78f (by rfl) (by rfl) (by rfl) rfl) ?_
          refine Rewrites.tran Rewrites._6d39855 ?_
          refine Rewrites.tran
            (look_in_frame
              (frame := functionFrame value LST SMALLEST SECOND COUNT)
              (value := SortVal.inj_SortInt value)
              (fresh := h)
              (frame_has "value" value LST SMALLEST SECOND COUNT
                (by simp))
              (frame_lookup_value value LST SMALLEST SECOND COUNT)) ?_
          simp only [inj_val_int]
          heat_compare_name (value, "!=", "smallest")
          refine Rewrites.tran
            (look_in_frame
              (frame := functionFrame value LST SMALLEST SECOND COUNT)
              (value := SortVal.inj_SortInt SMALLEST)
              (fresh := h)
              (frame_has "smallest" value LST SMALLEST SECOND COUNT
                (by simp))
              (frame_lookup_smallest value LST SMALLEST SECOND COUNT)) ?_
          simp only [inj_val_int]
          refine Rewrites.tran
            (Rewrites._aae3b52
              (HOLE := SortExpr.inj_SortInt SMALLEST)
              (_Gen0 := SortVal.inj_SortInt value) (_Gen1 := "!=")
              (_Val0 := true) (_Val1 := true)
              (by rfl) (by rfl) rfl) ?_
          refine Rewrites.tran
            (Rewrites._a00964a
              (LV := SortVal.inj_SortInt value)
              (RV := SortVal.inj_SortInt SMALLEST) (OP := "!=")
              (_Val0 := Bool.not (BEq.beq value SMALLEST))
              (applyCmp_int_ne value SMALLEST)) ?_
          by_cases value_eq : value = SMALLEST
          · have value_ne_bool :
                Bool.not (BEq.beq value SMALLEST) = false := by
              simp [value_eq]
            rw [value_ne_bool]
            simp only [if_pos value_eq]
            finish_if_false
            refine Rewrites.tran drop_empty_stmts ?_
            refine Rewrites.tran drop_empty_stmts ?_
            refine Rewrites.tran drop_empty_stmts ?_
            refine Rewrites.tran (continue_loop (by rfl)) ?_
            have ih' := ih COUNT SECOND SMALLEST value
            simp only [discard_function_frame SC _ h] at ih' ⊢
            exact ih'
          · have value_ne_bool :
                Bool.not (BEq.beq value SMALLEST) = true := by
              simp [value_eq]
            rw [value_ne_bool]
            simp only [if_neg value_eq]
            finish_if_true
            refine Rewrites.tran Rewrites._94bd14e ?_
            refine Rewrites.tran
              (Rewrites.«MPY_SYNTAX_If(_,_,_)_MPY_SYNTAX_Stmt_Expr_Stmts_Stmts1_heat»
                (_Val0 := false) (_Val1 := true) (_Val2 := true)
                (by rfl) (by rfl) (by rfl) rfl) ?_
            refine Rewrites.tran
              (Rewrites._b967e49
                (_Val0 := false) (_Val1 := true) (_Val2 := true)
                (by rfl) (by rfl) (by rfl) rfl) ?_
            refine Rewrites.tran
              (Rewrites._1f0e78f
                (_Val0 := false) (_Val1 := true) (_Val2 := true)
                (by rfl) (by rfl) (by rfl) rfl) ?_
            refine Rewrites.tran Rewrites._6d39855 ?_
            refine Rewrites.tran
              (look_in_frame
                (frame := functionFrame value LST SMALLEST SECOND COUNT)
                (value := SortVal.inj_SortInt COUNT)
                (fresh := h)
                (frame_has "count" value LST SMALLEST SECOND COUNT
                  (by simp))
                (frame_lookup_count value LST SMALLEST SECOND COUNT)) ?_
            simp only [inj_val_int]
            finish_int_compare (COUNT, 1, "==", COUNT == 1)
            refine Rewrites.tran
              (Rewrites._c582d87
                (HOLE := SortExpr.inj_SortBool (COUNT == 1))
                (_Val0 := true) (_Val1 := true)
                (by rfl) (by rfl) rfl) ?_
            by_cases count_one : COUNT = 1
            · simp only [count_one]
              refine Rewrites.tran
                (Rewrites._f5d43e4
                  (V := SortVal.inj_SortBool true)
                  (_Val0 := true) (by rfl) rfl) ?_
              finish_if_true
              refine Rewrites.tran Rewrites._94bd14e ?_
              heat_assign_name ("second", "value")
              refine Rewrites.tran
                (look_in_frame
                  (frame := functionFrame value LST SMALLEST SECOND 1)
                  (value := SortVal.inj_SortInt value)
                  (fresh := h)
                  (frame_has "value" value LST SMALLEST SECOND 1
                    (by simp))
                  (frame_lookup_value value LST SMALLEST SECOND 1)) ?_
              simp only [inj_val_int]
              cool_assign_int ("second", value)
              refine Rewrites.tran
                (assign_in_frame
                  (frame := functionFrame value LST SMALLEST SECOND 1)
                  (updated := functionFrame value LST SMALLEST value 1)
                  (value := SortVal.inj_SortInt value)
                  (fresh := h)
                  (frame_update_second
                    value LST SMALLEST SECOND value 1)) ?_
              refine Rewrites.tran Rewrites._94bd14e ?_
              eval_assign_literal ("count", 2)
              refine Rewrites.tran
                (assign_in_frame
                  (frame := functionFrame value LST SMALLEST value 1)
                  (updated := functionFrame value LST SMALLEST value 2)
                  (value := SortVal.inj_SortInt 2)
                  (fresh := h)
                  (frame_update_count value LST SMALLEST value 1 2)) ?_
              refine Rewrites.tran drop_empty_stmts ?_
              refine Rewrites.tran drop_empty_stmts ?_
              refine Rewrites.tran drop_empty_stmts ?_
              refine Rewrites.tran drop_empty_stmts ?_
              refine Rewrites.tran (continue_loop (by rfl)) ?_
              have ih' := ih 2 value SMALLEST value
              simp only [discard_function_frame SC _ h] at ih' ⊢
              exact ih'
            · have count_one_bool : (COUNT == 1) = false := by
                simp [count_one]
              simp only [count_one_bool, if_neg count_one]
              refine Rewrites.tran
                (Rewrites._3d156a6
                  (V := SortVal.inj_SortBool false)
                  (_Val0 := false) (_Val1 := true)
                  (by rfl) (by rfl) rfl) ?_
              refine Rewrites.tran
                (Rewrites._b967e49
                  (_Val0 := false) (_Val1 := true) (_Val2 := true)
                  (by rfl) (by rfl) (by rfl) rfl) ?_
              refine Rewrites.tran
                (Rewrites._1f0e78f
                  (_Val0 := false) (_Val1 := true) (_Val2 := true)
                  (by rfl) (by rfl) (by rfl) rfl) ?_
              refine Rewrites.tran Rewrites._6d39855 ?_
              refine Rewrites.tran
                (look_in_frame
                  (frame := functionFrame value LST SMALLEST SECOND COUNT)
                  (value := SortVal.inj_SortInt value)
                  (fresh := h)
                  (frame_has "value" value LST SMALLEST SECOND COUNT
                    (by simp))
                  (frame_lookup_value value LST SMALLEST SECOND COUNT)) ?_
              simp only [inj_val_int]
              heat_compare_name (value, "<", "second")
              refine Rewrites.tran
                (look_in_frame
                  (frame := functionFrame value LST SMALLEST SECOND COUNT)
                  (value := SortVal.inj_SortInt SECOND)
                  (fresh := h)
                  (frame_has "second" value LST SMALLEST SECOND COUNT
                    (by simp))
                  (frame_lookup_second value LST SMALLEST SECOND COUNT)) ?_
              simp only [inj_val_int]
              cool_compare_int (value, SECOND, "<", value < SECOND)
              refine Rewrites.tran
                (Rewrites._c582d87
                  (HOLE := SortExpr.inj_SortBool (value < SECOND))
                  (_Val0 := true) (_Val1 := true)
                  (by rfl) (by rfl) rfl) ?_
              refine Rewrites.tran
                (Rewrites._1d613f5
                  (V := SortVal.inj_SortBool (value < SECOND))) ?_
              by_cases value_second : value < SECOND
              · simp only [value_second]
                finish_if_true
                refine Rewrites.tran Rewrites._94bd14e ?_
                heat_assign_name ("second", "value")
                refine Rewrites.tran
                  (look_in_frame
                    (frame :=
                      functionFrame value LST SMALLEST SECOND COUNT)
                    (value := SortVal.inj_SortInt value)
                    (fresh := h)
                    (frame_has
                      "value" value LST SMALLEST SECOND COUNT (by simp))
                    (frame_lookup_value
                      value LST SMALLEST SECOND COUNT)) ?_
                simp only [inj_val_int]
                cool_assign_int ("second", value)
                refine Rewrites.tran
                  (assign_in_frame
                    (frame :=
                      functionFrame value LST SMALLEST SECOND COUNT)
                    (updated :=
                      functionFrame value LST SMALLEST value COUNT)
                    (value := SortVal.inj_SortInt value)
                    (fresh := h)
                    (frame_update_second
                      value LST SMALLEST SECOND value COUNT)) ?_
                refine Rewrites.tran Rewrites._94bd14e ?_
                eval_assign_literal ("count", 2)
                refine Rewrites.tran
                  (assign_in_frame
                    (frame :=
                      functionFrame value LST SMALLEST value COUNT)
                    (updated :=
                      functionFrame value LST SMALLEST value 2)
                    (value := SortVal.inj_SortInt 2)
                    (fresh := h)
                    (frame_update_count
                      value LST SMALLEST value COUNT 2)) ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran (continue_loop (by rfl)) ?_
                have ih' := ih 2 value SMALLEST value
                simp only [discard_function_frame SC _ h] at ih' ⊢
                exact ih'
              · have value_second_bool :
                    decide (value < SECOND) = false := by
                  exact decide_eq_false value_second
                simp only [value_second_bool, if_neg value_second]
                finish_if_false
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran drop_empty_stmts ?_
                refine Rewrites.tran (continue_loop (by rfl)) ?_
                have ih' := ih COUNT SECOND SMALLEST value
                simp only [discard_function_frame SC _ h] at ih' ⊢
                exact ih'

end Proof
