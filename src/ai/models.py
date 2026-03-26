from django.db import models


class Request(models.Model):
    request_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)

    input_text = models.TextField()

    # pending → success / failure
    status = models.CharField(max_length=20, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_id


class Response(models.Model):
    request = models.OneToOneField(
        Request, on_delete=models.CASCADE, related_name="response"
    )

    # store structured output (better than plain text)
    output_data = models.JSONField(null=True, blank=True)

    status = models.CharField(max_length=20)  # success / failure

    # structured error (aligned with ErrorContract)
    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class ToolExecution(models.Model):
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name="tool_executions"
    )

    tool_name = models.CharField(max_length=100)

    input_data = models.JSONField()
    output_data = models.JSONField(null=True, blank=True)

    status = models.CharField(max_length=20)  # success / failure

    # structured error
    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)