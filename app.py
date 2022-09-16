###################################################################################################################### 
#############################  INTERACTIVE PROTEIN DEPLETION SIMULATOR  ###########################################
"""
@Author:    Kevin Yar 
Email:      kevin.yar@biognosys.com 

""" 
######################################################################################################################

""" 
Sections
    1. Packages
    2. Layout
        2.1 Text / Colors
        2.2 Webpage
        2.3 Template text / formatting 
    3. Data
        3.1 Core Files
        3.2 Dictionaries for protein choices
        3.3 Dictionaries for sidebar input
    4. Functions
    5. Web-App Content
        5.1 Navigation bar (top)
        5.2 Sidebar
        5.3 Main Window 
        5.4 Merge
    ### CALLBACKS ###
    6. Sidebar collapse
    7. Protein specific depletion efficiency dictionary
    8. Core transformation
        8.1 Set the needed data
        8.2 Cut the tail and get LOD
        8.3 Depletion process
        8.4 Calculated summed abundance
        8.5 Calculate information for summary table
        8.6 Calculate PPM and Rank
        8.7 Regression Models
        8.8 Cut at LOD
        8.9 R-squared value 
        8.10 Summary table data
        8.11 Summary Dataframes --> for plots & Tables
    9. TOP15 Table
    10. Summary Table
    11. Visualization
    12. App server / port configurations
"""
# Section symbols

######### Functional Section ##########

#============== Section ==============#

#-------------- Subsection -----------# 

######################################################################################################################

#============================================   Packages   ==========================================================#
#Basic modules
from webbrowser import BackgroundBrowser
import pandas as pd
import numpy as np
from numpy import polyfit
from numpy import poly1d
import json
from typing import List, Set, Dict, Tuple, Optional
import argparse

#statistical modules
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
#gam
from pygam import LinearGAM, s, f, l

#for the Multi-layer-perceptron (MLP) fit + extrapolation
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.metrics import MeanAbsoluteError
from keras.optimizers import *

#Basic Dash necessities
import dash
#import dash_daq as daq
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
#Bash bootstrap extension for special frontend elements
import dash_bootstrap_components as dbc #read style from bootstrap
#For graphs
import plotly.express as px  
import plotly.graph_objects as go
import plotly.figure_factory as ff

#============================================   Layout   ==========================================================#

### INITIALIZATION OF THE APP
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = True

#-----------------------------------------  Layout: Text / Colors  ------------------------------------------------# 
#Colors for all possible elements in web-app as dictionaries
colors = {
    'head_background':' #facccc',
    'background':'#FFFFFF',
    'text':'#5f0606',
    "font-family":"sans-serif"
}

colorsT = {
    'color':'#ffffff',
    'background':'#800000',
    "text-align":"center",
    'border':'4px black solid', 
    'border-radius': 7.5,
    "margin":"5px auto",
    "font-family":"sans-serif"
}

subtitleStyle = {
            'color' :'#ffffff',
            'background':'rgb(75,75,75,0.5)',
            "text-align":"center",
            'border-radius': 7.5,
            'border':'4px black solid',
            "margin":"10px auto", "font-family":"sans-serif",
            "width" :"75%"
            }

switchStyle = {
            'color':'#ffffff',
            'background':'rgb(75,75,75,0.5)',
            "position":"left",
            'border-radius': 7.5,
            'border':'4px black solid',
            "margin":"10px auto",
            "font-family":"sans-serif"}

textfont_temp = {
    "family":"sans serif",
    "size": 18,
    "color":"white",
    "font-family":"sans-serif"
}

#-----------------------------------------  Layout: Webpage ------------------------------------------------# 

#find the URL of the biognosys website background picture with the inspection element and use it as the Web-app background
bgPic = "url(https://biognosys.com/content/uploads/2021/04/Biognosys-RFP_Concepts_Big-Data_2021-02-11_v08-GKM_Artboard-2-scaled.jpg)"


#The following two style dictionaries are needed for the sidebar button
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": "1rem",
    "bottom": 0,
    "width": "20%",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
    "font-family":"sans-serif","font-size":"1rem", "font-weight":400,
    "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",

}

SIDEBAR_HIDDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
    "font-family":"sans-serif"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "width": "100%",
    "margin-left": "25%",
    "margin-right": "0%",
    "padding": "2rem 1rem",
}

CONTENT_STYLE1 = {  #if  sidebar collapsed
    "transition": "margin-left .5s",
    "width": "80%",
    "margin-left": "15%",
    "margin-right": "15%",
    "padding": "2rem 1rem",
}

tab_style = {
    'borderBottom': '1px solid #2b2827',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': 'white',
    "backgroundColor":"#212529"
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold'
}

