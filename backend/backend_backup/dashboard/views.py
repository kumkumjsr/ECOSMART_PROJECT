from datetime import date

from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated
)

from accounts.models import User, EcoProfile
from waste.models import WasteScan



# ============================
# ADMIN DASHBOARD
# ============================

class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]


    def get(self, request):

        total_users = User.objects.filter(
            role="CITIZEN"
        ).count()


        total_staff = User.objects.filter(
            role="WORKER"
        ).count()


        total_scans = WasteScan.objects.count()



        # Waste Analytics

        waste_counts = (
            WasteScan.objects
            .values("waste_type")
            .annotate(
                count=Count("id")
            )
        )


        chart_data = []


        for item in waste_counts:

            chart_data.append({

                "name": item["waste_type"],

                "value": item["count"]

            })



        # Recent Users

        recent_users = User.objects.filter(
            role="CITIZEN"
        ).order_by("-date_joined")[:5]


        users = []


        for user in recent_users:

            users.append({

                "id": user.id,

                "username": user.username,

                "email": user.email,

                "phone": user.phone,

                "date": user.date_joined

            })



        # Recent Staff

        recent_staff = User.objects.filter(
            role="WORKER"
        ).order_by("-date_joined")[:5]


        staff = []


        for employee in recent_staff:

            staff.append({

                "id": employee.id,

                "username": employee.username,

                "email": employee.email,

                "phone": employee.phone,

                "date": employee.date_joined

            })



        # Recent Waste Scans

        recent_scans = WasteScan.objects.order_by(
            "-created_at"
        )[:5]


        scans = []


        for scan in recent_scans:

            scans.append({

                "id": scan.id,

                "waste_type": scan.waste_type,

                "confidence": scan.confidence_score,

                "date": scan.created_at

            })



        return Response({

            "total_users": total_users,

            "total_staff": total_staff,

            "total_scans": total_scans,

            "chart_data": chart_data,

            "recent_users": users,

            "recent_staff": staff,

            "recent_scans": scans

        })







# ============================
# USER DASHBOARD
# ============================


class UserDashboardView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        user = request.user



        scans = WasteScan.objects.filter(
            user=user
        )


        total_scans = scans.count()



        today_scans = scans.filter(
            created_at__date=date.today()
        ).count()




        # ============================
        # ECO PROFILE
        # ============================


        profile, created = EcoProfile.objects.get_or_create(
            user=user
        )


        eco_points = profile.eco_points


        badge = profile.badge



        # Next Badge

        if eco_points >= 500:

            next_badge = "Maximum Level"


        elif eco_points >= 250:

            next_badge = "Eco Champion"


        elif eco_points >= 100:

            next_badge = "Green Hero"


        else:

            next_badge = "Eco Explorer"







        # ============================
        # CATEGORY ANALYTICS
        # ============================


        waste_summary = (

            scans
            .values("waste_type")
            .annotate(
                value=Count("id")
            )

        )



        category_data = []



        for item in waste_summary:

            category_data.append({

                "name": item["waste_type"],

                "value": item["value"]

            })






        # ============================
        # ENVIRONMENT IMPACT
        # ============================


        co2_saved = total_scans * 1


        trees_saved = round(
            total_scans / 10,
            1
        )






        # ============================
        # RECENT SCANS
        # ============================


        recent = scans.order_by(
            "-created_at"
        )[:5]



        recent_data = []



        for scan in recent:


            recent_data.append({

                "id": scan.id,

                "image": (
                    scan.image.url
                    if scan.image
                    else None
                ),

                "waste_type": scan.waste_type,

                "confidence": scan.confidence_score,

                "recommendation": scan.recommendation,

                "date": scan.created_at

            })






        return Response({

            "username": user.username,

            "total_scans": total_scans,

            "today_scans": today_scans,

            "eco_points": eco_points,

            "badge": badge,

            "next_badge": next_badge,


            "category_data": category_data,


            "environment": {

                "co2_saved": f"{co2_saved} kg",

                "trees_saved": trees_saved

            },


            "recent_scans": recent_data

        })