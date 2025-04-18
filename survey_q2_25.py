# =================================== IMPORTS ================================= #

import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
import dash
from dash import dcc, html

# Google Web Credentials
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)

# ------ Pandas Display Options ------ #
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns (if needed)
pd.set_option('display.width', 1000)  # Adjust the width to prevent line wrapping

pd.reset_option('display.max_columns')
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
current_file = os.path.basename(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
# data_path = 'data/Submit_Review_Responses.xlsx'
# file_path = os.path.join(script_dir, data_path)
# data = pd.read_excel(file_path)
# df = data.copy()

# Define the Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1pxi6x6ikRZEjzEwM1Aw28yWK1h-G1p61wulYS5F9kOw/edit?resourcekey=&gid=586078421#gid=586078421"

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials
encoded_key = os.getenv("GOOGLE_CREDENTIALS")

if encoded_key:
    json_key = json.loads(base64.b64decode(encoded_key).decode("utf-8"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
else:
    creds_path = r"C:\Users\CxLos\OneDrive\Documents\BMHC\Data\bmhc-timesheet-4808d1347240.json"
    if os.path.exists(creds_path):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    else:
        raise FileNotFoundError("Service account JSON file not found and GOOGLE_CREDENTIALS is not set.")
    
expected_headers = [
    'Timestamp',
    'Email Address', 
    'Name:', 
    "Prior to today's visit, when was the last time you visited a doctor?", 
    'Which services were provided to you today?', 
    'How do you feel about the health issue that brought you to BMHC?', 
    'What is your overall stress level?', 
    'How would you rate your overall level of mental health?', 
    'How would you rate your overall physical health?',
    "What is your overall impression of the Black Men's Health Clinic?", 
    'Did the medical provider meet your expectations?', 
    'Did the medical care meet your needs?', 
    'Did the Outreach & Engagement Team provide a strong support system?', 
    'Are you a member of the HealthyCuts™ Program?',
]

# Authorize and load the sheet
client = gspread.authorize(creds)
sheet = client.open_by_url(sheet_url)
worksheet = sheet.get_worksheet(0)  
values = worksheet.get_all_values()
headers = values[0] 
rows = values[1:] # Remaining rows as data

# data = pd.DataFrame(rows, columns=headers)
# data = pd.DataFrame(worksheet.get_all_records())
# data = pd.DataFrame(client.open_by_url(sheet_url).get_all_records())
data = pd.DataFrame(worksheet.get_all_records(expected_headers=expected_headers))

df = data.copy()

# Get the reporting month:
current_month = datetime(2025, 3, 1).strftime("%B")

# Trim leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()

# Filtered df where 'Date of Activity:' is between Ocotber to December:
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df = df[(df['Timestamp'].dt.month >= 1) & (df['Timestamp'].dt.month <= 3)]
df['Month'] = df['Timestamp'].dt.month_name()

df_1 = df[df['Month'] == 'January']
df_2 = df[df['Month'] == 'February']
df_3 = df[df['Month'] == 'March']

# print(df.head(10))
# print('Total Marketing Events: ', len(df))
# print('Column Names: \n', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #

columns =[
    'Timestamp',
    'Email Address', 
    'Name:', 
    "Prior to today's visit, when was the last time you visited a doctor?", 
    'Which services were provided to you today?', 
    'How do you feel about the health issue that brought you to BMHC?', 
    'What is your overall stress level?', 
    'Explain the reason for your answer:', 
    'How would you rate your overall level of mental health?', 
    'How would you rate your overall physical health?', 'Please explain the reason for your answer:', 
    "What is your overall impression of the Black Men's Health Clinic?", 
    'Did the medical provider meet your expectations?', 
    'Did the medical care meet your needs?', 
    'Did the Outreach & Engagement Team provide a strong support system?', 'Please explain the reason for your answer:',
    'Are you a member of the HealthyCuts™ Program?',
    'Month'
]



# =============================== Missing Values ============================ #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])

# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")

df.rename(
    columns={
        'Timestamp': 'Timestamp',
        'Email Address': 'Email',
        'Name:': 'Name',
        "Prior to today's visit, when was the last time you visited a doctor?": 'Last Doctor Visit',
        'Which services were provided to you today?': 'Service',
        'How do you feel about the health issue that brought you to BMHC?': 'Health',
        'What is your overall stress level?': 'Stress',
        'Explain the reason for your answer:': 'Stress Explanation',
        'How would you rate your overall level of mental health?': 'Mental Health',
        'How would you rate your overall physical health?': 'Physical Health',
        'Please explain the reason for your answer:': 'Health Explanation',
        "What is your overall impression of the Black Men's Health Clinic?": 'Impression',
        'Did the medical provider meet your expectations?': 'Provider Expectations',
        'Did the medical care meet your needs?': 'Care Needs',
        'Did the Outreach & Engagement Team provide a strong support system?': 'Outreach Support',
        'Please explain the reason for your answer:': 'Outreach Explanation',
        'Are you a member of the HealthyCuts™ Program?': 'HealthyCuts Membership',
    },
    inplace=True
)

# Get the reporting quarter:
def get_custom_quarter(date_obj):
    month = date_obj.month
    if month in [10, 11, 12]:
        return "Q1"  # October–December
    elif month in [1, 2, 3]:
        return "Q2"  # January–March
    elif month in [4, 5, 6]:
        return "Q3"  # April–June
    elif month in [7, 8, 9]:
        return "Q4"  # July–September

# Reporting Quarter (use last month of the quarter)
report_date = datetime(2025, 3, 1)  # Example report date for Q2 (Jan–Mar)
month = report_date.month
report_year = report_date.year
current_quarter = get_custom_quarter(report_date)
# print(f"Reporting Quarter: {current_quarter}")

# Adjust the quarter calculation for custom quarters
if month in [10, 11, 12]:
    quarter = 1  # Q1: October–December
elif month in [1, 2, 3]:
    quarter = 2  # Q2: January–March
elif month in [4, 5, 6]:
    quarter = 3  # Q3: April–June
elif month in [7, 8, 9]:
    quarter = 4  # Q4: July–September

# Define a mapping for months to their corresponding quarter
quarter_months = {
    1: ['October', 'November', 'December'],  # Q1
    2: ['January', 'February', 'March'],    # Q2
    3: ['April', 'May', 'June'],            # Q3
    4: ['July', 'August', 'September']      # Q4
}

# Get the months for the current quarter
months_in_quarter = quarter_months[quarter]

# Calculate start and end month indices for the quarter
# all_months = [
#     'January', 'February', 'March', 
#     'April', 'May', 'June',
#     'July', 'August', 'September', 
#     'October', 'November', 'December'
# ]
# start_month_idx = (quarter - 1) * 3
# month_order = all_months[start_month_idx:start_month_idx + 3]

# ------------------------ Total Reviews ---------------------------- #

total_reviews = len(df)
# print('Total Reviews:', total_engagements)

# ------------------------ Services Provided ---------------------------- #

# print("Before: \n", df[''].unique().tolist())
# print("Value Counts: \n", df[''].unique().tolist())

_unique =[
    
]

# df[''] = (df['']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "" : ""
#     })          
# )

# print("After: \n", df[''].unique().tolist())

reviews = []
for month in months_in_quarter:
    reviews_in_month = df[df['Month'] == month].shape[0]  # Count the number of rows for each month
    reviews.append(reviews_in_month)
    # print(f'Clients Served in {month}:', clients_in_month)

df_reviews = pd.DataFrame(
    {
    'Month': months_in_quarter,
    'Reviews': reviews
    }
)

# print(df_)

client_fig = px.bar(
    df_reviews, 
    x='Month', 
    y='Reviews',
    labels={'Reviews': 'Number of Reviews'},
    color='Month', 
    text='Reviews',  
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=600, 
    width = 800,
    title=dict(
        text= f'{current_quarter} Reviews by Month',
        x=0.5, 
        font=dict(
            size=35,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text=None,
            # text="Month",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickvals=df_reviews['Month'].unique(),
        tickangle=0  
    ),
    legend=dict(
        # title='Administrative Activity',
        title=None,
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top" 
    ),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=20),  
    textposition='auto', 
    textangle=0, 
    hovertemplate=( 
        '<b>Name</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)

client_pie = px.pie(
    df_reviews,
    names='Month',
    values='Reviews',
    color='Month',
    height=550
).update_layout(
    title=dict(
        x=0.5,
        text=f'{current_quarter} Ratio of Clients Served', 
        font=dict(
            size=35,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    margin=dict(
        l=0, 
        r=0,  
        t=100,  
        b=0   
    )  
).update_traces(
    rotation=180,  #
    textfont=dict(size=19),  
    textinfo='value+percent',
    # texttemplate='<br>%{percent:.0%}', 
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# ------------------------ Health Issue ---------------------------- #

# The code is printing the unique values in the 'Health' column of a DataFrame called `df` as a list.
# print("Unique Health Before: \n", df['Health'].unique().tolist())
print("Health Value Counts: \n", df['Health'].value_counts())

_unique =[
    
]

df['Health'] = (df['Health']
    .astype(str)
    .str.strip()
    .replace({
        "" : ""
    })          
)

# print("After: \n", df[''].unique().tolist())

df_health = df['Health'].value_counts().reset_index(name='Count')

# health_reviews = []
# for month in months_in_quarter:
#     health_reviews_in_month = df[df['Month'] == month].shape[0]  # Count the number of rows for each month
#     reviews.append(reviews_in_month)
#     # print(f'Clients Served in {month}:', clients_in_month)

# df_reviews = pd.DataFrame(
#     {
#     'Month': months_in_quarter,
#     'Reviews': reviews
#     }
# )

df_health_counts = (
    df.groupby(['Month', 'Health'], sort=False)
    .size()
    .reset_index(name='Count')
)

df_health_counts['Month'] = pd.Categorical(
    df_health_counts['Month'],
    categories = months_in_quarter,
    ordered = True
)

df_health_counts = df_health_counts.sort_values(['Month', 'Health'])

# print(df_)

health_fig = px.bar(
    df_health_counts, 
    x='Month', 
    y='Count',
    color='Health', 
    text='Count',  
    barmode='group',
    labels={
        'Count': 'Count',
        'Month': 'Month',
        'Health': 'Health'
    },
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=600, 
    width = 800,
    title=dict(
        text= f'{current_quarter} How Clients are feeling about their health',
        x=0.5, 
        font=dict(
            size=25,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text=None,
            # text="Month",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickvals=df_reviews['Month'].unique(),
        tickangle=0  
    ),
    legend=dict(
        title='Rating',
        # title=None,
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top" 
    ),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=20),  
    textposition='auto', 
    textangle=0, 
    hovertemplate=( 
        '<b>Name</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)

health_pie = px.pie(
    df_health,
    names='Health',
    values='Count',
    color='Health',
    height=550
).update_layout(
    title=dict(
        x=0.5,
        text=f'{current_quarter} Ratio of How Clients are feeling about their health', 
        font=dict(
            size=25,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    legend=dict(
        title='Rating',
        # title=None,
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top" 
    ),
    margin=dict(
        l=0, 
        r=0,  
        t=100,  
        b=0   
    )  
).update_traces(
    rotation=180,  #
    textfont=dict(size=19),  
    textinfo='value+percent',
    # texttemplate='<br>%{percent:.0%}', 
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# --------------------------------- Stress Level -------------------------------- #



# --------------------- Mental Health ------------------------ # 



# --------------------- Physical Health ------------------------ #



# ------------------------ Impression of BMHC ? ---------------------------- #
# ------------------------ Provider Expectation ---------------------------- #
# ------------------------ Care Needs ---------------------------- #
# ------------------------ Outreach Support ---------------------------- #
# ------------------------ Healthy Cuts Membership ---------------------------- #



# # ========================== DataFrame Table ========================== #

# Engagement Table
engagement_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

engagement_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=60),  # Remove margins
    height=800,
    # width=1500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# ============================== Dash Application ========================== #

app = dash.Dash(__name__)
server= app.server 

app.layout = html.Div(
  children=[ 
    html.Div(
        className='divv', 
        children=[ 
          html.H1(
              f'BMHC Client Review Report {current_quarter} {report_year}', 
              className='title'),
          html.H2( 
              '01/01/2025 - 3/31/2024', 
              className='title2'),
          html.Div(
              className='btn-box', 
              children=[
                  html.A(
                    'Repo',
                    href= f'https://github.com/CxLos/Survey_{current_quarter}_{report_year}',
                    className='btn'),
    ]),
  ]),    

# Data Table
# html.Div(
#     className='row00',
#     children=[
#         html.Div(
#             className='graph00',
#             children=[
#                 html.Div(
#                     className='table',
#                     children=[
#                         html.H1(
#                             className='table-title',
#                             children='Client Review Table'
#                         )
#                     ]
#                 ),
#                 html.Div(
#                     className='table2', 
#                     children=[
#                         dcc.Graph(
#                             className='data',
#                             figure=survey_table
#                         )
#                     ]
#                 )
#             ]
#         ),
#     ]
# ),

# ROW 1
html.Div(
    className='row0',
    children=[
        html.Div(
            className='graph11',
            children=[
            html.Div(
                className='high1',
                children=[f'{current_quarter} Reviews']
            ),
            html.Div(
                className='circle1',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high3',
                            children=[total_reviews]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
        html.Div(
            className='graph22',
            children=[
            html.Div(
                className='high2',
                children=[f'{current_quarter} Placeholder']
            ),
            html.Div(
                className='circle2',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high4',
                            # children=[]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
    ]
),

# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph11',
            children=[
            html.Div(
                className='high1',
                children=[f'{current_quarter} Placeholder']
            ),
            html.Div(
                className='circle1',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high3',
                            # children=[]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    # figure=status_fig
                )
            ]
        ),
    ]
),

# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    figure=health_fig
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    figure=health_pie
                )
            ]
        ),
    ]
),

# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    # figure=hours_fig
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    # figure=hours_pie
                )
            ]
        ),
    ]
),

# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    # figure=travel_fig
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    # figure=travel_pie
                )
            ]
        ),
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=admin_fig
                )
            ]
        )
    ]
),
# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=admin_pie
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=care_fig
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=care_pie
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=comm_fig
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=comm_pie
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=person_fig
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    # figure=person_pie
                )
            ]
        )
    ]
),
])

