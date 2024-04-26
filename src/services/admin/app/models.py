import uuid

from django.db import models

from app.choices import PlanType, InstanceTier, InstanceType


class DeploymentPlan(models.Model):
    """
    This model will store each plan type which depict the EC2 instance type,
    Configured by the Admin
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        db_index=True,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    plan = models.CharField(
        max_length=5,
        choices=PlanType.get_values(),
        unique=True,
        error_messages={'unique': 'Plan already exists'}
    )
    instance_tier = models.CharField(
        max_length=10,
        choices=InstanceTier.get_values()
    )
    instance_type = models.CharField(
        max_length=10,
        choices=InstanceType.get_values()
    )

    class Meta:
        ordering = ('-modified_at',)

    def __str__(self):
        return f'{self.get_plan_display()}: {self.get_instance_tier_display()}.{self.instance_type}'
