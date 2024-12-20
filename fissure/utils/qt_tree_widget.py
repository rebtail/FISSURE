#!/usr/bin/env python3
"""
Helper functions for QT tree widgets
"""
import collections
from PyQt5 import QtWidgets

def build_subtree(parent: QtWidgets.QTreeWidgetItem, library: list):
    """
    Build a Subtree
    """
    if not library is None:
        for entry in library:
            if isinstance(entry, collections.abc.Mapping):
                k, v = list(entry.items())[0]

                # create new item
                new_item = QtWidgets.QTreeWidgetItem()
                new_item.setText(0,k)
                new_item.setDisabled(True)

                # top level item
                parent.addChild(new_item)

                build_subtree(new_item, v)

            else:
                # create new item
                new_item = QtWidgets.QTreeWidgetItem()
                new_item.setText(0,str(entry))
                new_item.setDisabled(True)

                # top level item
                parent.addChild(new_item)