import streamlit as st
import os
from pathlib import Path
from analyzer.audio_tools import detect_issues
from analyzer.transcriber import detect_rebuttal
from analyzer.report_generator import generate_text_report
from download_readymode_calls import download_all_call_recordings

st.set_page_config(page_title="Call Auditor | Mohamed Abdo", layout="centered")

# Updated Credentials for Login
CREDENTIALS = {"username": "Auditor1", "password": "Auditor1@3510"}

# List of agents
agents = [
    "OsamaAwad", "MaryemMohamed", "SamaKhaled", "Ibrahimmohamed", "HagarMotea Atia",
    "Nouresmael", "LamisSalah", "OmniaKhaled Briek", "AhmedAdel", "Emad Elhegawy",
    "ShehabYakoub", "EhabMohammed Ezzat Hassan", "ZyadHebisha", "AhmedHemdan", 
    "NorhanKhalid tantawy elsayed", "TarekAbdelfattah Mohammed Hamouda", "HelenSaber", 
    "MohamedFares Kamal eldin eissa", "AhmedAbd El-Sattar", "Yehia nasser", 
    "Ahmed Saber Abdelhafez Hussein", "DinaElkady", "YoussefYasser Tawfik Taha", 
    "Sayed Gamal", "HaneenAbdulmenom", "MalakSokkar", "Radwan", "MazenMohamed Abd El-kader", 
    "Abdillahihabib abdi houssein", "OmarAhmed Shaker", "KariemGerges", "AhmedAbdelhamid", 
    "RozanElhalaby", "Amira Mohamed Abdelmageed Radwan", "Youssef Refaat", "BelalAhmed", 
    "Yehiahassan ali", "YasserMohammed Mahmoud Ammar", "ReemDiaa Eldien Hamed Osman", 
    "BadawyHassan", "Hannamohamed ali ahmed ahmed", "AlaaWaleed Gamal Abdulmajeed", 
    "Ibrahim farouk ahmed Ibrahim", "RewanElmorsy", "RowanAli", "HagerEmad Eldeen", 
    "YoussefRefaat", "GamalEldin Mahmoud Hanafy Mahmoud", "AhmedKhaled Hamed", "MennaElkassar", 
    "RanaDiaa El-Deen Hamed Othman Ahmed", "Emankamal", "MohamedAyman Mohamed", 
    "Hanahani zaki ragab ramadan", "Moaz Darwish", "Hadymaamoun Gouda Mohamed", 
    "Omar Emad Abdelglel Ezzelregal", "Radwa Mohamed Amin Ibrahim", "Moazibrahim mohamed ibrahim", 
    "AhmedKhalil Ahmed Mohamed", "Hamza Diab", "HusseinNoureldin Hussein", "AhmedSayed Mohamed Fawzy", 
    "AdhamKhaled", "rawan ahmed mohamed", "ZainaMohamed Samir Mohamed", "RaghadAbdrabbo", "GamalSaad", 
    "Hadeer Ali", "Fouad", "YoussefTaha Mohamed Mohamed", "AhmedAbdEl-Hafeez", 
    "Ibrahimwael mohamed salama", "Heba Mahmoud", "MennaAllah Ali Sharaf Eldin Abdelghafar", 
    "RanaAshour", "Reemkhaled", "Basant Abdelrahman Rashed Hussen", "Hagar ahmed", 
    "MohamedThabet Mansour Mohamed", "HadeerMamdouh", "MaryamAshraf Farg Ali", "KirolloseAshraf", 
    "FatimaMostafa Kamel Ahmed Edrees", "Reem ghaly", "EsraaMedhat", "MaiTolba", "KarimAshraf Mohamed", 
    "Esraa Shaltout", "Kenzyfawzy mohamed elghobary", "MahmoudAhmed Reyad Ibrahim", 
    "Rowanmohamed mohamed hussien khorshed", "RowanAyman Mohamed", 
    "Abdalrahmansamir farahat ali", "Shahdamr hassan ghobashy", 
    "MohammedMostafa Abd Elmeged Mohammed", "MohamedNamra", "Hannah Ragab", "Mariam Mahgoub", 
    "Mohamedahmed abdelrahem yossef", "OmarAhmed Shaker", "MahmoudHamdi", "Gom3a", 
    "MohamedHesham sayed Tantawy", "YomnaHussein", "Asmaa Ahmed Farouk Basiouny", "MohamedShalaby", 
    "Aminaahmed saeed mohammed", "OmarMohamed Elsayed Ibrahim", "Ahmedmohamed saeed elsayed mahran", 
    "YassmineBassem", "AbdoMostafa", "MoaazMostafa Ali Hassan", "BegadEhab", 
    "Khaledabdelhameed mohamed Hassan", "AhmedNasr Fawzy Mahmoud Elqammash", "HadeerAli", 
    "rawanmuhammed ibraheem elsayed", "HagarMotea Atia", "Ahmedrabie", 
    "MazenMohamed Abd El-kader", "MalakAhmed", "HabibaYahia Mohamed elsayed", "YahiaNasser", 
    "HebaMahmoud", "HusseinNoureldin Hussein Aly", "Adham khaled Mohamed Hassan", "Ahmed magdy", 
    "HamzaDiab", "MahmoudAhmed", "Adham Khaled Mohamed Hassan", "FatmaDarwish Ragab Darwish Alaam", 
    "RaghadSaad", "Nourhan Mamdouh Shehata Hassan Swidan", "Bassantmuhammed fathi elabd", 
    "Menna Allah Ramadan Eldosoky", "Ahmed Khalil Ahmed Mohamed", "Traning1", "Traning2", 
    "Hussein Noureldin Hussein Aly", "Ahmed Sayed Mohamed Fawzy", "YoussefGohar", 
    "Youssef adel abbas el seddik", "Ahmed magdy abdalla ibrahim", "SalmaHussam", 
    "Mohamed Ayman Mohamed", "AyaAhmed Ahmed Ibrahim", "mohamed Moawad", "SeifAldin Eslam Mahmoud Hassan Ahmed", 
    "Soliman Youssef", "Ilham Ahmed Atyah Mohammedain", "karma amr hussein farahat", "TybaMusa", 
    "FarahWael Mohamed Attya", "Mahmoud Ahmed", "QA9", "Hagar Motea", "Malak Sokkar", 
    "Omar Emad Abdelglel Ezzelregal", "Reem Magdy", "Haneenabdelmonem", "Rozan Hany Elhalaby", 
    "Hamza Diab Mokhtar", "Adham Khaled Mohamed Hassan", "HusseinNoureldin Hussein", 
    "Ibrahim Mohamed Amin Ali", "Mazen Abdelkader"
]

