from rest_framework import generics, permissions

from .models import WasteScan
from .serializers import WasteScanSerializer

from accounts.models import EcoProfile


def analyze_waste(image):
    """
    Real AI prediction.
    AI module is imported only when waste scanning is requested,
    so Django startup does not load PyTorch immediately.
    """

    from ai.predictor import predict_waste

    result = predict_waste(image)

    return result


class WasteScanCreateView(generics.CreateAPIView):

    serializer_class = WasteScanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        image = serializer.validated_data.get("image")

        # AI Prediction
        result = analyze_waste(image)

        # Save Scan
        scan = serializer.save(
            user=self.request.user,
            waste_type=result["waste_type"],
            confidence_score=result["confidence_score"],
            recommendation=result["recommendation"]
        )

        # =========================
        # ECO POINT UPDATE
        # =========================

        profile, created = EcoProfile.objects.get_or_create(
            user=self.request.user
        )

        points_map = {
            "Organic": 15,
            "Plastic": 10,
            "Metal": 20,
            "Paper": 10,
            "E-Waste": 25
        }

        earned_points = points_map.get(
            result["waste_type"],
            5
        )

        profile.eco_points += earned_points
        profile.total_scans += 1

        profile.update_badge()

        profile.save()


class WasteScanListView(generics.ListAPIView):

    serializer_class = WasteScanSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):

        return WasteScan.objects.filter(
            user=self.request.user
        ).order_by("-created_at")