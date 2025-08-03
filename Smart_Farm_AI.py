import streamlit as st
import requests

# CONFIGURATION
API_KEY = "kGiA9NqPcnJrEMN0B7Ot_3Bv22ebTjtHpPy_nX34QwU1"
DEPLOYMENT_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1b037028-e3f3-4b77-8ad1-aee72027803d/ai_service?version=2021-05-01"

# FUNCTION TO GET ACCESS TOKEN
@st.cache_resource(show_spinner=False)
def get_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(url, headers=headers, data=data)

    try:
        token = response.json()["access_token"]
        return token
    except KeyError:
        st.error("❌ Failed to retrieve access token.")
        st.json(response.json()) 
        raise

# GET TOKEN + SET HEADERS
token = get_token()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# STREAMLIT UI
import streamlit as st

# Inject custom CSS
st.markdown("""
    <style>
    .stMainBlockContainer {
        padding: 3rem 1rem 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌾 Smart Farming AI Assistant")
st.markdown("Ask anything about crops, mandi prices, pest control, or weather!")

user_question = st.text_input("Type your question here:")

if st.button("Ask"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }

        try:
            res = requests.post(DEPLOYMENT_URL, headers=headers, json=payload) 

            if res.status_code != 200:
                st.error(f"❌ API call failed with status code {res.status_code}")
            else:
                try:
                    answer = res.json()["choices"][0]["message"]["content"]
                    st.success("🧠 Agent's Answer:")
                    st.write(answer)
                except KeyError:
                    st.error("❌ Unexpected response format:")
                    st.json(res.json())

        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")