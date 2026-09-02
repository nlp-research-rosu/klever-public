import Klean157RightAngleTriangle.Inj

axiom «.Map» : Option SortMap

axiom ListItem (x0 : SortKItem) : Option SortList

axiom _Map_ (x0 : SortMap) (x1 : SortMap) : Option SortMap

axiom «.List» : Option SortList

axiom _List_ (x0 : SortList) (x1 : SortList) : Option SortList

axiom «_|->_» (x0 : SortKItem) (x1 : SortKItem) : Option SortMap