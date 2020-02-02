# -*- coding: utf-8 -*-
import sys
import json
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog

# Global Version Variables
VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_PATCH = 0


def parse_version(ver_str):
    version = []
    str_split = ver_str.split(".")
    if len(str_split) != 3:
        raise RuntimeError("Provided version string is malformed: Missing version numbers")
    try:
        for y in str_split.split("."):
            version.append(int(y))
    except ValueError:
        raise RuntimeError("Provided version string is malformed: value is not a valid number")
    return version


def create_qt_text(name, x, y, width, height, parent):
    txtbox = QtWidgets.QPlainTextEdit(parent)
    txtbox.setGeometry(QtCore.QRect(x, y, width, height))
    txtbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    txtbox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    txtbox.setObjectName(name)
    return txtbox


def create_qt_chkbox(name, x, y, width, height, parent):
    chkbox = QtWidgets.QCheckBox(parent)
    chkbox.setGeometry(QtCore.QRect(x, y, width, height))
    chkbox.setObjectName(name)
    return chkbox


def create_qt_label(name, x, y, width, height, parent):
    label = QtWidgets.QLabel(parent)
    label.setGeometry(QtCore.QRect(x, y, width, height))
    label.setObjectName(name)
    return label


def create_qt_group(name, x, y, width, height, parent):
    grp_box = QtWidgets.QGroupBox(parent)
    grp_box.setGeometry(QtCore.QRect(x, y, width, height))
    grp_box.setTitle("")
    grp_box.setObjectName(name)
    return grp_box


