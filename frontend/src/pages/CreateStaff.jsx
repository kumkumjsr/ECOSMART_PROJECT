import { useState } from "react";
import api from "../services/api";
import DashboardLayout from "../layouts/DashboardLayout";

function CreateStaff() {
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone: "",
    address: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      // Check login token
      const token = localStorage.getItem("access");

      if (!token) {
        alert("❌ Please login again. Authentication token not found.");
        return;
      }

      // Create staff
      const response = await api.post(
        "/accounts/create-staff/",
        formData
      );

      console.log("Staff Created:", response.data);

      alert("✅ Staff Created Successfully");

      // Reset form
      setFormData({
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone: "",
        address: "",
      });

    } catch (error) {
      console.error("Create Staff Error:", error);

      if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Response:", error.response.data);

        if (error.response.status === 401) {
          alert("❌ Unauthorized. Please login again.");
        } else if (error.response.status === 403) {
          alert("❌ You don't have permission to create staff.");
        } else if (error.response.status === 400) {
          alert(
            "❌ Invalid data:\n" +
            JSON.stringify(error.response.data, null, 2)
          );
        } else if (error.response.status === 500) {
          alert(
            "❌ Server error. Please check Django terminal."
          );
        } else {
          alert(
            "❌ Error:\n" +
            JSON.stringify(error.response.data, null, 2)
          );
        }
      } else if (error.request) {
        alert(
          "❌ Backend server is not reachable.\n" +
          "Please make sure Django is running."
        );
      } else {
        alert("❌ Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-2xl p-8">

        {/* Heading */}
        <h2 className="text-3xl font-bold text-green-700 mb-6">
          👷 Create Staff
        </h2>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="grid grid-cols-1 md:grid-cols-2 gap-5"
        >

          {/* First Name */}
          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            value={formData.first_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />

          {/* Last Name */}
          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          {/* Username */}
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />

          {/* Email */}
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />

          {/* Phone */}
          <input
            type="text"
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          {/* Password */}
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />

          {/* Address */}
          <div className="md:col-span-2">
            <input
              type="text"
              name="address"
              placeholder="Address"
              value={formData.address}
              onChange={handleChange}
              className="border p-3 rounded-lg w-full"
            />
          </div>

          {/* Submit */}
          <div className="md:col-span-2">
            <button
              type="submit"
              disabled={loading}
              className={`w-full text-white p-3 rounded-lg font-semibold transition ${
                loading
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-green-600 hover:bg-green-700"
              }`}
            >
              {loading ? "Creating..." : "Create Staff"}
            </button>
          </div>

        </form>
      </div>
    </DashboardLayout>
  );
}

export default CreateStaff;

