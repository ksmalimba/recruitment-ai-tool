import streamlit as st
import os
from groq import Groq
import PyPDF2
from dotenv import load_dotenv
from prompt import getprompt

load_dotenv()
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.set_page_config(page_title="AI Assesment", layout="wide")
st.title("AI Assessment")

st.subheader("Candidate CV")
cv_file = st.file_uploader("Upload CV (PDF)", type="pdf", key="cv")

col1, col2 = st.columns(2)


with col1:
    st.subheader("Job Specification")
    js_tab1, js_tab2 = st.tabs(["Paste Text", "Upload PDF"])
    with js_tab1:
        jobspec_text = st.text_area("Paste Job Spec here", height=200, key="js_pasted")
    with js_tab2:
        jobspec_file = st.file_uploader("Upload Job Spec", type="pdf", key="jobspec_file")


with col2:
    st.subheader("Interview Transcript")
    it_tab1, it_tab2 = st.tabs(["Paste Text", "Upload PDF"])
    with it_tab1:
        transcript_text = st.text_area("Paste Transcript here", height=200, key="it_pasted")
    with it_tab2:
        transcript_file = st.file_uploader("Upload Transcript", type="pdf", key="it_file")

if st.button("Generate Assessment", type="primary"):
    

    if jobspec_text !="":
        final_jobspec = jobspec_text
    else:
        if jobspec_file:
            final_jobspec=extract_text_from_pdf(jobspec_file)
        else:
            final_jobspec =None

    if transcript_text !="":
        final_transcript = transcript_text
    else:
        if transcript_file:
            final_transcript=extract_text_from_pdf(transcript_file)
        else:
            final_transcript =None
   
    
    
    final_cv = extract_text_from_pdf(cv_file) if cv_file else None

    if final_jobspec and final_transcript and final_cv:
        with st.spinner("Processing the assessment..."):
            try:
           
                assessment_prompt = getprompt(final_jobspec, final_cv, final_transcript)
            
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": assessment_prompt}]
                )
            
                st.success("Assessment Complete!")
                st.markdown(completion.choices[0].message.content)
            
            except Exception as e:
           
                st.error(f"The AI encountered an error: {e}")
    else:
        st.error("Please ensure CV, Job Spec, and Transcript are all provided.")