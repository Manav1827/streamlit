# import streamlit as st
# from components import navbar

# st.set_page_config(page_title="Reel & Invitation Creator", page_icon="🎨", layout="wide")
# navbar.show_navbar()

# st.title("🎨 Reel & Invitation Creator")
# st.subheader("Welcome! Create stunning reels and invitations with AI ✨")

# st.markdown(
#     """
#     🚀 **Features**:
#     - AI-based invitation & reel generation.
#     - Frame-by-frame editing.
#     - Templates and customization.
#     """
# )

# st.page_link("pages/2_Create_New.py", label="🎬 Start Creating", icon="🎥")
# st.page_link("pages/3_My_Projects.py", label="📁 My Projects", icon="📂")
# st.page_link("pages/4_Templates.py", label="📑 Templates", icon="🗂️")
# st.page_link("pages/5_Profile.py", label="👤 Profile & Settings", icon="⚙️")
# st.page_link("pages/6_Inspiration.py", label="🌟 Inspiration", icon="✨")



# import streamlit as st
# from components import navbar
# import requests
# import streamlit.components.v1 as components


# # ---------------- APP CONFIG -----------------
# st.set_page_config(page_title="Reel & Invitation Creator", page_icon="🎨", layout="wide")

# # ---------------- FIREBASE CONFIG -----------------
# FIREBASE_WEB_API_KEY = "AIzaSyC9hbgiYgRwUSMD-ykdo-gG3gp-wy8PNlQ"  # <<< Add your key here

# # Firebase endpoints
# firebase_signup = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
# firebase_signin = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"


# # ---------------- SESSION PAGE HANDLER -----------------
# if "page" not in st.session_state:
#     st.session_state.page = "welcome"
# if "user" not in st.session_state:
#     st.session_state.user = None


# # ---------------- WELCOME SCREEN -----------------
# if st.session_state.page == "welcome":
#     st.title("🎬 Welcome to Reel & Invitation Creator")
#     st.subheader("✨ Create stunning reels, invitations, and more!")

#     st.markdown("""
#     🚀 **Features:**
#     - 🎥 AI-based reel and invitation generation
#     - 🧠 Smart templates and automation
#     - 🔥 Customize with photos, videos, and audio
#     """)

#     if st.button("Get Started"):
#         st.session_state.page = "auth"


# # ---------------- AUTH SCREEN -----------------
# if st.session_state.page == "auth":
#     st.subheader("🔐 Sign Up / Login")

#     auth_tab = st.tabs(["Login", "Sign Up"])

#     with auth_tab[0]:
#         st.write("### Login")
#         email = st.text_input("Email", key="login_email")
#         password = st.text_input("Password", type="password", key="login_password")

#         if st.button("Login"):
#             payload = {
#                 "email": email,
#                 "password": password,
#                 "returnSecureToken": True
#             }
#             req = requests.post(firebase_signin, json=payload)

#             if req.status_code == 200:
#                 st.success("✅ Logged in successfully!")
#                 st.session_state.user = req.json()
#                 st.session_state.page = "main"
#             else:
#                 st.error("❌ Invalid email or password")

#     with auth_tab[1]:
#         st.write("### Sign Up")
#         new_email = st.text_input("Email", key="signup_email")
#         new_password = st.text_input("Password (6+ chars)", type="password", key="signup_password")

#         if st.button("Sign Up"):
#             payload = {
#                 "email": new_email,
#                 "password": new_password,
#                 "returnSecureToken": True
#             }
#             req = requests.post(firebase_signup, json=payload)

#             if req.status_code == 200:
#                 st.success("✅ Account created successfully!")
#                 st.session_state.user = req.json()
#                 st.session_state.page = "main"
#             else:
#                 st.error(f"❌ {req.json().get('error', {}).get('message', 'Error occurred')}")


# # ---------------- MAIN APP SCREEN -----------------
# if st.session_state.page == "main":
#     navbar.show_navbar()

#     st.title("🎨 Reel & Invitation Creator")
#     st.subheader(f"Welcome {st.session_state.user.get('email', 'User')}! 🎉")

#     st.markdown(
#         """
#         🚀 **Features:**
#         - AI-based invitation & reel generation.
#         - Frame-by-frame editing.
#         - Templates and customization.
#         """
#     )

#     # ---------------- PAGE LINKS -----------------
#     st.page_link("pages/2_Create_New.py", label="🎬 Start Creating", icon="🎥")
#     st.page_link("pages/3_My_Projects.py", label="📁 My Projects", icon="📂")
#     st.page_link("pages/4_Templates.py", label="📑 Templates", icon="🗂️")
#     st.page_link("pages/5_Profile.py", label="👤 Profile & Settings", icon="⚙️")
#     st.page_link("pages/6_Inspiration.py", label="🌟 Inspiration", icon="✨")

#     st.divider()

#     # ---------------- FILE UPLOAD -----------------
#     st.subheader("📤 Upload Photos / Videos")
#     uploaded_files = st.file_uploader(
#         "Upload your media files (images/videos)",
#         accept_multiple_files=True,
#         type=['png', 'jpg', 'jpeg', 'mp4']
#     )

#     if uploaded_files:
#         for file in uploaded_files:
#             st.success(f"✅ Uploaded: {file.name}")

#     st.divider()

#     # ---------------- MICROPHONE RECORDING -----------------
#     st.subheader("🎙️ Record Audio (Beta)")

#     audio_html = """
#     <script>
#     let recorder;
#     navigator.mediaDevices.getUserMedia({ audio: true })
#         .then(function(stream) {
#             recorder = new MediaRecorder(stream);
#             let chunks = [];
#             recorder.ondataavailable = e => chunks.push(e.data);
#             recorder.onstop = e => {
#                 let blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
#                 let audioURL = window.URL.createObjectURL(blob);
#                 var player = document.getElementById('audio-player');
#                 player.src = audioURL;
#                 player.style.display = 'block';
#             }
#             window.startRecording = () => { chunks = []; recorder.start(); }
#             window.stopRecording = () => { recorder.stop(); }
#         });
#     </script>
#     <button onclick="startRecording()">⏺️ Start Recording</button>
#     <button onclick="stopRecording()">⏹️ Stop Recording</button>
#     <br>
#     <audio id="audio-player" controls style="display:none"></audio>
#     """
#     components.html(audio_html, height=300)

