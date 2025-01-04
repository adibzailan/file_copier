class Theme:
    # Colors
    BACKGROUND = "#1E1E1E"
    SURFACE = "#252526"
    PRIMARY = "#FF6F61"
    TEXT = "#FFFFFF"
    TEXT_SECONDARY = "#E0E0E0"
    BORDER = "#333333"
    SUCCESS = "#4CAF50"
    ERROR = "#f44336"

    # Styles
    WINDOW_STYLE = f"""
        QMainWindow, QWidget {{
            background-color: {BACKGROUND};
            color: {TEXT};
        }}
        QLabel {{
            color: {TEXT};
        }}
        QLineEdit {{
            color: {TEXT};
            background-color: {SURFACE};
            border: 1px solid {BORDER};
            padding: 4px 8px;
            border-radius: 4px;
        }}
        QLineEdit:focus {{
            border: 1px solid {PRIMARY};
        }}
    """

    COPY_SET_STYLE = f"""
        QWidget {{
            background-color: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 4px;
            color: {TEXT};
        }}
        QLabel {{
            border: none;
            color: {TEXT};
            font-family: 'Cerebri Sans';
            background-color: transparent;
        }}
        QPushButton {{
            background-color: {PRIMARY};
            color: {TEXT};
            border: none;
            padding: 4px 12px;
            border-radius: 4px;
            font-family: 'Cerebri Sans';
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY}DD;
        }}
        QLineEdit {{
            background-color: {BACKGROUND};
            color: {TEXT};
            border: 1px solid {BORDER};
            padding: 4px 8px;
            border-radius: 4px;
        }}
        QLineEdit:focus {{
            border: 1px solid {PRIMARY};
        }}
    """

    TREE_STYLE = f"""
        QTreeWidget {{
            background-color: {BACKGROUND};
            border: 1px solid {BORDER};
            border-radius: 4px;
            color: {TEXT};
        }}
        QTreeWidget::item {{
            color: {TEXT};
            padding: 4px;
        }}
        QTreeWidget::item:hover {{
            background-color: {SURFACE};
        }}
        QTreeWidget::item:selected {{
            background-color: {PRIMARY}33;
        }}
        QHeaderView::section {{
            background-color: {SURFACE};
            color: {TEXT};
            padding: 4px;
            border: none;
        }}
        QPushButton {{
            background-color: {PRIMARY};
            color: {TEXT};
            border: none;
            padding: 4px 12px;
            border-radius: 4px;
            font-family: 'Cerebri Sans';
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY}DD;
        }}
    """

    ADD_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {PRIMARY};
            color: {TEXT};
            border: none;
            padding: 8px 16px;
            font-family: 'Cerebri Sans';
            font-weight: bold;
            border-radius: 4px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY}DD;
        }}
    """

    SYNC_BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {SUCCESS};
            color: {TEXT};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 120px;
            font-family: 'Cerebri Sans';
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {SUCCESS}DD;
        }}
        QPushButton[syncing="true"] {{
            background-color: {ERROR};
        }}
        QPushButton[syncing="true"]:hover {{
            background-color: {ERROR}DD;
        }}
    """

    STATUS_STYLE = f"""
        QTextEdit {{
            background-color: {BACKGROUND};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 4px;
            padding: 8px;
        }}
    """

    FOOTER_STYLE = f"""
        QWidget {{
            background-color: {SURFACE};
            color: {TEXT};
            padding: 4px;
        }}
    """
