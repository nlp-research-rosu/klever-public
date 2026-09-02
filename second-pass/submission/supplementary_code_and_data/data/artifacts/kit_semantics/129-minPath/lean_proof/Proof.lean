import Klean129Minpath.Lemmas
import Lean.Elab.Tactic.Omega

namespace Proof

private def intSeqList : SortIntSeq → List Int
  | SortIntSeq.«.IntSeq_MPY-CORE_IntSeq» => []
  | SortIntSeq.«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» x xs => x :: intSeqList xs

private def valSeqList : SortValSeq → List SortVal
  | SortValSeq.«.ValSeq_MPY-CORE_ValSeq» => []
  | SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x xs => x :: valSeqList xs

private def listValSeq : List SortVal → SortValSeq
  | [] => SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | x :: xs => SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq» x (listValSeq xs)

@[simp] private theorem valSeqList_listValSeq (xs : List SortVal) :
    valSeqList (listValSeq xs) = xs := by
  induction xs <;> simp [listValSeq, valSeqList, *]

private def intSeqAtModel (xs : SortIntSeq) (i : Int) : Int :=
  if i < 0 then 0 else (intSeqList xs)[i.toNat]?.getD 0

private def gridAtModel (p : SortIntSeq) (n i j : Int) : Int :=
  intSeqAtModel p (i * n + j)

private def gridRowModel (p : SortIntSeq) (n i : Int) : SortValSeq :=
  listValSeq <| (List.range n.toNat).map fun j =>
    SortVal.inj_SortInt (gridAtModel p n i (Int.ofNat j))

private def gridRowsModel (p : SortIntSeq) (n : Int) : SortValSeq :=
  listValSeq <| (List.range n.toNat).map fun i =>
    SortVal.inj_SortIterable
      (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq»
        (gridRowModel p n (Int.ofNat i)))

private def valSeqAtModel (xs : SortValSeq) (i : Int) : SortVal :=
  if i < 0 then SortVal.«noneV_MPY-CORE_Val»
  else (valSeqList xs)[i.toNat]?.getD SortVal.«noneV_MPY-CORE_Val»

private def valSeqConcatModel (xs ys : SortValSeq) : SortValSeq :=
  listValSeq (valSeqList xs ++ valSeqList ys)

private def snocModel (xs : SortValSeq) (x : SortVal) : SortValSeq :=
  listValSeq (valSeqList xs ++ [x])

private def pairPrefixModel (a : SortValSeq) (m : Int) : Nat → SortValSeq
  | 0 => a
  | r + 1 =>
      pairPrefixModel
        (snocModel (snocModel a (SortVal.inj_SortInt 1)) (SortVal.inj_SortInt m))
        m r

private noncomputable def pairDoneModel (a o : SortValSeq) (r m : Int) : Bool :=
  @decide
    (valSeqList (pairPrefixModel a m r.toNat) = valSeqList o)
    (Classical.propDecidable _)

private noncomputable def oddDoneModel (a o : SortValSeq) (r m : Int) : Bool :=
  @decide
    (valSeqList o =
      valSeqList (snocModel (pairPrefixModel a m r.toNat) (SortVal.inj_SortInt 1)))
    (Classical.propDecidable _)

private def pyModModel (i n : Int) : Int :=
  if n = 0 then 0 else Int.tmod (Int.tmod i n + n) n

private def oneRowModel (p : SortIntSeq) (n : Int) : Int :=
  if 0 < n then
    match (intSeqList p).idxOf? 1 with
    | some k => Int.ofNat (k / n.toNat)
    | none => Int.tdiv (-1) n
  else 0

private def oneColModel (p : SortIntSeq) (n : Int) : Int :=
  if 0 < n then
    match (intSeqList p).idxOf? 1 with
    | some k => Int.ofNat (k % n.toNat)
    | none => pyModModel (-1) n
  else 0

private def expectedValues (m : Int) : List Int :=
  (List.range m.toNat).map fun k => Int.ofNat k + 1

private def validPermModel (p : SortIntSeq) (m : Int) : Bool :=
  decide (0 ≤ m ∧ (intSeqList p).Perm (expectedValues m))

private def vsLenModel (xs : SortValSeq) : Int :=
  Int.ofNat (valSeqList xs).length