#     st.divider()

#     # ---------------- LOGOUT -----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.page = "auth"
#         st.session_state.user = None



# import streamlit as st

# import requests
# import streamlit.components.v1 as components


# # ---------------- APP CONFIG -----------------
# st.set_page_config(page_title="Reel & Invitation Creator", page_icon="🎨", layout="wide")

# # ---------------- FIREBASE CONFIG -----------------
# FIREBASE_WEB_API_KEY = "AIzaSyC9hbgiYgRwUSMD-ykdo-gG3gp-wy8PNlQ"  # Your Firebase Web API Key

# firebase_signup = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
# firebase_signin = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"


# # ---------------- SESSION -----------------
# if "page" not in st.session_state:
#     st.session_state.page = "welcome"
# if "user" not in st.session_state:
#     st.session_state.user = None


# # ---------------- WELCOME SCREEN -----------------
# if st.session_state.page == "welcome":
#     st.title("🎬 Welcome to Reel & Invitation Creator")
#     st.subheader("✨ Create stunning reels, invitations, and more!")

#     st.markdown("""
#     🚀 **Features:**
#     - 🎥 Create Reels & Invitations
#     - 🧠 AI-based smart templates
#     - 🔥 Add personal photos, audio, and stickers
#     - 🎶 Record voice or upload background music
#     """)

#     st.image("assets/welcome_banner.png", use_column_width=True)  # Optional image

#     st.divider()

#     st.info("🔐 **Login or Sign Up to continue**")

#     if st.button("➡️ Get Started"):
#         st.session_state.page = "auth"


# # ---------------- AUTH SCREEN -----------------
# if st.session_state.page == "auth":
#     st.subheader("🔐 Sign Up / Login")

#     auth_tabs = st.tabs(["Login", "Sign Up"])

#     # ---- LOGIN TAB ----
#     with auth_tabs[0]:
#         st.subheader("Login")
#         email = st.text_input("Email", key="login_email")
#         password = st.text_input("Password", type="password", key="login_password")

#         if st.button("Login"):
#             payload = {
#                 "email": email,
#                 "password": password,
#                 "returnSecureToken": True
#             }
#             req = requests.post(firebase_signin, json=payload)

#             if req.status_code == 200:
#                 st.success("✅ Logged in successfully!")
#                 st.session_state.user = req.json()
#                 st.session_state.page = "main"
#             else:
#                 error = req.json().get('error', {}).get('message', 'Error')
#                 st.error(f"❌ {error}")

#     # ---- SIGN UP TAB ----
#     with auth_tabs[1]:
#         st.subheader("Sign Up")
#         new_email = st.text_input("Email", key="signup_email")
#         new_password = st.text_input("Password (6+ characters)", type="password", key="signup_password")

#         if st.button("Sign Up"):
#             payload = {
#                 "email": new_email,
#                 "password": new_password,
#                 "returnSecureToken": True
#             }
#             req = requests.post(firebase_signup, json=payload)

#             if req.status_code == 200:
#                 st.success("✅ Account created successfully!")
#                 st.session_state.user = req.json()
#                 st.session_state.page = "main"
#             else:
#                 error = req.json().get('error', {}).get('message', 'Error')
#                 st.error(f"❌ {error}")

#     st.divider()

#     st.markdown("👉 Don't have an account? Use the **Sign Up** tab.")

#     # ---- SOCIAL AUTH PLACEHOLDER ----
#     st.info("🟦 **Google / Facebook login coming soon...**")


# # ---------------- MAIN APP SCREEN -----------------
# if st.session_state.page == "main":
#     if st.session_state.user is None:
#         st.warning("🚫 Please login to access the app.")
#         st.stop()

    
#     st.title("🎨 Reel & Invitation Creator")
#     st.subheader(f"👋 Welcome {st.session_state.user.get('email', 'User')}!")

#     st.markdown("""
#     🔥 **App Features:**
#     - 🎥 Create reels with your media
#     - 📄 Beautiful invitation videos
#     - 🎨 Templates, stickers, and background music
#     """)

#     # ---------------- PAGE LINKS -----------------
#     st.page_link("pages/2_Create_New.py", label="🎬 Start Creating", icon="🎥")
#     st.page_link("pages/3_My_Projects.py", label="📁 My Projects", icon="📂")
#     st.page_link("pages/4_Templates.py", label="📑 Templates", icon="🗂️")
#     st.page_link("pages/5_Profile.py", label="👤 Profile & Settings", icon="⚙️")
#     st.page_link("pages/6_Inspiration.py", label="🌟 Inspiration", icon="✨")

#     st.divider()

#     # ---------------- FILE UPLOAD -----------------
#     st.subheader("📤 Media Access Permission")

#     if "media_permission" not in st.session_state:
#         st.session_state.media_permission = False

#     # Request Permission UI
#     if not st.session_state.media_permission:
#         st.info("🔐 This app needs permission to access your photos and videos to generate reels and invitations.")

#         if st.button("✅ Allow Access to Photos/Videos"):
#             st.session_state.media_permission = True
#             st.success("✅ Permission Granted")

#     else:
#         st.subheader("📤 Upload Your Photos / Videos")

#         uploaded_files = st.file_uploader(
#             "Upload your media files (images/videos)",
#             accept_multiple_files=True,
#             type=['png', 'jpg', 'jpeg', 'mp4']
#         )

#         if uploaded_files:
#             for file in uploaded_files:
#                 st.success(f"✅ Uploaded: {file.name}")

