from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import random
import dash_bootstrap_components as dbc

# Initialize the app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample Data for 10 Years with random sales and stock prices for multiple companies
years = list(range(2013, 2023))
companies = ["Company A", "Company B", "Company C"]
data = []

# Generate random data for each company
for company in companies:
    sales = [random.randint(100, 500) for _ in years]
    stock_prices = [random.randint(50, 200) for _ in years]
    data.extend({"Year": year, "Sales": sale, "Stock Price (₹)": price, "Company": company} for year, sale, price in zip(years, sales, stock_prices))

# Create DataFrame
df = pd.DataFrame(data)

VALID_USERNAME_PASSWORD_PAIRS = {"admin": "password123"}

# App layout with enhanced interface
app.layout = html.Div(children=[
    dbc.Container([
        # Header with Logo and Title
        dbc.Row([
            dbc.Col(html.Img(src="/assets/logo.png", style={"width": "200px"}), width="auto"),
            dbc.Col(html.H1("Stock Price Prediction & Data Visualization", className="text-center")),
        ], align="center", className="my-3"),

        # Theme Toggle Button
        dbc.Row([
            dbc.Col(dbc.Button("Toggle Theme", id="theme-toggle", className="btn btn-secondary"), width="auto")
        ], className="mb-3"),

        # Navigation Icons: Info, About, Policy, Buy, Sell, Security
        dbc.Row([
            dbc.Col(html.Img(src="/assets/info_icon.png", id="info-icon", style={"width": "70px", "cursor": "pointer"})),
            dbc.Col(html.Img(src="/assets/about_icon.png", id="about-icon", style={"width": "70px", "cursor": "pointer"})),
            dbc.Col(html.Img(src="/assets/policy_icon.png", id="policy-icon", style={"width": "70px", "cursor": "pointer"})),
            dbc.Col(html.Img(src="/assets/buy_icon.png", id="buy-icon", style={"width": "70px", "cursor": "pointer"})),
            dbc.Col(html.Img(src="/assets/sell_icon.png", id="sell-icon", style={"width": "70px", "cursor": "pointer"})),
            dbc.Col(html.Img(src="/assets/security_icon.png", id="security-icon", style={"width": "70px", "cursor": "pointer"})),
        ], justify="end", align="center", className="mb-3"),

        # Company Dropdown and Range Slider for Year Selection
        html.Label("Select Company:"),
        dcc.Dropdown(
            id="company-dropdown",
            options=[{"label": company, "value": company} for company in df["Company"].unique()],
            value="Company A"
        ),
        html.Label("Select a year range:"),
        dcc.RangeSlider(
            id="year-slider",
            min=df["Year"].min(),
            max=df["Year"].max(),
            step=1,
            marks={year: str(year) for year in df["Year"]},
            value=[df["Year"].min(), df["Year"].max()]
        ),

        # Sales and Stock Price Charts
        dbc.Row([
            dbc.Col(dcc.Graph(id="line-chart"), md=6),
            dbc.Col(dcc.Graph(id="bar-chart"), md=6)
        ]),

        # Stock Price Prediction Feature with Enhanced Interface
        dbc.Row([
            dbc.Col(html.H3("Predict Future Stock Price (₹)", className="mt-3"), width="auto"),
            dbc.Col(dcc.Input(id="years-ahead", type="number", placeholder="Years Ahead", min=1, max=10, value=1), width="auto"),
            dbc.Col(html.Button("Predict", id="predict-button", className="btn btn-primary")),
        ], align="center"),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Prediction Result"),
                    dbc.CardBody(id="prediction-output", style={"fontSize": "20px", "textAlign": "center"}),
                ], className="mt-3")
            )
        ]),

        # Popup Modals for Info, About, Policy, Buy, Sell, and Security Pages
        # Modals for informational content
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Information")),
                dbc.ModalBody("This app visualizes historical sales and stock prices and allows future stock price prediction."),
                dbc.ModalFooter(dbc.Button("Close", id="close-info", className="ml-auto")),
            ],
            id="modal-info",
            is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("About")),
                dbc.ModalBody("Data visualization and forecasting enable users to explore and make informed financial decisions."),
                dbc.ModalFooter(dbc.Button("Close", id="close-about", className="ml-auto")),
            ],
            id="modal-about",
            is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Policy")),
                dbc.ModalBody("The predictions are for educational purposes and should not be considered financial advice."),
                dbc.ModalFooter(dbc.Button("Close", id="close-policy", className="ml-auto")),
            ],
            id="modal-policy",
            is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Buying Stocks")),
                dbc.ModalBody("Buy stocks at predicted or current prices. Please contact your financial advisor."),
                dbc.ModalFooter(dbc.Button("Close", id="close-buy", className="ml-auto")),
            ],
            id="modal-buy",
            is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Selling Stocks")),
                dbc.ModalBody("Sell your stocks based on current market analysis. Note: This is not financial advice."),
                dbc.ModalFooter(dbc.Button("Close", id="close-sell", className="ml-auto")),
            ],
            id="modal-sell",
            is_open=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Security")),
                dbc.ModalBody("We prioritize user data privacy. Our policy ensures all information is secure and encrypted."),
                dbc.ModalFooter(dbc.Button("Close", id="close-security", className="ml-auto")),
            ],
            id="modal-security",
            is_open=False,
        ),
    ], fluid=True)
])

# Update charts based on company selection and year range
@app.callback(
    [Output("line-chart", "figure"), Output("bar-chart", "figure")],
    [Input("company-dropdown", "value"), Input("year-slider", "value")]
)
def update_charts(selected_company, selected_year_range):
    filtered_df = df[(df["Company"] == selected_company) & 
                     (df["Year"] >= selected_year_range[0]) & 
                     (df["Year"] <= selected_year_range[1])]

    line_fig = px.line(filtered_df, x="Year", y="Sales", title=f"Sales for {selected_company} Over Years")
    bar_fig = px.bar(filtered_df, x="Year", y="Stock Price (₹)", title=f"Stock Prices (₹) for {selected_company}")

    return line_fig, bar_fig

# Callback for stock price prediction
@app.callback(
    Output("prediction-output", "children"),
    Input("predict-button", "n_clicks"),
    State("years-ahead", "value"),
    State("company-dropdown", "value")
)
def predict_stock_price(n_clicks, years_ahead, selected_company):
    if n_clicks is None:
        return "Click 'Predict' to see the results."
    last_price = df[df["Company"] == selected_company]["Stock Price (₹)"].iloc[-1]
    predicted_price = last_price + random.randint(10, 30) * years_ahead
    return f"Predicted Stock Price for {selected_company} in {years_ahead} years: ₹{predicted_price}"

# Callbacks for toggling modals
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(Output("modal-info", "is_open"), [Input("info-icon", "n_clicks"), Input("close-info", "n_clicks")], [State("modal-info", "is_open")])(toggle_modal)
app.callback(Output("modal-about", "is_open"), [Input("about-icon", "n_clicks"), Input("close-about", "n_clicks")], [State("modal-about", "is_open")])(toggle_modal)
app.callback(Output("modal-policy", "is_open"), [Input("policy-icon", "n_clicks"), Input("close-policy", "n_clicks")], [State("modal-policy", "is_open")])(toggle_modal)
app.callback(Output("modal-buy", "is_open"), [Input("buy-icon", "n_clicks"), Input("close-buy", "n_clicks")], [State("modal-buy", "is_open")])(toggle_modal)
app.callback(Output("modal-sell", "is_open"), [Input("sell-icon", "n_clicks"), Input("close-sell", "n_clicks")], [State("modal-sell", "is_open")])(toggle_modal)
app.callback(Output("modal-security", "is_open"), [Input("security-icon", "n_clicks"), Input("close-security", "n_clicks")], [State("modal-security", "is_open")])(toggle_modal)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
