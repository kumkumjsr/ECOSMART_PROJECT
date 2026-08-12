import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";


function EditStaff() {

  const { id } = useParams();

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone: "",
    address: "",
    location: "",
  });


  useEffect(() => {

    fetchStaff();

  }, [id]);


  const fetchStaff = async () => {

    try {

      const token = localStorage.getItem("access");

      const response = await axios.get(

        `https://ecosmart-project.onrender.com/api/accounts/staff/${id}/update/`,

        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }

      );

      const data = response.data;

      setFormData({
        username: data.username || "",
        email: data.email || "",
        password: "",
        first_name: data.first_name || "",
        last_name: data.last_name || "",
        phone: data.phone || "",
        address: data.address || "",
        location: data.location || "",
      });

    } catch (error) {

      console.log(error);

      alert("Failed to load staff");

    }

  };


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

      const token = localStorage.getItem("access");


      const updateData = {
        username: formData.username,
        email: formData.email,
        first_name: formData.first_name,
        last_name: formData.last_name,
        phone: formData.phone,
        address: formData.address,
        location: formData.location,
      };


      if (formData.password.trim()) {

        updateData.password = formData.password;

      }


      await axios.patch(

        `https://ecosmart-project.onrender.com/api/accounts/staff/${id}/update/`,

        updateData,

        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }

      );


      alert("✅ Staff Updated Successfully");

      navigate("/admin/staff");


    } catch (error) {

      console.log(error);

      if (error.response) {

        alert(
          JSON.stringify(
            error.response.data
          )
        );

      } else {

        alert("Update Failed");

      }

    } finally {

      setLoading(false);

    }

  };


  return (

    <DashboardLayout>

      <div className="
        max-w-3xl
        mx-auto
        bg-white
        shadow-xl
        rounded-2xl
        p-8
      ">

        <h2 className="
          text-3xl
          font-bold
          text-green-700
          mb-6
        ">
          ✏️ Edit Staff
        </h2>


        <form
          onSubmit={handleSubmit}
          className="
            grid
            grid-cols-1
            md:grid-cols-2
            gap-5
          "
        >

          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            value={formData.first_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          <input
            type="text"
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          <input
            type="password"
            name="password"
            placeholder="New Password (optional)"
            value={formData.password}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


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


          {/* ⭐ LOCATION */}

          <div className="md:col-span-2">

            <input
              type="text"
              name="location"
              placeholder="Staff Location"
              value={formData.location}
              onChange={handleChange}
              className="
                border
                p-3
                rounded-lg
                w-full
                focus:ring-2
                focus:ring-green-500
                outline-none
              "
            />

          </div>


          <div className="md:col-span-2">

            <button
              type="submit"
              disabled={loading}
              className="
                w-full
                bg-green-600
                hover:bg-green-700
                disabled:bg-gray-400
                text-white
                p-3
                rounded-lg
                font-semibold
              "
            >

              {loading
                ? "Updating..."
                : "Update Staff"
              }

            </button>

          </div>

        </form>

      </div>

    </DashboardLayout>

  );

}


export default EditStaff;