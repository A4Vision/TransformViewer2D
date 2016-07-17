# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dock.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(154, 217)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttons_layout = QtGui.QVBoxLayout()
        self.buttons_layout.setObjectName(_fromUtf8("buttons_layout"))
        self.rotation = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotation.sizePolicy().hasHeightForWidth())
        self.rotation.setSizePolicy(sizePolicy)
        self.rotation.setMinimumSize(QtCore.QSize(114, 17))
        self.rotation.setObjectName(_fromUtf8("rotation"))
        self.buttons_layout.addWidget(self.rotation)
        self.translation = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translation.sizePolicy().hasHeightForWidth())
        self.translation.setSizePolicy(sizePolicy)
        self.translation.setObjectName(_fromUtf8("translation"))
        self.buttons_layout.addWidget(self.translation)
        self.rigid = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rigid.sizePolicy().hasHeightForWidth())
        self.rigid.setSizePolicy(sizePolicy)
        self.rigid.setObjectName(_fromUtf8("rigid"))
        self.buttons_layout.addWidget(self.rigid)
        self.similarity = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.similarity.sizePolicy().hasHeightForWidth())
        self.similarity.setSizePolicy(sizePolicy)
        self.similarity.setObjectName(_fromUtf8("similarity"))
        self.buttons_layout.addWidget(self.similarity)
        self.affine = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.affine.sizePolicy().hasHeightForWidth())
        self.affine.setSizePolicy(sizePolicy)
        self.affine.setObjectName(_fromUtf8("affine"))
        self.buttons_layout.addWidget(self.affine)
        self.projective = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projective.sizePolicy().hasHeightForWidth())
        self.projective.setSizePolicy(sizePolicy)
        self.projective.setObjectName(_fromUtf8("projective"))
        self.buttons_layout.addWidget(self.projective)
        self.bilinear_interpolant = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        self.bilinear_interpolant.setObjectName(_fromUtf8("bilinear_interpolant"))
        self.buttons_layout.addWidget(self.bilinear_interpolant)
        self.horizontalLayout.addLayout(self.buttons_layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget", None))
        self.rotation.setText(_translate("DockWidget", "Rotation", None))
        self.translation.setText(_translate("DockWidget", "Translation", None))
        self.rigid.setText(_translate("DockWidget", "Rigid", None))
        self.similarity.setText(_translate("DockWidget", "Similarity", None))
        self.affine.setText(_translate("DockWidget", "Affine", None))
        self.projective.setText(_translate("DockWidget", "Projective", None))
        self.bilinear_interpolant.setText(_translate("DockWidget", "Bilinear Interpolant", None))

