import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_gsheets import GSheetsConnection
from st_pages import Page, Section,show_pages, add_page_title, hide_pages
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_image_select import image_select
import control_flow as cf
from streamlit.components.v1 import html
import datetime
from PIL import Image

# Set page config
st.set_page_config(page_title='Bughaw Students\' Portal', page_icon='💙', layout="centered", initial_sidebar_state="auto", menu_items=None)

# Google Sheets Connection
conn = st.connection("user", type=GSheetsConnection)

# Update Google sheets
def update_data(survey_type):
    df = conn.read(worksheet='Sheet1', ttl=0)
    now = datetime.datetime.now()

    df.loc[len(df.index)] = [
        st.session_state.student_id,
        now,
        st.session_state.ga if survey_type=='g' else None,
        st.session_state.ma if survey_type=='m' else None,
        st.session_state.mood if survey_type=='d' else None
    ]

    conn.update(worksheet="Sheet1", data=df)
    st.success("Worksheet Updated! 🥳")


# Initialize
cf.load_initial_data_if_needed(force = True)

# Title
st.image('images/BUGHAW.png', width=150)
add_vertical_space(1)
st.caption('BUGHAW   |   STUDENTS\' PORTAL')

add_vertical_space(1)
st.markdown(f"""
    <div style="line-height:450%;">
        <span style=" font-size:80px ; color:#023E8A ; font-weight:bold; ">From blue </span>
        <span style=" font-size:80px ; color:#31333F ; font-weight:bold; ">to every hue</span>
        <span style=" font-size:80px ; color:#31333F ; font-weight:bold; ">.</span>
    </div>""",
    unsafe_allow_html=True
)

placeholder = st.empty()
with placeholder:
    with st.container(border=True):
        st.write('🔓 Try this sample student ID: s222869, password: hello876')

# User Authentication
def check_password():
    # Log-in
    def log_in():
        with st.form('Credentials'):
            st.text_input("Enter your student ID", type='default', key='student_id_input')
            st.text_input("Enter your password", type="password", key="password")
            st.form_submit_button("Log-in", on_click=password_entered)
 
    def password_entered():
        sql = 'SELECT * FROM Sheet1;'
        df = conn.query(sql=sql, ttl=0) 
        match = (df['user_id'].eq(st.session_state.student_id_input) & df['password'].eq(st.session_state.password)).any()
        if match:
            st.session_state["student_id"] = st.session_state.student_id_input
            st.session_state["password_correct"] = True  
            st.session_state['name'] = df[df.user_id == st.session_state.student_id].reset_index().at[0,'nickname']
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    log_in()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

if not check_password():
    st.stop()

# Start
placeholder.empty()

# Information about the app
st.write('Welcome to Bughaw Students\' Portal. Here, we believe that mental well-being is a fundamental aspect of student success. Our platform is dedicated to providing you with the tools and support you need to navigate the challenges of academic life while prioritizing your mental health. Whether you\'re looking for self-care resources, seeking guidance from a counselor, or connecting with peers in a safe space, Bughaw is here for you. Join us on your journey to empowerment and resilience.')
col1, col2 = st.columns(2)
with col1:
    with st.expander(label='WHAT IS BUGHAW', expanded=False):
        st.write("Bughaw is a web-based platform designed to address mental health issues among Filipino students, offering features like well-being check-ins, personalized toolkits, appointment scheduling, and anonymous support groups. It aims to provide accessible and data-driven solutions for students and counselors alike. ")
with col2:
    with st.expander(label='WHY BUGHAW'):
        section_text = ''
        st.markdown("The current counselor-to-student proportion among Philippine schools faces a staggering alarming ratio of 1 counselor for every 14,000 students, compared to the recommended global standard of 1:250. Hence, there is a growing need to further address this declining mental health and wellbeing among Filipino high school and college students.")

# Daily wellbeing
st.session_state.mood_button = False
with st.expander(label=f'📅 How are you today, {st.session_state.name}?'):
    st.write(f"🌱 Selet your mood for today by clicking on the corresponding image.")
    mood_lst = ["Happy", "Amused", "Inspired", "Don't Care", "Annoyed", "Afraid", "Sad", "Angry"]

    # Display mood images and get user input
    selected_mood = image_select(label="", images=["images/8_happy.png", "images/7_amused.png", 
                                                "images/6_inspired.png", "images/5_dont_care.png",
                                                "images/4_annoyed.png", "images/3_afraid.png",
                                                "images/2_sad.png", "images/1_angry.png"], 
                                                use_container_width=False,
                                                captions=["Happy", "Amused", "Inspired", "Don't Care",
                                                            "Annoyed", "Afraid", "Sad", "Angry"],
                                                    return_value="index")
    st.session_state.mood = mood_lst[int(str(selected_mood)[:100])]

    button = st.button('Submit')

    if button:
        st.session_state.mood_button = True
    
    if st.session_state.mood_button:
        update_data('d')

# Welcome
show_pages(
    [
        Page('Home.py', 'Homepage', '👤'),
        Page('menu_pages/wellbeing.py', 'Student Wellbeing', '📊'),
        Page('menu_pages/profile.py', f'{st.session_state.name}\'s Profile', '🧑'),
        Page('menu_pages/toolkit.py', f'{st.session_state.name}\'s Toolkit', '🛠️'),
        Page('menu_pages/appointment.py', 'Set an Appointment', '📄'),
        Page('menu_pages/support.py', 'Chat with Support Group', '🫂'),
        Page('menu_pages/counselor.py', 'Chat with Counselor', '💬'),
        Page('menu_pages/about.py', 'About', '💡'),
        Page('menu_pages/study.py', 'Study', '💡'),
        Page('menu_pages/meditate.py', 'Meditate', '🧘'),
        Page('menu_pages/read.py', 'Read', '📚')
    ]
)

