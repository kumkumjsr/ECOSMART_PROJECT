from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from notifications.models import Notification

from .models import User, Salary, EcoProfile, AdminSettings

from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    CreateStaffSerializer,
    SalarySerializer,
    ProfileSerializer,
)


# ============================================================
# REGISTER API
# ============================================================

# class RegisterView(generics.CreateAPIView):

#     queryset = User.objects.all()

#     serializer_class = RegisterSerializer

#     def perform_create(self, serializer):

#         # Create user first
#         user = serializer.save()

#         # Send welcome email
#         # Email failure should NOT break registration
#         try:

#             if user.email:

#                 send_mail(

#                     subject="🎉 Welcome to EcoSmart",

#                     message=f"""
# Hello {user.first_name or user.username},

# Welcome to EcoSmart 🌱

# Your EcoSmart account has been created successfully.

# ===========================
# Login Details
# ===========================

# Username : {user.username}
# Email    : {user.email}
# Role     : {user.role}

# Thank you for joining EcoSmart.

# Regards,
# EcoSmart Team
# """,

#                     from_email=settings.DEFAULT_FROM_EMAIL,

#                     recipient_list=[user.email],

#                     fail_silently=True,
#                 )

#         except Exception as e:

#             print(
#                 "WELCOME EMAIL ERROR:",
#                 e
#             )


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        print("========== REGISTER START ==========")
        print("REGISTER DATA:", request.data)

        try:

            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():

                print("SERIALIZER ERROR:")
                print(serializer.errors)

                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.save()

            print("USER CREATED:", user.username)
            print("USER EMAIL:", user.email)

            # Email
            try:

                send_mail(
                    subject="🎉 Welcome to EcoSmart",

                    message=f"""
Hello {user.first_name or user.username},

Welcome to EcoSmart 🌱

Your EcoSmart account has been created successfully.

Username : {user.username}
Email    : {user.email}
Role     : {user.role}

Thank you for joining EcoSmart.

Regards,
EcoSmart Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[user.email],

                    fail_silently=True
                )

                print("EMAIL STEP COMPLETED")

            except Exception as email_error:

                print("EMAIL ERROR:", repr(email_error))

            print("========== REGISTER SUCCESS ==========")

            return Response(
                {
                    "message": "Registration successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            print("========== REGISTER ERROR ==========")
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR:", repr(e))
            print("========== REGISTER ERROR END ==========")

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





# ============================================================
# LOGIN API
# ============================================================

class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


# ============================================================
# DASHBOARD STATS
# ============================================================

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


# ============================================================
# USER LIST
# ============================================================

class UserListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = RegisterSerializer

    def get_queryset(self):

        return User.objects.filter(
            role=User.CITIZEN
        ).order_by("-date_joined")


# ============================================================
# STAFF LIST
# ============================================================

class StaffListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = CreateStaffSerializer

    def get_queryset(self):

        return User.objects.filter(
            role=User.WORKER
        ).order_by("-date_joined")


# ============================================================
# CREATE STAFF
# ============================================================

class CreateStaffView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = CreateStaffSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        # Create staff
        staff = serializer.save()

        # Notify admin
        try:

            Notification.objects.create(

                user=self.request.user,

                title="New Staff Added",

                message=(
                    f"{staff.username} "
                    f"joined EcoSmart as staff"
                ),

                notification_type="SYSTEM",
            )

        except Exception as e:

            print(
                "STAFF NOTIFICATION ERROR:",
                e
            )

        # Welcome email
        try:

            if staff.email:

                send_mail(

                    subject="Welcome to EcoSmart Staff 🌱",

                    message=f"""
Hello {staff.first_name or staff.username},

Welcome to EcoSmart Team.

Your staff account has been created successfully.

Username:
{staff.username}

Email:
{staff.email}

Role:
{staff.role}

Regards,
EcoSmart Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        staff.email
                    ],

                    fail_silently=True,
                )

        except Exception as e:

            print(
                "STAFF EMAIL ERROR:",
                e
            )


