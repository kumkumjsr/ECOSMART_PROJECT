from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Dustbin
from .serializers import DustbinSerializer


# =========================================================
# USER / GENERAL - LIST ACTIVE DUSTBINS
# =========================================================

class DustbinListView(ListAPIView):

    queryset = Dustbin.objects.filter(
        is_active=True
    ).order_by("name")

    serializer_class = DustbinSerializer


# =========================================================
# ADMIN - CREATE DUSTBIN
# =========================================================

class CreateDustbinView(CreateAPIView):

    queryset = Dustbin.objects.all()

    serializer_class = DustbinSerializer

    permission_classes = [
        IsAdminUser
    ]


# =========================================================
# USER - REPORT DUSTBIN AS FULL
# =========================================================

class ReportDustbinView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, id):

        try:

            dustbin = Dustbin.objects.get(
                id=id
            )

            dustbin.is_full = True

            dustbin.save()

            return Response({

                "message":
                "Dustbin reported as full successfully"

            })

        except Dustbin.DoesNotExist:

            return Response({

                "error":
                "Dustbin not found"

            }, status=404)


# =========================================================
# ADMIN - REPORTED / FULL DUSTBINS
# =========================================================

class ReportedDustbinListView(APIView):

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        dustbins = Dustbin.objects.filter(
            is_full=True
        ).order_by("-id")

        data = []

        for dustbin in dustbins:

            data.append({

                "id": dustbin.id,

                "name": dustbin.name,

                "type": dustbin.dustbin_type,

                "address": dustbin.address,

                "latitude": dustbin.latitude,

                "longitude": dustbin.longitude,

                "status": "FULL"

            })

        return Response(data)