class Main(QMainWindow):

    def load_file(self):
        dialog = QFileDialog()
        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
        dialog.setDefaultSuffix('json')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['JSON (*.json)'])
        if dialog.exec_():
            # write out file
            input_file = open(dialog.selectedFiles()[0], "r")
            input_data = input_file.read()
            data = json.loads(input_data)
            for key in self.controls:
                control = self.controls[key]
                if type(control) == QtWidgets.QPlainTextEdit:
                    control.setPlainText(data[key])
                elif type(control) == QtWidgets.QCheckBox:
                    control.setChecked(data[key])

    def save_file(self):
        values = {"version": "{0}.{1}.{2}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)}

        for key in self.controls:
            control = self.controls[key]
            if type(control) == QtWidgets.QPlainTextEdit:
                values[key] = control.toPlainText()
            elif type(control) == QtWidgets.QCheckBox:
                values[key] = control.isChecked()

        dialog = QFileDialog()
        dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
        dialog.setDefaultSuffix('json')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['JSON (*.json)'])
        if dialog.exec_():
            # write out file
            outfile = open(dialog.selectedFiles()[0], "w")
            outfile.write(json.dumps(values, indent=2))
            outfile.close()

    def exitApp(self):
        app.quit()

    def about(self):
        my_dialog = QDialog(self)
        my_dialog.setWindowTitle("About")
        my_dialog.setGeometry(0, 0, 250, 100)
        label = create_qt_label("aboutLabel", 50, 0, 200, 100, my_dialog)
        label.setText("DnD 5e Character sheet editor" + "\n"
                      "folderisland.(com/net)" + "\n"
                      "Version: {0}.{1}.{2}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))
        my_dialog.exec_()  # blocks all other windows until this window is closed.

    def __init__(self):
        QMainWindow.__init__(self)
        self.setObjectName("MainWindow")
        self.resize(771, 902)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # Add all group boxes
        self.grpSave = create_qt_group("grpSave", 100, 210, 225, 147, self.centralwidget)
        self.grpStats = create_qt_group("grpStats", 10, 130, 81, 652, self.centralwidget)
        self.grpFluff = create_qt_group("grpFluff", 580, 130, 181, 341, self.centralwidget)
        self.grpMisc = create_qt_group("grpMisc", 330, 10, 431, 111, self.centralwidget)
        self.grpChar = create_qt_group("grpChar", 10, 10, 311, 111, self.centralwidget)
        self.grpBonuses = create_qt_group("grpBonuses", 100, 130, 225, 77, self.centralwidget)
        self.grpSkills = create_qt_group("grpSkills", 100, 360, 225, 422, self.centralwidget)
        self.grpEquip = create_qt_group("grpEquip", 330, 630, 241, 231, self.centralwidget)
        self.grpAtk = create_qt_group("grpAtk", 330, 405, 241, 219, self.centralwidget)
        self.grpProf = create_qt_group("grpProf", 580, 680, 181, 181, self.centralwidget)
        self.grpPsvWis = create_qt_group("grpPsvWis", 10, 790, 311, 71, self.centralwidget)
        self.grpFeats = create_qt_group("grpFeats", 580, 480, 181, 191, self.centralwidget)
        self.grpCmbtStats = create_qt_group("grpCmbtStats", 330, 130, 241, 271, self.centralwidget)
        self.grpLifeSave = create_qt_group("grpLifeSave", 110, 200, 121, 51, self.grpCmbtStats)
        self.grpDice = create_qt_group("grpDice", 7, 190, 91, 71, self.grpCmbtStats)
        self.txtTempHp = create_qt_text("txtTempHp", 86, 150, 131, 31, self.grpCmbtStats)
        self.txtMaxHp = create_qt_text("txtMaxHp", 86, 70, 131, 31, self.grpCmbtStats)
        self.label_21 = create_qt_label("label_21", 30, 120, 51, 20, self.grpCmbtStats)
        self.label_20 = create_qt_label("label_20", 10, 80, 71, 16, self.grpCmbtStats)
        self.txtHp = create_qt_text("txtHp", 86, 110, 131, 31, self.grpCmbtStats)
        self.label_22 = create_qt_label("label_22", 10, 160, 71, 16, self.grpCmbtStats)
        self.label_13 = create_qt_label("label_13", 46, 40, 61, 16, self.grpCmbtStats)
        self.txtInit = create_qt_text("txtInit", 117, 10, 31, 31, self.grpCmbtStats)
        self.txtSpeed = create_qt_text("txtSpeed", 169, 10, 31, 31, self.grpCmbtStats)
        self.label_15 = create_qt_label("label_15", 170, 40, 41, 16, self.grpCmbtStats)
        self.label_14 = create_qt_label("label_14", 113, 40, 41, 16, self.grpCmbtStats)
        self.txtArmor = create_qt_text("txtArmor", 62, 10, 31, 31, self.grpCmbtStats)
        self.chkDthSave1 = create_qt_chkbox("chkDthSave1", 55, 6, 16, 17, self.grpLifeSave)
        self.chkDthSave2 = create_qt_chkbox("chkDthSave2", 75, 6, 16, 17, self.grpLifeSave)
        self.chkDthSave3 = create_qt_chkbox("chkDthSave3", 95, 6, 16, 17, self.grpLifeSave)
        self.chkDthFail2 = create_qt_chkbox("chkDthFail2", 75, 26, 16, 17, self.grpLifeSave)
        self.chkDthFail3 = create_qt_chkbox("chkDthFail3", 95, 26, 16, 17, self.grpLifeSave)
        self.chkDthFail1 = create_qt_chkbox("chkDthFail1", 55, 26, 16, 17, self.grpLifeSave)
        self.label_27 = create_qt_label("label_27", 5, 6, 47, 13, self.grpLifeSave)
        self.label_26 = create_qt_label("label_26", 5, 26, 47, 13, self.grpLifeSave)
        self.label_28 = create_qt_label("label_28", 23, 49, 47, 17, self.grpDice)
        self.txtHitDie = create_qt_text("txtHitDie", 10, 29, 71, 20, self.grpDice)
        self.label_29 = create_qt_label("label_29", 2, 7, 31, 20, self.grpDice)
        self.txtTotalHitDie = create_qt_text("txtTotalHitDie", 30, 6, 51, 20, self.grpDice)
        self.txtStatStr = create_qt_text("txtStatStr", 25, 77, 31, 31, self.grpStats)
        self.txtScoreStr = create_qt_text("txtScoreStr", 15, 27, 51, 51, self.grpStats)
        self.label_7 = create_qt_label("label_7", 19, 12, 51, 16, self.grpStats)
        self.txtScoreDex = create_qt_text("txtScoreDex", 16, 131, 51, 51, self.grpStats)
        self.txtStatDex = create_qt_text("txtStatDex", 26, 181, 31, 31, self.grpStats)
        self.label_8 = create_qt_label("label_8", 20, 116, 51, 16, self.grpStats)
        self.label_9 = create_qt_label("label_9", 10, 224, 61, 19, self.grpStats)
        self.txtStatCon = create_qt_text("txtStatCon", 26, 289, 31, 31, self.grpStats)
        self.txtScoreCon = create_qt_text("txtScoreCon", 16, 239, 51, 51, self.grpStats)
        self.txtScoreInt = create_qt_text("txtScoreInt", 16, 343, 51, 51, self.grpStats)
        self.txtStatInt = create_qt_text("txtStatInt", 26, 393, 31, 31, self.grpStats)
        self.label_10 = create_qt_label("label_10", 10, 328, 61, 19, self.grpStats)
        self.txtScoreWis = create_qt_text("txtScoreWis", 16, 448, 51, 51, self.grpStats)
        self.txtStatWis = create_qt_text("txtStatWis", 26, 498, 31, 31, self.grpStats)
        self.label_11 = create_qt_label("label_11", 20, 433, 51, 16, self.grpStats)
        self.txtScoreChar = create_qt_text("txtScoreChar", 16, 552, 51, 51, self.grpStats)
        self.txtStatChar = create_qt_text("txtStatChar", 26, 602, 31, 31, self.grpStats)
        self.label_62 = create_qt_label("label_62", 20, 537, 51, 16, self.grpStats)
        self.label_19 = create_qt_label("label_19", 70, 303, 47, 16, self.grpFluff)
        self.txtBonds = create_qt_text("txtBonds", 10, 166, 161, 55, self.grpFluff)
        self.label_18 = create_qt_label("label_18", 70, 226, 47, 16, self.grpFluff)
        self.txtIdeals = create_qt_text("txtIdeals", 10, 86, 161, 55, self.grpFluff)
        self.label_16 = create_qt_label("label_16", 60, 66, 61, 10, self.grpFluff)
        self.label_17 = create_qt_label("label_17", 70, 146, 47, 10, self.grpFluff)
        self.txtFlaws = create_qt_text("txtFlaws", 10, 246, 161, 55, self.grpFluff)
        self.txtPersonality = create_qt_text("txtPersonality", 10, 6, 161, 55, self.grpFluff)
        self.txtExp = create_qt_text("txtExp", 290, 60, 131, 31, self.grpMisc)
        self.label_23 = create_qt_label("label_23", 10, 90, 81, 16, self.grpMisc)
        self.label_2 = create_qt_label("label_2", 10, 40, 81, 16, self.grpMisc)
        self.label_24 = create_qt_label("label_24", 150, 90, 81, 16, self.grpMisc)
        self.txtAlign = create_qt_text("txtAlign", 150, 60, 131, 31, self.grpMisc)
        self.label_25 = create_qt_label("label_25", 290, 90, 101, 16, self.grpMisc)
        self.txtBackground = create_qt_text("txtBackground", 150, 10, 131, 31, self.grpMisc)
        self.label_3 = create_qt_label("label_3", 150, 40, 81, 16, self.grpMisc)
        self.label_4 = create_qt_label("label_4", 290, 40, 81, 16, self.grpMisc)
        self.txtClass = create_qt_text("txtClass", 10, 10, 131, 31, self.grpMisc)
        self.txtPlayer = create_qt_text("txtPlayer", 290, 10, 131, 31, self.grpMisc)
        self.txtRace = create_qt_text("txtRace", 10, 60, 131, 31, self.grpMisc)
        self.label_12 = create_qt_label("label_12", 50, 50, 91, 16, self.grpBonuses)
        self.txtInsperation = create_qt_text("txtInsperation", 10, 5, 31, 31, self.grpBonuses)
        self.label_5 = create_qt_label("label_5", 50, 15, 61, 16, self.grpBonuses)
        self.txtProfBonus = create_qt_text("txtProfBonus", 10, 40, 31, 31, self.grpBonuses)
        self.label = create_qt_label("label", 110, 70, 81, 16, self.grpChar)
        self.txtCharName = create_qt_text("txtCharName", 40, 20, 231, 41, self.grpChar)
        self.label_30 = create_qt_label("label_30", 147, 5, 58, 20, self.grpSave)
        self.label_33 = create_qt_label("label_33", 147, 74, 58, 20, self.grpSave)
        self.label_32 = create_qt_label("label_32", 147, 51, 58, 20, self.grpSave)
        self.label_34 = create_qt_label("label_34", 147, 97, 58, 20, self.grpSave)
        self.txtSaveChar = create_qt_text("txtSaveChar", 25, 120, 116, 20, self.grpSave)
        self.chkSaveInt = create_qt_chkbox("chkSaveInt", 6, 77, 13, 13, self.grpSave)
        self.chkSaveDex = create_qt_chkbox("chkSaveDex", 6, 31, 13, 13, self.grpSave)
        self.chkSaveChar = create_qt_chkbox("chkSaveChar", 6, 123, 13, 13, self.grpSave)
        self.txtSaveInt = create_qt_text("txtSaveInt", 25, 74, 116, 20, self.grpSave)
        self.txtSaveStr = create_qt_text("txtSaveStr", 25, 5, 116, 20, self.grpSave)
        self.chkSaveWis = create_qt_chkbox("chkSaveWis", 6, 100, 13, 13, self.grpSave)
        self.chkSaveCon = create_qt_chkbox("chkSaveCon", 6, 54, 13, 13, self.grpSave)
        self.txtSaveCon = create_qt_text("txtSaveCon", 25, 51, 116, 20, self.grpSave)
        self.txtSaveDex = create_qt_text("txtSaveDex", 25, 28, 116, 20, self.grpSave)
        self.label_31 = create_qt_label("label_31", 147, 28, 58, 20, self.grpSave)
        self.label_35 = create_qt_label("label_35", 147, 120, 58, 19, self.grpSave)
        self.txtSaveWis = create_qt_text("txtSaveWis", 25, 97, 116, 20, self.grpSave)
        self.chkSaveStr = create_qt_chkbox("chkSaveStr", 6, 8, 13, 13, self.grpSave)
        self.chkSkillAcro = create_qt_chkbox("chkSkillAcro", 4, 10, 13, 13, self.grpSkills)
        self.txtSkillDec = create_qt_text("txtSkillDec", 23, 99, 116, 20, self.grpSkills)
        self.label_37 = create_qt_label("label_37", 145, 53, 58, 20, self.grpSkills)
        self.txtSkillAcro = create_qt_text("txtSkillAcro", 23, 7, 116, 20, self.grpSkills)
        self.chkSkillAnim = create_qt_chkbox("chkSkillAnim", 4, 33, 13, 13, self.grpSkills)
        self.txtSkillArc = create_qt_text("txtSkillArc", 23, 53, 116, 20, self.grpSkills)
        self.chkSkillArc = create_qt_chkbox("chkSkillArc", 4, 56, 13, 13, self.grpSkills)
        self.label_41 = create_qt_label("label_41", 145, 122, 58, 19, self.grpSkills)
        self.chkSkillAth = create_qt_chkbox("chkSkillAth", 4, 79, 13, 13, self.grpSkills)
        self.chkSkillHist = create_qt_chkbox("chkSkillHist", 4, 125, 13, 13, self.grpSkills)
        self.label_40 = create_qt_label("label_40", 145, 30, 81, 20, self.grpSkills)
        self.txtSkillAth = create_qt_text("txtSkillAth", 23, 76, 116, 20, self.grpSkills)
        self.chkSkillDec = create_qt_chkbox("chkSkillDec", 4, 102, 13, 13, self.grpSkills)
        self.label_36 = create_qt_label("label_36", 145, 76, 58, 20, self.grpSkills)
        self.txtSkillHist = create_qt_text("txtSkillHist", 23, 122, 116, 20, self.grpSkills)
        self.label_38 = create_qt_label("label_38", 145, 99, 58, 20, self.grpSkills)
        self.label_39 = create_qt_label("label_39", 145, 7, 58, 20, self.grpSkills)
        self.txtSkillAnim = create_qt_text("txtSkillAnim", 23, 30, 116, 20, self.grpSkills)
        self.chkSkillIns = create_qt_chkbox("chkSkillIns", 4, 148, 13, 13, self.grpSkills)
        self.txtSkillInv = create_qt_text("txtSkillInv", 23, 191, 116, 20, self.grpSkills)
        self.label_44 = create_qt_label("label_44", 145, 237, 58, 20, self.grpSkills)
        self.label_43 = create_qt_label("label_43", 145, 191, 71, 20, self.grpSkills)
        self.txtSkillNat = create_qt_text("txtSkillNat", 23, 237, 116, 20, self.grpSkills)
        self.chkSkillMed = create_qt_chkbox("chkSkillMed", 4, 217, 13, 13, self.grpSkills)
        self.label_42 = create_qt_label("label_42", 145, 214, 58, 20, self.grpSkills)
        self.txtSkillPerc = create_qt_text("txtSkillPerc", 23, 260, 116, 20, self.grpSkills)
        self.chkSkillInti = create_qt_chkbox("chkSkillInti", 4, 171, 13, 13, self.grpSkills)
        self.chkSkillNat = create_qt_chkbox("chkSkillNat", 4, 240, 13, 13, self.grpSkills)
        self.chkSkillPerc = create_qt_chkbox("chkSkillPerc", 4, 263, 13, 13, self.grpSkills)
        self.label_45 = create_qt_label("label_45", 145, 145, 58, 20, self.grpSkills)
        self.label_46 = create_qt_label("label_46", 145, 168, 58, 20, self.grpSkills)
        self.txtSkillInt = create_qt_text("txtSkillInt", 23, 168, 116, 20, self.grpSkills)
        self.label_47 = create_qt_label("label_47", 145, 260, 58, 19, self.grpSkills)
        self.txtSkillMed = create_qt_text("txtSkillMed", 23, 214, 116, 20, self.grpSkills)
        self.chkSkillInv = create_qt_chkbox("chkSkillInv", 4, 194, 13, 13, self.grpSkills)
        self.txtSkillIns = create_qt_text("txtSkillIns", 23, 145, 116, 20, self.grpSkills)
        self.txtSkillPerf = create_qt_text("txtSkillPerf", 23, 283, 116, 20, self.grpSkills)
        self.label_51 = create_qt_label("label_51", 145, 283, 58, 20, self.grpSkills)
        self.txtSkillStealth = create_qt_text("txtSkillStealth", 23, 375, 116, 20, self.grpSkills)
        self.chkSkillRel = create_qt_chkbox("chkSkillRel", 4, 332, 13, 13, self.grpSkills)
        self.label_52 = create_qt_label("label_52", 145, 306, 58, 20, self.grpSkills)
        self.txtSkillSoh = create_qt_text("txtSkillSoh", 23, 352, 116, 20, self.grpSkills)
        self.chkSkillSte = create_qt_chkbox("chkSkillSte", 4, 378, 13, 13, self.grpSkills)
        self.label_48 = create_qt_label("label_48", 145, 375, 58, 20, self.grpSkills)
        self.chkSkillSurv = create_qt_chkbox("chkSkillSurv", 4, 401, 13, 13, self.grpSkills)
        self.chkSkillPers = create_qt_chkbox("chkSkillPers", 4, 309, 13, 13, self.grpSkills)
        self.label_49 = create_qt_label("label_49", 145, 329, 71, 20, self.grpSkills)
        self.txtSkillSurv = create_qt_text("txtSkillSurv", 23, 398, 116, 20, self.grpSkills)
        self.chkSkillSoh = create_qt_chkbox("chkSkillSoh", 4, 355, 13, 13, self.grpSkills)
        self.txtSkillRel = create_qt_text("txtSkillRel", 23, 329, 116, 20, self.grpSkills)
        self.label_53 = create_qt_label("label_53", 145, 398, 58, 19, self.grpSkills)
        self.chkSkillPerf = create_qt_chkbox("chkSkillPerf", 4, 286, 13, 13, self.grpSkills)
        self.txtSkillPers = create_qt_text("txtSkillPers", 23, 306, 116, 20, self.grpSkills)
        self.label_50 = create_qt_label("label_50", 145, 352, 81, 20, self.grpSkills)
        self.label_55 = create_qt_label("label_55", 50, 170, 91, 16, self.grpFeats)
        self.txtFeatsTraits = create_qt_text("txtFeatsTraits", 10, 10, 161, 161, self.grpFeats)
        self.txtPasWis = create_qt_text("txtPasWis", 10, 10, 51, 51, self.grpPsvWis)
        self.label_54 = create_qt_label("label_54", 100, 30, 171, 16, self.grpPsvWis)
        self.label_56 = create_qt_label("label_56", 14, 160, 151, 16, self.grpProf)
        self.txtProfLang = create_qt_text("txtProfLang", 10, 10, 161, 151, self.grpProf)
        self.label_57 = create_qt_label("label_57", 114, 210, 61, 16, self.grpEquip)
        self.txtEquipment = create_qt_text("txtEquipment", 60, 10, 171, 201, self.grpEquip)
        self.txtCurCP = create_qt_text("txtCurCP", 10, 20, 41, 21, self.grpEquip)
        self.txtCurSP = create_qt_text("txtCurSP", 10, 60, 41, 21, self.grpEquip)
        self.txtCurEP = create_qt_text("txtCurEP", 10, 100, 41, 21, self.grpEquip)
        self.txtCurGP = create_qt_text("txtCurGP", 10, 140, 41, 21, self.grpEquip)
        self.txtCurPP = create_qt_text("txtCurPP", 10, 180, 41, 21, self.grpEquip)
        self.label_62 = create_qt_label("label_62", 24, 40, 16, 16, self.grpEquip)
        self.label_63 = create_qt_label("label_63", 24, 80, 16, 16, self.grpEquip)
        self.label_64 = create_qt_label("label_64", 24, 120, 16, 16, self.grpEquip)
        self.label_65 = create_qt_label("label_65", 24, 160, 16, 16, self.grpEquip)
        self.label_66 = create_qt_label("label_66", 24, 200, 16, 16, self.grpEquip)
        self.label_58 = create_qt_label("label_58", 60, 200, 131, 16, self.grpAtk)
        self.txtAtkType1 = create_qt_text("txtAtkType1", 143, 20, 91, 21, self.grpAtk)
        self.txtAtkType2 = create_qt_text("txtAtkType2", 143, 44, 91, 21, self.grpAtk)
        self.txtAtkType3 = create_qt_text("txtAtkType3", 143, 68, 91, 21, self.grpAtk)
        self.txtAtkBonus3 = create_qt_text("txtAtkBonus3", 103, 68, 38, 21, self.grpAtk)
        self.txtAtkBonus2 = create_qt_text("txtAtkBonus2", 103, 44, 38, 21, self.grpAtk)
        self.txtAtkBonus1 = create_qt_text("txtAtkBonus1", 103, 20, 38, 21, self.grpAtk)
        self.txtAtkName2 = create_qt_text("txtAtkName2", 10, 44, 91, 21, self.grpAtk)
        self.txtAtkName1 = create_qt_text("txtAtkName1", 10, 20, 91, 21, self.grpAtk)
        self.txtAtkName3 = create_qt_text("txtAtkName3", 10, 68, 91, 21, self.grpAtk)
        self.txtAtksSpells = create_qt_text("txtAtksSpells", 10, 90, 224, 111, self.grpAtk)
        self.label_59 = create_qt_label("label_59", 11, 6, 47, 12, self.grpAtk)
        self.label_60 = create_qt_label("label_60", 103, 3, 31, 16, self.grpAtk)
        self.label_61 = create_qt_label("label_61", 145, 5, 71, 12, self.grpAtk)
        # Set Up Menu
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(self)
        self.actionLoad.triggered.connect(self.load_file)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.triggered.connect(self.exitApp)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.triggered.connect(self.about)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.controls = {"TempHp": self.txtTempHp, "MaxHp": self.txtMaxHp, "Hp": self.txtHp, "Init": self.txtInit,
                         "Speed": self.txtSpeed, "Armor": self.txtArmor, "DthSave1": self.chkDthSave1,
                         "DthSave3": self.chkDthSave3, "DthFail2": self.chkDthFail2, "DthFail3": self.chkDthFail3,
                         "HitDie": self.txtHitDie, "TotalHitDie": self.txtTotalHitDie, "StatStr": self.txtStatStr,
                         "ScoreDex": self.txtScoreDex, "StatDex": self.txtStatDex, "StatCon": self.txtStatCon,
                         "ScoreInt": self.txtScoreInt, "StatInt": self.txtStatInt, "ScoreWis": self.txtScoreWis,
                         "ScoreChar": self.txtScoreChar, "StatChar": self.txtStatChar, "Bonds": self.txtBonds,
                         "Flaws": self.txtFlaws, "Personality": self.txtPersonality, "ProfBonus": self.txtProfBonus,
                         "Background": self.txtBackground, "Class": self.txtClass, "Player": self.txtPlayer,
                         "Race": self.txtRace, "SkillAcroProf": self.chkSkillAcro, "ScoreStr": self.txtScoreStr,
                         "CharName": self.txtCharName, "SaveChar": self.txtSaveChar, "SkillHistProf": self.chkSkillHist,
                         "SaveDexProf": self.chkSaveDex, "Insperation": self.txtInsperation, "Electrum": self.txtCurEP,
                         "SaveCharProf": self.chkSaveChar, "SaveInt": self.txtSaveInt, "SaveIntProf": self.chkSaveInt,
                         "SaveStr": self.txtSaveStr, "SaveWisProf": self.chkSaveWis, "SaveConProf": self.chkSaveCon,
                         "SaveDex": self.txtSaveDex, "SaveWis": self.txtSaveWis, "SaveStrProf": self.chkSaveStr,
                         "SkillDec": self.txtSkillDec, "SkillAcro": self.txtSkillAcro, "SkillAth": self.txtSkillAth,
                         "SkillAnimProf": self.chkSkillAnim, "SkillArc": self.txtSkillArc, "ScoreCon": self.txtScoreCon,
                         "SkillArcProf": self.chkSkillArc, "SkillAthProf": self.chkSkillAth, "Platinum": self.txtCurPP,
                         "SkillDecProf": self.chkSkillDec, "SkillHist": self.txtSkillHist, "DthSave2": self.chkDthSave2,
                         "SkillAnim": self.txtSkillAnim, "SkillInsProf": self.chkSkillIns, "DthFail1": self.chkDthFail1,
                         "SkillInv": self.txtSkillInv, "SkillNat": self.txtSkillNat, "SkillMedProf": self.chkSkillMed,
                         "SkillPerc": self.txtSkillPerc, "SkillPercProf": self.chkSkillPerc, "StatWis": self.txtStatWis,
                         "SkillInti": self.chkSkillInti, "SkillNatProf": self.chkSkillNat, "Ideals": self.txtIdeals,
                         "SkillInt": self.txtSkillInt, "SkillMed": self.txtSkillMed, "SkillInvProf": self.chkSkillInv,
                         "SkillIns": self.txtSkillIns, "SkillPerf": self.txtSkillPerf, "Align": self.txtAlign,
                         "SkillStealth": self.txtSkillStealth, "FeatsTraits": self.txtFeatsTraits, "Exp": self.txtExp,
                         "SkillRelProf": self.chkSkillRel, "SkillSoh": self.txtSkillSoh, "SkillSte": self.chkSkillSte,
                         "SkillSurvProf": self.chkSkillSurv, "SkillPersProf": self.chkSkillPers, "Gold": self.txtCurGP,
                         "SkillSurv": self.txtSkillSurv, "SkillSohProf": self.chkSkillSoh, "SkillRel": self.txtSkillRel,
                         "SkillPerfProf": self.chkSkillPerf, "SkillPers": self.txtSkillPers, "SaveCon": self.txtSaveCon,
                         "PasWis": self.txtPasWis, "ProfLang": self.txtProfLang, "Equipment": self.txtEquipment,
                         "AtkType1": self.txtAtkType1, "AtkType2": self.txtAtkType2, "AtkType3": self.txtAtkType3,
                         "AtkBonus3": self.txtAtkBonus3, "AtkBonus2": self.txtAtkBonus2, "AtkBonus1": self.txtAtkBonus1,
                         "AtkName2": self.txtAtkName2, "AtkName1": self.txtAtkName1, "AtkName3": self.txtAtkName3,
                         "AtksSpells": self.txtAtksSpells, "Copper": self.txtCurCP, "Silver": self.txtCurSP,
                          }

        self.retranslate_ui(self)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "DnD 5e Character Sheet"))
        self.label_21.setText(_translate("MainWindow", "Hit Points"))
        self.label_20.setText(_translate("MainWindow", "Max Hit Points"))
        self.label_22.setText(_translate("MainWindow", "Temporary HP"))
        self.label_13.setText(_translate("MainWindow", "Armor Class"))
        self.label_15.setText(_translate("MainWindow", "Speed"))
        self.label_14.setText(_translate("MainWindow", "Initiative"))
        self.label_27.setText(_translate("MainWindow", "Succeses"))
        self.label_26.setText(_translate("MainWindow", "Failures"))
        self.label_28.setText(_translate("MainWindow", "Hit Dice"))
        self.label_29.setText(_translate("MainWindow", "Total"))
        self.label_7.setText(_translate("MainWindow", "Strength"))
        self.label_8.setText(_translate("MainWindow", "Dexterity"))
        self.label_9.setText(_translate("MainWindow", "Constitution"))
        self.label_10.setText(_translate("MainWindow", "Intelligence"))
        self.label_11.setText(_translate("MainWindow", "Wisdom"))
        self.label_62.setText(_translate("MainWindow", "Charisma"))
        self.label_19.setText(_translate("MainWindow", "Flaws"))
        self.label_18.setText(_translate("MainWindow", "Bonds"))
        self.label_16.setText(_translate("MainWindow", "Personality"))
        self.label_17.setText(_translate("MainWindow", "Ideals"))
        self.label_23.setText(_translate("MainWindow", "Race"))
        self.label_2.setText(_translate("MainWindow", "Class & Level"))
        self.label_24.setText(_translate("MainWindow", "Alignment"))
        self.label_25.setText(_translate("MainWindow", "Experience Points"))
        self.label_3.setText(_translate("MainWindow", "Background"))
        self.label_4.setText(_translate("MainWindow", "Player Name"))
        self.label_12.setText(_translate("MainWindow", "Proficiency Bonus"))
        self.label_5.setText(_translate("MainWindow", "Insperation"))
        self.label.setText(_translate("MainWindow", "Character Name"))
        self.label_30.setText(_translate("MainWindow", "Strength"))
        self.label_33.setText(_translate("MainWindow", "Intelligence"))
        self.label_32.setText(_translate("MainWindow", "Constitution"))
        self.label_34.setText(_translate("MainWindow", "Wisdom"))
        self.label_31.setText(_translate("MainWindow", "Dexterity"))
        self.label_35.setText(_translate("MainWindow", "Charisma"))
        self.label_37.setText(_translate("MainWindow", "Arcana"))
        self.label_41.setText(_translate("MainWindow", "History"))
        self.label_40.setText(_translate("MainWindow", "Animal Handling"))
        self.label_36.setText(_translate("MainWindow", "Athletics"))
        self.label_38.setText(_translate("MainWindow", "Deception"))
        self.label_39.setText(_translate("MainWindow", "Acrobatics"))
        self.label_44.setText(_translate("MainWindow", "Nature"))
        self.label_43.setText(_translate("MainWindow", "Investigation"))
        self.label_42.setText(_translate("MainWindow", "Medicine"))
        self.label_45.setText(_translate("MainWindow", "Insight"))
        self.label_46.setText(_translate("MainWindow", "Intimidation"))
        self.label_47.setText(_translate("MainWindow", "Perception"))
        self.label_51.setText(_translate("MainWindow", "Performance"))
        self.label_52.setText(_translate("MainWindow", "Persuasion"))
        self.label_48.setText(_translate("MainWindow", "Stealth"))
        self.label_49.setText(_translate("MainWindow", "Religion"))
        self.label_53.setText(_translate("MainWindow", "Survival"))
        self.label_50.setText(_translate("MainWindow", "Sleight of Hand"))
        self.label_55.setText(_translate("MainWindow", "Features & Traits"))
        self.label_54.setText(_translate("MainWindow", "Passive Wisdom (Perception)"))
        self.label_56.setText(_translate("MainWindow", "Proficiencies & Languages"))
        self.label_57.setText(_translate("MainWindow", "Equipment"))
        self.label_58.setText(_translate("MainWindow", "Attacks & Spellcasting"))
        self.label_59.setText(_translate("MainWindow", "Name"))
        self.label_60.setText(_translate("MainWindow", "Bonus"))
        self.label_61.setText(_translate("MainWindow", "Damage Type"))
        self.label_62.setText(_translate("MainWindow", "CP"))
        self.label_63.setText(_translate("MainWindow", "SP"))
        self.label_64.setText(_translate("MainWindow", "EP"))
        self.label_65.setText(_translate("MainWindow", "GP"))
        self.label_66.setText(_translate("MainWindow", "PP"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec_())
