def empty_list_truth():
    if []:
        return True
    return False


# CPython and the supplied fixed semantics both require this to pass because
# an empty list is falsey. The PAIRS-VERIFICATION-LEMMAS bridge instead stores
# list(intValues(.IntSeq)), which the fixed truthy(list(VS)) equation sees as
# nonempty because it is not syntactically .ValSeq.
assert empty_list_truth() == False
