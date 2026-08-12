from rest_framework import generics, permissions

from .models import WasteScan
from .serializers import WasteScanSerializer

from ai.predictor import predict_waste

from accounts.models import EcoProfile


# =========================================================
# AI ANALYSIS
# =========================================================

def analyze_waste(image):

    return predict_waste(image)


# =========================================================
# CREATE WASTE SCAN
# =========================================================

class WasteScanCreateView(
    generics.CreateAPIView
):

    serializer_class = WasteScanSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def perform_create(self, serializer):

        # -------------------------------------------------
        # Get uploaded image
        # -------------------------------------------------

        image = serializer.validated_data.get(
            "image"
        )

        # -------------------------------------------------
        # AI prediction
        # -------------------------------------------------

        result = analyze_waste(image)

        # -------------------------------------------------
        # Check AI error
        # -------------------------------------------------

        if "error" in result:

            raise Exception(
                "AI prediction failed: "
                + result["error"]
            )

        # -------------------------------------------------
        # Save scan
        # -------------------------------------------------

        serializer.save(

            user=self.request.user,

            waste_type=result[
                "waste_type"
            ],

            confidence_score=result[
                "confidence_score"
            ],

            recommendation=result[
                "recommendation"
            ],
        )

        # -------------------------------------------------
        # Eco Profile
        # -------------------------------------------------

        profile, created = (
            EcoProfile.objects.get_or_create(
                user=self.request.user
            )
        )

        # -------------------------------------------------
        # Points
        # -------------------------------------------------

        points_map = {

            "Organic": 15,

            "Plastic": 10,

            "Metal": 20,

            "Paper": 10,

            "Glass": 10,

            "Other": 5,

            "E-Waste": 25,
        }

        earned_points = points_map.get(
            result["waste_type"],
            5
        )

        # -------------------------------------------------
        # Update profile
        # -------------------------------------------------

        profile.eco_points += earned_points

        profile.total_scans += 1

        # -------------------------------------------------
        # Update badge
        # -------------------------------------------------

        profile.update_badge()

        profile.save()


# =========================================================
# WASTE SCAN LIST
# =========================================================

class WasteScanListView(
    generics.ListAPIView
):

    serializer_class = WasteScanSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):

        return WasteScan.objects.filter(

            user=self.request.user

        ).order_by(
            "-created_at"
        )