print(f"Serving Flask app '{current_file}'! 🚀")

if __name__ == '__main__':
    app.run_server(debug=
                   True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = f'data/Survey_{current_quarter}_{report_year}.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.

# Heroku Setup:
# heroku login
# heroku create mc-impact-11-2024
# heroku git:remote -a mc-impact-11-2024
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a mc-impact-11-2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].

# rm -rf ~$bmhc_data_2024_cleaned.xlsx
# rm -rf ~$bmhc_data_2024.xlsx
# rm -rf ~$bmhc_q4_2024_cleaned2.xlsx

# print("Before: \n", df[''].unique().tolist())
# print("Value Counts: \n", df[''].unique().tolist())

_unique =[
    
]

# df[''] = (df['']
#     .astype(str)
#     .str.strip()
#     .replace({
#         "" : ""
#     })          
# )

# print("After: \n", df[''].unique().tolist())

b = []
for month in months_in_quarter:
    b_in_month = df[df['Month'] == month].shape[0]  # Count the number of rows for each month
    b.append(b_in_month)
    # print(f'Clients Served in {month}:', clients_in_month)

df_ = pd.DataFrame(
    {
    'Month': months_in_quarter,
    'Reviews': b
    }
)

# print(df_)

client_fig = px.bar(
    df_, 
    x='Month', 
    y='',
    labels={'': 'Number of Reviews'},
    color='Month', 
    text='Reviews',  
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=600, 
    width = 800,
    title=dict(
        text= f'{current_quarter} Reviews by Month',
        x=0.5, 
        font=dict(
            size=35,
            family='Calibri',
            color='black',
            )
    ),
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        title=dict(
            text=None,
            # text="Month",
            font=dict(size=20), 
        ),
        tickmode='array',
        tickvals=df_reviews['Month'].unique(),
        tickangle=0  
    ),
    legend=dict(
        # title='Administrative Activity',
        title=None,
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top" 
    ),
).update_traces(
    texttemplate='%{text}',
    textfont=dict(size=20),  
    textposition='auto', 
    textangle=0, 
    hovertemplate=( 
        '<b>Name</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)

client_pie = px.pie(
    df_reviews,
    names='Month',
    values='Reviews',
    color='Month',
    height=550
).update_layout(
    title=dict(
        x=0.5,
        text=f'{current_quarter} Ratio of Clients Served', 
        font=dict(
            size=35,  
            family='Calibri',  
            color='black'  
        ),
    ),  
    margin=dict(
        l=0, 
        r=0,  
        t=100,  
        b=0   
    )  
).update_traces(
    rotation=180,  #
    textfont=dict(size=19),  
    textinfo='value+percent',
    # texttemplate='<br>%{percent:.0%}', 
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)