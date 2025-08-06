from django.db import models
import datetime 
from django.utils import timezone
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    
    
    def __str__(self):
        return f"this is question {self.question_text} \n this is the id {self.id} \n this is the date {self.pub_date}"
  
   
    
class Choice(models.Model):
  
    choice_text = models.CharField(max_length = 200)
    votes  = models.IntegerField(default = 0)
  
    
    def __str__(self):
        return f"this is for the choice id: {self.id}\t question: {self.question}\t choice text: {self.choice_text}\t votes: {self.votes}"
    
class Check(models.Model):
    checkOne  = models.ForeignKey(Choice, on_delete = models.CASCADE)
    correct123 = models.BooleanField(default = False)
    
    def __str__(self):
        return f"this is for the Check table {self.checkOne}\t and {self.correct}"

    