# ============================================================
# DELETE USER
# ============================================================

class DeleteUserView(generics.DestroyAPIView):

    queryset = User.objects.filter(
        role=User.CITIZEN
    )

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def delete(self, request, *args, **kwargs):

        user = self.get_object()

        user.delete()

        return Response(

            {
                "message":
                    "User deleted successfully"
            },

            status=status.HTTP_200_OK
        )


# ============================================================
# DELETE STAFF
# ============================================================

class DeleteStaffView(generics.DestroyAPIView):

    queryset = User.objects.filter(
        role=User.WORKER
    )

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def delete(self, request, *args, **kwargs):

        staff = self.get_object()

        staff.delete()

        return Response(

            {
                "message":
                    "Staff deleted successfully"
            },

            status=status.HTTP_200_OK
        )


# ============================================================
# UPDATE STAFF
# ============================================================

class UpdateStaffView(generics.UpdateAPIView):

    queryset = User.objects.filter(
        role=User.WORKER
    )

    serializer_class = CreateStaffSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def update(self, request, *args, **kwargs):

        response = super().update(
            request,
            *args,
            **kwargs
        )

        staff = self.get_object()

        # Send email but don't break update
        try:

            if staff.email:

                send_mail(

                    subject="EcoSmart Staff Profile Updated 🌱",

                    message=f"""
Hello {staff.first_name or staff.username},

Your EcoSmart staff profile has been updated successfully.

Username:
{staff.username}

Email:
{staff.email}

Phone:
{staff.phone}

Address:
{staff.address}

Role:
{staff.role}

Regards,
EcoSmart Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        staff.email
                    ],

                    fail_silently=True,
                )

        except Exception as e:

            print(
                "STAFF UPDATE EMAIL ERROR:",
                e
            )

        return response


# ============================================================
# UPDATE USER
# ============================================================

class UpdateUserView(generics.UpdateAPIView):

    queryset = User.objects.filter(
        role=User.CITIZEN
    )

    serializer_class = RegisterSerializer

    permission_classes = [IsAuthenticated]

    lookup_field = "id"

    def update(self, request, *args, **kwargs):

        response = super().update(
            request,
            *args,
            **kwargs
        )

        user = self.get_object()

        try:

            if user.email:

                send_mail(

                    subject="EcoSmart Account Updated 🌱",

                    message=f"""
Hello {user.first_name or user.username},

Your EcoSmart account details have been updated successfully.

Username:
{user.username}

Email:
{user.email}

Phone:
{user.phone}

Address:
{user.address}

Regards,
EcoSmart Team
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        user.email
                    ],

                    fail_silently=True,
                )

        except Exception as e:

            print(
                "USER UPDATE EMAIL ERROR:",
                e
            )

        return response


