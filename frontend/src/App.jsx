import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

// =====================================================
// COMMON
// =====================================================

import WasteScanner from "./pages/WasteScanner";
import History from "./pages/History";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Logout from "./pages/Logout";

import ProtectedRoute from "./components/ProtectedRoute";

// =====================================================
// ADMIN LAYOUT
// =====================================================

import AdminLayout from "./layouts/AdminLayout";

// =====================================================
// ADMIN PAGES
// =====================================================

import AdminDashboard from "./pages/admin/Dashboard";

import CreateStaff from "./pages/CreateStaff";
import EditStaff from "./pages/EditStaff";
import StaffList from "./pages/StaffList";

import UserList from "./pages/UserList";
import EditUser from "./pages/EditUser";

import TaskList from "./pages/admin/TaskList";
import TaskDetails from "./pages/admin/TaskDetails";
import CreateTask from "./pages/admin/CreateTask";
import EditTask from "./pages/admin/EditTask";

import Reports from "./pages/admin/Reports";
import Notifications from "./pages/admin/Notifications";
import Settings from "./pages/admin/Settings";
import Salary from "./pages/admin/Salary";

import ReportedDustbins from "./pages/admin/ReportedDustbins";
import Dustbins from "./pages/admin/Dustbins";
import Complaints from "./pages/admin/Complaints";

// =====================================================
// STAFF
// =====================================================

import StaffDashboard from "./pages/staff/Dashboard";
import StaffTasks from "./pages/staff/StaffTasks";
import CompleteTask from "./pages/staff/CompleteTask";

import StaffSalary from "./pages/staff/Salary";
import StaffNotifications from "./pages/staff/Notifications";
import StaffProfile from "./pages/staff/Profile";
import StaffSettings from "./pages/staff/Settings";

// =====================================================
// USER
// =====================================================

import UserRoutes from "./routes/UserRoutes";


// =====================================================
// APP
// =====================================================

