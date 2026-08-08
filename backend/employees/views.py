# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser

# from .models import Employee



# class AvailableWorkersView(APIView):

#     permission_classes = [IsAdminUser]


#     def get(self, request):

#         workers = Employee.objects.filter(
#             is_available=True
#         )


#         data = []


#         for worker in workers:

#             data.append({

#                 "id": worker.id,

#                 "employee_id": worker.employee_id,

#                 "name": worker.user.username,

#                 "department": worker.department

#             })


#         return Response(data)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser

# from .models import Employee


# class AvailableWorkersView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         workers = Employee.objects.all()

#         data = []

#         for worker in workers:

#             data.append({

#                 "id": worker.id,

#                 "employee_id": worker.employee_id,

#                 "name": worker.user.username,

#                 "first_name": worker.user.first_name,

#                 "last_name": worker.user.last_name,

#                 "department": worker.department,

#                 "is_available": worker.is_available

#             })

#         return Response(data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from accounts.models import User
from .models import Employee


class AvailableWorkersView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        # ==================================================
        # GET ALL WORKERS FROM USER TABLE
        # ==================================================

        workers = User.objects.filter(
            role="WORKER"
        ).order_by("-id")


        # ==================================================
        # GET EMPLOYEE RECORDS
        # ==================================================

        employees = Employee.objects.select_related(
            "user"
        )

        employee_map = {
            employee.user_id: employee
            for employee in employees
        }


        data = []


        # ==================================================
        # BUILD STAFF LIST
        # ==================================================

        for worker in workers:

            employee = employee_map.get(
                worker.id
            )


            # ----------------------------------------------
            # EMPLOYEE AVAILABILITY
            # ----------------------------------------------

            if employee:

                is_available = employee.is_available

            else:

                # New worker without Employee record
                is_available = True


            # ----------------------------------------------
            # CHECK USER NAME
            # ----------------------------------------------

            full_name = (
                f"{worker.first_name} "
                f"{worker.last_name}"
            ).strip()


            if not full_name:

                full_name = worker.username


            # ----------------------------------------------
            # EMPLOYEE ID
            # ----------------------------------------------

            if employee:

                employee_id = employee.employee_id

            else:

                # New worker has no Employee record
                employee_id = f"NEW-{worker.id}"


            # ----------------------------------------------
            # DEPARTMENT
            # ----------------------------------------------

            if employee:

                department = employee.department

            else:

                department = "Cleaning"


            # ----------------------------------------------
            # PHONE
            # ----------------------------------------------

            if employee:

                phone = employee.phone

            else:

                phone = getattr(
                    worker,
                    "phone",
                    ""
                )


            # ----------------------------------------------
            # RESPONSE
            # ----------------------------------------------

            data.append({

                # IMPORTANT:
                # This is USER ID now
                "id": worker.id,

                "user_id": worker.id,

                "employee_id": employee_id,

                "name": full_name,

                "username": worker.username,

                "first_name": worker.first_name,

                "last_name": worker.last_name,

                "department": department,

                "phone": phone,

                "is_available": is_available,

                "has_employee_record":
                    employee is not None

            })


        return Response(data)