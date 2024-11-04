import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)
        self.load(QUrl("http://www.google.com"))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_night_mode = True  
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Navegador MK")
        self.setStyleSheet("background-color: #333; color: #DDD;")  

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setStyleSheet("QTabWidget::pane { border: 0; } QTabBar::tab { background: #444; color: #DDD; }")
        self.setCentralWidget(self.tabs)

       
        navbar = QToolBar("Navegação")
        navbar.setStyleSheet("QToolBar { background-color: #222; }")
        self.addToolBar(navbar)

        navbar.addAction(QAction('Voltar', self, triggered=lambda: self.tabs.currentWidget().back()))
        navbar.addAction(QAction('Avançar', self, triggered=lambda: self.tabs.currentWidget().forward()))
        navbar.addAction(QAction('Recarregar', self, triggered=lambda: self.tabs.currentWidget().reload()))
        navbar.addAction(QAction('Início', self, triggered=lambda: self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))))
        navbar.addAction(QAction('Nova Aba', self, triggered=self.add_new_tab))
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("background-color: #555; color: #DDD;")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        
        bookmarks_btn = QAction('Favoritos', self)
        bookmarks_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmarks_btn)

      
        fullscreen_btn = QAction('Tela Cheia', self)
        fullscreen_btn.triggered.connect(self.toggle_fullscreen)
        navbar.addAction(fullscreen_btn)

        history_btn = QAction('Histórico', self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

      
        downloads_btn = QAction('Downloads', self)
        downloads_btn.triggered.connect(self.show_downloads)
        navbar.addAction(downloads_btn)

       
        night_mode_btn = QAction('Alternar Modo', self)
        night_mode_btn.triggered.connect(self.toggle_night_mode)
        navbar.addAction(night_mode_btn)

       
        self.add_new_tab(QUrl('http://www.google.com'), 'Página Inicial')

    def add_new_tab(self, qurl=None, label="Nova Aba"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')
        browser = BrowserTab()
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, q, browser=None):
        if browser is self.tabs.currentWidget():
            self.url_bar.setText(q.toString())

    def show_bookmarks(self):
      
        print("Exibindo favoritos")

    def show_history(self):
      
        print("Exibindo histórico")

    def show_downloads(self):
      
        print("Exibindo downloads")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_night_mode(self):
        
        if self.is_night_mode:
            self.setStyleSheet("background-color: #FFF; color: #000;")
            self.url_bar.setStyleSheet("background-color: #EEE; color: #000;")
            self.tabs.setStyleSheet("QTabWidget::pane { border: 0; } QTabBar::tab { background: #DDD; color: #000; }")
            self.is_night_mode = False
        else:
            self.setStyleSheet("background-color: #333; color: #DDD;")
            self.url_bar.setStyleSheet("background-color: #555; color: #DDD;")
            self.tabs.setStyleSheet("QTabWidget::pane { border: 0; } QTabBar::tab { background: #444; color: #DDD; }")
            self.is_night_mode = True

    def current_tab_changed(self, i):
        if i >= 0 and self.tabs.count() > 0:
            qurl = self.tabs.currentWidget().url()
            self.url_bar.setText(qurl.toString())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  
    app = QApplication(sys.argv)
    QApplication.setApplicationName('Navegador MK')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