#         if st.button("🔒 Revoke Access"):
#             st.session_state.media_permission = False
#             st.info("🚫 Access to photos/videos has been revoked.")

#     st.divider()

#     # ---------------- MICROPHONE RECORDING -----------------
#     st.subheader("🎙️ Record Audio (Permission Needed)")

#     st.info("Note: You may be prompted by your browser to allow microphone access.")

#     audio_html = """
#     <script>
#     let recorder;
#     navigator.mediaDevices.getUserMedia({ audio: true })
#         .then(function(stream) {
#             recorder = new MediaRecorder(stream);
#             let chunks = [];
#             recorder.ondataavailable = e => chunks.push(e.data);
#             recorder.onstop = e => {
#                 let blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
#                 let audioURL = window.URL.createObjectURL(blob);
#                 var player = document.getElementById('audio-player');
#                 player.src = audioURL;
#                 player.style.display = 'block';
#             }
#             window.startRecording = () => { chunks = []; recorder.start(); }
#             window.stopRecording = () => { recorder.stop(); }
#         });
#     </script>
#     <button onclick="startRecording()">⏺️ Start Recording</button>
#     <button onclick="stopRecording()">⏹️ Stop Recording</button>
#     <br>
#     <audio id="audio-player" controls style="display:none"></audio>
#     """
#     components.html(audio_html, height=300)

#     st.divider()

#     # ---------------- LOGOUT -----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.page = "auth"
#         st.session_state.user = None



# import streamlit as st
# import requests
# import streamlit.components.v1 as components

# # ---------------- APP CONFIG -----------------
# st.set_page_config(page_title="Reel & Invitation Creator", page_icon="🎨", layout="wide")

# # ---------------- CUSTOM CSS -----------------
# def load_css():
#     st.markdown("""
#     <style>
#     /* Hide Streamlit default elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* Main app styling */
#     .stApp {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }
    
#     /* Custom header */
#     .custom-header {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         padding: 1rem 2rem;
#         border-radius: 15px;
#         margin-bottom: 2rem;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
#     }
    
#     .logo-title {
#         font-size: 1.5rem;
#         font-weight: bold;
#         color: white;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }
    
#     .user-info {
#         color: white;
#         display: flex;
#         align-items: center;
#         gap: 1rem;
#     }
    
#     /* Welcome screen */
#     .welcome-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         color: white;
#     }
    
#     .welcome-title {
#         font-size: 4rem;
#         font-weight: bold;
#         margin-bottom: 1rem;
#         background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#     }
    
#     .welcome-subtitle {
#         font-size: 1.5rem;
#         margin-bottom: 3rem;
#         opacity: 0.9;
#     }
    
#     /* Feature cards */
#     .feature-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
#         gap: 2rem;
#         margin: 3rem 0;
#     }
    
#     .feature-card {
#         background: rgba(255, 255, 255, 0.15);
#         backdrop-filter: blur(10px);
#         padding: 2rem;
#         border-radius: 20px;
#         text-align: center;
#         color: white;
#         transition: all 0.3s ease;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#         box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
#     }
    
#     .feature-card:hover {
#         transform: translateY(-10px);
#         box-shadow: 0 20px 40px rgba(31, 38, 135, 0.5);
#     }
    
#     .feature-icon {
#         font-size: 3rem;
#         margin-bottom: 1rem;
#     }
    
#     .feature-title {
#         font-size: 1.5rem;
#         font-weight: bold;
#         margin-bottom: 1rem;
#     }
    
#     .feature-desc {
#         opacity: 0.8;
#         line-height: 1.6;
#     }
    
#     /* CTA Button */
#     .cta-button {
#         background: linear-gradient(45deg, #ff6b6b, #ffa500);
#         color: white;
#         padding: 1rem 3rem;
#         border: none;
#         border-radius: 50px;
#         font-size: 1.2rem;
#         font-weight: bold;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
#         text-decoration: none;
#         display: inline-block;
#         margin: 2rem 0;
#     }
    
#     .cta-button:hover {
#         transform: translateY(-3px);
#         box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
#     }
    
#     /* Auth screen */
#     .auth-container {
#         max-width: 400px;
#         margin: 0 auto;
#         padding: 2rem;
#         background: rgba(255, 255, 255, 0.95);
#         border-radius: 20px;
#         box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
#         text-align: center;
#     }
    
#     .auth-title {
#         font-size: 2rem;
#         margin-bottom: 1rem;
#         color: #333;
#     }
    
#     .auth-subtitle {
#         color: #666;
#         margin-bottom: 2rem;
#     }
    
#     /* Action cards for main screen */
#     .action-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
#         gap: 1.5rem;
#         margin: 2rem 0;
#     }
    
#     .action-card {
#         background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px);
#         padding: 2rem;
#         border-radius: 15px;
#         text-align: center;
#         color: white;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#     }
    
#     .action-card:hover {
#         background: rgba(255, 255, 255, 0.3);
#         transform: translateY(-5px);
#     }
    
#     .action-icon {
#         font-size: 2.5rem;
#         margin-bottom: 1rem;
#     }
    
#     .action-title {
#         font-size: 1.2rem;
#         font-weight: bold;
#         margin-bottom: 0.5rem;
#     }
    
#     .action-desc {
#         opacity: 0.8;
#         font-size: 0.9rem;
#     }
    
#     /* Permission card */
#     .permission-card {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         padding: 2rem;
#         border-radius: 20px;
#         text-align: center;
#         color: white;
#         margin: 2rem 0;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#     }
    
#     .permission-icon {
#         font-size: 4rem;
#         margin-bottom: 1rem;
#     }
    
#     /* Floating icons */
#     .floating-icons {
#         position: fixed;
#         right: 2rem;
#         top: 50%;
#         transform: translateY(-50%);
#         display: flex;
#         flex-direction: column;
#         gap: 1rem;
#         z-index: 1000;
#     }
    
