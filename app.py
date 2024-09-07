import streamlit as st

from ai_debate.ai_model import AIModel
from ai_debate.debate import Debate
from ai_debate.judge import Judge

st.title('AI Debate APP')

model_options = [
    'llama3-8b-8192',
    'llama3-70b-8192',
    'llama-3.1-70b-versatile',
    'llama-3.1-8b-instant',
    'mixtral-8x7b-32768-groq',
    'gemma-7b-it',
    'gemma2-9b-it',

    'gemini-pro',
    'gemini-1.5-pro',
    'gemini-1.5-flash',

    'gpt-4o',
    'gpt-4o-mini',
    'gpt-4-turbo',
    'gpt-4',
    'gpt-3.5-turbo',
    'chatgpt-4o-latest',

    'claude-3-opus-20240229',
    'claude-3-sonnet-20240229',
    'claude-3-haiku-20240307',

    'mistral-large-2402',
    'mistral-large-2407',
]
# Here we will map model_name to api_provider
model_dict = {
    'llama3-8b-8192': 'groq',
    'llama3-70b-8192': 'groq',
    'llama-3.1-70b-versatile': 'groq',
    'llama-3.1-8b-instant': 'groq',
    'mixtral-8x7b-32768-groq': 'groq',
    'gemma-7b-it': 'groq',
    'gemma2-9b-it': 'groq',

    'gemini-pro': 'google',
    'gemini-1.5-pro': 'google',
    'gemini-1.5-flash': 'google',

    'gpt-4o': 'openai',
    'gpt-4o-mini': 'openai',
    'gpt-4-turbo': 'openai',
    'gpt-4': 'openai',
    'gpt-3.5-turbo': 'openai',
    'chatgpt-4o-latest': 'openai',

    'claude-3-opus-20240229': 'anthropic',
    'claude-3-sonnet-20240229': 'anthropic',
    'claude-3-haiku-20240307': 'anthropic',

    'mistral-large-2402': 'mistralai',
    'mistral-large-2407': 'mistralai'
}

with st.sidebar:
    fighter_a = st.selectbox('Select the first fighter: ', model_options)
    temperature_a = st.number_input('Temperature for first fighter', 0.7)
    fighter_b = st.selectbox('Select the second fighter', model_options)
    temperature_b = st.number_input('Temperature for second fighter', 0.7)
    
    # Multiple judge selection
    judge_options = [judge for judge in model_options if judge not in [fighter_a, fighter_b]]
    selected_judges = st.multiselect('Select judges (at least one):', judge_options)
    temperature_judges = st.number_input('Temperature for judges', 0)

    topic = st.text_input('Enter the desired topic: ', 'Existence of the god')
    rounds_no = int(st.text_input('Number of debate rounds', 4))

    fighter_a_side = st.text_input("First Fighter's view point:", 'God Exists')
    fighter_b_side = st.text_input("Second Fighter's view point:", "God does'nt exist")

    model_1 = AIModel(fighter_a, model_dict[fighter_a], temperature_a)
    model_2 = AIModel(fighter_b, model_dict[fighter_b], temperature_b)

    if model_1.model_name == model_2.model_name:
        model_1.model_name += '_01'
        model_2.model_name += '_02'

    # Initialize judges based on user selection
    judges = [Judge(model_name, model_dict[model_name], temperature=temperature_judges) for model_name in selected_judges]

    debate = Debate(model_1, model_2, judges, topic, fighter_a_side, fighter_b_side)

# Check if at least one judge is selected
if not selected_judges:
    st.warning("Please select at least one judge before starting the debate.")
    st.stop()  # This will prevent the rest of the app from running

if st.button('Start Fight 🥊'):
    scores_final = []

    for i in range(rounds_no):
        response = debate.fight_round(i+1)
        score_1, score_2 = debate.scoring(*response)
        scores_final.append([score_1, score_2])
        
        # Display responses and scores
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"<div style='background-color:orange;padding:10px;border-radius:5px;'>"
                        f"<strong>{model_1.model_name}:</strong><br>{response[0]}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='background-color:purple;padding:10px;border-radius:5px;text-align:center;'>"
                        f"<strong>Round {i+1} Scores</strong><br>", unsafe_allow_html=True)
            
            st.markdown(f"<br>Model 1 - {score_1:.2f}<br>Model 2 - {score_2:.2f}", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<div style='background-color:brown;padding:10px;border-radius:5px;'>"
                        f"<strong>{model_2.model_name}:</strong><br>{response[1]}</div>", unsafe_allow_html=True)

        st.write(f'-------------------------------------------------------------End of round no: {i+1}-------------------------------------------------------')

    # Average and final Score
    avg_score_model_1 = sum([score[0] for score in scores_final])/len(scores_final)
    avg_score_model_2 = sum([score[1] for score in scores_final])/len(scores_final)

    st.markdown(f"<div style='background-color:red;padding:10px;border-radius:5px;text-align:center;'>"
                f"<strong>Final Scores</strong><br>"
                f"{model_1.model_name}: {avg_score_model_1:.2f}<br>"
                f"{model_2.model_name}: {avg_score_model_2:.2f}</div>", unsafe_allow_html=True)