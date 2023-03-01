from django.db import models
from django.contrib.auth.models import User


class Tarefa(models.Model):
    
    choices_status = (
        ('doing', 'Doing'),
        ('done', 'Done')
    )


    titulo = models.CharField(max_length=60)
    descricao = models.TextField()
    status = models.CharField(
        max_length=5,
        choices=choices_status,
        default='doing',
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Tarefa: ' + self.titulo