#     .floating-icon {
#         width: 60px;
#         height: 60px;
#         background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px);
#         border-radius: 15px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1.5rem;
#         color: white;
#         cursor: pointer;
#         transition: all 0.3s ease;
#     }
    
#     .floating-icon:hover {
#         background: rgba(255, 255, 255, 0.3);
#         transform: scale(1.1);
#     }
    
#     /* Hide Streamlit widgets styling */
#     .stButton > button {
#         background: linear-gradient(45deg, #667eea, #764ba2);
#         color: white;
#         border: none;
#         border-radius: 10px;
#         padding: 0.5rem 2rem;
#         font-weight: bold;
#         transition: all 0.3s ease;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
#     }
    
#     /* Tab styling */
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 2rem;
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 10px;
#         padding: 0.5rem;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: white;
#         background: transparent;
#         border-radius: 8px;
#         padding: 0.5rem 1rem;
#     }
    
#     .stTabs [aria-selected="true"] {
#         background: rgba(255, 255, 255, 0.2);
#     }
    
#     /* Input styling */
#     .stTextInput > div > div > input {
#         background: rgba(255, 255, 255, 0.9);
#         border: none;
#         border-radius: 10px;
#         padding: 1rem;
#     }
    
#     /* Responsive */
#     @media (max-width: 768px) {
#         .feature-grid {
#             grid-template-columns: 1fr;
#         }
#         .action-grid {
#             grid-template-columns: 1fr;
#         }
#         .floating-icons {
#             display: none;
#         }
#         .welcome-title {
#             font-size: 2.5rem;
#         }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Load CSS
# load_css()

# # ---------------- FIREBASE CONFIG -----------------
# FIREBASE_WEB_API_KEY = "AIzaSyC9hbgiYgRwUSMD-ykdo-gG3gp-wy8PNlQ"
# firebase_signup = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
# firebase_signin = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

# # ---------------- SESSION -----------------
# if "page" not in st.session_state:
#     st.session_state.page = "welcome"
# if "user" not in st.session_state:
#     st.session_state.user = None

# # ---------------- FLOATING ICONS -----------------
# def render_floating_icons():
#     st.markdown("""
#     <div class="floating-icons">
#         <div class="floating-icon" title="Profile">🎨</div>
#         <div class="floating-icon" title="Camera">📹</div>
#         <div class="floating-icon" title="Music">🎵</div>
#         <div class="floating-icon" title="Magic">✨</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ---------------- WELCOME SCREEN -----------------
# if st.session_state.page == "welcome":
#     render_floating_icons()
    
#     st.markdown("""
#     <div class="welcome-container">
#         <h1 class="welcome-title">Creator</h1>
#         <p class="welcome-subtitle">✨ Create stunning reels, invitations, and more!</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Feature cards
#     st.markdown("""
#     <div class="feature-grid">
#         <div class="feature-card">
#             <div class="feature-icon">📹</div>
#             <div class="feature-title">Create Reels & Invitations</div>
#             <div class="feature-desc">Professional quality videos in minutes</div>
#         </div>
#         <div class="feature-card">
#             <div class="feature-icon">🧠</div>
#             <div class="feature-title">AI-Based Templates</div>
#             <div class="feature-desc">Smart templates that adapt to your content</div>
#         </div>
#         <div class="feature-card">
#             <div class="feature-icon">🖼️</div>
#             <div class="feature-title">Rich Media Support</div>
#             <div class="feature-desc">Photos, audio, stickers and animations</div>
#         </div>
#         <div class="feature-card">
#             <div class="feature-icon">🎙️</div>
#             <div class="feature-title">Voice Recording</div>
#             <div class="feature-desc">Record voice or upload background music</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # CTA Button
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         if st.button("🚀 Get Started", key="get_started"):
#             st.session_state.page = "auth"

