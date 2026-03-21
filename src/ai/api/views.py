from dataclasses import asdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.api.serializers import AgentQuerySerializer
from ai.core.contracts import RequestContract

from ai.supervisor.main import run_supervisor


class AgentQueryAPIView(APIView):
    def post(self, request):
        serializer = AgentQuerySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "status": "failure",
                    "selected_agent": None,
                    "result": None,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Invalid request body",
                        "details": serializer.errors,
                    },
                    "meta": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data

        request_contract = RequestContract(
            user_id=validated_data.get("user_id"),
            message=validated_data["message"],
            context=validated_data.get("context", {}),
            constraints=validated_data.get("constraints", {}),
        )

        supervisor_result = run_supervisor(request_contract)

        return Response(asdict(supervisor_result), status=status.HTTP_200_OK)