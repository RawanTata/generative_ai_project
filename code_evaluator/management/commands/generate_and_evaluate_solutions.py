from django.core.management.base import BaseCommand
from code_evaluator.models import NewExercise
from code_evaluator.utils import generate_solution, post_process_generated_code, evaluate_correctness, evaluate_efficiency, evaluate_best_practices
# Import necessary utilities for evaluation
import time


MODEL_1_CHECKPOINT = 'EleutherAI/gpt-neo-1.3B'
MODEL_2_CHECKPOINT = 'microsoft/CodeGPT-small-py'

class Command(BaseCommand):
    help = 'Generate and evaluate solutions for all exercises using two models'

    def handle(self, *args, **kwargs):
        for exercise in NewExercise.objects.all():
            if not exercise.generated_solution_model1:
                exercise.generated_solution_model1 = generate_solution(exercise.description, MODEL_1_CHECKPOINT)
            if not exercise.generated_solution_model2:
                exercise.generated_solution_model2 = generate_solution(exercise.description, MODEL_2_CHECKPOINT)
            
            # Evaluate solutions from both models
            correctness_model1 = evaluate_correctness(exercise.generated_solution_model1, exercise.test_cases)
            efficiency_model1 = evaluate_efficiency(exercise.generated_solution_model1)
            best_practices_model1 = evaluate_best_practices(exercise.generated_solution_model1)

            correctness_model2 = evaluate_correctness(exercise.generated_solution_model2, exercise.test_cases)
            efficiency_model2 = evaluate_efficiency(exercise.generated_solution_model2)
            best_practices_model2 = evaluate_best_practices(exercise.generated_solution_model2)

            # Update the exercise object with the evaluation results for both models
            exercise.evaluation_metrics_model1 = {
                'correctness': correctness_model1,
                'efficiency': efficiency_model1,
                'best_practices': best_practices_model1
            }
            exercise.evaluation_metrics_model2 = {
                'correctness': correctness_model2,
                'efficiency': efficiency_model2,
                'best_practices': best_practices_model2
            }
            exercise.save()

            self.stdout.write(self.style.SUCCESS(f'Processed and evaluated exercise ID {exercise.exercise_id} using both models'))

# Ensure the evaluation functions (evaluate_correctness, evaluate_efficiency, evaluate_best_practices)
# are correctly defined and handle the output of both models appropriately.


