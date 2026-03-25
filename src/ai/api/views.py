from dataclasses import asdict
import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.api.serializers import AgentQuerySerializer
from ai.core.contracts import RequestContract
from ai.core.error_codes import VALIDATION_ERROR
from ai.core.logger import log_event
from ai.core.tracing import TraceContext, generate_request_id
from ai.supervisor.main import run_supervisor
from ai.models import Request  # ✅ NEW IMPORT

class AgentQueryAPIView(APIView):
    def post(self, request):
        request_id = generate_request_id()
        trace = TraceContext(request_id=request_id)

        log_event(
            event="request_received",
            layer="api",
            request_id=request_id,
        )
        trace.add_step(layer="api", event="request_received")

        serializer = AgentQuerySerializer(data=request.data)

        if not serializer.is_valid():
            log_event(
                event="validation_failed",
                layer="api",
                request_id=request_id,
                errors=serializer.errors,
            )
            trace.add_step(
                layer="api",
                event="validation_failed",
                errors=serializer.errors,
            )

            return Response(
                {
                    "status": "failure",
                    "selected_agent": None,
                    "result": None,
                    "error": {
                        "code": VALIDATION_ERROR,
                        "message": "Invalid request body",
                        "details": serializer.errors,
                    },
                    "meta": trace.to_dict(),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data

        # ✅ NEW: Create Request record in DB
        db_request = Request.objects.create(
            request_id=request_id,
            user_id=validated_data.get("user_id"),
            input_text=validated_data["message"],
            status="pending",
        )

        request_contract = RequestContract(
            user_id=validated_data.get("user_id"),
            message=validated_data["message"],
            context=validated_data.get("context", {}),
            constraints=validated_data.get("constraints", {}),
        )

        log_event(
            event="supervisor_called",
            layer="api",
            request_id=request_id,
        )
        trace.add_step(layer="api", event="supervisor_called")

        supervisor_result = run_supervisor(
            request_contract,
            request_id=request_id,
            trace=trace,
        )

        response_data = asdict(supervisor_result)

        log_event(
            event="response_returned",
            layer="api",
            request_id=request_id,
            status=response_data.get("status"),
        )
        trace.add_step(
            layer="api",
            event="response_returned",
            status=response_data.get("status"),
        )

        response_data["meta"] = {
            **response_data.get("meta", {}),
            **trace.to_dict(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

