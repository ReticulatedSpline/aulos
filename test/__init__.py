import sys, os
testdir = os.path.dirname(__file__)
projdir = os.path.dirname(testdir)
srcdir = os.path.join(projdir, "src")
print(srcdir)
sys.path.insert(0, srcdir)

def _item_list_equal(self, list1, list2) -> bool:
    """run through a list of View.Items and check for equality"""
    while len(list1) > 0 and len(list2) > 0:
        item1 = list1.pop()
        item2 = list2.pop()
        if item1.item_type != item2.item_type:
            return False
        if item1.path != item2.path:
            return False
    return True

def _display_stacks_equal(self, list2, list1) -> bool:
    """compare two lists of View.Displays for equality.
        Useful for unit-testing view state."""
    while len(list1) > 0 and len(list2) > 0:
        display1 = list1.pop()
        display2 = list2.pop()
        if display1.menu_path != display2.menu_path:
            return False
        if display1.index != display2.index:
            return False
        if display1.start_index != display2.start_index:
            return False
        if not self._item_list_equal(display1.items, display2.items):
            return False
    if len(list1) != len(list2):
        return False
    return True