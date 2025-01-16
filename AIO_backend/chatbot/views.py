from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

class ChatbotView(APIView):
    permission_classes = [AllowAny] 
    """
    POST /api/chatbot/chat/
    Body: {
        "email": <string>,
        "message": <string>,
        "timestamp": <string>
    }
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user_message = request.data.get('message')
        timestamp = request.data.get('timestamp')  # 실제 사용 여부는 선택

        # (선택) email, message 유효성 체크
        if not user_message:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 1) 여기서 AI 서버나 로컬 로직으로 챗봇 응답 생성
        #    예: bot_response = some_ai_logic(user_message) 
        bot_response = self._dummy_response(user_message)

        # 2) (선택) DB에 대화 기록 저장, 사용자 식별 위해 email 활용
        # ChatHistory.objects.create(email=email, question=user_message, answer=bot_response, ...)

        # 3) 프론트가 원하는 JSON 구조로 응답
        return Response(
            {"responseMessage": bot_response},
            status=status.HTTP_200_OK
        )

    def _dummy_response(self, message):
        """
        실제 AI 로직 대신, 간단한 테스트 응답.
        """
        return f"'{message}' 라는 메시지를 받았습니다! 답변 준비 중이에요."