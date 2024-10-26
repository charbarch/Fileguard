
from PyQt5.QtWidgets import QMessageBox

def show_credits():
    credits_text = """
    FileGuard Software
    
    Developed by:
    - Paul Estephan
    - Charbel Rahme
    - Peter Chalhoub
    """
    msg_box = QMessageBox()
    msg_box.setStyleSheet("QMessageBox {background-color: #2b2b2b; color: white;}")
    msg_box.information(None, "Credits", credits_text)