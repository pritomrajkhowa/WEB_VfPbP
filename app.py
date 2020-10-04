import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import subprocess, threading
import sys
import os
import viap_svcomp as tool_fun


currentdirectory = os.path.dirname(os.path.realpath(__file__))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

prev_click=0


"""
Reading the contain of the file 
"""
def readingFile( filename ):
    content=None
    with open(currentdirectory+"/benchmark/"+filename) as f:
        content = f.readlines()
    return content

"""
Wrtitting the contain on file 
"""
def writtingFile( filename , content ):
	file = open(currentdirectory+"/"+filename, "w")
	file.write(str(content))
	file.close()


"""
Construct The Program  
"""
def constructProgram( content_values ):
    content=''
    for content_value in content_values:
        content+=content_value
    return content


                                
                      
                    
          
                      

app.layout = html.Div([
    html.H1(children='Automatic Program Verifier For Probabilistic Program based on First Order Logic'),
    html.H6(children='Designed by Pritom Rajkhowa and Fangzhen Lin'),
    html.H6(children='Development Team : Pritom Rajkhowa, Fangzhen Lin, Prashant Saikia, Jyoti Prakash Sahoo'),
    dcc.Dropdown(id='data-dropdown-program', options=[
          {'label':'test_test.i', 'value':'test_test.i'},
          {'label':'binomial.i', 'value':'binomial.i'},
          {'label':'nested.i', 'value': 'nested.i'},
          {'label':'square.i', 'value': 'stuttering_p.i'},
          {'label':'CC4.i', 'value':'CC4.i'},
          {'label':'product_dep_var.i', 'value': 'product_dep_var.i'},
          {'label':'stuttering_a.i', 'value': 'stuttering_a.i'},
          {'label':'sum_rnd_series.i', 'value': 'sum_rnd_series.i'},
          {'label':'CC.i', 'value': 'CC.i'},
          {'label':'random_walk_1d_cts.i', 'value':  'random_walk_1d_cts.i'},
          {'label':'stuttering_b.i', 'value': 'stuttering_b.i'},
          {'label':'test.i', 'value': 'test.i'},
          {'label':'duelling_cowboys.i', 'value': 'duelling_cowboys.i'},
          {'label':'random_walk_2d.i', 'value': 'random_walk_2d.i'},
          {'label':'stuttering_c.i', 'value': 'stuttering_c.i'},
          {'label':'test_init_rv.i', 'value':'test_init_rv.i'},
          {'label':'geometric.i', 'value':'geometric.i'},
          {'label':'running.i', 'value':'running.i'},
          {'label':'stuttering_d.i', 'value':'stuttering_d.i'}
    ], value='test_test.i'),
      html.H6(children='Input Program'),
      dcc.Textarea(
        id='textarea-input-program1',
        style={'width': '100%', 'height': 200},
    ),
     html.Div([
		html.Button('Verify', id='submit_button'),
      ]),
      html.H6(children='Translated Axioms (First Moment)'),
      dcc.Textarea(
        id='textarea-input-program2',
        style={'width': '100%', 'height': 200},
    ),
      html.H6(children='Translated Axioms (Second Moment)'),
      dcc.Textarea(
        id='textarea-input-program3',
        style={'width': '100%', 'height': 200},
    ),

     html.H6(children='Translated Axioms (Third Moment)'),
      dcc.Textarea(
        id='textarea-input-program4',
        style={'width': '100%', 'height': 200},
    ),




])


@app.callback(
    [Output('textarea-input-program1', 'value'),
    Output('textarea-input-program2', 'value'),
    Output('textarea-input-program3', 'value'),
    Output('textarea-input-program4', 'value')],
    [Input('data-dropdown-program', 'value'), Input('submit_button', 'n_clicks')],
    [State('textarea-input-program1', 'value')])
def callback_a(x, y, input_program):
    global prev_click


    #input_program = ''
    input_assem   = ''
    display_info_1mom  = 'Loading ....'
    display_info_2mom  = 'Loading ....'
    display_info_3mom  = 'Loading ....'
    if y is None:
       
       input_program = constructProgram(readingFile( x ))
       
    elif prev_click < y:
       prev_click = y
       if input_program is not None and input_program.strip()!='':


          display_map = tool_fun.prove_auto(currentdirectory+"/benchmark/"+x)


          display_info_1mom = display_map['1MOM'][0]+display_map['1MOM'][1]+display_map['1MOM'][2]

          display_info_2mom = display_map['2MOM'][0]+display_map['2MOM'][1]+display_map['2MOM'][2]

          display_info_3mom = display_map['3MOM'][0]+display_map['3MOM'][1]+display_map['3MOM'][2]


    else:
       input_program = constructProgram(readingFile(x))

    return input_program,display_info_1mom,display_info_2mom,display_info_3mom


if __name__ == '__main__':
    app.run_server(debug=True)
