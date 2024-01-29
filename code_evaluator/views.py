from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewExercise
from .utils import generate_solution
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import evaluate_solution

import logging

# ... (other imports)

logger = logging.getLogger(__name__)

def home(request):
    # Add logic for your home view
 #   return render(request, 'home.html')  # Ensure you have a template named 'home.html'
    return render(request, 'code_evaluator/home.html')


# Define your model checkpoints
MODEL_1_CHECKPOINT = 'EleutherAI/gpt-neo-1.3B'
MODEL_2_CHECKPOINT = 'microsoft/CodeGPT-small-py'


@require_http_methods(["POST"])
@csrf_exempt
def generate_and_evaluate(request):
    results = {}
    for exercise in NewExercise.objects.all():
        # Generate solutions for both models if not already generated
        if not exercise.generated_solution_model1:
            exercise.generated_solution_model1 = generate_solution(
                exercise.description, MODEL_1_CHECKPOINT)
            exercise.save()

        if not exercise.generated_solution_model2:
            exercise.generated_solution_model2 = generate_solution(
                exercise.description, MODEL_2_CHECKPOINT)
            exercise.save()

        # Evaluate solutions for both models
        evaluation_result_model1 = evaluate_solution(
            exercise.generated_solution_model1, 
            exercise.expected_solution,
            exercise.test_cases)
        evaluation_result_model2 = evaluate_solution(
            exercise.generated_solution_model2, 
            exercise.expected_solution,
            exercise.test_cases)

        # Update evaluation metrics
        exercise.evaluation_metrics_model1 = evaluation_result_model1
        exercise.evaluation_metrics_model2 = evaluation_result_model2
        exercise.save()

        results[exercise.exercise_id] = {
            'model1_metrics': exercise.evaluation_metrics_model1,
            'model2_metrics': exercise.evaluation_metrics_model2
        }
    return JsonResponse(results)


@api_view(['GET'])
def get_exercise(request, exercise_id):
    exercise = get_object_or_404(NewExercise, exercise_id=exercise_id)

    # Ensure solutions are generated for both models
    if not exercise.generated_solution_model1:
        exercise.generated_solution_model1 = generate_solution(
            exercise.description, 'MODEL_1_CHECKPOINT')  # Replace with actual model checkpoint
        exercise.save()

    if not exercise.generated_solution_model2:
        exercise.generated_solution_model2 = generate_solution(
            exercise.description, 'MODEL_2_CHECKPOINT')  # Replace with actual model checkpoint
        exercise.save()

    data = {
        'exercise_id': exercise.exercise_id,
        'description': exercise.description,
        'expected_solution': exercise.expected_solution,
        'generated_solution_model1': exercise.generated_solution_model1,
        'evaluation_metrics_model1': exercise.evaluation_metrics_model1,
        'generated_solution_model2': exercise.generated_solution_model2,
        'evaluation_metrics_model2': exercise.evaluation_metrics_model2,
        'programming_language': exercise.programming_language,
        'difficulty_level': exercise.difficulty_level,
    }
    return Response(data)
