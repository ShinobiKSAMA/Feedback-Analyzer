from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3

i=-1
conn = sqlite3.connect('FeedB.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS FeedTable
	(
		username varchar(15),
		Faculty varchar(15),
		Feed TEXT,
		Review varchar(15),
		PRIMARY KEY(username, Faculty)
	)""")
cur.close()
conn.commit()
conn.close()

class Ui_MainWindow(object):
	def storeFeedback(self, user, text, fac):
		from rnn import fbsrnn
		conn = sqlite3.connect('FeedB.db')
		cur = conn.cursor()
		try:
			cur.execute('''insert into FeedTable Values("%s","%s","%s","%s")'''%(user, str(fac), text, fbsrnn(text)))
			self.status.setText('Feedback is Submitted')
		except:
			self.status.setText('You Have Already Given Feedback to The Faculty')
		finally:
			cur.close()
			conn.commit()
			conn.close()
			print(fbsrnn(text))

	def nextDB(self, fac):
		global i
		conn = sqlite3.connect('FeedB.db')
		cur = conn.cursor()
		cur.execute('''select username, Feed, Review from FeedTable where Faculty = "%s"'''%(str(fac)))
		res = cur.fetchall()
		if i < len(res)-1:
			i += 1
			self.feedgiver.setText(res[i][0])
			self.FeedText.setText(res[i][1])
			self.reviewans.setText(res[i][2])
		cur.close()
		conn.close()

	def prevDB(self, fac):
		global i
		conn = sqlite3.connect('FeedB.db')
		cur = conn.cursor()
		cur.execute('''select username, Feed, Review from FeedTable where Faculty = "%s"'''%(str(fac)))
		res = cur.fetchall()
		if i > 0:
			i -= 1
			self.feedgiver.setText(res[i][0])
			self.FeedText.setText(res[i][1])
			self.reviewans.setText(res[i][2])
		cur.close()
		conn.close()

	def delDB(self, fac, usr):
		conn = sqlite3.connect('FeedB.db')
		cur = conn.cursor()
		cur.execute('''delete from FeedTable where Faculty = "%s" and username = "%s"'''%(str(fac), usr))
		cur.close()
		conn.commit()
		conn.close()
		self.prevDB(str(fac))

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(491, 265)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
		self.tabWidget.setGeometry(QtCore.QRect(0, 0, 491, 261))
		self.tabWidget.setObjectName("tabWidget")
		self.Homepage = QtWidgets.QWidget()
		self.Homepage.setObjectName("Homepage")
		self.textBrowser = QtWidgets.QTextBrowser(self.Homepage)
		self.textBrowser.setGeometry(QtCore.QRect(10, 60, 450, 120))
		self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.textBrowser.setObjectName("textBrowser")
		self.tabWidget.addTab(self.Homepage, "")
		
		self.Feedback = QtWidgets.QWidget()
		self.Feedback.setObjectName("Feedback")
		self.Userid = QtWidgets.QLineEdit(self.Feedback)
		self.Userid.setGeometry(QtCore.QRect(10, 40, 131, 20))
		self.Userid.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.Userid.setInputMask("")
		self.Userid.setObjectName("Userid")
		self.textEdit = QtWidgets.QTextEdit(self.Feedback)
		self.textEdit.setGeometry(QtCore.QRect(160, 10, 311, 201))
		self.textEdit.setObjectName("textEdit")
		self.status = QtWidgets.QLabel(self.Feedback)
		self.status.setGeometry(QtCore.QRect(170,210,320,20))
		self.status.setObjectName("Status")
		self.label_4 = QtWidgets.QLabel(self.Feedback)
		self.label_4.setGeometry(QtCore.QRect(10, 20, 64, 13))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setObjectName("label_4")
		self.Faculty = QtWidgets.QComboBox(self.Feedback)
		self.Faculty.setGeometry(QtCore.QRect(10, 100, 131, 22))
		self.Faculty.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
		self.Faculty.setObjectName("Faculty")
		self.Faculty.addItem("")
		self.Faculty.addItem("")
		self.Faculty.addItem("")
		self.Faculty.addItem("")
		self.FeedB = QtWidgets.QPushButton(self.Feedback)
		self.FeedB.setGeometry(QtCore.QRect(10, 180, 131, 23))
		self.FeedB.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.FeedB.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
		self.FeedB.setDefault(False)
		self.FeedB.setFlat(False)
		self.FeedB.setObjectName("FeedB")
		self.FeedB.clicked.connect(lambda: self.storeFeedback(self.Userid.text(), self.textEdit.toPlainText(), self.Faculty.currentText()))
		self.label_5 = QtWidgets.QLabel(self.Feedback)
		self.label_5.setGeometry(QtCore.QRect(10, 80, 91, 16))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.label_5.setFont(font)
		self.label_5.setObjectName("label_5")
		self.tabWidget.addTab(self.Feedback, "")
		
		self.Table = QtWidgets.QWidget()
		self.Table.setObjectName("Table")
		self.FacultyDB = QtWidgets.QComboBox(self.Table)
		self.FacultyDB.setGeometry(QtCore.QRect(10, 70, 131, 22))
		self.FacultyDB.setStyleSheet("background-color: rgb(51, 51, 51);\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);")
		self.FacultyDB.setObjectName("FacultyDB")
		self.FacultyDB.addItem("")
		self.FacultyDB.addItem("")
		self.FacultyDB.addItem("")
		self.FacultyDB.addItem("")
		self.review = QtWidgets.QLabel(self.Table)
		self.review.setGeometry(QtCore.QRect(10, 110, 161, 22))
		self.review.setObjectName("Review")
		self.reviewans = QtWidgets.QLabel(self.Table)
		self.reviewans.setGeometry(QtCore.QRect(70, 110, 131, 22))
		self.reviewans.setObjectName("Reviewans")
		self.label_7 = QtWidgets.QLabel(self.Table)
		self.label_7.setGeometry(QtCore.QRect(10, 50, 91, 16))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.label_7.setFont(font)
		self.label_7.setObjectName("label_7")
		self.label_8 = QtWidgets.QLabel(self.Table)
		self.label_8.setGeometry(QtCore.QRect(160, 10, 101, 21))
		self.label_8.setObjectName("label_8")
		self.feedgiver = QtWidgets.QLabel(self.Table)
		self.feedgiver.setGeometry(QtCore.QRect(280, 10, 171, 16))
		self.feedgiver.setObjectName("feedgiver")
		self.FeedText = QtWidgets.QTextBrowser(self.Table)
		self.FeedText.setGeometry(QtCore.QRect(160, 40, 311, 151))
		self.FeedText.setObjectName("FeedText")
		self.prevB = QtWidgets.QPushButton(self.Table)
		self.prevB.setGeometry(QtCore.QRect(170, 200, 75, 23))
		self.prevB.setObjectName("prevB")
		self.prevB.clicked.connect(lambda: self.prevDB(self.FacultyDB.currentText()))
		self.delB = QtWidgets.QPushButton(self.Table)
		self.delB.setGeometry(QtCore.QRect(390, 200, 75, 23))
		self.delB.setObjectName("delB")
		self.delB.clicked.connect(lambda: self.delDB(self.FacultyDB.currentText(), self.feedgiver.text()))
		self.nextB = QtWidgets.QPushButton(self.Table)
		self.nextB.setGeometry(QtCore.QRect(280, 200, 75, 23))
		self.nextB.setObjectName("nextB")
		self.nextB.clicked.connect(lambda: self.nextDB(self.FacultyDB.currentText()))
		self.tabWidget.addTab(self.Table, "")
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Feedback Analyzing System"))
		self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt; font-weight:600;\">Feedback Analyzing</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt; font-weight:600;\">System</span></p></body></html>"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Homepage), _translate("MainWindow", "Homepage"))
		self.label_4.setText(_translate("MainWindow", "Username :"))
		self.Faculty.setItemText(0, _translate("MainWindow", "Fac1"))
		self.Faculty.setItemText(1, _translate("MainWindow", "Fac2"))
		self.Faculty.setItemText(2, _translate("MainWindow", "Fac3"))
		self.Faculty.setItemText(3, _translate("MainWindow", "Fac4"))
		self.FeedB.setText(_translate("MainWindow", "Submit Feedback"))
		self.label_5.setText(_translate("MainWindow", "Select Faculty:"))
		self.status.setText(_translate("Ui_MainWindow","Status"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Feedback), _translate("MainWindow", "Feedback"))
		self.prevB.setText(_translate("MainWindow", "Prev"))
		self.nextB.setText(_translate("MainWindow", "Next"))
		self.delB.setText(_translate("MainWindow", "Delete"))
		self.FacultyDB.setItemText(0, _translate("MainWindow", "Fac1"))
		self.FacultyDB.setItemText(1, _translate("MainWindow", "Fac2"))
		self.FacultyDB.setItemText(2, _translate("MainWindow", "Fac3"))
		self.FacultyDB.setItemText(3, _translate("MainWindow", "Fac4"))
		self.review.setText(_translate("MainWindow", "Review: "))
		self.reviewans.setText(_translate("MainWindow", "Answer "))
		self.label_7.setText(_translate("MainWindow", "Select Faculty:"))
		self.label_8.setText(_translate("MainWindow", "Feedback Given By: "))
		self.feedgiver.setText(_translate("MainWindow", "Username"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.Table), _translate("MainWindow", "Table"))


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	FrameMain = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(FrameMain)
	FrameMain.show()
	sys.exit(app.exec_())