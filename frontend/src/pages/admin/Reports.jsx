import { useEffect, useState } from "react";
import axios from "axios";
import {
    Users,
    UserCheck,
    ClipboardList,
    Recycle,
    Clock,
    CheckCircle,
    Loader,
    MapPin,
} from "lucide-react";

import {
    PieChart,
    Pie,
    Tooltip,
    ResponsiveContainer,
    Cell,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Legend,
} from "recharts";

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

function Reports() {

    const [summary, setSummary] = useState({});

    const [staffReport, setStaffReport] = useState([]);

    const [wasteReport, setWasteReport] = useState([]);

    const [areaReport, setAreaReport] = useState([]);

    const token = localStorage.getItem("access");

    const headers = {
        Authorization: `Bearer ${token}`,
    };

    const loadReports = async () => {
        try {

            const summaryRes = await axios.get(
                "https://ecosmart-project.onrender.com/api/tasks/reports/",
                { headers }
            );

            const staffRes = await axios.get(
                "https://ecosmart-project.onrender.com/api/tasks/reports/staff/",
                { headers }
            );

            const wasteRes = await axios.get(
                "https://ecosmart-project.onrender.com/api/tasks/reports/waste/",
                { headers }
            );

            const areaRes = await axios.get(
                "https://ecosmart-project.onrender.com/api/tasks/reports/area/",
                { headers }
            );

            setSummary(summaryRes.data);

            setStaffReport(staffRes.data);

            setWasteReport(wasteRes.data);

            setAreaReport(areaRes.data);

        } catch (error) {

            console.log(error);

        }
    };

    useEffect(() => {

        loadReports();

    }, []);

    const pieColors = [
        "#2563eb",
        "#16a34a",
        "#f59e0b",
        "#dc2626",
        "#9333ea",
    ];

    const taskStatus = [
        {
            name: "Completed",
            value: summary.completed_tasks || 0,
        },
        {
            name: "Pending",
            value: summary.pending_tasks || 0,
        },
        {
            name: "Progress",
            value: summary.in_progress_tasks || 0,
        },
    ];

    const exportExcel = () => {

        const worksheet = XLSX.utils.json_to_sheet([
            {
                "Total Users": summary.total_users,
                "Total Staff": summary.total_staff,
                "Total Tasks": summary.total_tasks,
                "Completed": summary.completed_tasks,
                "Pending": summary.pending_tasks,
                "In Progress": summary.in_progress_tasks,
                "Total Scans": summary.total_scans,
            },
        ]);

        const workbook = XLSX.utils.book_new();

        XLSX.utils.book_append_sheet(
            workbook,
            worksheet,
            "Report"
        );

        XLSX.writeFile(
            workbook,
            "EcoSmart_Report.xlsx"
        );

    };



    const exportPDF = () => {

        const doc = new jsPDF();

        doc.setFontSize(18);

        doc.text(
            "EcoSmart Report",
            14,
            20
        );

        autoTable(doc, {

            startY: 30,

            head: [["Title", "Value"]],

            body: [

                ["Total Users", summary.total_users],

                ["Total Staff", summary.total_staff],

                ["Total Tasks", summary.total_tasks],

                ["Completed", summary.completed_tasks],

                ["Pending", summary.pending_tasks],

                ["In Progress", summary.in_progress_tasks],

                ["Total Scans", summary.total_scans],

            ],

        });

        doc.save("EcoSmart_Report.pdf");

    };


    return (

        <div className="p-6">

            <h1 className="text-3xl font-bold mb-8">

                Reports Dashboard

            </h1>

            <div className="grid md:grid-cols-4 gap-6">

                <div className="bg-white rounded-xl shadow p-5">

                    <div className="flex items-center gap-3">

                        <Users size={28} />

                        <div>

                            <p>Total Users</p>

                            <h2 className="text-3xl font-bold">

                                {summary.total_users}

                            </h2>

                        </div>

                    </div>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <div className="flex items-center gap-3">

                        <UserCheck size={28} />

                        <div>

                            <p>Total Staff</p>

                            <h2 className="text-3xl font-bold">

                                {summary.total_staff}

                            </h2>

                        </div>

                    </div>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <div className="flex items-center gap-3">

                        <ClipboardList size={28} />

                        <div>

                            <p>Total Tasks</p>

                            <h2 className="text-3xl font-bold">

                                {summary.total_tasks}

                            </h2>

                        </div>

                    </div>

                </div>

                <div className="bg-white rounded-xl shadow p-5">

                    <div className="flex items-center gap-3">

                        <Recycle size={28} />

                        <div>

                            <p>Total Waste Scans</p>

                            <h2 className="text-3xl font-bold">

                                {summary.total_scans}

                            </h2>

                        </div>

                    </div>

                </div>

            </div>

            <div className="grid md:grid-cols-3 gap-5 mt-8">

                <div className="bg-yellow-100 rounded-xl p-5">

                    <div className="flex items-center gap-2">

                        <Clock />

                        <h3 className="font-bold">

                            Pending

                        </h3>

                    </div>

                    <p className="text-4xl font-bold mt-3">

                        {summary.pending_tasks}

                    </p>

                </div>

                <div className="bg-blue-100 rounded-xl p-5">

                    <div className="flex items-center gap-2">

                        <Loader />

                        <h3 className="font-bold">

                            In Progress

                        </h3>

                    </div>

                    <p className="text-4xl font-bold mt-3">

                        {summary.in_progress_tasks}

                    </p>

                </div>

                <div className="bg-green-100 rounded-xl p-5">

                    <div className="flex items-center gap-2">

                        <CheckCircle />

                        <h3 className="font-bold">

                            Completed

                        </h3>

                    </div>

                    <p className="text-4xl font-bold mt-3">

                        {summary.completed_tasks}

                    </p>

                </div>

            </div>



            {/* STAFF PERFORMANCE */}

            <div className="bg-white shadow rounded-xl p-6 mt-8">

                <h2 className="text-2xl font-bold mb-5">

                    👷 Staff Performance

                </h2>

                <div className="overflow-x-auto">

                    <table className="w-full border">

                        <thead className="bg-green-600 text-white">

                            <tr>

                                <th className="p-3">Staff</th>

                                <th className="p-3">Assigned</th>

                                <th className="p-3">Completed</th>

                                <th className="p-3">Pending</th>

                                <th className="p-3">In Progress</th>

                                <th className="p-3">Completion %</th>

                            </tr>

                        </thead>

                        <tbody>

                            {

                                staffReport.map((staff, index) => (

                                    <tr
                                        key={index}
                                        className="border-b hover:bg-gray-100"
                                    >

                                        <td className="p-3">

                                            {staff.staff}

                                        </td>

                                        <td className="p-3">

                                            {staff.assigned}

                                        </td>

                                        <td className="p-3">

                                            {staff.completed}

                                        </td>

                                        <td className="p-3">

                                            {staff.pending}

                                        </td>

                                        <td className="p-3">

                                            {staff.in_progress}

                                        </td>

                                        <td className="p-3 font-bold text-green-700">

                                            {staff.completion_percentage}%

                                        </td>

                                    </tr>

                                ))

                            }

                        </tbody>

                    </table>

                </div>

            </div>


            {/* WASTE CATEGORY */}

            <div className="bg-white shadow rounded-xl p-6 mt-8">

                <h2 className="text-2xl font-bold mb-5">

                    ♻ Waste Category Report

                </h2>

                <table className="w-full border">

                    <thead className="bg-blue-600 text-white">

                        <tr>

                            <th className="p-3">

                                Waste Type

                            </th>

                            <th className="p-3">

                                Total

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            wasteReport.map((item, index) => (

                                <tr
                                    key={index}
                                    className="border-b"
                                >

                                    <td className="p-3">

                                        {item.waste_type}

                                    </td>

                                    <td className="p-3">

                                        {item.total}

                                    </td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>



            {/* AREA REPORT */}

            <div className="bg-white shadow rounded-xl p-6 mt-8">

                <h2 className="text-2xl font-bold mb-5">

                    📍 Area Wise Cleaning

                </h2>

                <table className="w-full border">

                    <thead className="bg-purple-600 text-white">

                        <tr>

                            <th className="p-3">

                                Location

                            </th>

                            <th className="p-3">

                                Tasks

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            areaReport.map((item, index) => (

                                <tr
                                    key={index}
                                    className="border-b"
                                >

                                    <td className="p-3">

                                        {item.location}

                                    </td>

                                    <td className="p-3">

                                        {item.total}

                                    </td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>



            {/* CHARTS */}

            <div className="grid md:grid-cols-2 gap-8 mt-8">

                <div className="bg-white rounded-xl shadow p-6">

                    <h2 className="text-xl font-bold mb-5">
                        📊 Task Status
                    </h2>

                    <ResponsiveContainer width="100%" height={300}>

                        <BarChart data={taskStatus}>

                            <CartesianGrid strokeDasharray="3 3" />

                            <XAxis dataKey="name" />

                            <YAxis />

                            <Tooltip />

                            <Legend />

                            <Bar
                                dataKey="value"
                                fill="#16a34a"
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </div>



                <div className="bg-white rounded-xl shadow p-6">

                    <h2 className="text-xl font-bold mb-5">
                        ♻ Waste Distribution
                    </h2>

                    <ResponsiveContainer width="100%" height={300}>

                        <PieChart>

                            <Pie
                                data={wasteReport}
                                dataKey="total"
                                nameKey="waste_type"
                                outerRadius={100}
                                label
                            >

                                {

                                    wasteReport.map((entry, index) => (

                                        <Cell
                                            key={index}
                                            fill={pieColors[index % pieColors.length]}
                                        />

                                    ))

                                }

                            </Pie>

                            <Tooltip />

                        </PieChart>

                    </ResponsiveContainer>

                </div>

            </div>



            {/* ACTION BUTTONS */}

            <div className="flex flex-wrap gap-4 mt-10">

                <button

                    className="bg-red-600 text-white px-6 py-3 rounded-lg"

                    onClick={() => window.print()}

                >

                    🖨 Print Report

                </button>




                <button
                    onClick={exportPDF}
                    className="bg-red-600 text-white px-6 py-3 rounded-lg"
                >
                    📄 Export PDF
                </button>

                <button
                    onClick={exportExcel}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg"
                >
                    📊 Export Excel
                </button>




            </div>



        </div>

    );


}





export default Reports;

