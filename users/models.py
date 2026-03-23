from django.db import models

class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=10)
    email = models.EmailField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.TextField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='waiting')

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'user_registrations'


class PredictionHistory(models.Model):
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    cell_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'prediction_history'
        ordering = ['-timestamp']


class TrainingHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    epochs_completed = models.IntegerField(default=0)
    final_accuracy = models.FloatField(blank=True, null=True)
    final_val_accuracy = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=50, default='completed')

    class Meta:
        db_table = 'training_history'
        ordering = ['-timestamp']