popoverStyle = {
                    "width": "400 px",
                    "margin-right": "10%",
                    "border-radius": "10px",
                    "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                }

sidebarStyle = {
                    "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                }
#-----------------------------------------  Layout: Template text / formatting   ------------------------------------------------# 
"""
This section sets some variables for text outputs as well as text styles in the webapp. 
"""

#text
title = 'IP821 - Depletion Simulator'
subtitle = 'Interactive protein depletion simulator for general Proteomics application'
text = '''Please choose the set of proteins which you want to deplete. 
\n Choose the antibodies which you want to use to deplete (commercially available on the [Biognosys](https://biognosys.com/)  '''

text_style = {'textAlign':'center', 'color':colors['text'], "size":18, "font-family":"sans-serif"}
text_style_left = {'textAlign':'left', 'color':colors['text'], "font-family":"sans-serif"}
text_style_right = {'textAlign':'right', 'color':colors['text'], "font-family":"sans-serif"}

table_title = "Top 15 high abundant plasma proteins sorted by PPM"
#the logo was not extracted from the official biognosys website due to recent changes of the server and therefore the locations of the logo. 
logo = "https://www.greaterzuricharea.com/sites/default/files/inline-images/logo-global-social.jpg"

#The following text variables are the POPOVER instruction for the web-app
#the problem of the missing line breaks in the popovers was solved using https://stackoverflow.com/questions/14459691/bootstrap-popover-hides-line-breaks which requires an additional css file
textDataset = """
3 Datasets are available: \n
Native (Undepleted blood plasma samples), \n
Depleted (Blood plasma samples depleted with the MARS14 column from Agilent) and \n
Reconstituted (Depleted blood plasma samples for which the MARS14 target proteins are reconstituted by their depletion efficiency).
"""

textDepletedProteins = """The first dropdown shows the target proteins of the MARS14 depletion column. \n
The second column shows the the top30 proteins with the highest abundance AFTER the blood plasma is depleted. In both dropdowns the proteins are sorted by their Abundance (Descending). 
If not further specified in the sidebar tab "Efficiency" the depletion efficiencies of the MARS14 proteins are taken from the experimental data and the depletion efficiencies of the top30 proteins are set to 99%."""

textDepletionKit = """An alternative to choosing single proteins is to deplete these proteins which are targeted of the depletion kits MARS14 or Sepromix20 together."""

textGeneralDepEff = """Choose a depletion efficiency which affects every chosen protein independent of the protein specific input chosen. 0 = No depletion and 100 = fully depleted. If a value remains in this field other depletion efficiencies are ignored."""

textPredictionModel = """4 prediction models are available. \n
Each model fits to the protein distribution in a specified range (Described as startRank and stopRank) and extrapolates the distribution to Rank (x) 10'000. 
The extrapolated data is then cut at the limit of detection (determined from the original data in red). \n
    Linear (Fits from startRank to stopRank which are in the linear range evaluated by the getStartAndStop algorithm. y = m*x + c), \n
    Non-linear (Fits from Rank 0 to stopRank of the linear range, y = a * (x^b + c)^-1 + d ), \n
    (Linear) GAM or generalized additive model (fits from Rank 0 to stopRank with 25 splines with a normal distribution, E[y|X] = beta0 + f1(X1) + f2(X2, X3) + ... + fM(XN)), \n
    MLP or Multi Layer Perceptron which is a small neural network containing 2 hidden layers with 32 neurons each containing the tanH activation function (Fits from Rank 0 to Rank 3500 with 100 epochs and a batch size of 32, takes a moment to calculate)"""


textDisplayMethod = """This dropdown changes the y-scale of the scatter-plot"""

textTabSummary = """Summary Table which includes some important information"""
textTabDepEff = """The purpose of this violin plot is to show how the chosen proteins to deplete behaved experimentally after the depletion with MARS14. 
By choosing a protein to deplete the corresponding white line will appear which shows if the target was co-depleted (left from red line), unchanged (near the red line) or enriched (right from red line) after the experimental depletion with MARS14"""

textTabDepEffTitle = """In this tab you can enter protein specific depletion efficiencies or checkout the uniprot page of the most abundant MARS14 and Non-MARS14 proteins. 
Each protein card consists of the protein Name the uniprot Identifier and an input field. \n
In the first section only MARS14 proteins are listed ordered by their Abundance (descending). By clicking the grey rectangle the uniprot page of the chosen protein will open.  
For the input field the possible values ranges between 0 = no depletion up to 100 = full depletion. \n
REMARK! If a value is given in the input field "General Depletion Eff" no changes will be made. Please remove this value to specify protein specific depletion efficiencies """


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

The Data section reads all necessary files saved on the shared Biognosys driver. 

The data preprocessing for the SIMULATOR_DATA.csv (summaryAll variable) file was done with the IP821_DataPreparationForSimulator Markdown which is located in the bitbucket repository under:
biognosys-research\Kevin_Yar\app environment\IP821_DataPreparationForSimulator.Rmd
This markdown uses the raw Spectronaut report files for the given calculation. More information about these raw data files and their location can be found on the markdown itself. 
"""       

#-----------------------------------------  Data: Core files  ------------------------------------------# 

#Uniprot ID List of the MARS14 and sepromix20 targets
mars14      = ["P02768","P02787","P02671","P01024","P01876","P01023","P01871","P01009","P02647","P00738","P02766","P02652","P02763,","P01860"]
sepromix20  = ['P02768', 'P02647', 'P02787', 'P00738', 'P02675', 'P01009', 'P01023', 'P02671', 'P02679', 'P01024', 'P02763', 'P00450', 'P0C0L4', 'P00747', 'P04114', 'P02747', 'P02745', 'P02746', 'P02766', 'P0C0L5']

stringDBImmunoglobulins = pd.read_csv(r"S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\stringDBImmunoglobulins.csv")["PG.ProteinAccessions"].tolist() 
mars14ANDstringDBImmunoglobulins = list(set(mars14 + stringDBImmunoglobulins))

mars14CoTargetInteractor= pd.read_csv(r"S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\mars14CoTargetInteractor.csv")["PG.ProteinAccessions"].tolist() 
mars14ANDCoTargetInteractor = list(set(mars14 + mars14CoTargetInteractor))
        
#Combination of data from native, depleted, and native reconstituted -> calculated in the IP821_DataPreparationForSimulator.Rmd Markdown
summaryAll      = pd.read_csv(r"S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\SIMULATOR_DATA.csv").sort_values(by=["abundance"], ascending=False)

#depletion efficiency file 
depEffDataFrame = pd.read_csv(r"S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\depletionEfficiencyDataFrameMS2.csv")

#the plasmaprot contains protein concentration information from literature as for example the human plasma atlas (thpa). This data is also used for the summary table in the app 
plasmaprot      = pd.read_csv(r'S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\plasmaprot.csv')

#ultra deep file for the only purpose of showing protein names and uniprot ID's when hovering over points on the extrapolated data
summaryGeneral  = pd.read_csv(r"S:\Ana\2022\821_Depletion_Panel_Designer_DPD\appDataEnvironment\summaryGeneral.csv").sort_values(by="Rank")

#-----------------------------------------  Data: Dictionaries for protein choices  ------------------------------------------# 
"""
In this subsection 2 dictionaries are created for the dropdown choice of which proteins to deplete. 
These 2 dictionaries are only created with the reconstituted data due to the fact that:
    - The mars14 proteins will mostly end in their native rank order
    - Using a depleted set has the codepletion effect already included. And because the interest of creating a new depletion column with the same targets as the MARS14 column is minimal, 
        the proteins which end up having a higher abundance after depletion are of higher interest.
"""

protDep = summaryAll[ (summaryAll.QuantMethod == "nativeReconstituted") ].copy(deep=True)

#get the uniprot IDs and names of the  mars14 proteins and top 30 non mars14 proteins
protDepDict       = protDep[ (protDep.mars14 == 0) ].iloc[:30, :].copy(deep=True)
protDepDictMars14 = protDep[ (protDep.mars14 == 1) ].copy(deep=True)
#print("\n", protDepDictMars14, "\n")

depleted_proteins = []
depleted_mars14 = []

for lab, val in zip(protDepDict.proteinName.tolist(), protDepDict.uniprot.tolist()): #zip is love 💖💕💕
    depleted_proteins.append({'label':lab, "value":val}) 

for lab, val in zip(protDepDictMars14.proteinName.tolist(), protDepDictMars14.uniprot.tolist()): #zip is love 💖💕💕
    depleted_mars14.append({'label':lab, "value":val}) 

#-----------------------------------------  Data: Dictionaries for sidebar input   ------------------------------------------------# 
"""These dictionaries are used as dropdown options for the sidebar"""

# Proteins removed by Depletion Kit
KITlabel_ = [{"label":"MARS14"                  , "value": "MARS14"},
             {"label":"MARS14StringDBImmuno"    , "value": "MARS14 and stringDB interacting Immunogloulins"},
             {"label":"MARS14CoTargetInteractor", "value": "MARS14 and co-targets"},
             {"label":"SEPROMIX20"              , "value": "SEPROMIX20"}]        

# Fit + extrapolation model options
model_    = [{"label":"None"            , "value":"None"},
             {"label":"linear"          , "value":"linear"},
             {"label":"non-linear"      , "value":"non-linear"},
             {"label":"GAM"             , "value":"GAM"},                #General Additive Model
             {"label":"MLP"             , "value":"MLP"}]                #Multi-layer Perceptron

# Display / Y-Scale option
dispMet   = [{"label":"log10"           , "value":"log10"},
             {"label":"sqrt"            , "value":"sqrt"},
             {"label":"-"               , "value":"-"}]

# dataset used
dataset   = [{"label":"Reconstituted"   , "value":"Reconstituted"},
             {"label":"Depleted"        , "value":"Depleted"},
             {"label":"Native"          , "value":"Native"}]


#============================================   Functions   ==========================================================#

"""
In this section different functions are declared which are used either in the front- or backend. Each function has an own description
"""

def make_break(num_breaks: int) -> List:
    """Makes number of html breaks specified"""
    br_list = [html.Br()] * int(num_breaks)
    return br_list

def returnHoverButton(idTitle = "", title="", text="", color="light", style={}, size="md", placement = "auto"):
    
    return html.Div(children=[
                    #cardHead
                    dbc.Button(
                        title,
                        id= "returnHoverButton"+ idTitle,
                        color= color,
                        className="me-1",
                        n_clicks=0,
                        style={},
                        size=size
                    ),
                    dbc.Popover(
                        text,
                        target="returnHoverButton"+ idTitle,
                        body=True,
                        trigger="hover",
                        delay={"hide":25},
                        style=style,
                        placement = placement
                    )])    

def colInRowCard(cardHead="", interaction = "drop", hoverText="", **kwargs):
    if interaction == "drop":
        """Creates a dash dropdown element inside a dbc card element with a specified card header inside a dbc column inside a dbc row layout. Card has a horizontal rule (Hr) to be separated"""
        return  dbc.Row(
                    dbc.Col([
                    dbc.CardHeader(
                        returnHoverButton(idTitle = cardHead , title=cardHead, text = hoverText, style=popoverStyle)    
                    ),
                    dbc.Card([dcc.Dropdown(**kwargs, style={"margin":"10px", "height":"75%"}, optionHeight = 35)], style={"font-size": "6"}),
                    html.Hr()
                    ])
                )
    elif interaction == "input":
        """Creates a dash input element inside a dbc card element with a specified card header inside a dbc column inside a dbc row layout. Card has a horizontal rule (Hr) to be separated"""
        return  dbc.Row(
                    dbc.Col([
                    dbc.CardHeader(
                        returnHoverButton(idTitle = cardHead , title=cardHead, text = hoverText, style=popoverStyle)    
                    ),
                    dbc.Card(dcc.Input(**kwargs, style={"margin":"10px"})),
                    html.Hr()
                    ])
                )        
    
def colInRowCardDropProtChoice(cardHead="", optionFirst = [], idFirst="", idSecond="", optionSecond=[], placeholderFirst="", placeholderSecond="", hoverText="", **kwargs):
    """Same as colInRowCardDrop() but with 2 dropdown's in the same card (one for mars14 and one for top30 protein choices"""
    return  dbc.Row(
                dbc.Col([
                dbc.CardHeader( 
                    returnHoverButton(idTitle = cardHead , title=cardHead, text = hoverText, style=popoverStyle)         
                    ),
                dbc.Card([
                            dcc.Dropdown(id=idFirst, options=optionFirst,   style={"margin":"10px", "height":"75%"}, optionHeight = 50, placeholder=placeholderFirst,   **kwargs),
                            dcc.Dropdown(id=idSecond,options=optionSecond,  style={"margin":"10px", "height":"75%"}, optionHeight = 50, placeholder=placeholderSecond,  **kwargs )
                            ], style={"font-size": "6"}),
                html.Hr()
                ])
            )


def colInRowCardSlider(cardHead="", **kwargs):
    """Creates a dash dropdown element inside a dbc card element with a specified card header inside a dbc column inside a dbc row layout. Card has a horizontal rule (Hr) to be separated.
    Not in use anymore, but might be useful later."""
    return  dbc.Row(
                dbc.Col([
                dbc.CardHeader(cardHead),
                dbc.Card(dcc.Slider(**kwargs, style={"margin":"10px"}))
                ])
            )


def protInput(uni, placeH=None):
    """
    Location: Sidepanel, tab 2
    Function to create the efficiency card html-elements. 
    rowA = extract the protein name the uniprot ID and the foldChange for the chosen protein (uni) to then
    put the protein Name as card title, the uniprot ID as html element ID and the foldChange as depletion efficiency
    Return a html card element with an dash input element to change the depletion efficiency for one specific protein. 
    The id of the input is used as the input of the coreTransformationFunction in the Core section below to recalculate the depletion. 
    If the protein is not chosen in tab1 the depletion doesn't change.  
    """
    #get the information from the 
    rowA = depEffDataFrame[ (depEffDataFrame.uniprot == str(uni)) ][["proteinName", "uniprot",  "foldChange"]].values.flatten().tolist() 
    try:
        proteinName_    = str(rowA[0])
        uniprot_        = str(rowA[1])
        depEff_         = (1-rowA[2]) * 100
        placeH          = "depEff = %.2f " % depEff_
        #Use a depletion efficiency of 99% for all non-mars14 proteins BUT show their original depletion efficiency as a placeholder to get an information about codepletion and enrichement
        if uniprot_ not in mars14:
            depEff_ = 99
    except:
        proteinName_    = str(uni)
        uniprot_        = str(uni)
        depEff_         = 99
        placeH          = "Example: 95"

    return  dbc.Row(
                dbc.Col([ 
                    dbc.Button(
                        proteinName_, 
                        outline=True, 
                        color="light", 
                        external_link = True,
                        target="_blank",
                        href = "https://www.uniprot.org/uniprotkb/" + uniprot_ +"/entry",
                        style=dict(color="black", backgroundColor="#d4d4d4")),
                    #html.H6(proteinName_), 
                                html.H6(uniprot_), 
                                dcc.Input(
                                    id = uniprot_, type="number", min=-3000, max=100, 
                                    value = round(depEff_, 3),
                                    placeholder = placeH
                                ), 
                                *make_break(1),
                                html.Hr()
                                ]))

def protInputMars14(**kwargs):
    """This function uses the previous 'protInput' function to create the first section (MARS14) of tab 2. 
    This function concatenates multiple protInput cards with the MARS14 Target proteins ordered after their Rank in MS2 in the Reconstituted Dataset """
    return      html.Div([
                protInput("P02768"), #albumin
                protInput("P02787"), # Serotransferrin
                protInput("P02671"), # Fibrinogen alpha chain
                protInput("P01024"), # Complement C3
                protInput("P01876"), # Immunoglobulin heavy constant alpha 1
                protInput("P01023"), # Alpha-2-macroglobulin
                protInput("P01871"), # Immunoglobulin heavy constant mu 
                protInput("P01009"), # Alpha-1-antitrypsin
                protInput("P02647"), # Apolipoprotein A-I
                protInput("P00738"), # Haptoglobin
                protInput("P02766"),  # Transthyretin
                protInput("P02652"), # Apolipoprotein A-II 
                protInput("P02763"), # Alpha-1-acid glycoprotein 1
                #protInput("P0DOX5"), # Immunoglobulin gamma-1 heavy chain <- OLD MARS14 target, changed due to non-visibility/non-detectability after depletion
                protInput("P01860"), # Immunoglobulin heavy constant gamma 3
                    ], **kwargs)

def protInputHAP(**kwargs):         
    """This function uses the previous 'protInput' function to create the first section (MARS14) of tab 2. 
    This function concatenates multiple protInput cards with the Non-MARS14 TOP30 proteins ordered after their Rank in MS2 in the Reconstituted Dataset 
    """
    return      html.Div([
                        protInput("P02790"), #hemopexin
                        protInput("P0C0L4"), #Complement C4-A
                        protInput("P04114"), #Apolipoprotein B-100 
                        protInput("P02751"), # Fibronectin 
                        protInput("P08603"), #Complement factor H 
                        protInput("P02679"), #Fibrinogen gamma chain
                        protInput("P19823"), #Inter-alpha-trypsin inhibitor heavy chain H2
                        protInput("P00450"), #Ceruloplasmin
                        protInput("P02675"), #Fibrinogen beta chain
                        protInput("P01011"), #Alpha-1-antichymotrypsin
                        protInput("P00751"), #Complement factor B   
                        protInput("P00747"), #Plasminogen
                        protInput("P02774"), #Vitamin D-binding protein
                        protInput("P05155"), # Plasma protease C1 inhibitor
                        protInput("P01008"), #Antithrombin-III
                        protInput("P00734"), #Prothrombin
                        protInput("Q14624"), #Inter-alpha-trypsin inhibitor heavy chain H4
                        protInput("P04004"), #Vitronectin
                        protInput("P01042"), #Kininogen-1
                        protInput("P02749"), #Beta-2-glycoprotein 1
                        protInput("P01031"), #Complement C5
                        protInput("P06727"), #Apolipoprotein A-IV
                        protInput("P02760"), #Protein AMBP
                        protInput("P43652"), #Afamin
                        protInput("P06396"), # Gelsolin  
                        protInput("P19827"), # Inter-alpha-trypsin inhibitor heavy chain H1 
                        protInput("P04217"), #Alpha-1B-glycoprotein
                        protInput("P02649"), #Apolipoprotein E
                        protInput("P10909") #Clusterin
                ], **kwargs)


def GAMpred(Xtrain, ytrain_, Xtest, n_splines = 50):
    """This function removes NANs from the input (should not have any) fits the generalized additive model and returns the extrapolation. 
    50 Splines ares used (n_splines=50), the more the higher the fit to the original data but the extrapolation takes more information from the tail of the data"""
    ytrain = ytrain_[~np.isnan(ytrain_)]
    Xtrain = Xtrain[~np.isnan(ytrain_)]
    Xtest = Xtest[~np.isnan(Xtest)]
    gam = LinearGAM(s(0), n_splines=n_splines)
    gam.fit(Xtrain, ytrain)
    yP = gam.predict(Xtest)
    return yP

def jsonToTable(df):
    """This function can be used to read in a temporary saved json table and return a dash bootstrap table element. 
    Not used but may be useful in the future."""
    return dbc.Table.from_dataframe(pd.read_json(df).head(), striped=True, bordered=True, hover=True, dark=True)

def getStartAndStop(df_, col = "ppm", window = 250, linParam = "mean", iniCut = "y"):
    """
    This function is used for two tasks:
        - find the linear range of the distribution
        - Find the tail of a distribution
    
    Parameters:
        col = which column of the df should be calculated
        window = what size should the rank window be the distinguish between anomaly or non anomaly
        linParam = what should the values of the window be compared with to evaluate, mean or median?
        iniCut = should the first and last 10% of proteins be removed? (y, n) only for linear range  

    To get a better robustness For the first task, the function takes an iniCut input which decides wether the first AND last 10% of proteins are removed.
    Then the derivative is calculated over 3 rank steps and saved as derivativeArray. This Array is used to get the 
    startRank and the stopRank (the array is then flipped). Depending on the window size and the linParam the iteration stops earlier with smaller windows sizes. 
    """
    df = df_.copy(deep=True)
    #cut the first and last 10%
    lenDf = len(df[col])
    if iniCut == "y":
        rankStart = round(lenDf*0.1)
        rankStop  = round(lenDf*0.9 )
        df = df.iloc[rankStart:rankStop]

    #create zero array
    derivativeArray = np.zeros(len(df[col]))
    #calculate the diff over 3 steps
    for i in range(len(df[col])):
        try:
            derivativeArray[i] = abs( 
                (np.log10(df[col].values[i+3]) - np.log10(df[col].values[i])) / 1 #the division with 1 is just to show that this is a derivative 
                )
        except:
            #exit when end of array
            break

    #linParam
    if linParam == "mean":
        linParam_   = np.mean(derivativeArray)
    elif linParam == "median":
        linParam_ = np.median(derivativeArray)

    #get start and stop initialization
    startStop   = [0, len(df[col])]
    nrOfWindows = round(len(derivativeArray) / window)

    #to get the startRank we'll use the normal order of the derivativeArray. To get the stopRank the derivativeArray is flipped
    for ini_, array_  in enumerate([derivativeArray, np.flip(derivativeArray)]):
        for windowsIter in range(nrOfWindows):
            #leave these comments here in case of debugging
#            print("window", (windowsIter)*window, "-", (windowsIter+1)*window)
#            print("Mean: ", np.mean(devArray[(windowsIter)*window : (windowsIter+1)*window]))
#            print("p-value: ", scipy.stats.ttest_ind(devArray[(windowsIter)*window : (windowsIter+1)*window], devArray).pvalue)
#            print("------")
            if np.mean(array_[(windowsIter)*window : (windowsIter+1)*window]) < linParam_:
                startStop[ini_] = windowsIter 
                print(startStop[ini_])
                break
            else:
                next

    #return the rank
    startStop[0] = startStop[0]*window                
    startStop[1] = (nrOfWindows - startStop[1]) * window

    return startStop

def mlpFitandPredict(x, y, predictFrom = 1, predictTo=10000, epochs=50, batch_size=32): 
    """
    This function initializes a Multi layer perceptron with 4 layers, compiles it and fits the given input data
    which are x=rank and y=log10(ppm). It is used as an option for the prediction model in tab1
    It only returns the predicted log10(ppm) as pandas series.
    the following parameters can be changed:
    x       = ranks (you can use np.arange(startValue, stopValue))
    y       = ppm (should be used as log10)
    predictFrom   = start rank to predict
    predictTo     = stop rank to predict
    epochs        = how many epochs should the model train, the more epochs the longer it takes AND it may fit the unwanted tail  
    """
    model = Sequential()
    model.add(Dense(units = 1, activation = 'linear', input_shape=[1]))
    model.add(Dense(units = 32, activation = 'tanh'))
    model.add(Dense(units = 32, activation = 'tanh'))
    model.add(Dense(units = 1, activation = 'linear'))
    #add early stopping, stops fitting after hitting 30times same loss
    callback = keras.callbacks.EarlyStopping(monitor='loss', patience=30)
    # Compile model with loss as mean squared error and adam as the optimizer
    model.compile(loss='mse', optimizer="adam")
    # Fit the model and define history output
    log = model.fit(x, y, epochs=epochs, validation_split=0.1, batch_size=batch_size, callbacks=[callback], verbose=1)
    #return prediction as pandas series
    pred = model.predict(np.arange(predictFrom, predictTo))
    #keras.backend.clear_session()
    return pd.Series(pred.flatten(), name="deplPredNew")

#============================================   Web-App Content    ==========================================================#

"""    
  ___                   ___               _      _  _                _                      
 / _ \                 / _ \             | |    (_)| |              | |                     
/ /_\ \ _ __   _ __   / /_\ \ _ __   ___ | |__   _ | |_   ___   ___ | |_  _   _  _ __   ___ 
|  _  || '_ \ | '_ \  |  _  || '__| / __|| '_ \ | || __| / _ \ / __|| __|| | | || '__| / _ \
| | | || |_) || |_) | | | | || |   | (__ | | | || || |_ |  __/| (__ | |_ | |_| || |   |  __/
\_| |_/| .__/ | .__/  \_| |_/|_|    \___||_| |_||_| \__| \___| \___| \__| \__,_||_|    \___|
       | |    | |                                                                           
       |_|    |_|                                                                           
                                                                                            
In this section the different content elements of the Web-app are programmed and merged. 
The web-app contains of a Navigation Bar (top), Sidebar (left) and Content area (center) which have different styles (section Layout) and contents.
These 3 elements are then merged in the last subsection.
"""

#-----------------------------------------    Web-App Layout: Navigation bar (top)     ------------------------------------------------# 
navbar =  dbc.Container(fluid=True, children=[
        dbc.Navbar(
            dbc.Container([
                dbc.Col(dbc.Button("Sidebar", color="warning", className="mr-1", id="btn_sidebar", style=sidebarStyle)),
                html.A( #<A>
                    dbc.Row([
                        dbc.Col(html.Img(src=logo, height="40px", style=sidebarStyle)),
                        dbc.Col(dbc.NavbarBrand("IP821 depletion simulator", className="ms-2"))
                    ], align = "center", className="g-0" ),#style Row
                    href="https://biognosys.com/", style = {"textDecoration":"none"}, target="_blank"
                    ),  #</A>
                    ]),
            color="#800000", dark=True, style = {'border':'4px black solid','border-radius': 7.5, "font-family":"sans-serif"  }
            ),
        html.Br()
        ])

#-----------------------------------------  Web-App Content: Sidebar  ------------------------------------------------# 

"""
This web-app element contains all the content of the sidebar. The sidebar has 2 tabs:
    1. tab: (Choices are created in the Section "DATA")
        - Choice of Dataset 
        1.1 tab: 
            - Choice of proteins to deplete
            - Choice how many of the Top N proteins to deplete
        - Choice of depletion kit
        - Choice of general depletion efficiency
        - Choice of the Fit & predict Model
        - Choice of the Y-scale for the plot
    2. Tab: 
        - Protein Specific depletion efficiency input. If the prewritten value is removed, 
          you can see the experimental depletion efficiency and therefore get more information about the protein being codepleted or enriched. 
"""
sidebar = html.Div(                    
                children=[
                    dbc.Tabs([
                        dbc.Tab([
                            colInRowCard("Dataset", interaction="drop",  hoverText = textDataset, options=dataset,  value=dataset[0]["label"],  id='dataset',   multi=False),
                            dbc.Tabs([
                                dbc.Tab([
                                    colInRowCardDropProtChoice("Depleted Proteins (sort. by Abu)", hoverText = textDepletedProteins,
                                                                optionFirst=depleted_mars14, idFirst='depleted_mars14', placeholderFirst="Deplete MARS14 ",
                                                                optionSecond=depleted_proteins,  idSecond='depleted_proteins', placeholderSecond="Deplete TOP30 proteins",
                                                                multi=True)
                                                                ], label="Manual depletion", id="sidebarTab1.1"),
                                dbc.Tab([       
                                    colInRowCard("Deplete Top N proteins", interaction="input", 
                                                hoverText = textGeneralDepEff,  id="topN", type="number", 
                                                min=0, max=30, value=None, placeholder="Ex. 5")
                                                ], label="Top N depletion", id="sidebarTab1.2")
                                    ]),                     
                            colInRowCard("Depletion Kit", interaction="drop",  hoverText = textDepletionKit, options=KITlabel_, id='KITProtSel', placeholder="Alternatively choose the depletion Kit"),
                            colInRowCard("Prediction Model", interaction="drop",options=model_, hoverText = textPredictionModel,  value=model_[1]["label"],   id='modelSel',  multi=False),
                            colInRowCard("Display Method", interaction="drop",  options=dispMet,  hoverText = textDisplayMethod,   value=dispMet[0]["label"],  id='dispMet',   multi=False),                            
                            *make_break(5)
                        ], label="Depletion", id="sidebarTab1"),
                        dbc.Tab([
                            html.Div(returnHoverButton(title="Enter the depletion efficiency [%]", text = textTabDepEffTitle, placement = "right", size="lg", style={"font-family":"sans-serif"})),
                            html.Hr(), 
                            colInRowCard("General Depletion efficiency / %", interaction="input", hoverText = textGeneralDepEff,  id="depEff", type="number", min=0, max=100, value=None, placeholder="Ex. 98.2"), #for autom. change                    
                            html.B("TOP14 (MARS14) Proteins (sort. by Abu)"),
                            #return the protein cards for the depletion efficiency input
                            protInputMars14(),
                            html.B("TOP30 MAP Proteins (sort. by Abu)"), # NOT SORTED YET   
                            #return the protein cards for the depletion efficiency input
                            protInputHAP(),                            
                            *make_break(2)
                        ], label="Efficiency", id="sidebarTab2")
                    ])
                ], id="sidebar", style = SIDEBAR_STYLE)

#-----------------------------------------   Web-App Content: Main Window     ------------------------------------------------# 

"""
Together with the main content elements like figure, summary table and overview table. Additionaly a storage container is created which stores relevant intermediate information in the browsers RAM.
These storage elements are used to pass json files through callbacks aka temporary save points.
"""

content =  dbc.Container(children=[  #<container>
                    html.H2(subtitle, style=colorsT),
                                *make_break(2),
                    dbc.Row(children=[
                        dbc.Col(
                            #loading function which shows when the graph is being generated
                            dcc.Loading( 
                                id="loadingGraph", type="default",                                                
                                    children=[dcc.Graph( id='depleted_fig', style={'border':'4px solid', 'border-radius': 7.5})]
                                    ), width = 7), 
#                        dbc.Col(
#                            children=[
#                            #daq.BooleanSwitch(id='dynamicLOD', on=False, label="Activate dynamic LOD", style=switchStyle),
#                            html.Div(id="summary_table")], width={"size": 5 })

                        dbc.Col(children=[
                                dcc.Tabs(id="summaryTableTab",
                                children=[
                                    dcc.Tab(id="summaryTableTabSummary", label="Summary Table", value="tabSummary", style=tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(id="summaryTableTabDepEff", label="Depletion Eff.", value="tabPlot", style=tab_style, selected_style=tab_selected_style)
                                    ], value="tabPlot"),
                                        dbc.Popover(textTabSummary, target="summaryTableTabSummary",body=True,trigger="hover",delay={"hide":25},placement="top"),
                                        dbc.Popover(textTabDepEff,  target="summaryTableTabDepEff", body=True,trigger="hover",delay={"hide":25},placement="top"),
                                    html.Div(id="summaryTablePlotTab"),
                                ], width={"size": 5 }
                                )
                        ]),
                        *make_break(2),                    
                      ##  
                    dbc.Row(
                        html.H3(table_title, style=subtitleStyle)
                        ),*make_break(1),
                    dbc.Row( #Titel für Tabelle style=text_style),
                        html.Div(id="depleted_df_table", style={'border-radius': 7.5, "margin":"auto", "width":"75%"})
                        )
                    ], fluid=False, id="page-content", style=CONTENT_STYLE
                    ) #</container>

storage = html.Div([dcc.Store(id='side_click'),#for the collapse of the sidebar
                    dcc.Store(id="depleted_df_JSON"),
                    dcc.Store(id="summary_json"),
                    dcc.Store(id="effDict"),
                    dcc.Store(id="targetProtsJson")])


#-----------------------------------------    Web-App Content: MERGE       ------------------------------------------------# 

app.layout = html.Div([
    sidebar, 
    navbar,
    content,
    storage],
    style={'background-image': bgPic})
    

#################################################       Callbacks       #######################################################################
                 
#==================================  Sidebar collapse ==================================#
"""
This call back reacts if the user clicks the collapse button on the navigation bar and then changes the layout of the sidebar and the main window
"""
@dash.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [
        Input("btn_sidebar", "n_clicks"),
        Input("side_click", "data")
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

#================================================      Protein specific depletion efficiency dictionary       ==========================================================#
""" 
Callback to get the manually written depletion efficiency of Tab 2 and output the input/given 
values as a list. Check "content" Container for the dummy element.
The order of the lines are extremely important because they will set the input to the dictionary.
The proteins, mars14 and non-mars14 are ordered by their rank in the reconstituted dataset for MS2
"""
@dash.callback( 
    Output(component_id="effDict", component_property="data"), 
    #Mars14
    [Input(component_id="P02768", component_property="value"), #Albumin
    Input(component_id="P02787", component_property="value"), # Serotransferrin
    Input(component_id="P02671", component_property="value"), #Fibrinogen alpha chain
    Input(component_id="P01024", component_property="value"), #Complement C3
    Input(component_id="P01876", component_property="value"), # Immunoglobulin heavy constant alpha 1
    Input(component_id="P01023", component_property="value"), #Alpha-2-macroglobulin
    Input(component_id="P01871", component_property="value"), # Immunoglobulin heavy constant mu 
    Input(component_id="P01009", component_property="value"), #Alpha-1-antitrypsin
    Input(component_id="P02647", component_property="value"), #Apolipoprotein A-I
    Input(component_id="P00738", component_property="value"), #Haptoglobin
    Input(component_id="P02766", component_property="value"), #Transthyretin
    Input(component_id="P02652", component_property="value"), #Apolipoprotein A-II 
    Input(component_id="P02763", component_property="value"), #Alpha-1-acid glycoprotein 1
    Input(component_id="P01860", component_property="value"), # Immunoglobulin heavy constant gamma 3
    #top30 MAP
    Input(component_id="P02790", component_property="value"), #hemopexin
    Input(component_id="P0C0L4", component_property="value"), #Complement C4-A
    Input(component_id="P04114", component_property="value"), #Apolipoprotein B-100 
    Input(component_id="P02751", component_property="value"), #Fibronectin 
    Input(component_id="P08603", component_property="value"), #Complement factor H 
    Input(component_id="P02679", component_property="value"), ##Fibrinogen gamma chain 
    Input(component_id="P19823", component_property="value"), #Inter-alpha-trypsin inhibitor heavy chain H2
    Input(component_id="P00450", component_property="value"), #Ceruloplasmin
    Input(component_id="P02675", component_property="value"), #Fibrinogen beta chain
    Input(component_id="P01011", component_property="value"), #Alpha-1-antichymotrypsin
    Input(component_id="P00751", component_property="value"), #Complement factor B
    Input(component_id="P00747", component_property="value"), #Plasminogen
    Input(component_id="P02774", component_property="value"), #Vitamin D-binding protein 
    Input(component_id="P05155", component_property="value"), #Plasma protease C1 inhibitor
    Input(component_id="P01008", component_property="value"), #Antithrombin-III
    Input(component_id="P00734", component_property="value"), #Prothrombin
    Input(component_id="Q14624", component_property="value"), #Inter-alpha-trypsin inhibitor heavy chain H4
    Input(component_id="P04004", component_property="value"), ##Vitronectin
    Input(component_id="P01042", component_property="value"), #Kininogen-1
    Input(component_id="P02749", component_property="value"), #Beta-2-glycoprotein 1 
    Input(component_id="P01031", component_property="value"), #Complement C5
    Input(component_id="P06727", component_property="value"), #Apolipoprotein A-IV
    Input(component_id="P02760", component_property="value"), #Protein AMBP
    Input(component_id="P43652", component_property="value"), #Afamin
    Input(component_id="P06396", component_property="value"), #Gelsolin
    Input(component_id="P19827", component_property="value"), #Inter-alpha-trypsin inhibitor heavy chain H1
    Input(component_id="P04217", component_property="value"), ##Alpha-1B-glycoprotein
    Input(component_id="P02649", component_property="value"), #Apolipoprotein E
    Input(component_id="P10909", component_property="value")  #Clusterin
    ])

def effListFun( 
    #MARS14
    P02768,P02787,P02671,P01024,P01876,P01023,P01871,P01009,P02647,P00738,P02766,P02652,P02763,P01860,
    #Top30
    P02790,P0C0L4,P04114,P02751,P08603,P02679,P19823,P00450,P02675,P01011,P00751,P00747,P02774,
    P05155,P01008,P00734,Q14624,P04004,P01042,P02749,P01031,P06727,P02760,P43652,P06396,
    P19827,P04217,P02649,P10909
    ):
    
    effVal = [  
    #MARS14
    P02768,P02787,P02671,P01024,P01876,P01023,P01871,P01009,P02647,P00738,P02766,P02652,P02763,P01860,
    #Top30
    P02790,P0C0L4,P04114,P02751,P08603,P02679,P19823,P00450,P02675,P01011,P00751,P00747,P02774,
    P05155,P01008,P00734,Q14624,P04004,P01042,P02749,P01031,P06727,P02760,P43652,P06396,
    P19827,P04217,P02649,P10909
    ]

    effUni = [ 
    #MARS14
    "P02768","P02787","P02671","P01024","P01876","P01023","P01871","P01009","P02647","P00738","P02766","P02652","P02763,","P01860",
    #Top30
    "P02790","P0C0L4","P04114","P02751","P08603","P02679","P19823","P00450","P02675","P01011","P00751","P00747","P02774",
    "P05155","P01008","P00734","Q14624","P04004","P01042","P02749","P01031","P06727","P02760","P43652","P06396",
    "P19827","P04217","P02649","P10909"
    ]

    eff    = dict(zip(effUni, effVal))
    return json.dumps(eff)


#================================================ ==========================================================#

"""                                                                        
        CCCCCCCCCCCCC     OOOOOOOOO     RRRRRRRRRRRRRRRRR   EEEEEEEEEEEEEEEEEEEEEE
     CCC::::::::::::C   OO:::::::::OO   R::::::::::::::::R  E::::::::::::::::::::E
   CC:::::::::::::::C OO:::::::::::::OO R::::::RRRRRR:::::R E::::::::::::::::::::E
  C:::::CCCCCCCC::::CO:::::::OOO:::::::ORR:::::R     R:::::REE::::::EEEEEEEEE::::E
 C:::::C       CCCCCCO::::::O   O::::::O  R::::R     R:::::R  E:::::E       EEEEEE
C:::::C              O:::::O     O:::::O  R::::R     R:::::R  E:::::E             
C:::::C              O:::::O     O:::::O  R::::RRRRRR:::::R   E::::::EEEEEEEEEE   
C:::::C              O:::::O     O:::::O  R:::::::::::::RR    E:::::::::::::::E   
C:::::C              O:::::O     O:::::O  R::::RRRRRR:::::R   E:::::::::::::::E   
C:::::C              O:::::O     O:::::O  R::::R     R:::::R  E::::::EEEEEEEEEE   
C:::::C              O:::::O     O:::::O  R::::R     R:::::R  E:::::E             
 C:::::C       CCCCCCO::::::O   O::::::O  R::::R     R:::::R  E:::::E       EEEEEE
  C:::::CCCCCCCC::::CO:::::::OOO:::::::ORR:::::R     R:::::REE::::::EEEEEEEE:::::E
   CC:::::::::::::::C OO:::::::::::::OO R::::::R     R:::::RE::::::::::::::::::::E
     CCC::::::::::::C   OO:::::::::OO   R::::::R     R:::::RE::::::::::::::::::::E
        CCCCCCCCCCCCC     OOOOOOOOO     RRRRRRRR     RRRRRRREEEEEEEEEEEEEEEEEEEEEE
                               
"""                            
#================================================        8.  CORE TRANSFORMATION             ==========================================================#







""" Main part of data transformation. This Callback takes in all the inputs from tab 1.
> > > TASKS:             
--> Filter DF for different values
--> Calulcate Nr of new Proteins
--> Calulcate Abundance Increase
--> Create Prediction model LINEAR, NON-LINEAR, GAM etc
--> Create a dfPlot JSON table which is then used in the visualisation callback to create the graphs
--> Create a summaryDf JSON table which is then showed as a dbc table in the app"""

@dash.callback(
    [Output(component_id="depleted_df_JSON", component_property="data"),
    Output(component_id="summary_json", component_property="data"),
    Output(component_id="targetProtsJson", component_property="data")],
    Input(component_id="depleted_mars14", component_property="value"),
    [Input(component_id="depleted_proteins", component_property="value"),
    Input(component_id="KITProtSel", component_property="value"),
    Input(component_id="modelSel", component_property="value"),
    Input(component_id="depEff", component_property="value"),
    Input(component_id="effDict", component_property="data"),
    Input(component_id="dispMet", component_property="value"),
    Input(component_id="dataset", component_property="value"),
    Input(component_id="topN", component_property="value")
    ]
)
def coreTransformationFunction(depleted_mars14=[], depleted_proteinsFUN=[], KITProtSel=[], 
                               model=None, depEff=None, effDict=[], dispMet = [], 
                               dataset = "qvalueLocalNormalisation", topN = None
        ): #💖

    #-----------------------------------------------------------------------------------------#
    #mars14          = ["P02768", "P02671", "P01009", "P02787", "P01024", "P01023", "P02647", "P00738", "P01860", "P01876", "P02652", "P02766", "P02763", "P01871"]
    #sepromix20      = ['P02768', 'P02647', 'P02787', 'P00738', 'P02675', 'P01009', 'P01023', 'P02671', 'P02679', 'P01024', 'P02763', 'P00450', 'P0C0L4', 'P00747', 'P04114', 'P02747', 'P02745', 'P02746', 'P02766', 'P0C0L5']
    #-----------------------------------------------------------------------------------------#

    reconCut = False
    # data choice
    if dataset == "Reconstituted":
        QuantMethodChoice = "nativeReconstituted"
        reconCut = True
    elif dataset == "Depleted":
        QuantMethodChoice = "depleted"
    else:
        QuantMethodChoice = "native"

    df      = summaryAll[ (summaryAll.QuantMethod == QuantMethodChoice) ].reset_index(drop=True).copy(deep=True) #for predicted
    dfOri   = summaryAll[ (summaryAll.QuantMethod == QuantMethodChoice) ].reset_index(drop=True).copy(deep=True) #for original
    
    print(df.head())

    #for the namings, not important for calculation
    dfGeneral       = summaryGeneral.copy()

    #--------------------------------------  8.1 Set the needed data ---------------------------------------------#

    # choose data for the choosen depletion KIT
    if not KITProtSel:
        KITProtSel = []
    elif KITProtSel == KITlabel_[0]["value"]:
        KITProtSel = mars14
    elif KITProtSel == KITlabel_[1]["value"]:
        KITProtSel = mars14ANDstringDBImmunoglobulins
    elif KITProtSel == KITlabel_[2]["value"]:
        KITProtSel = mars14ANDCoTargetInteractor
    else:
        KITProtSel = sepromix20

    #Set empty List for depleted_proteinsFUN
    if not depleted_proteinsFUN:
        depleted_proteinsFUN = []

    #Set empty List for depleted_mars14
    if not depleted_mars14:
        depleted_mars14 = []

    #set the topN choice
    if not topN:
        topN = 0

    #set choosen general depletion efficiency
    if not depEff:
        print("")
    else:
        depEff = float(depEff)

    #Combine the depletion choice of single proteins and depletion kits, remove proteins if chosen twice
    print("AAAAAAAAAAAA \n", f"depleted_proteinsFUN:{depleted_proteinsFUN} \n KITProtSel: {KITProtSel} \n depleted_mars14: {depleted_mars14}")
    depleted_proteinsManual = list(set(depleted_proteinsFUN + KITProtSel + depleted_mars14)) 
    print(f"*Manually Selected proteins to deplete: \n {pd.DataFrame(dict(UserChoice=depleted_proteinsManual))}")

    #Get the uniprot ID's of the topN after removing the manual input
    try:
        depleted_proteinsTopN = df[ ~df.uniprot.isin(depleted_proteinsManual) ].uniprot.tolist()[:topN]
    except Exception as err:
        print(err)
        depleted_proteinsTopN = df[ ~df.uniprot.isin(depleted_proteinsManual) ].uniprot.tolist()
    print(f"*TopN Selected proteins to deplete: \n {pd.DataFrame(dict(UserChoice=depleted_proteinsTopN))}")

    #add manual and topN depletion choice together
    depleted_proteinsTot = list(set(depleted_proteinsManual + depleted_proteinsTopN))
    targetProtsJson      = json.dumps(depleted_proteinsTot)

    # Load the depletion efficiency table which was created in Callback: "effListFun", to get the user specified protein specific depletion efficiencies
    effDict = json.loads(effDict)

    print("----------", "\n", f"Depletion efficiency Table loaded and ready", "\n", "----------")

    #if not dynamicLOD_:
    #    print("Dynamic LOD: deactivated")
    #else:
    #    dynamicLOD_ = True

    #--------------------------------------  8.2 Cut the tail and get LOD -------------------------------------------#
    """This subsection is responsible to use the function getStartAndStop with specified parameters to find 
    the tail of the protein distribution, remove it and calculate the LOD by taking the mean of the last 10 proteins"""

    if reconCut:
        df = df[ df.ppm > 0.2238]
        dfOri = dfOri[ dfOri.ppm > 0.2238]
    else:
        # determine the tail and cut it
        startRank, stopRank = getStartAndStop(df, col="ppm", window=25, linParam="mean", iniCut="n")
        df                  = df.iloc[:stopRank, :]
        print("----Core: Tail Cut------", "\n", f"The tail was cut at Rank {stopRank}", "\n", "----------")

    #define limit of detectiona
    limitOfDetection    = df.ppm[-10:].mean()


    #-------------------------------------- 8.3 Depletion process  ---------------------------------------------#
    """In this subsection the chosen proteins are being depleted with the corresponding chosen general or specific depletion efficiency.
    The summed abundance of mars14, the targeted proteins and the overall proteins are calculated before the depletion."""

    #calculate the sum of the mars14 protein abundance
    mars14SumAbu    = df[ (df.mars14 == 1) ].abundance.sum()
    #Summed abundance of the choosen proteins to depleted
    targetSumAbuBeforeDepletion       = df[(df.uniprot.isin( depleted_proteinsTot )) ].abundance.sum()
    #Summed abundance of the whole dataset
    overallSumAbuBeforeDepletion      = df.abundance.sum()


    if not depEff: # empiric depletion efficiencies
        for protein in depleted_proteinsTot:
            
            #print(f"get Protein {effDict.get(protein)}")
            #use this exception handling in case that one of the top30 proteins which was taken from the nativeReconstituted data was not found in depleted AND native and therefore does not have an experimental 
            try: 
                #USE DF.LOC to change values inside an iteration!!
                df.loc[ df.uniprot == protein, "abundance" ]  = df.loc[ df.uniprot == protein, "abundance" ] * (1 - (effDict.get(protein) / 100)) 
            except Exception as err:
                print(err)
                df.loc[ df.uniprot == protein, "abundance" ]  = df.loc[ df.uniprot == protein, "abundance" ] * (1 - (100 / 100)) 


    else:   # Given depletion efficiencies
        for protein in depleted_proteinsTot:
            df.loc[ df.uniprot == protein, "abundance" ]  = df.loc[ df.uniprot == protein, "abundance" ] * (1 - (depEff / 100)) 

    print("*** Depletion: DONE", "\n", "----------")

    #-------------------      8.4   Calculated summed abundance         --------------------------------------#

    #Summed abundance of the choosen proteins to depleted
    targetSumAbuAfterDepletion       = df[(df.uniprot.isin( depleted_proteinsTot )) ].abundance.sum()

    #Summed abundance of the whole dataset
    overallSumAbuAfterDepletion      = overallSumAbuBeforeDepletion - (targetSumAbuBeforeDepletion-targetSumAbuAfterDepletion)

    print("---- Depletion overview ------", "\n", 
                f"General Depletion efficiency choice: {depEff}", "\n", 

                "Target protein summmed abundance: \n",
                f"   *Before depletion: {targetSumAbuBeforeDepletion} \n",
                f"   *After depletion: {targetSumAbuAfterDepletion} \n",

                "Overall summmed abundance: \n",
                f"   *Before depletion: {overallSumAbuBeforeDepletion}\n",
                f"   *After depletion: {overallSumAbuAfterDepletion}\n",
                f"   *Tot Abundance removed: {targetSumAbuBeforeDepletion-targetSumAbuAfterDepletion}\n",
                "\n", "Depletion Overview: DONE \n",  "----------")
    
    #-------------------      8.5   Calculate Information for summary table       --------------------------------------#
    """This section calculates the removed abundance ratio for 
        - the internal biognosys data
        - the data from Philipp E Geyers Paper - should be updated
        - The data from the human proteome atlas"""
    abuRatio            = (targetSumAbuBeforeDepletion - targetSumAbuAfterDepletion) / overallSumAbuBeforeDepletion
    massRatioNatGeyer   = plasmaprot[ (plasmaprot.uniprot.isin(depleted_proteinsTot)) ].conc_inter_geyer_ppd_ugl.sum() / plasmaprot.conc_inter_geyer_ppd_ugl.sum()
    massRatioNatThpa    = plasmaprot[ (plasmaprot.uniprot.isin(depleted_proteinsTot)) ].conc_thpa_ugl.sum() / plasmaprot.conc_thpa_ugl.sum()

    #-------------------------------------- 8.6 Calculate PPM and Rank ---------------------------------------------#
    """In this section the parts per millions ppm column is updated with the overall summed abundance after the depletion. 
    The Rank is then calculated again and the dataframe is sorted by the Rank ascending"""

    df["ppm"]   = df.abundance / overallSumAbuAfterDepletion * 1e6
    df.Rank     = df.ppm.rank(method="max", ascending=False).reset_index(drop=True)
    df.sort_values(by="Rank", inplace=True, ascending=True)

    print("----Core: PPM calculation ------", "\n", "   *Done", "\n", "----------")
    #---------------------------------     Regression Models       -----------------------------#
    """
    This section is build as following:
        1. To use the linear part of the newly depleted distribution, the linear range must be evaluated with the getStartAndStop algorithm 
        2. Depending on the users choice of "Prediction Model" one of these is used and always outputs the extrapolated distribution in normal (non-log) scale = deplPredNew

    Each model consists of 
        - Fitting a specified area (Only in log10 scale)
        - predict and extrapolate to 10000 datapoints
        - Returning a pandas series in normal scale
    """

     #get linear range, changing these values has a big effect on the extrapolation
    start, stop     = getStartAndStop(df, window=250, linParam="median", iniCut="y")

    print("start: ", start, "stop: ", stop)    

        
    
    if model == "None" or not model:
        deplPredNew     = df.ppm
    
    elif model == "linear":
       
        try:
            depModel        = polyfit(df.Rank[start:stop], np.log10(df.ppm[start:stop]), 1)
        except:
            depModel        = polyfit(df.Rank[500:1000], np.log10(df.ppm[500:1000]), 1)

        predMachine     = poly1d(depModel)
        _X              = np.arange(start, 10000)
        deplPredNew     = pd.Series(predMachine(_X)).reset_index(drop=True)
        deplPredNew     = pd.concat([df.ppm[:start], 10**deplPredNew])

    elif model == "non-linear":

        def opt(X, a, b, c, d):
            return a * (X**b + c)**(-1) + d

    # fit to log10(data)
        try:            
            popt, pcov = curve_fit(
                                f = opt,  
                                xdata = df.Rank[:stop], 
                                ydata=  np.log10(df.ppm[:stop]), 
                                p0=[173,  0.3,  10.5,  -9], #these values are a good starting point
                                maxfev = 50000)             #the higher this value the more combination the algo tries and therefore less errors occur but the longer it takes 
        except Exception as e: 
            print(repr(e)) # if none of the combinations found a good solution
            print("something went wrong with prediction")
            popt, pcov = curve_fit(
                                f = opt,  
                                xdata = df.Rank[:stop], 
                                ydata=  np.log10(df.ppm[:stop]), 
                                p0=[5e9, 1.75, 0.1, -4],
                                maxfev = 50000)

        print("----Core: Non-linear function parameters------", "\n", f"optimal parameters found {popt}", "\n", "----------")

        deplPredNew = opt(np.arange(start=0, stop=10000), *popt) #predict from start to 10000

        # leave output to normal scale due to scale choice in app
        deplPredNew = pd.concat([pd.Series(10**deplPredNew)]).reset_index(drop=True) #concat original to start and predicted from start

    elif model == "GAM":       
        deplPredNew = GAMpred(df.Rank[:stop], np.log10(df.ppm[:stop]), np.arange(0, 10000), n_splines = 25)
        deplPredNew = pd.concat([pd.Series(10**deplPredNew)]).reset_index(drop=True)
        #deplPredNew = GAMpred(df.Rank[start:stop], np.log10(df.ppm[start:stop]), np.arange(start, 10000))
        #deplPredNew     = pd.concat([df.ppm[:start], pd.Series(10**deplPredNew)]).reset_index(drop=True)

    elif model == "MLP":
        deplPredNew_ = mlpFitandPredict(x=df.Rank[:3500], y=np.log10(df.ppm[:3500]), epochs=100, batch_size=32)
        deplPredNew  = 10**deplPredNew_

    else:
        print("please define which model you want. linear (s) or non-linear (m)")
    
    #---------------------------------     Cut at LOD       -----------------------------#
    """To ensure that the extrapolation is not unlimited the LOD which was calculated with 
    the mean of the last 10 proteins after the tail cut is used as a limit. The next step would be to make a one-point calibration to have a connection
    between removed abundance and decrease in LOD with the bottom limit of 1500 Abundance (Thermo fisher MS instrument limit)
    y = LOD
    x = removedAbundance
    m = compared native and depleted LOD and slope was calculated as -6e-11
    c = intercept is 3.5 because of thats the LOD with native in MS2"""
    
    #print(f"dynamiLOD {dynamicLOD_}")
    #if dynamicLOD_:
    #    removedAbundance = targetSumAbuBeforeDepletion-targetSumAbuAfterDepletion
    #    limitOfDetection = removedAbundance * -6e-11 + 10**3.5 #IN PPM

    deplPredNew = deplPredNew[deplPredNew > limitOfDetection]

    #---------------------------------     R-squared value       -----------------------------#   
    """Calculate the R2 value of the depleted ppm with the extrapolation"""
    try:
        R2 = r2_score(np.log10(df.ppm), np.log10(deplPredNew[:len(df.ppm)]))      
    except:
        R2 = None
        pass
    
    print("----Core: R2 Score------", "\n", f"The calculated R2 score between depleted data and extrapolation is {R2}", "\n", "----------")
    #---------------------------------     Summary table data       -----------------------------#

    """In this section the data is prepared for the summary table in the web-app. """
    #SUMMARY TABLE
    nrRemovedProts  = len(depleted_proteinsTot)

    remRelPpm       = round(abuRatio*100, 3)

    remRelMass      = round(massRatioNatThpa*100, 3)

    gainedProts     = len(deplPredNew) - len(df)

    dynamicPpmRange = [ round(deplPredNew.min(), 2), round(deplPredNew.max(), 2)]

    dfSummary = pd.DataFrame({
        "Summary Table" : ["Removed proteins", "Removed rel. ppm / %", "Removed rel. Mass (thpa) / %", "Gained proteins", "Total proteins detected", "Dynamic ppm Range"],
        "  "            : [ nrRemovedProts,     remRelPpm,              remRelMass,                     gainedProts,        len(deplPredNew),              f"{dynamicPpmRange[0]} - {dynamicPpmRange[1]}"]
    })


    try:
        dfSummary.loc[len(dfSummary)] = ["R2 rel. to depleted (not visible)", round(R2, 3)]
    except:
        print("no R2 possible")
        pass


    print(f"Summarized table {dfSummary}")
    print("Summaryzing Table: DONE")

    #--------------------------     Summary Dataframes --> for plots & Tables   -------------------------------------------#
    """
    In this section the data from the coreTransformeration is reshaped into 3 dataframes. :

        - Original: Contains the unchanged data from the user selected dataset
        - Adjusted: Contains the depleted data from the user selection without extrapolation (not exported)
        - Depleted Predicted: Contains all the relevant computation in this callback, is shown as the green prediction line

    The transformer function changes the Y-scale depending on the users input
    """
    # Transfomer to change data depending on the choosen display method
    conditions = [
        (dispMet == "log10"),
        (dispMet == "sqrt"),
        (dispMet == "-")
    ]

    def transformer(pdSeries):
        """create a masked array (np.ma) to avoid error when applying log10 or sqrt to 0 or negative numbers and returns the transformed data"""
        pdSeries = pdSeries.reset_index(drop=True)
        choices = [np.ma.log10(pdSeries.values).data, np.ma.sqrt(pdSeries.values).data, pdSeries]  # 
        return choices

    #========= 
    # ORIGINAL
    #=========
    dfPlot1 = dfOri[["proteinName", "uniprot", "Rank"]].copy(deep=True)

    dfPlot1["Original"] = np.select(conditions, transformer(dfOri.ppm))

    dfPlot1 = pd.melt(dfPlot1, id_vars=["proteinName", "uniprot", "Rank"], 
                                    value_vars=["Original"], 
                                        var_name="status", 
                                            value_name="ppm")
    #=========
    #ADJUSTED (after the depletion without the extrapolation)
    #=========
    dfPlot2 = df[["proteinName", "uniprot", "Rank"]].copy(deep=True)

    dfPlot2["adjusted"] = np.select(conditions, transformer(df.ppm))
#    dfPlot1.to_clipboard()


    dfPlot2 = pd.melt(dfPlot2, id_vars=["proteinName", "uniprot", "Rank"], 
                                    value_vars=["adjusted"], 
                                        var_name="status", 
                                            value_name="ppm")
    #=========
    #DEPLETED PREDICTED
    #=========
    
    #make dfGeneral longer
    dfName = pd.concat([df, df[1500:], dfGeneral, dfGeneral, dfGeneral])
    try:
        dfPlot3 = pd.DataFrame(dict(   # ADD PROTEINS FROM NEW RECORD FILE
            proteinName     = dfName.proteinName[:len(deplPredNew)].reset_index(drop=True),
            uniprot         = dfName.uniprot[:len(deplPredNew)].reset_index(drop=True), #gleich lang wie predDepNewProt
            Rank            = np.arange(1,len(deplPredNew)+1)
        ))
    except Exception as e:
        print(e) 
        print("prob summar ygeneral to small for extrapolation to 5000")
        
    dfPlot3["Predicted"] = np.select(conditions, transformer(deplPredNew))

    dfPlot3 = pd.melt(dfPlot3, id_vars=["proteinName", "uniprot", "Rank"], 
                                    value_vars=["Predicted"], 
                                        var_name="status", 
                                            value_name="ppm")


    #COMBINE ALL DF'S
    dfPlot = pd.concat([
        dfPlot1, 
        #dfPlot2, leave out 
        dfPlot3
        ]).reset_index(drop=True)

    #dfPlot.to_clipboard()

    return dfPlot.to_json(), dfSummary.to_json(), targetProtsJson #return both big table and summary table
    
#================================     TOP15 Table      ===========================================#
"""This Callback returns the Table with the 15 proteins which have the highest ppm after the depletion process as a dash element.
It reads in the output from the coreTransformationFunction which is temporarelly saved (hidden file)"""
@dash.callback(
    Output("depleted_df_table" , "children"),
    [Input("depleted_df_JSON", "data"),
    Input(component_id="dispMet", component_property="value")]
    )

def plotTable(depleted_df_JSON, dispMet = "-"):
    df = pd.read_json(depleted_df_JSON)
    df = df[ (df.status == "Predicted") ][["Rank", "proteinName", "uniprot", "ppm"]].iloc[:15,:]

    if dispMet == "log10":
        df.ppm = 10**df.ppm
    elif dispMet == "sqrt":
        df.ppm = df.ppm**2
    else:
        print("Nothing to do here :D")
        
    df.ppm = df.ppm.round(3)
    #df.ppm = df.ppm.apply("{:.2e}".format())

    return dbc.Table.from_dataframe( df, striped=True, bordered=True, hover=True, color="dark", responsive="md", size="md")


#================================       Visualization    ===========================================#
"""
.______    __        ______   .___________.
|   _  \  |  |      /  __  \  |           |
|  |_)  | |  |     |  |  |  | `---|  |----`
|   ___/  |  |     |  |  |  |     |  |     
|  |      |  `----.|  `--'  |     |  |     
| _|      |_______| \______/      |__|     

This section creates the figures used in the web-app.
It reads in the output from the coreTransformationFunction which is temporarelly saved (hidden file) and the user input for the y-scaling.

"""
@dash.callback(
    Output(component_id="depleted_fig", component_property="figure"),
    [Input(component_id="depleted_df_JSON", component_property="data"),
    Input(component_id="dispMet", component_property="value")])

def plot_fig(dfSummaryFUN, dispMet = "log10"):

    dfSummaryFUN = pd.read_json(dfSummaryFUN)
    
    if dispMet == "log10":
        yaxis = "log10( ppm )"
    elif dispMet == "sqrt":
        yaxis = "sqrt( ppm )"
    elif dispMet == "-":
        yaxis = "ppm"
    else:
        yaxis = "ppm"

    print(dfSummaryFUN.columns)

    fig = px.scatter(dfSummaryFUN, x="Rank", y="ppm", color="status", marginal_y="violin", hover_data=["proteinName","uniprot"],
                        opacity = 0.9,
                        color_discrete_map={
                                    "Original":"#db7979"
                                    #,"deplPredLog10":"#1978a5", 
                                    ,"Predicted":"#05716c"
                                    #,"depletedOriginal":"#b0e0e6"
                                    },
                        template="plotly_dark")

    fig.update_traces(marker=dict(
        size=4,
        symbol="diamond-dot"
#        ,opacity=0.5,
    ))

    fig.update_yaxes(
        #range=[0,9.5], 
        title_text=yaxis, row=1, col=1)

    fig.update_xaxes(
        ticks="",title_text="Rank"
    )
 
    fig.update_layout(
        paper_bgcolor="#212529",
        font_color= 'white', 
        font_family="sans-serif",
        margin=dict(l=15, r=15, t=10, b=5)
    )
    return fig

#-----------------------------------------------------

@dash.callback(
    Output(component_id="summaryTablePlotTab", component_property="children"),
    [Input(component_id="summaryTableTab", component_property="value"),
    Input(component_id="summary_json", component_property="data"),
    Input(component_id="targetProtsJson", component_property="data")
    ])

def depEffDensityPlot(tab, summary_json, targetProtsJson=[]):

    if tab == "tabSummary":
        return html.Div(
            dbc.Table.from_dataframe( pd.read_json(summary_json), striped=True, bordered=True, hover=True, dark=True)
            )
    
    elif tab == "tabPlot":

        #load chosen target prots
        if targetProtsJson:
            depletedProts = json.loads(targetProtsJson)
        else:
            depletedProts = []

        #copy the depletion efficiency dataframe
        depEffDensityPlotDf                 = depEffDataFrame.copy(deep=True)
        depEffDensityPlotDf["foldChange"]   = depEffDensityPlotDf["foldChange"].apply(np.log2)
        depletedProtsDf                     = depEffDensityPlotDf[ depEffDensityPlotDf.uniprot.isin(depletedProts) ].reset_index(drop=True) 
        print("----PLOT: function ------", "\n", f"Head of table is {depletedProtsDf.head()}", "\n", "----------")

        fig = px.violin(
                depEffDensityPlotDf, 
                x="foldChange",
                box=True,
                template="plotly_dark"
                )    

        fig.add_vline(x=0, line_width=3, line_color="red", opacity=0.5)

        #long list to avoid overlapping of annotation
        textPositionList = ["top left", "bottom left", "top right", "bottom right"] * 30

        for index, row in depletedProtsDf.iterrows():
            fig.add_vline(
                x=row.foldChange, 
                annotation_text = str(row.proteinName),
                annotation_position = textPositionList[index],
                #hover_data = row,
                line_width=3, line_color="white"
                )

        fig.update_layout(
            paper_bgcolor="#212529",
            font_color= 'white', 
            font_family="sans-serif",
            margin=dict(l=20, r=15, t=10, b=5),
            yaxis_title="Frequency",
            xaxis_title="log2( depletion efficiency )"
        )    

        return html.Div(children=[
            dcc.Graph(id="hi", figure=fig)
            ])

    else:
        print("hi")

#########################################  RUN APP AT SPECIFIED PORT  ###################################################################
parser = argparse.ArgumentParser(description="Define Port")
parser.add_argument("-port", help="choose on which port the app should run")
args = parser.parse_args()
port = args.port
if not args:
    port = 9999


if __name__ == '__main__':
   app.run_server(debug=True, host='0.0.0.0', port=port)   # 🐱‍🐉 change port on ip http://192.168.101.124:6969/ with host= '0.0.0.0', port=6969