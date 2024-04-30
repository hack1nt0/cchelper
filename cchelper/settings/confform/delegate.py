from cchelper import *

class ConfDelegate(QStyledItemDelegate):
    def setEditorData(
        self, editor: QWidget, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        raw = index.data(Qt.ItemDataRole.EditRole)
        col = index.model().cols[index.column()]
        match col:
            case 'languages' | 'tags':
                editor.setData(raw)
            # case 'build_debug' | 'submit_code':
            #     editor.setChecked(raw)
            case _:
                super().setEditorData(editor, index)

    def setModelData(
        self,
        editor: QWidget,
        model: QAbstractItemModel,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        col = model.cols[index.column()]
        match col:
            case 'languages' | 'tags':
                model.setData(index, editor.getData())
            case 'build_debug' | 'submit_code':
                model.setData(index, editor.isChecked())
            case _:
                super().setModelData(editor, model, index)