private theorem expectedValues_nodup (m : Int) : (expectedValues m).Nodup := by
  unfold expectedValues
  exact List.Pairwise.map (R := fun a b : Nat => a ≠ b)
    (S := fun a b : Int => a ≠ b) (fun k => (k : Int) + 1)
    (by
      intro a b hab heq
      apply hab
      apply Int.ofNat_inj.mp
      exact Int.add_left_cancel (a := (1 : Int)) (b := (a : Int)) (c := (b : Int))
        (by simpa [Int.add_comm] using heq)) List.nodup_range

private theorem one_mem_expectedValues {m : Int} (hm : 0 < m) :
    1 ∈ expectedValues m := by
  unfold expectedValues
  rw [List.mem_map]
  refine ⟨0, List.mem_range.mpr ?_, by simp⟩
  omega

private theorem expectedValues_mem_bounds {m x : Int} (hm : 0 ≤ m)
    (hx : x ∈ expectedValues m) : 0 < x ∧ x < m + 1 := by
  unfold expectedValues at hx
  rw [List.mem_map] at hx
  rcases hx with ⟨k, hk, rfl⟩
  have hk' : k < m.toNat := List.mem_range.mp hk
  have hm' : (Int.ofNat m.toNat) = m := Int.toNat_of_nonneg hm
  change 0 < (k : Int) + 1 ∧ (k : Int) + 1 < m + 1
  constructor <;> omega

