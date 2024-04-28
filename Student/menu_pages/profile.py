import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from streamlit_gsheets import GSheetsConnection
from PIL import Image
import pandas as pd

# Google Sheets Connection
conn = st.connection("survey", type=GSheetsConnection)

# Title
st.caption('BUGHAW   |   STUDENTS\' PORTAL')
st.title(f'Welcome {st.session_state.name}! 👋')
st.write(f'Student ID: {st.session_state.student_id}')

def check_streak():
    sql = f"""SELECT Date FROM Sheet1 WHERE "Student ID"='{st.session_state.student_id}' ORDER BY Date;"""
    df = conn.query(sql=sql)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date_Diff'] = df['Date'].diff().dt.days
    df['Streak_ID'] = (df['Date_Diff'] > 1).cumsum()
    streaks = df.groupby('Streak_ID').cumcount() + 1

    return streaks.max()
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.metric('Answer Streak', f'{check_streak()} days', delta='Nice work!')

# Daily Survey
with st.expander('Daily Mood'):
    sql = f"""SELECT Mood FROM Sheet1 WHERE "Student ID" = '{st.session_state.student_id}' ORDER BY Date;"""
    df = conn.query(sql=sql, ttl=0).dropna(how = "all").reset_index(drop = True)

    def visualize_moods_with_images(df):
        mood_images = {
            'Happy': mpimg.imread('images/8_happy.png'),
            'Amused': mpimg.imread('images/7_amused.png'),
            'Inspired': mpimg.imread('images/6_inspired.png'),
            'Don\'t Care': mpimg.imread('images/5_dont_care.png'),
            'Annoyed': mpimg.imread('images/4_annoyed.png'),
            'Afraid': mpimg.imread('images/3_afraid.png'),
            'Sad': mpimg.imread('images/2_sad.png'),
            'Angry': mpimg.imread('images/1_angry.png')
        }

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.axis('off')

        rectangle = plt.Rectangle((0, 0), 10, 10, fill=False, edgecolor='white')
        ax.add_patch(rectangle)
        for i, mood in enumerate(df['Mood'].unique()):
            ax.imshow(mood_images[mood], extent=(i, i+1, 0, 1))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)

        st.pyplot(fig)

    visualize_moods_with_images(df)

# Weekly Survey
questions = """I can concentrate regularly.
I lose sleep over worrying.
I play a useful role in the community.
I can make the right decisions for myself.
I am always under stress.
I cannot overcome challenges.
I enjoy day-to-day activities.
I can face problems.
I feel sad and anxious.
I lose confidence.
I see myself as worthless.
I feel reasonably happy."""

question_lst = questions.split('\n')

with st.expander('Weekly Wellbeing'):
    sql = f"""SELECT "General Survey",Date FROM Sheet1 WHERE "Student ID" = '{st.session_state.student_id}' ORDER BY Date;"""
    df = conn.query(sql=sql, ttl=0)

    for i in range(12):
        df[i] = df['General Survey'].str[1:-1].str.split(',').str[i]
    option = st.selectbox('', question_lst, index=None)
    if option:
        ind = question_lst.index(option)
        filtered_df = df[['Date', ind]]

        fig = px.line(df, x='Date', y=ind, title='Response History')
        fig.update_traces(line=dict(width=2, color='DarkSlateGrey'))

        st.plotly_chart(fig, use_container_width=True)

# Monthly Survey
questions = """Do you have the feeling that you don’t really care about what goes on around you?
Has it happened in the past that you were surprised by the behaviour of people whom you thought you knew well?
Has it happened that people whom you counted on disappointed you?
Until now your life has had: no clear goals or purpose at all—very clear goals and purpose
Do you have the feeling that you’re being treated unfairly?
Do you have the feeling that you are in an unfamiliar situation and don’t know what to do?
Doing the things you do every day is: a source of deep pleasure and satisfaction—a source of pain and boredom
Do you have very mixed-up feelings and ideas?
Does it happen that you have feelings inside you would rather not feel?
Many people—even those with strong character—sometimes feel like sad losers in certain situations. How often have you felt this way in the past?
When something has happened have you generally found that: you overestimated or underestimated its importance—you saw things in the right proportion
How often do you have the feeling that there's little meaning in the things you doin your daily life?
How often do you have the feeling that you’re not sure you can keep under control?"""

question_lst = questions.split('\n')

with st.expander('Monthly Wellbeing'):
    sql = f"""SELECT "Monthly Survey",Date FROM Sheet1 WHERE "Student ID" = '{st.session_state.student_id}' ORDER BY Date;"""
    df = conn.query(sql=sql, ttl=0)

    for i in range(12):
        df[i] = df['Monthly Survey'].str[1:-1].str.split(',').str[i]
    option = st.selectbox('', question_lst, index=None)
    if option:
        ind = question_lst.index(option)
        filtered_df = df[['Date', ind]]

        fig = px.line(df, x='Date', y=ind, title='Response History')
        fig.update_traces(line=dict(width=2, color='DarkSlateGrey'))

        st.plotly_chart(fig, use_container_width=True)