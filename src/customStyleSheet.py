from textwrap import dedent

#USAGE: for buttons: cpalette [ colorString ] [ 0: normal | 1: hover | 2: pressed ]
cpalette = {
    "black": ["#1D1C1A"],
    "red": ["#F9665E", "#D9404A", "#9B0700"],
    "orange": ["#FC6600","#FF964F", "#D45500"]
}


mainwindow_style = "QWidget { background-color: black; border: 2px solid beige; }"

exit_button_style = dedent(
    """QPushButton { 
            color: """+ cpalette["black"][0] +""";
            background-color: """+ cpalette["red"][0] +"""; 
            border-style: outset; 
            border-width: 2px; 
            border-radius: 10px; 
            border-color: beige; 
            font: bold 28px; 
            padding: 6px; 
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["red"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["red"][2] +"""; 
            border-style: inset; 
        }""")

time_label_style = dedent(
    """QLabel { 
            color: """+ cpalette["black"][0] +""";
            background-color: """+ "beige" +"""; 
            border-style: outset; 
            border-width: 2px; 
            border-radius: 10px;  
            font: 36px; 
            padding: 4px; 
        } """)

icon_style = dedent(
    """QPushButton { 
            background-color: """+ "beige" +"""; 
            border-style: outset; 
            border-width: 2px; 
            border-radius: 10px;  
            font: 36px; 
            padding: 4px; 
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")

small_icon_style = dedent(
    """QPushButton { 
            background-color: white;
            border-style: outset; 
            border-width: 1px; 
            border-radius: 5px;  
            border-color: grey;
            font: 18px bold; 
            padding: 1px; 
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")

small_line_style = dedent(
    """QLineEdit { 
            background-color: white;
            border-style: outset; 
            border-width: 1px; 
            border-color: grey;
            border-radius: 5px;  
            font: 18px; 
            padding: 2px; 
        }  """
)

webBrowser_style = dedent(
    """
    background-color:white; 
    border-style: outset; 
    border-width: 2px; 
    border-bottom-right-radius: 10px; 
    border-bottom-left-radius: 10px; 
    padding: 4px
    """
)

no_border_icon_style = dedent(
    """QPushButton { 
            background-color: white;
            border-style: outset; 
            border-width: 0px; 
            border-radius: 0px;  
            border-color: none;
            font: 24px bold; 
            padding: 0px; 
            min-width:35px;
            max-width:35px;
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")