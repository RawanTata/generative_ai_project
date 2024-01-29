### Project Documentation: Generative AI for Code Generation

#### Overview:
This project aims to evaluate the effectiveness of large language models like GPT-4 in generating program code. We'll build a database and test environment to assess these models' capabilities.

#### Technology:
- Models: GPT-4, [Starcoder](https://huggingface.co/blog/starcoder), [Microsoft Phi-1](https://huggingface.co/microsoft/phi-1)
- Languages: Python, JavaScript
- Database: PostgreSQL
- Backend: Django
- Frontend: Streamlit
- AI Integration: Hugging Face Transformers

#### Implementation Steps:

1. **Database Setup**: Create a PostgreSQL database integrated with Django. Store exercises and expected solutions.

2. **Model Integration**: Use Hugging Face Transformers to integrate models like GPT-4, Starcoder, and Microsoft Phi-1.

3. **Backend Development**: Develop Django backend to manage database interactions and AI model communications.

4. **AI-Powered Code Generation**: Implement functions to generate solutions using AI models for given exercises.

5. **Evaluation Mechanism**: Develop methods to evaluate AI-generated solutions against expected solutions.

6. **Frontend Development with Streamlit**: Create an interactive interface for users to view exercises, AI-generated solutions, and evaluation results.

7. **Deployment**: Deploy the Django backend and Streamlit frontend.

8. **Result Analysis and Presentation**: Analyze results and present them in information graphics using Streamlit.

#### Running the Application:

1. Install dependencies:
   ```
   pip install django psycopg2 torch torchvision torchaudio transformers djangorestframework
   ```

2. Run Django migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Import exercises (adjust the path to your JSON file):
   ```
   python manage.py import_exercises "<path_to_json>"
   ```

4. Generate and evaluate solutions:
   ```
   python manage.py generate_and_evaluate_solutions
   ```

5. Run the Django server:
   ```
   python manage.py runserver
   ```

6. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

#### Key Considerations:

- **Testing**: Rigorously test AI models in diverse scenarios.
- **Security**: Implement security measures for API and user inputs.
- **Resource Management**: Ensure server can handle model computations.
- **Ethical Use**: Consider ethical implications of AI-generated code.

#### Future Work:

- Expand model selection.
- Enhance evaluation metrics.
- Explore additional use cases and programming languages.

#### Contact:
Andreas Stöckl; Email: andreas.stoeckl@fh-hagenberg.at

---

This document serves as a high-level guide for setting up, running, and understanding the project. For detailed code, refer to the project's GitHub repository.