def hide_page(page_name, **kwargs):
    _inject_page_script(page_name, 'link.style.display = "none";', **kwargs)

def show_page(page_name, **kwargs):
    _inject_page_script(page_name, 'link.style.display = "";', **kwargs)

def disable_page(page_name, **kwargs):
    _inject_page_script(page_name, 'link.style.pointerEvents = "none"; '
                                   'link.style.opacity = 0.5;', **kwargs)

def enable_page(page_name, **kwargs):
    _inject_page_script(page_name, 'link.style.pointerEvents = ""; '
                                   'link.style.opacity = "";', **kwargs)

def _inject_page_script(page_name, action_script, timeout_secs=3):
    page_script = """
        <script type="text/javascript">
            function attempt_exec_page_action(page_name, start_time, timeout_secs, action_fn) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        action_fn(links[i]);
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_exec_page_action, 100, page_name, start_time, timeout_secs, action_fn);
                } else {
                    alert("Unable to locate link to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_exec_page_action("%s", new Date(), %d, function(link) {
                    %s
                });
            });
        </script>
    """ % (page_name, timeout_secs, action_script)
    html(page_script, height=0)

hide_page("study")
hide_page("meditate")
hide_page("read")

# About Bughaw
st.header('Get to know your Bughaw!')

# Impact
st.caption('IMPACT BY NUMBERS')
col1, col2, col3 = st.columns(3)
row1= [col1, col2, col3]
homepage_impact = {
    0 : ['Active Students', '2748 🧑‍🎓', 1406],
    1 : ['Successful Consultations', '376 🫂', 8],
    2 : ['Mental Health Volunteers', '49 💙', 16]

}
for ind, col in enumerate(row1):
    col.metric(label=homepage_impact[ind][0], value=homepage_impact[ind][1], delta=homepage_impact[ind][2])

style_metric_cards(border_left_color='#023E8A', border_radius_px=7, box_shadow=False)

st.divider()

# Features Overview
import streamlit as st

option = st.radio('Get to know Bughaw\'s features!', ['Student Wellbeing', 'Profile', 'Toolkit', 'Appointment', 'Support Group Chat', 'Counselor Chat'])

descriptions = {
    'Student Wellbeing': '''
        Bughaw's Student Wellbeing feature is designed to make mental health resources and support accessible to people regardless of location, income, or cultural background. Through this feature, users can access a diverse range of mental health resources, including articles, videos, and self-help tools, available in multiple languages. Additionally, Bughaw provides a directory of local mental health services and support groups, ensuring that users can find assistance tailored to their specific needs and circumstances.
    ''',

    'Profile': '''
        The Profile feature allows users to create personalized profiles where they can track their mental health journey and set wellness goals. By regularly updating their profiles with mood indicators, journal entries, and self-assessment tools, users can monitor their mental health status and identify early warning signs of mental health struggles. Bughaw utilizes machine learning algorithms to analyze user data and provide personalized recommendations for mental wellness activities and resources.
    ''',

    'Toolkit': '''
        Bughaw's Toolkit feature empowers individuals to create their own mental wellness toolkit with techniques that work for them. Users can explore a variety of evidence-based coping strategies, such as mindfulness exercises, breathing techniques, and relaxation techniques, and add their favorites to their toolkit. The toolkit also includes customizable self-care plans and reminders, helping users integrate mental wellness practices into their daily routines and manage stress more effectively.
    ''',

    'Appointment': '''
        The Appointment feature allows users to schedule confidential appointments with licensed mental health professionals, including counselors, therapists, and psychiatrists. Through Bughaw's secure telehealth platform, users can connect with providers via video conferencing or messaging, eliminating barriers to accessing mental health care, such as long wait times and transportation issues. Bughaw also offers flexible payment options, including sliding-scale fees and insurance billing, to ensure affordability and accessibility.
    ''',

    'Support Group Chat': '''
        Bughaw's Support Group Chat feature provides a creative way to anonymously connect people seeking support with those willing to offer it. Users can join virtual support groups based on shared experiences or interests, such as depression, anxiety, LGBTQ+ identity, or student stress. Within these supportive communities, users can engage in group discussions, share coping strategies, and offer mutual encouragement and understanding, fostering a sense of belonging and connection.
    ''',

    'Counselor Chat': '''
        Bughaw's Counselor Chat feature leverages technology to offer self-soothing tools and guided techniques for managing acute anxiety or panic attacks. Users can access a variety of resources, such as relaxation exercises, grounding techniques, and cognitive-behavioral therapy (CBT) interventions, designed to help them cope with distressing symptoms in real-time. Additionally, users have the option to connect with licensed counselors and crisis intervention specialists for immediate support and guidance.
    '''
}

emoji = {
    'Student Wellbeing': "Student Wellbeing 📊",
    'Profile': "Profile 🧑",
    'Toolkit': "Toolkit 🛠️",
    'Appointment': "Appointment 📄",
    'Support Group Chat': "Support Group Chat 🫂",
    'Counselor Chat': "Counselor Chat 💬"
}

with st.container(border=True):
    st.subheader(emoji[option])
    st.write(descriptions[option])