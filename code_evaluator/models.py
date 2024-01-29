from django.db import models


class NewExercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    description = models.TextField()
    expected_solution = models.TextField()

    # Fields to store AI-generated solutions
    generated_solution_model1 = models.TextField(blank=True, null=True)
    generated_solution_model2 = models.TextField(blank=True, null=True)

    # Fields to store evaluation metrics for each model
    evaluation_metrics_model1 = models.JSONField(blank=True, null=True)
    evaluation_metrics_model2 = models.JSONField(blank=True, null=True)

    programming_language = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20)
    test_cases = models.JSONField(blank=True, null=True)
