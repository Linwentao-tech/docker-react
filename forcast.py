import base64
from dash.dependencies import Output, Input
import data_reader
import main
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([html.H1("Stock Forecast"),
                       html.Div(dcc.Input(id='input_box', type='text', placeholder='Enter the stock name')),
                       html.Div(dcc.Input(id='day_box', type='text', placeholder='Enter the days')),
                       html.Div(dcc.Dropdown(id='stock_dropdown',
                                             options=[
                                                 {'label': '', 'value': ''}
                                             ])),
                       html.Div([html.Button('Submit', id='button'), html.Button('View Image', id='image_button')],
                                style={'display': 'inline-block'}),
                       html.Div(id='output-container-button',
                                children='Enter the information and press submit'),
                       html.Div(id='output-result',
                                children=''), html.Img(
        id="body-image",

    )

                       ])


@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [Input(component_id='input_box', component_property='value')],
    [Input(component_id='day_box', component_property='value')]
)
def update_output(input_box, day_box):
    return 'The stock is "{}" and prediction day is {} , please select stock and wait for the prediction result..'.format(
        input_box,
        day_box
    )


@app.callback(
    Output(component_id='stock_dropdown', component_property='options'),
    [Input(component_id='input_box', component_property='value')]
)
def update_stock_info(name):
    return [{'label': key + ":" + data_reader.search(name)[key], 'value': data_reader.search(name)[key]} for key in
            data_reader.search(name)]


@app.callback(
    Output(component_id='output-result', component_property='children'),
    [Input(component_id='input_box', component_property='value')],
    [Input(component_id='day_box', component_property='value')],
    [Input(component_id='stock_dropdown', component_property='value')],
    [Input(component_id='button', component_property='n_clicks')]
)
def update_result_info(input_box, day_box, stock_dropdown, n_clicks):
    try:
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        else:
            data_reader.initialize()
            price = round(float(main.main(int(day_box), stock_dropdown)[0]), 2)
            main.remove()
            return 'The future price of {} after {} days will be ${} '.format(

                str(input_box).upper(), day_box, price
            )
    except AssertionError:
        return 'STOCK NOT FOUND'


@app.callback(
    Output(component_id='body-image', component_property='src'),
    [Input(component_id='image_button', component_property='n_clicks')]
)
def update_img_info(n_clicks):
    try:
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate
        else:
            image_filename = 'static/model_prediction.png'
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
            src = 'data:image/png;base64,{}'.format(encoded_image.decode())
            return src
    except AssertionError:
        return 'STOCK NOT FOUND'


if __name__ == '__main__':
    app.run_server(debug=True)