# Dialer selection dropdown
dialer_options = ['resva7', 'resva6', 'resva5', 'resva4', 'resva2', 'resva']
dialer = st.selectbox("Select Dialer", dialer_options)

# Agent selection dropdown
agent = st.selectbox("Select Agent", agents)

# Show the selected dialer and agent
st.write(f"Selected Dialer: {dialer}")
st.write(f"Selected Agent: {agent}")

# Login Section
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Call Audit Login")
    st.subheader("Developed by Mohamed Abdo")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == CREDENTIALS["username"] and password == CREDENTIALS["password"]:
            st.session_state.authenticated = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

else:
    st.title("📞 AI Call Auditing Dashboard")
    st.subheader("Welcome, Mohamed Abdo")
    st.markdown("Easily audit ReadyMode recordings for silent agents, missing rebuttals, and dead calls.")

    st.markdown("## 📥 Download MP3s from ReadyMode")
    if st.button("🎧 Download All Recordings"):
        with st.spinner("Logging in and downloading recordings..."):
            try:
                progress = st.progress(0, text="Initializing...")

                def update_progress(current, total):
                    percent = int((current / total) * 100)
                    progress.progress(percent, text=f"Downloading MP3s: {current}/{total}")

                # Download function to be integrated with the download_readymode_calls.py script
                download_all_call_recordings(dialer, agent, update_callback=update_progress)
                progress.empty()
                st.success("✅ All recordings downloaded successfully!")

            except Exception as e:
                st.error(f"❌ Download failed:\n\n{e}")
                raise

    folder_path = st.text_input("📂 Enter the full path to your MP3 folder")
    if st.button("🚀 Start Auditing") and folder_path:
        if not os.path.isdir(folder_path):
            st.error("Invalid folder path.")
        else:
            st.success("Analyzing...")
            results = []
            for file in Path(folder_path).glob("*.mp3"):
                issues = detect_issues(file)
                rebuttal = detect_rebuttal(file)
                if rebuttal:
                    issues.append(rebuttal)
                if issues:
                    results.append((file.stem, issues))

            if results:
                st.markdown("### 🔍 Flagged Samples")
                for name, flags in results:
                    for issue in flags:
                        st.write(f"**{name}** – {issue}")

                if st.button("📄 Generate Full Report"):
                    report = generate_text_report(results)
                    st.text_area("📋 Report", value=report, height=400)
            else:
                st.success("No issues detected.")








