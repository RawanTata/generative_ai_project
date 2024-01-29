import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Django server details
DJANGO_SERVER = "http://127.0.0.1:8000"

# Endpoint to trigger code generation and evaluation
GENERATE_AND_EVALUATE_ENDPOINT = f"{DJANGO_SERVER}/generate_and_evaluate"

def trigger_generation_and_evaluation():
    placeholder = st.empty()
    placeholder.image('GIF LOADING - Dog chases his tail.gif', width=900)
    try:
        response = requests.post(GENERATE_AND_EVALUATE_ENDPOINT)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Django server: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error: {e}")
        return None
    finally:
        # Clear the loading GIF
        placeholder.empty()

def display_evaluation_results(results):
    aggregate_performance = {model: {'Correctness': 0, 'Efficiency': 0, 'Best Practices': 0} for model in ['model1_metrics', 'model2_metrics']}
    total_exercises = len(results)

    for exercise_id, exercise_results in results.items():
        st.subheader(f"Exercise ID: {exercise_id}")
        for model_key in ['model1_metrics', 'model2_metrics']:
            model_results = exercise_results.get(model_key, {})
            st.write(f"Results for {model_key.replace('_', ' ').title()}:")
            
            df = pd.DataFrame({
                'Metric': ['Correctness', 'Efficiency', 'Best Practices'],
                'Value': [
                    model_results.get('correctness', 'N/A'),
                    model_results.get('efficiency', 'N/A'),
                    model_results.get('best_practices', 'N/A')
                ]
            })
            fig = px.bar(df, x='Metric', y='Value', title=f"Results for {model_key.replace('_', ' ').title()}")
            st.plotly_chart(fig)

            # Update aggregate performance
            for metric in aggregate_performance[model_key]:
                if model_results.get(metric.lower(), None) is not None:
                    aggregate_performance[model_key][metric] += model_results.get(metric.lower(), 0) / total_exercises

    # Aggregated Performance Visualization
    aggregate_df = pd.DataFrame(aggregate_performance).T.melt(var_name='Metric', value_name='Average Score')
    fig_agg = px.bar(aggregate_df, x=aggregate_df.index, y='Average Score', color='Metric', barmode='group', title="Aggregated Model Performance")
    st.plotly_chart(fig_agg)
def model_toolbar():
    with st.sidebar:
        st.header("View Model Parameters")
        model = st.selectbox("Model", ["gpt-neo-1.3B", "CodeGPT-small-py", "Both"])
        temperature = st.slider("Temperature", 0.01, 5.00, 1.00, 0.01)
        top_p = st.slider("Top P", 0.01, 1.00, 0.50, 0.01)
        max_length = st.slider("Max Length", 32, 128, 64, 1)
        st.write("Selected Model:", model)
        st.write("Temperature:", temperature)
        st.write("Top P:", top_p)
        st.write("Max Length:", max_length)

def save_json_file(uploaded_file):
    # Save the file to a directory
    with open(os.path.join('U:\Third-Trial-fourth-try\Third-Trial-fourth-try\generative_ai_project\Dataset', uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} saved successfully.")

def upload_file_ui():
    st.subheader("Upload JSON File")
    uploaded_file = st.file_uploader("Choose a file", type="json")
    if uploaded_file is not None:
        save_json_file(uploaded_file)


def main():
    st.title("AI Code Generator Evaluation")
    st.markdown("""
        **Project Goal:**

        Large language models, such as the GPT4 behind ChatGPT, are increasingly being used to generate program code. 
        The goal of this project is to build a database and test environment to test the power of these language models.

        **Technology:**

        Examples of code generating models:
        - [StarCoder (Hugging Face)](https://huggingface.co/blog/starcoder)
        - [Microsoft Phi-1 (Hugging Face)](https://huggingface.co/microsoft/phi-1)

        **The Result:**

        For this purpose, typical exercises in the programming languages Python or Javascript will be recorded in a database. 
        Furthermore, the possibility should be created to test different language models with these tasks as effectively as possible and to evaluate the results. 
        The results will be presented in information graphics.
    """)
    model_toolbar()
    upload_file_ui()

    # Trigger generation and evaluation
    if st.button("Generate and Evaluate"):
 #       with st.spinner("Generating and evaluating solutions. Please wait..."):
            evaluation_results = trigger_generation_and_evaluation()
            if evaluation_results:
                st.success("Generation and evaluation successful!")
                display_evaluation_results(evaluation_results)
            else:
                st.error("Error during generation and evaluation. Please check the server logs.")

if __name__ == "__main__":
    main()