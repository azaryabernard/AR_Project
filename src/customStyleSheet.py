from textwrap import dedent

#USAGE: for buttons: cpalette [ colorString ] [ 0: normal | 1: hover | 2: pressed ]
cpalette = {
    "black": ["#1D1C1A"],
    "red": ["#F9665E", "#D9404A", "#9B0700"],
    "orange": ["#FC6600","#FF964F", "#D45500", "#ff751a"],
    "white": ["#F8F8FF"],
    "gray": ["gray"]
}


#mainwindow_style = "QWidget { background-color: green;}"

smallIcon_style = dedent(
    """QPushButton { 
            color: """+ cpalette["gray"][0] +""";
            background-color: """+ cpalette["white"][0] +"""; 
            border-style: outset; 
            border-width: 0px; 
            border-radius: 10px; 
            border-color: """+ cpalette["white"][0] +"""; 
            font: bold 21px; 
            padding: 5px;
            qproperty-iconSize: 34px;
            outline: none;
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")

time_label_style = dedent(
    """QLabel { 
            color: """+ cpalette["white"][0] +""";
            border-width: 0px; 
            font: 28px; 
            padding: 3px; 
        } """)

speech_label_style = dedent(
    """QLabel { 
            color: """+ cpalette["white"][0] +""";
            border-width: 0px; 
            font: 22px; 
            padding: 3px; 
        } """)
        
widget_label_style = dedent(
    """QLabel { 
            color: """+ cpalette["white"][0] +""";
            background-color: """ + cpalette["orange"][3] +""";
            border-width: 2px; 
            border-top-right-radius: 10px; 
            border-bottom-right-radius: 10px; 
            border-color: """+ cpalette["orange"][1] +""";
            padding: 10px;
            min-width:64px;
            max-width:64px;
            min-height:96px;
            max-height:96px;
        } """)

long_widget_label_style = dedent(
    """QLabel { 
            color: """+ cpalette["white"][0] +""";
            background-color: """ + cpalette["orange"][3] +""";
            border-width: 2px; 
            border-radius: 10px;
            border-color: """+ cpalette["orange"][1] +""";
            padding: 10px;
            min-width:384px;
            max-width:384px;
            min-height:48px;
            max-height:48px;
        } """)

icon_style = dedent(
    """QPushButton { 
            background-color: """+ cpalette["white"][0] +"""; 
            border-style: outset; 
            border-width: 2px; 
            border-radius: 10px;  
            font: 27px; 
            padding: 3px;
            min-width:96px;
            max-width:96px;
            min-height:96px;
            max-height:96px;
            qproperty-iconSize: 72px;
            outline: none;
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
            background-color: """+ cpalette["white"][0] +""";
            border-style: outset; 
            border-width: 1px; 
            border-radius: 5px;  
            border-color: grey;
            font: 14px bold; 
            padding: 8px; 
            outline: none;
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")

widget_icon_style = dedent(
    """QPushButton { 
            color: """+ cpalette["white"][0] +""";
            background-color: """+ cpalette["orange"][1] +"""; 
            border-style: outset; 
            border-width: 2px; 
            border-radius: 10px;
            border-color: transparent;
            font: 27px; 
            padding: 10px;
            padding-left: 24px;
            min-width:188px;
            max-width:188px;
            min-height:96px;
            max-height:96px;
            text-align:left;
            qproperty-iconSize: 88px;
            outline: none;
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][3] +""";  
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
            font: 14px; 
            padding: 5px; 
        }  """
)

webBrowser_style = dedent(
    """
    background-color:white; 
    border-style: outset; 
    border-width: 2px; 
    border-color: white;
    border-bottom-right-radius: 10px; 
    border-bottom-left-radius: 10px; 
    padding: 4px;
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
            min-width:32px;
            max-width:32px;
            outline: none;
        }  
        QPushButton:hover { 
            background-color: """+ cpalette["orange"][1] +""";  
        } 
        QPushButton:pressed {
            background-color: """+ cpalette["orange"][2] +"""; 
            border-style: inset; 
        }""")

log_style = "color:green; font: 20px; border:0px;"

ht_border_style = "border-style: inset; border-width: 3px; border-color: pink;"

cornerWidget_style = "background-color: white; border-width: 0px; spacing: 0; border-top-left-radius:10px; border-top-right-radius:10px; margin-right:0px;"