function App() {

    return (

        <BrowserRouter>

            <div className="min-h-screen bg-gray-50">

                {/* ================================================= */}
                {/* COMMON NAVIGATION */}
                {/* ================================================= */}

                <nav
                    className="
                        bg-white
                        shadow-lg
                        px-6
                        py-4
                        flex
                        flex-wrap
                        items-center
                        gap-4
                        border-b
                        border-green-100
                    "
                >

                    {/* ================================================= */}
                    {/* LOGO */}
                    {/* ================================================= */}

                    <Link
                        to="/"
                        className="
                            flex
                            items-center
                            gap-2
                            mr-5
                            text-green-700
                            font-bold
                            text-xl
                        "
                    >

                        🌱 EcoSmart

                    </Link>


                    {/* ================================================= */}
                    {/* LOGIN */}
                    {/* ================================================= */}

                    <Link
                        to="/login"
                        className="
                            px-4
                            py-2
                            rounded-xl
                            text-gray-700
                            hover:bg-green-100
                            hover:text-green-700
                            transition
                            font-medium
                        "
                    >

                        🔐 Login

                    </Link>


                    {/* ================================================= */}
                    {/* REGISTER */}
                    {/* ================================================= */}

                    <Link
                        to="/register"
                        className="
                            px-4
                            py-2
                            rounded-xl
                            text-gray-700
                            hover:bg-green-100
                            hover:text-green-700
                            transition
                            font-medium
                        "
                    >

                        📝 Register

                    </Link>


                    {/* ================================================= */}
                    {/* LOGOUT */}
                    {/* ================================================= */}

                    <div className="ml-auto">

                        <Logout />

                    </div>

                </nav>


                {/* ================================================= */}
                {/* ROUTES */}
                {/* ================================================= */}

                <Routes>

                    {/* ================================================= */}
                    {/* AUTHENTICATION */}
                    {/* ================================================= */}

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/register"
                        element={<Register />}
                    />


                    {/* ================================================= */}
                    {/* COMMON WASTE SCANNER */}
                    {/* ================================================= */}

                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <WasteScanner />
                            </ProtectedRoute>
                        }
                    />


                    <Route
                        path="/history"
                        element={
                            <ProtectedRoute>
                                <History />
                            </ProtectedRoute>
                        }
                    />


                    {/* ================================================= */}
                    {/* ADMIN PANEL */}
                    {/* ================================================= */}

                    <Route
                        path="/admin"
                        element={
                            <ProtectedRoute>
                                <AdminLayout />
                            </ProtectedRoute>
                        }
                    >

                        {/* ----------------------------------------- */}
                        {/* ADMIN DASHBOARD */}
                        {/* ----------------------------------------- */}

                        <Route
                            index
                            element={<AdminDashboard />}
                        />


                        {/* ----------------------------------------- */}
                        {/* USERS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="users"
                            element={<UserList />}
                        />

                        <Route
                            path="users/edit/:id"
                            element={<EditUser />}
                        />


                        {/* ----------------------------------------- */}
                        {/* STAFF */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="staff"
                            element={<StaffList />}
                        />

                        <Route
                            path="staff/create"
                            element={<CreateStaff />}
                        />

                        <Route
                            path="staff/edit/:id"
                            element={<EditStaff />}
                        />


                        {/* ----------------------------------------- */}
                        {/* TASKS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="tasks"
                            element={<TaskList />}
                        />

                        <Route
                            path="tasks/create"
                            element={<CreateTask />}
                        />

                        <Route
                            path="tasks/:id"
                            element={<TaskDetails />}
                        />

                        <Route
                            path="tasks/edit/:id"
                            element={<EditTask />}
                        />


                        {/* ----------------------------------------- */}
                        {/* REPORTS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="reports"
                            element={<Reports />}
                        />


                        {/* ----------------------------------------- */}
                        {/* NOTIFICATIONS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="notifications"
                            element={<Notifications />}
                        />


                        {/* ----------------------------------------- */}
                        {/* SETTINGS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="settings"
                            element={<Settings />}
                        />


                        {/* ----------------------------------------- */}
                        {/* SALARY */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="salary"
                            element={<Salary />}
                        />


                        {/* ----------------------------------------- */}
                        {/* REPORTED DUSTBINS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="reported-dustbins"
                            element={<ReportedDustbins />}
                        />


                        {/* ----------------------------------------- */}
                        {/* DUSTBINS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="dustbins"
                            element={<Dustbins />}
                        />


                        {/* ----------------------------------------- */}
                        {/* COMPLAINTS */}
                        {/* ----------------------------------------- */}

                        <Route
                            path="complaints"
                            element={<Complaints />}
                        />

                    </Route>


                    {/* ================================================= */}
                    {/* STAFF PANEL */}
                    {/* ================================================= */}

                    <Route
                        path="/staff"
                        element={
                            <ProtectedRoute>
                                <StaffDashboard />
                            </ProtectedRoute>
                        }
                    />


                    <Route
                        path="/staff/dashboard"
                        element={
                            <ProtectedRoute>
                                <StaffDashboard />
                            </ProtectedRoute>
                        }
                    />


                    {/* ----------------------------------------- */}
                    {/* STAFF TASKS */}
                    {/* ----------------------------------------- */}

                    <Route
                        path="/staff/tasks"
                        element={
                            <ProtectedRoute>
                                <StaffTasks />
                            </ProtectedRoute>
                        }
                    />


                    <Route
                        path="/staff/tasks/:id/complete"
                        element={
                            <ProtectedRoute>
                                <CompleteTask />
                            </ProtectedRoute>
                        }
                    />


                    {/* ----------------------------------------- */}
                    {/* STAFF SALARY */}
                    {/* ----------------------------------------- */}

                    <Route
                        path="/staff/salary"
                        element={
                            <ProtectedRoute>
                                <StaffSalary />
                            </ProtectedRoute>
                        }
                    />


                    {/* ----------------------------------------- */}
                    {/* STAFF PROFILE */}
                    {/* ----------------------------------------- */}

                    <Route
                        path="/staff/profile"
                        element={
                            <ProtectedRoute>
                                <StaffProfile />
                            </ProtectedRoute>
                        }
                    />


                    {/* ----------------------------------------- */}
                    {/* STAFF SETTINGS */}
                    {/* ----------------------------------------- */}

                    <Route
                        path="/staff/settings"
                        element={
                            <ProtectedRoute>
                                <StaffSettings />
                            </ProtectedRoute>
                        }
                    />


                    {/* ----------------------------------------- */}
                    {/* STAFF NOTIFICATIONS */}
                    {/* ----------------------------------------- */}

                    <Route
                        path="/staff/notifications"
                        element={
                            <ProtectedRoute>
                                <StaffNotifications />
                            </ProtectedRoute>
                        }
                    />


                    {/* ================================================= */}
                    {/* USER PANEL */}
                    {/* ================================================= */}

                    <Route
                        path="/user/*"
                        element={
                            <ProtectedRoute>
                                <UserRoutes />
                            </ProtectedRoute>
                        }
                    />


                    {/* ================================================= */}
                    {/* 404 PAGE */}
                    {/* ================================================= */}

                    <Route
                        path="*"
                        element={
                            <div className="min-h-[70vh] flex items-center justify-center">

                                <div className="text-center">

                                    <h1 className="text-6xl font-bold text-green-700">
                                        404
                                    </h1>

                                    <p className="text-gray-600 mt-3">
                                        Page not found
                                    </p>

                                    <Link
                                        to="/"
                                        className="
                                            inline-block
                                            mt-5
                                            bg-green-600
                                            hover:bg-green-700
                                            text-white
                                            px-6
                                            py-3
                                            rounded-xl
                                            font-semibold
                                        "
                                    >
                                        Go Home
                                    </Link>

                                </div>

                            </div>
                        }
                    />

                </Routes>

            </div>

        </BrowserRouter>
    );
}


export default App;