private theorem int_idxOf?_eq_some_idxOf {xs : List Int} (h : 1 ∈ xs) :
    xs.idxOf? 1 = some (xs.idxOf 1) := by
  induction xs with
  | nil => simp at h
  | cons x xs ih =>
      by_cases hx : x = 1
      · subst x
        simp [List.idxOf?_cons]
      · have hx' : 1 ≠ x := fun heq => hx heq.symm
        have ht : 1 ∈ xs := by simpa [hx'] using h
        have hbeq : (x == (1 : Int)) = false := beq_eq_false_iff_ne.mpr hx
        simp [List.idxOf?_cons, List.idxOf_cons, hbeq, ih ht]

private theorem mem_of_get?_eq_some {xs : List α} {k : Nat} {a : α}
    (h : xs[k]? = some a) : a ∈ xs := by
  induction xs generalizing k with
  | nil => simp at h
  | cons x xs ih =>
      cases k with
      | zero =>
          simp at h
          subst x
          simp
      | succ k =>
          simp at h
          exact List.mem_cons_of_mem _ (ih h)

private theorem int_get?_idxOf_eq_one {xs : List Int} (h : 1 ∈ xs) :
    xs[xs.idxOf 1]? = some 1 := by
  induction xs with
  | nil => simp at h
  | cons x xs ih =>
      by_cases hx : x = 1
      · subst x
        simp
      · have hx' : 1 ≠ x := fun heq => hx heq.symm
        have ht : 1 ∈ xs := by simpa [hx'] using h
        have hbeq : (x == (1 : Int)) = false := beq_eq_false_iff_ne.mpr hx
        simp [List.idxOf_cons, hbeq, ih ht]

private theorem int_idxOf_eq_of_get? {xs : List Int} {k : Nat}
    (hnd : xs.Nodup) (hget : xs[k]? = some 1) : xs.idxOf 1 = k := by
  induction xs generalizing k with
  | nil => simp at hget
  | cons x xs ih =>
      cases k with
      | zero =>
          simp at hget
          subst x
          simp
      | succ k =>
          simp at hget
          have hnd' := List.nodup_cons.mp hnd
          have hne : x ≠ 1 := by
            intro hx
            subst x
            exact hnd'.1 (mem_of_get?_eq_some hget)
          have hbeq : (x == (1 : Int)) = false := beq_eq_false_iff_ne.mpr hne
          simp [List.idxOf_cons, hbeq, ih hnd'.2 hget]

private theorem flat_nonneg {i n j : Int} (hi : 0 ≤ i) (hn : 0 ≤ n)
    (hj : 0 ≤ j) : 0 ≤ i * n + j :=
  Int.add_nonneg (Int.mul_nonneg hi hn) hj

private theorem flat_lt_square {i n j : Int} (hn : 0 ≤ n) (hi : i < n)
    (hj : j < n) : i * n + j < n * n := by
  have h₁ : i * n + j < i * n + n := Int.add_lt_add_left hj (i * n)
  have h₂raw : (i + 1) * n ≤ n * n :=
    Int.mul_le_mul_of_nonneg_right (Int.add_one_le_iff.mpr hi) hn
  have h₂ : i * n + n ≤ n * n := by
    simpa [Int.add_mul] using h₂raw
  exact Int.lt_of_lt_of_le h₁ h₂

private theorem flat_toNat {i n j : Int} (hi : 0 ≤ i) (hn : 0 ≤ n)
    (hj : 0 ≤ j) :
    (i * n + j).toNat = i.toNat * n.toNat + j.toNat := by
  rw [Int.toNat_add (Int.mul_nonneg hi hn) hj, Int.toNat_mul hi hn]

/- KORE symbol: Lbl'Unds'andBool'Unds'; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70, rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def _andBool_ : SortBool → SortBool → SortBool := (· && ·)
/- KORE symbol: Lbl'Unds-GT-Eqls'Int'Unds'; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70, rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987, rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_>=Int_» (a b : SortInt) : SortBool := decide (a ≥ b)
/- KORE symbol: Lbl'Unds-LT-'Int'Unds'; frozen source obligations: rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_<Int_» (a b : SortInt) : SortBool := decide (a < b)
/- KORE symbol: Lbl'UndsEqlsEqls'Int'Unds'; frozen source obligations: rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_==Int_» (a b : SortInt) : SortBool := decide (a = b)
/- KORE symbol: Lbl'UndsPlus'Int'Unds'; frozen source obligations: rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_+Int_» : SortInt → SortInt → SortInt := (· + ·)
/- KORE symbol: Lbl'UndsStar'Int'Unds'; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70, rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «_*Int_» : SortInt → SortInt → SortInt := (· * ·)
/- KORE symbol: LblgridAt; frozen source obligations: rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def gridAt : SortIntSeq → SortInt → SortInt → SortInt → SortInt := gridAtModel
/- KORE symbol: LblgridRow; frozen source obligations: rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def gridRow : SortIntSeq → SortInt → SortInt → SortValSeq := gridRowModel
/- KORE symbol: LblgridRows; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70, rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149. Replace this stub with its honest total meaning from the frozen K semantics. -/
def gridRows : SortIntSeq → SortInt → SortValSeq := gridRowsModel
/- KORE symbol: LbloddDone; frozen source obligations: rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def oddDone : SortValSeq → SortValSeq → SortInt → SortInt → SortBool := oddDoneModel
/- KORE symbol: LbloneCol; frozen source obligations: rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def oneCol : SortIntSeq → SortInt → SortInt := oneColModel
/- KORE symbol: LbloneRow; frozen source obligations: rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1. Replace this stub with its honest total meaning from the frozen K semantics. -/
def oneRow : SortIntSeq → SortInt → SortInt := oneRowModel
/- KORE symbol: LblpairDone; frozen source obligations: rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348. Replace this stub with its honest total meaning from the frozen K semantics. -/
noncomputable def pairDone : SortValSeq → SortValSeq → SortInt → SortInt → SortBool := pairDoneModel
/- KORE symbol: LblsnocVS; frozen source obligations: rule-79cc3308597d2aedf94188a46aa45b9302edb4bd5dc309fcd4bc218ec8dc5894, rule-9b8ee50fdbbf692e2fa2c6bc4aa68e73f5759ff24a19c85fc3e0de3519dd9348. Replace this stub with its honest total meaning from the frozen K semantics. -/
def snocVS : SortValSeq → SortVal → SortValSeq := snocModel
/- KORE symbol: LblvalSeqAt'LParUndsCommUndsRParUnds'MPY-SUBSCRIPT'Unds'Val'Unds'ValSeq'Unds'Int; frozen source obligations: rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» : SortValSeq → SortInt → SortVal :=
  valSeqAtModel
/- KORE symbol: LblvalSeqConcat'LParUndsCommUndsRParUnds'MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq; frozen source obligations: rule-79cc3308597d2aedf94188a46aa45b9302edb4bd5dc309fcd4bc218ec8dc5894. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» : SortValSeq → SortValSeq → SortValSeq :=
  valSeqConcatModel
/- KORE symbol: LblvalidPerm; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70, rule-97b792417dedc7de0727ca3c557d6c412015002a77809892b5d5cc700a2fd149, rule-cf5a0acce1b2eb580bfbacadd2e910a549de9a696af1ebfcf37925160d22a22b, rule-6239181de49e2422109895baef3c3011f33d8b5f0ae6785549600addc1a5cfc1, rule-b8a75762e8baeaf13b848647832cf0455607cbda75166ad623cdc8ded53ef987. Replace this stub with its honest total meaning from the frozen K semantics. -/
def validPerm : SortIntSeq → SortInt → SortBool := validPermModel
/- KORE symbol: LblvsLen'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'ValSeq; frozen source obligations: rule-c542bea0ad56e556c87d2f0a1f3b92b8ebc7ede934ee79e3380edd4c8eec4a70. Replace this stub with its honest total meaning from the frozen K semantics. -/
def «vsLen(_)_MPY-CORE_Int_ValSeq» : SortValSeq → SortInt := vsLenModel

theorem final :
    Klean129Minpath.Lemmas.targetStatement _andBool_ «_>=Int_» «_<Int_» «_==Int_» «_+Int_» «_*Int_» gridAt gridRow gridRows oddDone oneCol oneRow pairDone snocVS «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int» «valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» validPerm «vsLen(_)_MPY-CORE_Int_ValSeq» := by
  unfold Klean129Minpath.Lemmas.targetStatement
  constructor
  · intro N P h
    simp [_andBool_, «_>=Int_», validPerm, validPermModel, «_*Int_»] at h
    have hN : 0 ≤ N := Int.le_trans (by decide) h.1
    simp [«vsLen(_)_MPY-CORE_Int_ValSeq», vsLenModel, gridRows, gridRowsModel,
      Int.toNat_of_nonneg hN]
  constructor
  · intro I N P h
    simp [_andBool_, «_>=Int_», «_<Int_», validPerm, validPermModel,
      «_*Int_»] at h
    have hI0 : 0 ≤ I := h.1.2
    have hIN : I < N := h.2
    have hN0 : 0 ≤ N := Int.le_trans (by decide) h.1.1.1
    have hNat : I.toNat < N.toNat := Int.ofNat_lt.mp (by
      simpa [Int.toNat_of_nonneg hI0, Int.toNat_of_nonneg hN0] using hIN)
    change valSeqAtModel (gridRowsModel P N) I =
      SortVal.inj_SortIterable
        (SortIterable.«list(_)_MPY-CORE_Iterable_ValSeq» (gridRowModel P N I))
    simp [gridRowsModel, valSeqAtModel, Int.not_lt_of_ge hI0, hNat,
      Int.toNat_of_nonneg hI0]
  constructor
  · intro J I N P h
    simp [_andBool_, «_>=Int_», «_<Int_», validPerm, validPermModel,
      «_*Int_»] at h
    have hJ0 : 0 ≤ J := h.1.2
    have hJN : J < N := h.2
    have hN0 : 0 ≤ N := Int.le_trans (by decide) h.1.1.1.1.1
    have hNat : J.toNat < N.toNat := Int.ofNat_lt.mp (by
      simpa [Int.toNat_of_nonneg hJ0, Int.toNat_of_nonneg hN0] using hJN)
    simp [gridRow, gridRowModel,
      «valSeqAt(_,_)_MPY-SUBSCRIPT_Val_ValSeq_Int», valSeqAtModel,
      Int.not_lt_of_ge hJ0, hNat, Int.toNat_of_nonneg hJ0, gridAt]
  constructor
  · intro J I N P h
    simp [_andBool_, «_>=Int_», «_<Int_», «_==Int_», validPerm,
      validPermModel, «_*Int_»] at h ⊢
    have hN0 : 0 ≤ N := Int.le_trans (by decide) h.1.1.1.1.1
    have hNpos : 0 < N :=
      Int.lt_of_lt_of_le (by decide : (0 : Int) < 2) h.1.1.1.1.1
    have hI0 : 0 ≤ I := h.1.1.1.2
    have hIN : I < N := h.1.1.2
    have hJ0 : 0 ≤ J := h.1.2
    have hJN : J < N := h.2
    have hM0 : 0 ≤ N * N := h.1.1.1.1.2.1
    have hPerm : (intSeqList P).Perm (expectedValues (N * N)) :=
      h.1.1.1.1.2.2
    have hMpos : 0 < N * N := Int.mul_pos hNpos hNpos
    have hExpectedOne : 1 ∈ expectedValues (N * N) :=
      one_mem_expectedValues hMpos
    have hMemOne : 1 ∈ intSeqList P := hPerm.mem_iff.mpr hExpectedOne
    have hNodup : (intSeqList P).Nodup :=
      hPerm.symm.nodup (expectedValues_nodup (N * N))
    have hIdxOpt : (intSeqList P).idxOf? 1 = some ((intSeqList P).idxOf 1) :=
      int_idxOf?_eq_some_idxOf hMemOne
    have hRow : oneRow P N =
        Int.ofNat ((intSeqList P).idxOf 1 / N.toNat) := by
      unfold oneRow oneRowModel
      rw [if_pos hNpos, hIdxOpt]
    have hCol : oneCol P N =
        Int.ofNat ((intSeqList P).idxOf 1 % N.toNat) := by
      unfold oneCol oneColModel
      rw [if_pos hNpos, hIdxOpt]
    have hFlat0 : 0 ≤ I * N + J := flat_nonneg hI0 hN0 hJ0
    have hFlatLt : I * N + J < N * N := flat_lt_square hN0 hIN hJN
    have hFlatNat : (I * N + J).toNat < (N * N).toNat :=
      Int.ofNat_lt.mp (by
        simpa [Int.toNat_of_nonneg hFlat0, Int.toNat_of_nonneg hM0] using hFlatLt)
    have hLen : (intSeqList P).length = (N * N).toNat := by
      calc
        (intSeqList P).length = (expectedValues (N * N)).length := hPerm.length_eq
        _ = (N * N).toNat := by simp [expectedValues]
    have hBound : (I * N + J).toNat < (intSeqList P).length := by
      rw [hLen]
      exact hFlatNat
    have hGet := List.getElem?_eq_getElem hBound
    have hGrid : gridAt P N I J = (intSeqList P)[(I * N + J).toNat] := by
      unfold gridAt gridAtModel intSeqAtModel
      rw [if_neg (Int.not_lt_of_ge hFlat0), hGet]
      rfl
    have hNnatPos : 0 < N.toNat := Int.ofNat_lt.mp (by
      simpa [Int.toNat_of_nonneg hN0] using hNpos)
    have hJNat : J.toNat < N.toNat := Int.ofNat_lt.mp (by
      simpa [Int.toNat_of_nonneg hJ0, Int.toNat_of_nonneg hN0] using hJN)
    rw [← Bool.decide_and, decide_eq_decide]
    constructor
    · intro hOne
      have hAtOne : (intSeqList P)[(I * N + J).toNat]? = some 1 := by
        rw [hGet]
        exact congrArg some (hGrid.symm.trans hOne)
      have hIdx : (intSeqList P).idxOf 1 = (I * N + J).toNat :=
        int_idxOf_eq_of_get? hNodup hAtOne
      have hDivMod :
          (I * N + J).toNat / N.toNat = I.toNat ∧
          (I * N + J).toNat % N.toNat = J.toNat := by
        apply (Nat.div_mod_unique hNnatPos).2
        constructor
        · rw [flat_toNat hI0 hN0 hJ0]
          simp [Nat.add_comm, Nat.mul_comm]
        · exact hJNat
      constructor
      · rw [hRow]
        calc
          I = Int.ofNat I.toNat := (Int.toNat_of_nonneg hI0).symm
          _ = Int.ofNat ((I * N + J).toNat / N.toNat) :=
            congrArg Int.ofNat hDivMod.1.symm
          _ = Int.ofNat ((intSeqList P).idxOf 1 / N.toNat) := by rw [hIdx]
      · rw [hCol]
        calc
          J = Int.ofNat J.toNat := (Int.toNat_of_nonneg hJ0).symm
          _ = Int.ofNat ((I * N + J).toNat % N.toNat) :=
            congrArg Int.ofNat hDivMod.2.symm
          _ = Int.ofNat ((intSeqList P).idxOf 1 % N.toNat) := by rw [hIdx]
    · rintro ⟨hIRow, hJCol⟩
      rw [hRow] at hIRow
      rw [hCol] at hJCol
      have hINat : I.toNat = (intSeqList P).idxOf 1 / N.toNat := by
        have := congrArg Int.toNat hIRow
        simpa only [Int.toNat_natCast] using this
      have hJNatEq : J.toNat = (intSeqList P).idxOf 1 % N.toNat := by
        have := congrArg Int.toNat hJCol
        simpa only [Int.toNat_natCast] using this
      have hIdxFlat : (intSeqList P).idxOf 1 = (I * N + J).toNat := by
        rw [flat_toNat hI0 hN0 hJ0]
        calc
          (intSeqList P).idxOf 1 =
              N.toNat * ((intSeqList P).idxOf 1 / N.toNat) +
                (intSeqList P).idxOf 1 % N.toNat :=
            (Nat.div_add_mod ((intSeqList P).idxOf 1) N.toNat).symm
          _ = I.toNat * N.toNat + J.toNat := by
            rw [← hINat, ← hJNatEq]
            simp [Nat.mul_comm]
      have hAtIdx := int_get?_idxOf_eq_one hMemOne
      have hAtFlat : (intSeqList P)[(I * N + J).toNat]? = some 1 := by
        rw [← hIdxFlat]
        exact hAtIdx
      rw [hGrid]
      rw [hGet] at hAtFlat
      exact Option.some.inj hAtFlat
  constructor
  · intro N J I P h
    simp [_andBool_, «_>=Int_», «_<Int_», «_+Int_», validPerm,
      validPermModel, «_*Int_»] at h ⊢
    have hN0 : 0 ≤ N := Int.le_trans (by decide) h.1.1.1.1.1
    have hI0 : 0 ≤ I := h.1.1.1.2
    have hIN : I < N := h.1.1.2
    have hJ0 : 0 ≤ J := h.1.2
    have hJN : J < N := h.2
    have hM0 : 0 ≤ N * N := h.1.1.1.1.2.1
    have hPerm : (intSeqList P).Perm (expectedValues (N * N)) :=
      h.1.1.1.1.2.2
    have hFlat0 : 0 ≤ I * N + J := flat_nonneg hI0 hN0 hJ0
    have hFlatLt : I * N + J < N * N := flat_lt_square hN0 hIN hJN
    have hFlatNat : (I * N + J).toNat < (N * N).toNat :=
      Int.ofNat_lt.mp (by
        simpa [Int.toNat_of_nonneg hFlat0, Int.toNat_of_nonneg hM0] using hFlatLt)
    have hLen : (intSeqList P).length = (N * N).toNat := by
      calc
        (intSeqList P).length = (expectedValues (N * N)).length := hPerm.length_eq
        _ = (N * N).toNat := by simp [expectedValues]
    have hBound : (I * N + J).toNat < (intSeqList P).length := by
      rw [hLen]
      exact hFlatNat
    have hGet := List.getElem?_eq_getElem hBound
    have hGrid : gridAt P N I J = (intSeqList P)[(I * N + J).toNat] := by
      unfold gridAt gridAtModel intSeqAtModel
      rw [if_neg (Int.not_lt_of_ge hFlat0), hGet]
      rfl
    have hMem : (intSeqList P)[(I * N + J).toNat] ∈ intSeqList P :=
      List.getElem_mem hBound
    have hExpected : (intSeqList P)[(I * N + J).toNat] ∈ expectedValues (N * N) :=
      hPerm.mem_iff.mp hMem
    have hBounds := expectedValues_mem_bounds hM0 hExpected
    rw [hGrid]
    exact hBounds.2
  constructor
  · intro V A
    simp [«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq»,
      valSeqConcatModel, snocVS, snocModel, valSeqList]
  · intro M R P A h
    simp [«_>=Int_», oddDone, oddDoneModel, pairDone, pairDoneModel,
      snocVS, snocModel, eq_comm] at h ⊢

end Proof