# # ---------------- AUTH SCREEN -----------------
# elif st.session_state.page == "auth":
#     # Center the auth form
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown("""
#         <div class="auth-container">
#             <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
#             <h2 class="auth-title">Welcome Back</h2>
#             <p class="auth-subtitle">Sign in to continue creating amazing content</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         auth_tabs = st.tabs(["Login", "Sign Up"])
        
#         # ---- LOGIN TAB ----
#         with auth_tabs[0]:
#             st.markdown("### Email Address")
#             email = st.text_input("", placeholder="Enter your email", key="login_email", label_visibility="collapsed")
            
#             st.markdown("### Password")
#             password = st.text_input("", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
            
#             if st.button("🚀 Login", key="login_btn", use_container_width=True):
#                 payload = {
#                     "email": email,
#                     "password": password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signin, json=payload)
                
#                 if req.status_code == 200:
#                     st.success("✅ Logged in successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     error = req.json().get('error', {}).get('message', 'Error')
#                     st.error(f"❌ {error}")
        
#         # ---- SIGN UP TAB ----
#         with auth_tabs[1]:
#             st.markdown("### Email Address")
#             new_email = st.text_input("", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
            
#             st.markdown("### Password")
#             new_password = st.text_input("", type="password", placeholder="Enter your password (6+ characters)", key="signup_password", label_visibility="collapsed")
            
#             if st.button("🚀 Sign Up", key="signup_btn", use_container_width=True):
#                 payload = {
#                     "email": new_email,
#                     "password": new_password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signup, json=payload)
                
#                 if req.status_code == 200:
#                     st.success("✅ Account created successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     error = req.json().get('error', {}).get('message', 'Error')
#                     st.error(f"❌ {error}")
        
#         st.markdown("---")
#         st.markdown("**More authentication options coming soon...**")
        
#         # Social auth buttons
#         col1, col2 = st.columns(2)
#         with col1:
#             st.button("📧 Google", disabled=True, use_container_width=True)
#         with col2:
#             st.button("📘 Facebook", disabled=True, use_container_width=True)
        
#         if st.button("← Back to Home", key="back_home"):
#             st.session_state.page = "welcome"
#             st.rerun()

# # ---------------- MAIN APP SCREEN -----------------
# elif st.session_state.page == "main":
#     if st.session_state.user is None:
#         st.warning("🚫 Please login to access the app.")
#         st.stop()
    
#     # Custom header
#     st.markdown(f"""
#     <div class="custom-header">
#         <div class="logo-title">
#             🎨 Reel & Invitation Creator
#         </div>
#         <div class="user-info">
#             👋 Welcome {st.session_state.user.get('email', 'User').split('@')[0]}!
#             <button onclick="location.reload()" style="background: #ff4757; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">🚪 Logout</button>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # App Features section
#     st.markdown("""
#     <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 2rem; border-radius: 15px; margin: 2rem 0; color: white;">
#         <h2 style="margin-bottom: 1rem;">🔥 App Features</h2>
#         <div style="display: flex; flex-wrap: wrap; gap: 2rem;">
#             <div style="display: flex; align-items: center; gap: 0.5rem;">
#                 <span style="font-size: 1.5rem;">📹</span>
#                 <span>Create reels with your media</span>
#             </div>
#             <div style="display: flex; align-items: center; gap: 0.5rem;">
#                 <span style="font-size: 1.5rem;">📄</span>
#                 <span>Beautiful invitation videos</span>
#             </div>
#             <div style="display: flex; align-items: center; gap: 0.5rem;">
#                 <span style="font-size: 1.5rem;">🎨</span>
#                 <span>Templates, stickers, and background music</span>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Action cards
#     st.markdown("""
#     <div class="action-grid">
#         <div class="action-card">
#             <div class="action-icon">▶️</div>
#             <div class="action-title">Start Creating</div>
#             <div class="action-desc">Begin your new project</div>
#         </div>
#         <div class="action-card">
#             <div class="action-icon">📁</div>
#             <div class="action-title">My Projects</div>
#             <div class="action-desc">View your saved work</div>
#         </div>
#         <div class="action-card">
#             <div class="action-icon">📋</div>
#             <div class="action-title">Templates</div>
#             <div class="action-desc">Browse design templates</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Media Access Section
#     st.markdown("""
#     <div class="permission-card">
#         <h2 style="margin-bottom: 1rem;">📷 Media Access</h2>
#     """, unsafe_allow_html=True)
    
#     if "media_permission" not in st.session_state:
#         st.session_state.media_permission = False
    
#     if not st.session_state.media_permission:
#         st.markdown("""
#         <div class="permission-icon">🔐</div>
#         <h3>Permission Required</h3>
#         <p>This app needs permission to access your photos and videos to generate reels and invitations.</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col2:
#             if st.button("✅ Allow Access to Photos/Videos", key="allow_access"):
#                 st.session_state.media_permission = True
#                 st.rerun()
#     else:
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         st.markdown("### 📤 Upload Your Photos / Videos")
#         uploaded_files = st.file_uploader(
#             "Upload your media files",
#             accept_multiple_files=True,
#             type=['png', 'jpg', 'jpeg', 'mp4'],
#             label_visibility="collapsed"
#         )
        
#         if uploaded_files:
#             for file in uploaded_files:
#                 st.success(f"✅ Uploaded: {file.name}")
        
#         if st.button("🔒 Revoke Access", key="revoke_access"):
#             st.session_state.media_permission = False
#             st.rerun()
    
#     # Audio Recording Section
#     st.markdown("""
#     <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 2rem; border-radius: 15px; margin: 2rem 0; color: white;">
#         <h3 style="margin-bottom: 1rem;">🎙️ Record Audio</h3>
#         <p style="margin-bottom: 1rem;">Note: You may be prompted by your browser to allow microphone access.</p>
#     """, unsafe_allow_html=True)
    
#     audio_html = """
#     <script>
#     let recorder;
#     navigator.mediaDevices.getUserMedia({ audio: true })
#         .then(function(stream) {
#             recorder = new MediaRecorder(stream);
#             let chunks = [];
#             recorder.ondataavailable = e => chunks.push(e.data);
#             recorder.onstop = e => {
#                 let blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
#                 let audioURL = window.URL.createObjectURL(blob);
#                 var player = document.getElementById('audio-player');
#                 player.src = audioURL;
#                 player.style.display = 'block';
#             }
#             window.startRecording = () => { chunks = []; recorder.start(); }
#             window.stopRecording = () => { recorder.stop(); }
#         });
#     </script>
#     <div style="text-align: center; margin: 1rem 0;">
#         <button onclick="startRecording()" style="background: #27ae60; color: white; border: none; padding: 1rem 2rem; border-radius: 10px; margin: 0.5rem; cursor: pointer;">⏺️ Start Recording</button>
#         <button onclick="stopRecording()" style="background: #e74c3c; color: white; border: none; padding: 1rem 2rem; border-radius: 10px; margin: 0.5rem; cursor: pointer;">⏹️ Stop Recording</button>
#     </div>
#     <audio id="audio-player" controls style="display:none; width: 100%; margin-top: 1rem;"></audio>
#     """
#     components.html(audio_html, height=200)
    
#     st.markdown("</div>", unsafe_allow_html=True)
    
#     # Logout in sidebar
#     with st.sidebar:
#         if st.button("🚪 Logout", key="sidebar_logout"):
#             st.session_state.page = "auth"
#             st.session_state.user = None
#             st.rerun()


# import streamlit as st
# import requests
# import streamlit.components.v1 as components

# # ---------------- APP CONFIG -----------------
# st.set_page_config(page_title="Reel & Invitation Creator", page_icon="🎨", layout="wide")

# # ---------------- FIREBASE CONFIG -----------------
# FIREBASE_WEB_API_KEY = "AIzaSyC9hbgiYgRwUSMD-ykdo-gG3gp-wy8PNlQ"
# firebase_signup = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
# firebase_signin = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

# # ---------------- SESSION -----------------
# if "page" not in st.session_state:
#     st.session_state.page = "welcome"
# if "user" not in st.session_state:
#     st.session_state.user = None

# # ---------------- FLOATING ICONS -----------------
# def render_floating_icons():
#     st.markdown("""
#     <div style="position: fixed; top: 50%; right: 20px; transform: translateY(-50%);
#     display: flex; flex-direction: column; gap: 1rem; z-index: 1000;">
#         <div style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px); border-radius: 15px; display: flex; align-items: center;
#         justify-content: center; font-size: 1.5rem; color: white; cursor: pointer;">
#             🎨
#         </div>
#         <div style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px); border-radius: 15px; display: flex; align-items: center;
#         justify-content: center; font-size: 1.5rem; color: white; cursor: pointer;">
#             📹
#         </div>
#         <div style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px); border-radius: 15px; display: flex; align-items: center;
#         justify-content: center; font-size: 1.5rem; color: white; cursor: pointer;">
#             🎵
#         </div>
#         <div style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.2);
#         backdrop-filter: blur(10px); border-radius: 15px; display: flex; align-items: center;
#         justify-content: center; font-size: 1.5rem; color: white; cursor: pointer;">
#             ✨
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ---------------- WELCOME SCREEN -----------------
# if st.session_state.page == "welcome":
#     render_floating_icons()

#     st.markdown("""
#     <div style="text-align: center; padding: 3rem 2rem; color: white;">
#         <h1 style="font-size: 4rem; font-weight: bold;
#             background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;">
#             🎨 Creator
#         </h1>
#         <p style="font-size: 1.5rem; opacity: 0.9;">✨ Create stunning reels, invitations, and more!</p>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown("""
#     <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
#         <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; text-align: center;">
#             <div style="font-size: 3rem;">📹</div>
#             <h3>Create Reels & Invitations</h3>
#             <p>Professional quality videos in minutes</p>
#         </div>
#         <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; text-align: center;">
#             <div style="font-size: 3rem;">🧠</div>
#             <h3>AI-Based Templates</h3>
#             <p>Smart templates that adapt to your content</p>
#         </div>
#         <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; text-align: center;">
#             <div style="font-size: 3rem;">🖼️</div>
#             <h3>Rich Media Support</h3>
#             <p>Photos, audio, stickers and animations</p>
#         </div>
#         <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 20px; text-align: center;">
#             <div style="font-size: 3rem;">🎙️</div>
#             <h3>Voice Recording</h3>
#             <p>Record voice or upload background music</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     if st.button("🚀 Get Started"):
#         st.session_state.page = "auth"


# # ---------------- AUTH SCREEN -----------------
# elif st.session_state.page == "auth":
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         auth_tabs = st.tabs(["Login", "Sign Up"])

#         with auth_tabs[0]:
#             st.subheader("Login")
#             email = st.text_input("Email", key="login_email")
#             password = st.text_input("Password", type="password", key="login_password")

#             if st.button("Login"):
#                 payload = {
#                     "email": email,
#                     "password": password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signin, json=payload)

#                 if req.status_code == 200:
#                     st.success("✅ Logged in successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid email or password")

#         with auth_tabs[1]:
#             st.subheader("Sign Up")
#             new_email = st.text_input("Email", key="signup_email")
#             new_password = st.text_input("Password (6+ characters)", type="password", key="signup_password")

#             if st.button("Sign Up"):
#                 payload = {
#                     "email": new_email,
#                     "password": new_password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signup, json=payload)

#                 if req.status_code == 200:
#                     st.success("✅ Account created successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     st.error(f"❌ {req.json().get('error', {}).get('message', 'Error')}")

#         if st.button("← Back"):
#             st.session_state.page = "welcome"
#             st.rerun()


# # ---------------- MAIN APP SCREEN -----------------
# elif st.session_state.page == "main":
#     if st.session_state.user is None:
#         st.warning("🚫 Please login to access the app.")
#         st.stop()

#     st.markdown(f"""
#     <div style="background: rgba(255,255,255,0.1); padding: 1rem 2rem; border-radius: 15px;
#     display: flex; justify-content: space-between; align-items: center;">
#         <div style="font-weight: bold; font-size: 1.5rem; color: white;">
#             🎨 Reel & Invitation Creator
#         </div>
#         <div style="color: white;">
#             👋 Welcome {st.session_state.user.get('email', 'User').split('@')[0]}!
#             <button onclick="location.reload()" style="margin-left: 1rem;
#             background: red; color: white; border: none; padding: 0.3rem 1rem;
#             border-radius: 5px; cursor: pointer;">🚪 Logout</button>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Action Buttons
#     st.markdown("""
#     <div style="display: flex; gap: 1rem; margin-top: 2rem;">
#         <button onclick="window.location.href='pages/2_Create_New.py'"
#         style="flex:1; padding:1rem; background:#00cec9; color:white; border:none; border-radius:10px;">
#         🎬 Start Creating
#         </button>

#         <button onclick="window.location.href='pages/3_My_Projects.py'"
#         style="flex:1; padding:1rem; background:#0984e3; color:white; border:none; border-radius:10px;">
#         📁 My Projects
#         </button>

#         <button onclick="window.location.href='pages/4_Templates.py'"
#         style="flex:1; padding:1rem; background:#6c5ce7; color:white; border:none; border-radius:10px;">
#         📑 Templates
#         </button>
#     </div>
#     """, unsafe_allow_html=True)

#     # Media Upload with Permission
#     st.markdown("<h3 style='color:white;'>📷 Media Access</h3>", unsafe_allow_html=True)

#     if "media_permission" not in st.session_state:
#         st.session_state.media_permission = False

#     if not st.session_state.media_permission:
#         if st.button("✅ Allow Access to Photos/Videos"):
#             st.session_state.media_permission = True
#             st.rerun()
#     else:
#         uploaded_files = st.file_uploader(
#             "Upload your media files",
#             accept_multiple_files=True,
#             type=['png', 'jpg', 'jpeg', 'mp4']
#         )

#         if uploaded_files:
#             for file in uploaded_files:
#                 st.success(f"✅ Uploaded: {file.name}")

#         if st.button("🔒 Revoke Access"):
#             st.session_state.media_permission = False
#             st.rerun()

#     # Audio Recording
#     st.markdown("<h3 style='color:white;'>🎙️ Record Audio</h3>", unsafe_allow_html=True)

#     audio_html = """
#     <script>
#     let recorder;
#     navigator.mediaDevices.getUserMedia({ audio: true })
#         .then(function(stream) {
#             recorder = new MediaRecorder(stream);
#             let chunks = [];
#             recorder.ondataavailable = e => chunks.push(e.data);
#             recorder.onstop = e => {
#                 let blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
#                 let audioURL = window.URL.createObjectURL(blob);
#                 var player = document.getElementById('audio-player');
#                 player.src = audioURL;
#                 player.style.display = 'block';
#             }
#             window.startRecording = () => { chunks = []; recorder.start(); }
#             window.stopRecording = () => { recorder.stop(); }
#         });
#     </script>
#     <button onclick="startRecording()">⏺️ Start Recording</button>
#     <button onclick="stopRecording()">⏹️ Stop Recording</button>
#     <br>
#     <audio id="audio-player" controls style="display:none; width: 100%; margin-top: 1rem;"></audio>
#     """
#     components.html(audio_html, height=200)
    


import streamlit as st
import requests
from streamlit_option_menu import option_menu
from st_audiorec import st_audiorec
from streamlit_extras.switch_page_button import switch_page
from google_auth_oauthlib.flow import Flow
import streamlit.components.v1 as components
import os
st.markdown("""
    <style>
    /* --- Sidebar background and layout --- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem 1rem;
        border-right: 4px solid #ff6b6b;
    }

    /* --- Sidebar app title (default style override) --- */
    .css-1d391kg, .css-h5rgaw {  /* Update if Streamlit class changes */
        font-size: 24px;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
        text-align: center;
    }

    /* --- Sidebar links --- */
    .css-1v0mbdj, .css-1v3fvcr {  /* Update if Streamlit class changes */
        font-size: 17px;
        font-weight: 500;
        color: #2d3436;
        margin-bottom: 10px;
        border-radius: 10px;
        padding: 10px;
        transition: all 0.3s ease-in-out;
    }

    .css-1v0mbdj:hover, .css-1v3fvcr:hover {
        background-color: #ff6b6b;
        color: white;
        transform: scale(1.03);
    }

    /* Scrollbar design for sidebar */
    section[data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background-color: #ff6b6b;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)



# ---------------- APP CONFIG -----------------
st.set_page_config(page_title="Creator | Reels & Invitations", page_icon="🎨", layout="wide")


# ---------------- FIREBASE CONFIG -----------------
FIREBASE_WEB_API_KEY = "AIzaSyC9hbgiYgRwUSMD-ykdo-gG3gp-wy8PNlQ"
firebase_signup = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
firebase_signin = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
firebase_google = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_WEB_API_KEY}"

# Google OAuth credentials file
CLIENT_SECRETS_FILE = "C:/Users/PC-16/Desktop/reel_invitation_creator/client_secret.json"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# ---------------- SESSION -----------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "user" not in st.session_state:
    st.session_state.user = None
# ---------------- GOOGLE LOGIN FUNCTION -----------------
def google_login_flow():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri="http://localhost:8501"
    )
    auth_url, state = flow.authorization_url(prompt="consent")
    return flow, auth_url, state

# ---------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* General */
.stApp {
    background: linear-gradient(135deg, #6a85f1, #a777e3);
    color: black;
}
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Buttons */
button {
    background-color: #ff7f50;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    color: white;
    cursor: pointer;
    transition: 0.3s;
}
button:hover {
    background-color: #ff6333;
}

/* Floating Icons */
.floating-icons {
    position: fixed;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 16px;
    z-index: 1000;
}
.floating-icons div {
    background: rgba(255, 255, 255, 0.15);
    padding: 12px;
    border-radius: 16px;
    font-size: 22px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}
.card h3 {
    margin: 10px 0;
}
.card p {
    color: #ddd;
}

/* Centered */
.center {
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- FLOATING ICONS -----------------
def floating_icons():
    st.markdown("""
    <div class="floating-icons">
        <div title="Home">🏠</div>
        <div title="Reels">🎥</div>
        <div title="Music">🎵</div>
        <div title="Templates">🎨</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- WELCOME SCREEN -----------------
if st.session_state.page == "welcome":
    floating_icons()

    st.markdown("<h1 class='center'>🎨 <b>Creator</b></h1>", unsafe_allow_html=True)
    st.markdown("<p class='center'>✨ Create stunning reels, invitations, and more!</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style="display: flex; gap: 20px; flex-wrap: wrap; justify-content:center;">
      <div class="card">
        <div style="font-size: 3rem;">📹</div>
        <h3>Create Reels & Invitations</h3>
        <p>Professional quality videos in minutes</p>
      </div>
      <div class="card">
        <div style="font-size: 3rem;">🧠</div>
        <h3>AI-Based Templates</h3>
        <p>Smart templates that adapt to your content</p>
      </div>
      <div class="card">
        <div style="font-size: 3rem;">🖼️</div>
        <h3>Rich Media Support</h3>
        <p>Photos, audio, stickers and animations</p>
      </div>
      <div class="card">
        <div style="font-size: 3rem;">🎤</div>
        <h3>Voice Recording</h3>
        <p>Record voice or upload background music</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Get Started"):
        st.session_state.page = "auth"


# ---------------- AUTH SCREEN -----------------
# elif st.session_state.page == "auth":
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown("<h2 class='center'>🔐 Welcome Back</h2>", unsafe_allow_html=True)
#         st.markdown("<p class='center'>Sign in to continue creating amazing content</p>", unsafe_allow_html=True)

#         auth_tabs = st.tabs(["Login", "Sign Up"])

#         with auth_tabs[0]:
#             st.subheader("Login")
#             email = st.text_input("Email", key="login_email")
#             password = st.text_input("Password", type="password", key="login_password")

#             if st.button("➡️ Login"):
#                 payload = {
#                     "email": email,
#                     "password": password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signin, json=payload)

#                 if req.status_code == 200:
#                     st.success("✅ Logged in successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     st.error(f"❌ {req.json().get('error', {}).get('message', 'Error')}")

#         with auth_tabs[1]:
#             st.subheader("Sign Up")
#             new_email = st.text_input("Email", key="signup_email")
#             new_password = st.text_input("Password (6+ characters)", type="password", key="signup_password")

#             if st.button("➕ Sign Up"):
#                 payload = {
#                     "email": new_email,
#                     "password": new_password,
#                     "returnSecureToken": True
#                 }
#                 req = requests.post(firebase_signup, json=payload)

#                 if req.status_code == 200:
#                     st.success("✅ Account created successfully!")
#                     st.session_state.user = req.json()
#                     st.session_state.page = "main"
#                     st.rerun()
#                 else:
#                     st.error(f"❌ {req.json().get('error', {}).get('message', 'Error')}")


#         if st.button("← Back"):
#             st.session_state.page = "welcome"
#             st.rerun()
# ---------------- AUTH SCREEN -----------------
elif st.session_state.page == "auth":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔐 Welcome Back</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Sign in to continue creating amazing content</p>", unsafe_allow_html=True)

        auth_tabs = st.tabs(["Login", "Sign Up", "Google Login"])

        # --------- Login Tab ---------
        with auth_tabs[0]:
            st.subheader("Login with Email")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("➡️ Login"):
                payload = {
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                }
                req = requests.post(firebase_signin, json=payload)

                if req.status_code == 200:
                    st.success("✅ Logged in successfully!")
                    st.session_state.user = req.json()
                    st.session_state.page = "main"
                    st.rerun()
                else:
                    st.error(f"❌ {req.json().get('error', {}).get('message', 'Error')}")

        # --------- Signup Tab ---------
        with auth_tabs[1]:
            st.subheader("Sign Up with Email")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password (6+ characters)", type="password", key="signup_password")

            if st.button("➕ Sign Up"):
                payload = {
                    "email": new_email,
                    "password": new_password,
                    "returnSecureToken": True
                }
                req = requests.post(firebase_signup, json=payload)

                if req.status_code == 200:
                    st.success("✅ Account created successfully!")
                    st.session_state.user = req.json()
                    st.session_state.page = "main"
                    st.rerun()
                else:
                    st.error(f"❌ {req.json().get('error', {}).get('message', 'Error')}")

        # --------- Google Login Tab ---------
        with auth_tabs[2]:
            st.subheader("Login with Google")

            if "auth_url" not in st.session_state:
                if st.button("🔑 Login with Google"):
                    flow, auth_url, state = google_login_flow()
                    st.session_state.flow = flow
                    st.session_state.auth_url = auth_url
                    st.session_state.state = state

                    js = f"window.open('{auth_url}')"  # open in new tab
                    components.html(f"<script>{js}</script>", height=0)

            # Handle callback
            query_params = st.query_params.to_dict()

            if query_params.get("state") == st.session_state.get("state") and "code" in query_params:
                try:
                    flow = st.session_state.flow
                    flow.fetch_token(
                        authorization_response=st.experimental_get_query_params()
                    )

                    credentials = flow.credentials
                    token = credentials.id_token

                    user_info = requests.get(
                        "https://openidconnect.googleapis.com/v1/userinfo",
                        headers={"Authorization": f"Bearer {credentials.token}"}
                    ).json()

                    # Firebase authentication with Google token
                    payload = {
                        "postBody": f"id_token={token}&providerId=google.com",
                        "requestUri": "http://localhost",
                        "returnSecureToken": True
                    }

                    firebase_response = requests.post(firebase_google, json=payload).json()

                    if "error" in firebase_response:
                        st.error(f"❌ Google Login Failed: {firebase_response['error']['message']}")
                    else:
                        st.success(f"✅ Logged in as {firebase_response.get('email')}")
                        st.session_state.user = firebase_response
                        st.session_state.page = "main"
                        st.rerun()

                except Exception as e:
                    st.error(f"Google Login Error: {e}")

        if st.button("← Back"):
            st.session_state.page = "welcome"
            st.rerun()

# ---------------- MAIN SCREEN -----------------
elif st.session_state.page == "main":
    if st.session_state.user is None:
        st.warning("🚫 Please login to access the app.")
        st.stop()

    selected = option_menu(
        menu_title=None,
        options=["Home", "Create", "Projects", "Templates"],
        icons=["house", "film", "folder2", "palette"],
        orientation="horizontal",
        default_index=0,
    )

    st.subheader(f"✨ {selected} Page")

    # ---------------- HOME -----------------
    if selected == "Home":
        st.success(f"👋 Welcome {st.session_state.user.get('email').split('@')[0]}!")

    # ---------------- CREATE -----------------
    if selected == "Create":
        st.info("Redirecting to Create Page...")
        st.switch_page("pages/2_Create_New_Updated_UI.py")



    # ---------------- PROJECTS -----------------
    if selected == "Projects":
        st.info("Redirecting to Create Page...")
        st.switch_page("pages/3_My_Projects.py")
        
    # ---------------- TEMPLATES -----------------
    if selected == "Templates":
        st.info("Redirecting to Create Page...")
        st.switch_page("pages/4_Templates.py")        

    # ---------------- LOGOUT -----------------
    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.page = "welcome"
        st.rerun()

