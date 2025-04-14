import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re
from sentence_transformers import SentenceTransformer, util
import base64

# Set Streamlit page config
st.set_page_config(page_title="AI Quiz Generator", page_icon="🧠")

# Session state initialization
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'form_html' not in st.session_state:
    st.session_state.form_html = ""
if 'form_created' not in st.session_state:
    st.session_state.form_created = False

# Force GPU usage if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device.type == "cuda":
    torch.cuda.empty_cache()

# Load quiz generation model
try:
    tokenizer = AutoTokenizer.from_pretrained("iarfmoose/t5-base-question-generator")
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "iarfmoose/t5-base-question-generator"
    ).to(device)
    model.eval()
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# Load semantic similarity model
try:
    similarity_model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
except Exception as e:
    st.error(f"SentenceTransformer loading failed: {e}")
    st.stop()

# Generate questions
def generate_questions(context, num_questions=5):
    prompt = "generate questions: " + context.strip().replace("\n", " ")
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512).to(device)

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=64,
            do_sample=True,
            top_p=0.95,
            temperature=0.7,
            num_return_sequences=num_questions * 3,
            no_repeat_ngram_size=2,
        )

    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return clean_questions(decoded, num_questions)

# Clean generated questions
def clean_questions(raw_questions, max_questions):
    cleaned = []
    seen = set()
    for q in raw_questions:
        q = q.strip().replace("  ", " ")
        q = re.sub(r"[^\w\d\s?,]", "", q)
        q = re.sub(r"\s+", " ", q).strip("?").strip() + "?"
        q_lower = q.lower()

        if (
            len(q) > 15
            and not re.search(r"\b(name|someone|he|she|him|her|Mr|Ms|Mrs|Dr|Prof)\b", q_lower)
            and q_lower not in seen
        ):
            seen.add(q_lower)
            cleaned.append(q)

    # Semantic deduplication
    unique = []
    if cleaned:
        embeddings = similarity_model.encode(cleaned, convert_to_tensor=True, device=device)
        for i, q in enumerate(cleaned):
            if not unique:
                unique.append(q)
            else:
                sim_scores = util.cos_sim(embeddings[i], embeddings[[cleaned.index(u) for u in unique]])
                if max(sim_scores[0]) < 0.9:
                    unique.append(q)
            if len(unique) >= max_questions:
                break
    return unique

# Download link helper
def get_binary_file_downloader_html(bin_file, file_label='File'):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.html">Download {file_label}</a>'
        return href
    except Exception:
        return "Error: File not found."

# ---------------- UI ----------------
st.title("📚 AI Quiz Generator")
st.markdown("Paste your study notes or content below to generate quiz questions.")

context = st.text_area("Enter study content here:", height=200)
num_questions = st.slider("Number of quiz questions:", 1, 20, 5)
form_owner_email = st.text_input("Enter your email for form responses:", "")

if st.button("Generate Quiz"):
    if not context.strip():
        st.warning("Please enter study content.")
    elif not form_owner_email:
        st.warning("Please enter your email.")
    else:
        with st.spinner("Generating questions..."):
            try:
                questions = generate_questions(context, num_questions)
                if questions:
                    st.session_state.questions = questions
                    st.success("✅ Generated Questions:")
                    for i, q in enumerate(questions, 1):
                        st.markdown(f"**{i}. {q}**")
                else:
                    st.warning("No valid questions generated. Try different input.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Question approval and form creation
if st.session_state.questions:
    st.markdown("### Approve Questions")
    if st.button("Questions Look Good?"):
        form_html = f"""
        <html>
        <head><title>Quiz Form</title></head>
        <body>
        <h1>Quiz Form</h1>
        <form action="{form_owner_email}" method="POST">
        {''.join([f'<div><label>{i}. {q}</label><input type="text" name="q{i}" required></div>' for i, q in enumerate(st.session_state.questions, 1)])}
        <input type="hidden" name="total_questions" value="{len(st.session_state.questions)}">
        <input type="hidden" name="points_per_question" value="1">
        <input type="submit" value="Submit">
        </form>
        <p>Replace the form action with your actual Formspree endpoint from <a href='https://formspree.io/'>Formspree.io</a>.</p>
        </body>
        </html>
        """
        st.session_state.form_html = form_html
        st.session_state.form_created = True
        with open("quiz_form.html", "w") as f:
            f.write(form_html)
        st.success("✅ Form Created!")

# Form download
if st.session_state.form_created:
    st.markdown("### Download Quiz Form")
    st.markdown(get_binary_file_downloader_html("quiz_form.html", "Quiz_Form"), unsafe_allow_html=True)
else:
    st.info("Generate and approve questions to create and download a form.")
