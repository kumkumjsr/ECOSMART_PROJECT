from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.mail import send_mail
from django.conf import settings

from notifications.models import Notification

from .models import (
    User,
    Salary,
    EcoProfile,
    AdminSettings,
)

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    CreateStaffSerializer,
    SalarySerializer,
    ProfileSerializer,
)


# =========================================================
# REGISTER
# =========================================================

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            user = serializer.save()

            return Response(
                {
                    "message": "Registration successful",
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            print("REGISTER ERROR:", repr(e))

            return Response(
                {
                    "error": "Registration failed",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =========================================================
# LOGIN
# =========================================================

class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


# =========================================================
# PROFILE
# =========================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(
            request.user
        )

        profile, created = EcoProfile.objects.get_or_create(
            user=request.user
        )

        data = serializer.data

        data.update({
            "id": request.user.id,
            "role": request.user.role,
            "eco_points": profile.eco_points,
            "total_scans": profile.total_scans,
            "badge": profile.badge,
        })

        return Response(data)

    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# DASHBOARD STATS
# =========================================================

class DashboardStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({

            "total_users":
                User.objects.filter(
                    role=User.CITIZEN
                ).count(),

            "total_staff":
                User.objects.filter(
                    role=User.WORKER
                ).count(),

            "total_admin":
                User.objects.filter(
                    role=User.ADMIN
                ).count(),

            "total_accounts":
                User.objects.count(),

        })


# =========================================================
# USER LIST
# =========================================================

class UserListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_queryset(self):

        return User.objects.filter(
            role=User.CITIZEN
        ).order_by("-date_joined")


# =========================================================
# STAFF LIST
# =========================================================

class StaffListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CreateStaffSerializer

    def get_queryset(self):

        return User.objects.filter(
            role=User.WORKER
        ).order_by("-date_joined")


# =========================================================
# CREATE STAFF
# =========================================================

class CreateStaffView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = CreateStaffSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        print("===================================")
        print("CREATE STAFF REQUEST")
        print("USER:", request.user.username)
        print("ROLE:", request.user.role)
        print("DATA:", request.data)
        print("===================================")

        serializer = self.get_serializer(
            data=request.data
        )

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not serializer.is_valid():

            print(
                "STAFF VALIDATION ERROR:",
                serializer.errors
            )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # CREATE STAFF
        # -----------------------------------------

        try:

            staff = serializer.save()

            print(
                "STAFF CREATED:",
                staff.username,
                staff.id
            )

        except Exception as e:

            print(
                "STAFF CREATE ERROR:",
                repr(e)
            )

            return Response(
                {
                    "error": "Staff creation failed",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -----------------------------------------
        # NOTIFICATION
        # -----------------------------------------
        # IMPORTANT:
        # Notification fail hone par staff creation
        # fail nahi hoga.

        try:

            Notification.objects.create(

                user=request.user,

                title="New Staff Added",

                message=(
                    f"{staff.username} "
                    f"joined EcoSmart as staff"
                ),

                notification_type="SYSTEM"
            )

            print(
                "NOTIFICATION CREATED"
            )

        except Exception as e:

            print(
                "NOTIFICATION ERROR:",
                repr(e)
            )

        # -----------------------------------------
        # EMAIL
        # -----------------------------------------

        try:

            send_mail(

                subject="Welcome to EcoSmart Staff Team 🌱",

                message=f"""
Hello {staff.first_name or staff.username},

Welcome to EcoSmart Staff Team.

Your staff account has been created successfully.

Username:
{staff.username}

Role:
{staff.role}

EcoSmart Team
""",

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    staff.email
                ],

                fail_silently=True
            )

            print(
                "STAFF EMAIL PROCESS COMPLETED"
            )

        except Exception as e:

            print(
                "STAFF EMAIL ERROR:",
                repr(e)
            )

        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        return Response(

            {
                "message":
                    "Staff created successfully",

                "id":
                    staff.id,

                "username":
                    staff.username,

                "email":
                    staff.email,

                "role":
                    staff.role,
            },

            status=status.HTTP_201_CREATED
        )


# =========================================================
# DELETE USER
# =========================================================

class DeleteUserView(generics.DestroyAPIView):

    queryset = User.objects.filter(
        role=User.CITIZEN
    )

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def delete(self, request, *args, **kwargs):

        user = self.get_object()

        user.delete()

        return Response({
            "message":
                "User deleted successfully"
        })


# =========================================================
# DELETE STAFF
# =========================================================

class DeleteStaffView(generics.DestroyAPIView):

    queryset = User.objects.filter(
        role=User.WORKER
    )

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def delete(self, request, *args, **kwargs):

        staff = self.get_object()

        staff.delete()

        return Response({
            "message":
                "Staff deleted successfully"
        })


# =========================================================
# UPDATE STAFF
# =========================================================

class UpdateStaffView(generics.UpdateAPIView):

    queryset = User.objects.filter(
        role=User.WORKER
    )

    serializer_class = CreateStaffSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "id"


# =========================================================
# UPDATE USER
# =========================================================

class UpdateUserView(generics.UpdateAPIView):

    queryset = User.objects.filter(
        role=User.CITIZEN
    )

    serializer_class = RegisterSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "id"


# =========================================================
# REWARDS
# =========================================================

class RewardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile, created = EcoProfile.objects.get_or_create(
            user=request.user
        )

        points = profile.eco_points

        rewards = [

            {
                "id": 1,
                "name": "🌱 Eco Beginner",
                "required_points": 0,
                "description": "Start your eco journey",
                "unlocked": True
            },

            {
                "id": 2,
                "name": "🥉 Eco Explorer",
                "required_points": 100,
                "description":
                    "Complete waste scans and save environment",
                "unlocked":
                    points >= 100
            },

            {
                "id": 3,
                "name": "🥈 Green Hero",
                "required_points": 250,
                "description":
                    "Become a regular waste recycler",
                "unlocked":
                    points >= 250
            },

            {
                "id": 4,
                "name": "🥇 Eco Champion",
                "required_points": 500,
                "description":
                    "Amazing contribution towards clean city",
                "unlocked":
                    points >= 500
            },

            {
                "id": 5,
                "name": "🌍 Earth Guardian",
                "required_points": 1000,
                "description":
                    "Ultimate environmental protector",
                "unlocked":
                    points >= 1000
            },

        ]

        next_reward = None

        for reward in rewards:

            if not reward["unlocked"]:

                next_reward = reward

                break

        if next_reward:

            progress = (
                points /
                next_reward["required_points"]
            ) * 100

            progress = min(
                round(progress, 2),
                100
            )

        else:

            progress = 100

        return Response({

            "username":
                request.user.username,

            "eco_points":
                points,

            "badge":
                profile.badge,

            "total_scans":
                profile.total_scans,

            "progress":
                progress,

            "next_reward":
                next_reward,

            "rewards":
                rewards,

        })


# =========================================================
# ADMIN SETTINGS
# =========================================================

class AdminSettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        settings_obj, created = (
            AdminSettings.objects.get_or_create(
                user=request.user
            )
        )

        return Response({

            "email_notifications":
                settings_obj.email_notifications,

            "task_notifications":
                settings_obj.task_notifications,

            "system_notifications":
                settings_obj.system_notifications,

            "dark_mode":
                settings_obj.dark_mode,

        })

    def put(self, request):

        settings_obj, created = (
            AdminSettings.objects.get_or_create(
                user=request.user
            )
        )

        settings_obj.email_notifications = (
            request.data.get(
                "email_notifications",
                settings_obj.email_notifications
            )
        )

        settings_obj.task_notifications = (
            request.data.get(
                "task_notifications",
                settings_obj.task_notifications
            )
        )

        settings_obj.system_notifications = (
            request.data.get(
                "system_notifications",
                settings_obj.system_notifications
            )
        )

        settings_obj.dark_mode = (
            request.data.get(
                "dark_mode",
                settings_obj.dark_mode
            )
        )

        settings_obj.save()

        return Response({

            "message":
                "Admin settings updated successfully",

            "email_notifications":
                settings_obj.email_notifications,

            "task_notifications":
                settings_obj.task_notifications,

            "system_notifications":
                settings_obj.system_notifications,

            "dark_mode":
                settings_obj.dark_mode,

        })


# =========================================================
# CHANGE PASSWORD
# =========================================================

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        current_password = request.data.get(
            "current_password"
        )

        new_password = request.data.get(
            "new_password"
        )

        confirm_password = request.data.get(
            "confirm_password"
        )

        if not current_password:

            return Response(
                {
                    "error":
                        "Current password is required"
                },
                status=400
            )

        if not new_password:

            return Response(
                {
                    "error":
                        "New password is required"
                },
                status=400
            )

        if not confirm_password:

            return Response(
                {
                    "error":
                        "Confirm password is required"
                },
                status=400
            )

        if not check_password(
            current_password,
            request.user.password
        ):

            return Response(
                {
                    "error":
                        "Current password is incorrect"
                },
                status=400
            )

        if new_password != confirm_password:

            return Response(
                {
                    "error":
                        "New passwords do not match"
                },
                status=400
            )

        if len(new_password) < 8:

            return Response(
                {
                    "error":
                        "Password must be at least 8 characters"
                },
                status=400
            )

        if check_password(
            new_password,
            request.user.password
        ):

            return Response(
                {
                    "error":
                        "New password must be different from current password"
                },
                status=400
            )

        request.user.set_password(
            new_password
        )

        request.user.save()

        return Response({
            "message":
                "Password changed successfully"
        })


# =========================================================
# SETTINGS
# =========================================================

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({

            "email_notifications": True,
            "task_notifications": True,
            "system_notifications": True,
            "dark_mode": False,

        })


# =========================================================
# SALARY LIST + CREATE
# =========================================================

class SalaryListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        salaries = (
            Salary.objects
            .select_related("staff")
            .filter(
                staff__role=User.WORKER
            )
            .order_by(
                "-year",
                "-id"
            )
        )

        serializer = SalarySerializer(
            salaries,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = SalarySerializer(
            data=request.data
        )

        if serializer.is_valid():

            salary = serializer.save()

            return Response(
                SalarySerializer(
                    salary
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# SALARY DETAIL
# =========================================================

class SalaryDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:

            return Salary.objects.select_related(
                "staff"
            ).get(
                pk=pk
            )

        except Salary.DoesNotExist:

            return None

    def get(self, request, pk):

        salary = self.get_object(pk)

        if not salary:

            return Response(
                {
                    "error":
                        "Salary record not found"
                },
                status=404
            )

        return Response(
            SalarySerializer(
                salary
            ).data
        )

    def put(self, request, pk):

        salary = self.get_object(pk)

        if not salary:

            return Response(
                {
                    "error":
                        "Salary record not found"
                },
                status=404
            )

        serializer = SalarySerializer(
            salary,
            data=request.data
        )

        if serializer.is_valid():

            salary = serializer.save()

            return Response(
                SalarySerializer(
                    salary
                ).data
            )

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        salary = self.get_object(pk)

        if not salary:

            return Response(
                {
                    "error":
                        "Salary record not found"
                },
                status=404
            )

        salary.delete()

        return Response({
            "message":
                "Salary record deleted successfully"
        })


# =========================================================
# STAFF SALARY
# =========================================================

class StaffSalaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        salaries = Salary.objects.filter(
            staff=request.user
        )

        serializer = SalarySerializer(
            salaries,
            many=True
        )

        return Response(
            serializer.data
        )


# =========================================================
# PROFILE UPDATE
# =========================================================

class ProfileUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        user = request.user

        serializer = ProfileSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )