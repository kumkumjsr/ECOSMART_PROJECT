from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Complaint
from .serializers import ComplaintSerializer



class CreateComplaintView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        serializer = ComplaintSerializer(
            data=request.data
        )


        if serializer.is_valid():

            serializer.save(
                user=request.user
            )


            return Response({

                "message":
                "Complaint submitted successfully"

            })


        return Response(
            serializer.errors,
            status=400
        )




class MyComplaintView(APIView):

    permission_classes=[
        IsAuthenticated
    ]


    def get(self,request):

        complaints = Complaint.objects.filter(
            user=request.user
        ).order_by("-created_at")


        serializer = ComplaintSerializer(
            complaints,
            many=True
        )


        return Response(
            serializer.data
        )

# ==================================
# ADMIN VIEW ALL COMPLAINTS
# ==================================

class AdminComplaintListView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        complaints = Complaint.objects.all().order_by(
            "-created_at"
        )


        serializer = ComplaintSerializer(
            complaints,
            many=True
        )


        return Response(
            serializer.data
        )



# ==================================
# ADMIN UPDATE STATUS
# ==================================

class UpdateComplaintStatusView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, id):

        try:

            complaint = Complaint.objects.get(
                id=id
            )

        except Complaint.DoesNotExist:

            return Response(
                {
                    "error":
                    "Complaint not found"
                },
                status=404
            )


        complaint.status = request.data.get(
            "status"
        )


        complaint.save()


        return Response(
            {
                "message":
                "Complaint status updated"
            }
        )
    