# ============================================================
# REWARD SYSTEM
# ============================================================

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
                "description":
                    "Start your eco journey",
                "unlocked": True,
            },

            {
                "id": 2,
                "name": "🥉 Eco Explorer",
                "required_points": 100,
                "description":
                    "Complete waste scans and save environment",
                "unlocked": points >= 100,
            },

            {
                "id": 3,
                "name": "🥈 Green Hero",
                "required_points": 250,
                "description":
                    "Become a regular waste recycler",
                "unlocked": points >= 250,
            },

            {
                "id": 4,
                "name": "🥇 Eco Champion",
                "required_points": 500,
                "description":
                    "Amazing contribution towards clean city",
                "unlocked": points >= 500,
            },

            {
                "id": 5,
                "name": "🌍 Earth Guardian",
                "required_points": 1000,
                "description":
                    "Ultimate environmental protector",
                "unlocked": points >= 1000,
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


# ============================================================
# PROFILE API
# ============================================================

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(
            request.user
        )

        return Response(
            serializer.data
        )

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


# ============================================================
# PROFILE UPDATE API
# ============================================================

class ProfileUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        user = request.user

        user.username = request.data.get(
            "username",
            user.username
        )

        user.email = request.data.get(
            "email",
            user.email
        )

        user.first_name = request.data.get(
            "first_name",
            user.first_name
        )

        user.last_name = request.data.get(
            "last_name",
            user.last_name
        )

        user.phone = request.data.get(
            "phone",
            user.phone
        )

        user.address = request.data.get(
            "address",
            user.address
        )

        if request.FILES.get("profile_image"):

            user.profile_image = (
                request.FILES.get(
                    "profile_image"
                )
            )

        user.save()

        return Response({

            "message":
                "Profile Updated Successfully",

            "username":
                user.username,

            "email":
                user.email,

            "first_name":
                user.first_name,

            "last_name":
                user.last_name,

            "phone":
                user.phone,

            "address":
                user.address,

            "profile_image":

                request.build_absolute_uri(
                    user.profile_image.url
                )
                if user.profile_image
                else None,

            "role":
                user.role,
        })


# ============================================================
# ADMIN SETTINGS API
# ============================================================

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


# ============================================================
# GENERAL SETTINGS API
# ============================================================

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        settings_data = {

            "email_notifications":
                True,

            "task_notifications":
                True,

            "system_notifications":
                True,

            "dark_mode":
                False,
        }

        saved_settings = request.session.get(
            "ecosmart_settings",
            {}
        )

        settings_data.update(
            saved_settings
        )

        return Response(
            settings_data
        )

    def put(self, request):

        settings_data = {

            "email_notifications":
                request.data.get(
                    "email_notifications",
                    True
                ),

            "task_notifications":
                request.data.get(
                    "task_notifications",
                    True
                ),

            "system_notifications":
                request.data.get(
                    "system_notifications",
                    True
                ),

            "dark_mode":
                request.data.get(
                    "dark_mode",
                    False
                ),
        }

        request.session[
            "ecosmart_settings"
        ] = settings_data

        request.session.modified = True

        return Response({

            "message":
                "Settings saved successfully",

            **settings_data
        })


# ============================================================
# CHANGE PASSWORD API
# ============================================================

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

        # Required fields
        if not current_password:

            return Response(

                {
                    "error":
                        "Current password is required"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        if not new_password:

            return Response(

                {
                    "error":
                        "New password is required"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        if not confirm_password:

            return Response(

                {
                    "error":
                        "Confirm password is required"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        # Check current password
        if not check_password(

            current_password,

            request.user.password
        ):

            return Response(

                {
                    "error":
                        "Current password is incorrect"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        # Confirm new password
        if new_password != confirm_password:

            return Response(

                {
                    "error":
                        "New passwords do not match"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        # Password length
        if len(new_password) < 8:

            return Response(

                {
                    "error":
                        "Password must be at least 8 characters"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        # Same password
        if check_password(

            new_password,

            request.user.password
        ):

            return Response(

                {
                    "error":
                        "New password must be different from current password"
                },

                status=status.HTTP_400_BAD_REQUEST
            )

        # Save
        request.user.set_password(
            new_password
        )

        request.user.save()

        return Response(

            {
                "message":
                    "Password changed successfully"
            },

            status=status.HTTP_200_OK
        )


# ============================================================
# SALARY LIST + CREATE
# ============================================================

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


# ============================================================
# SALARY DETAIL
# ============================================================

class SalaryDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:

            return (

                Salary.objects

                .select_related("staff")

                .get(pk=pk)
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

                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SalarySerializer(
            salary
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):

        salary = self.get_object(pk)

        if not salary:

            return Response(

                {
                    "error":
                        "Salary record not found"
                },

                status=status.HTTP_404_NOT_FOUND
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

            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        salary = self.get_object(pk)

        if not salary:

            return Response(

                {
                    "error":
                        "Salary record not found"
                },

                status=status.HTTP_404_NOT_FOUND
            )

        salary.delete()

        return Response(

            {
                "message":
                    "Salary record deleted successfully"
            },

            status=status.HTTP_200_OK
        )


# ============================================================
# STAFF SALARY
# ============================================================

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