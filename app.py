###################################################################################################################### 
#############################  INTERACTIVE PROTEIN DEPLETION SIMULATOR  ###########################################
"""
@Author:    Kevin Yar
Email:      kevin.yar@biognosys.com

""" 
######################################################################################################################
######################################################################################################################

#============================================   Packages   ==========================================================#
#from dash_bootstrap_components import themes
#from matplotlib.pyplot import figimage
import pandas as pd
import numpy as np
from numpy import polyfit
from numpy import poly1d
import json

import dash
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import dash_bootstrap_components as dbc #read style from bootstrap

# For graphs
import plotly.express as px  
import plotly.graph_objects as go


#============================================   Layout:   ==========================================================#

### INITIALIZATION OF THE APP
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

#mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
#app.scripts.append_script({ 'external_url' : mathjax })

#-----------------------------------------  Layout: Text / Colors  ------------------------------------------------# 
#Colors for all possible elements in web-app as dictionair
colors = {
    'head_background':' #facccc',
    'background':'#FFFFFF',
    'text':'#5f0606'
}

colorsT = {
    'color':'#ffffff',
    'background':'#800000',
    "text-align":"center",
    'border':'4px black solid', 
    'border-radius': 7.5,
    "margin":"10px auto"
}

textfont_temp = {
    "family":"sans serif",
    "size": 18,
    "color":"white"
}

#-----------------------------------------  Layout: Webpage ------------------------------------------------# 

bgPic = "url(https://biognosys.com/content/uploads/2021/04/Biognosys-RFP_Concepts_Big-Data_2021-02-11_v08-GKM_Artboard-2-scaled.jpg)"


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "width": "100%",
    "margin-left": "0%",
    "margin-right": "0%",
#    "background-image":bgPic
}


#-----------------------------------------  Layout: Template text / formatting   ------------------------------------------------# 

#Styling 
"""
def style_c():
    layout_style={'display':'inline-block','margin':'0 auto','padding':'20px'}
    return layout_style
"""

#text
title = 'IceCream transformer'
subtitle = 'Get a rapid Answer from inbounds'
text = '''Please choose the set of proteins which you want to deplete. 
\n Choose the antibodies which you want to use to deplete (commercialy available on the [Biognosys](https://biognosys.com/)  '''

text_style = {'textAlign':'center', 'color':colors['text'], "size":18}
text_style_left = {'textAlign':'left', 'color':colors['text']}
text_style_right = {'textAlign':'right', 'color':colors['text']}

table_title = "Top 15 high abundant plasma proteins sorted by concentration pgL / -1"
logo = "https://www.greaterzuricharea.com/sites/default/files/inline-images/logo-global-social.jpg"

"""
image = dict(source=bgPic, opacity=0.5)
"""

#some more styling layous
""" import plotly.io as pio 
pio.templates.default = "plotly_dark" #Darken the general layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
W3 = "https://www.w3schools.com/w3css/4/w3.css" #👀👀
FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"  #👀👀? """

#============================================   DATA    ==========================================================#
"""                                                                                                   
DDDDDDDDDDDDD                       AAA               TTTTTTTTTTTTTTTTTTTTTTT               AAA               
D::::::::::::DDD                   A:::A              T:::::::::::::::::::::T              A:::A              
D:::::::::::::::DD                A:::::A             T:::::::::::::::::::::T             A:::::A             
DDD:::::DDDDD:::::D              A:::::::A            T:::::TT:::::::TT:::::T            A:::::::A            
  D:::::D    D:::::D            A:::::::::A           TTTTTT  T:::::T  TTTTTT           A:::::::::A           
  D:::::D     D:::::D          A:::::A:::::A                  T:::::T                  A:::::A:::::A          
  D:::::D     D:::::D         A:::::A A:::::A                 T:::::T                 A:::::A A:::::A         
  D:::::D     D:::::D        A:::::A   A:::::A                T:::::T                A:::::A   A:::::A        
  D:::::D     D:::::D       A:::::A     A:::::A               T:::::T               A:::::A     A:::::A       
  D:::::D     D:::::D      A:::::AAAAAAAAA:::::A              T:::::T              A:::::AAAAAAAAA:::::A      
  D:::::D     D:::::D     A:::::::::::::::::::::A             T:::::T             A:::::::::::::::::::::A     
  D:::::D    D:::::D     A:::::AAAAAAAAAAAAA:::::A            T:::::T            A:::::AAAAAAAAAAAAA:::::A    
DDD:::::DDDDD:::::D     A:::::A             A:::::A         TT:::::::TT         A:::::A             A:::::A   
D:::::::::::::::DD     A:::::A               A:::::A        T:::::::::T        A:::::A               A:::::A  
D::::::::::::DDD      A:::::A                 A:::::A       T:::::::::T       A:::::A                 A:::::A 
DDDDDDDDDDDDD        AAAAAAA                   AAAAAAA      TTTTTTTTTTT      AAAAAAA                   AAAAAAA                              
  """       

mars14      = ["P02768", "P02671", "P01009", "P02787", "P01024", "P01023", "P02647", "P00738", "P0DOX5", "P01876", "P02652", "P02766", "P02763", "P01871"]
sepromix20  = ['P02768', 'P02647', 'P02787', 'P00738', 'P02675', 'P01009', 'P01023', 'P02671', 'P02679', 'P01024', 'P02763', 'P00450', 'P0C0L4', 'P00747', 'P04114', 'P02747', 'P02745', 'P02746', 'P02766', 'P0C0L5']


#============================================   Dictionairs     ==========================================================#



#============================================   Functions   ==========================================================#



#============================================   Web-App Layout    ==========================================================#

#-----------------------------------------            Sidebar                ------------------------------------------------# 


#-----------------------------------------            Navigation bar (top)               ------------------------------------------------# 
navbar =  dbc.Container(fluid=True, children=[
        dbc.Navbar(
            dbc.Container([
                html.A( #<A>
                    dbc.Row([
                        dbc.Col(html.Img(src=logo, height="40px")),
                        dbc.Col(dbc.NavbarBrand("IceCream Transformer", className="ms-2"))
                    ], align = "center", className="g-0" ),#style Row
                    href="https://biognosys.com/", style = {"textDecoration":"none"}
                    ),  #</A>
                    ]),
            color="#800000", dark=True, style = {'border':'4px black solid','border-radius': 7.5}
            ),
        html.Br()
        ])

testBsp = """ Dear mr X \n How much is the price of product Y"""
testBsp2 = """ Dear mr A \n thank you for your mail \n the price is 500 CHF without shipping"""
#-----------------------------------------            WebApp Content                ------------------------------------------------# 
content =  dbc.Container(children=[  #<container>
                    html.H2(subtitle, style={
                                'color':'#ffffff',
                                'background':'rgb(75,75,75,0.5)',
                                "text-align":"center",
                                'border-radius': 7.5,
                                "margin":"auto"}),
                    dbc.Row(children=[
                        dbc.Col(
                            dcc.Textarea(id="test", value=testBsp, style={'width': '100%', 'height': 200})
                            ),
                        dbc.Col(
                            dcc.Textarea(id="test2", value=testBsp2, style={'width': '100%', 'height': 200})
                            ),
                    ]),
                    ], fluid=False, id="page-content", style=CONTENT_STYLE
                    ) #</container>

#-----------------------------------------            MERGE                ------------------------------------------------# 

app.layout = html.Div([
    navbar,
    content],
    style={'background-image': bgPic})
    

#################################################       Callbacks       #######################################################################
                 


#########################################  RUN APP AT SPECIFIED PORT  ###################################################################
if __name__ == '__main__':
   app.run_server(debug=True, host='0.0.0.0', port=9999)   # 🐱‍🐉 change port on ip http://192.168.101.124:6969/ with host= '0.0.0.0', port=6969