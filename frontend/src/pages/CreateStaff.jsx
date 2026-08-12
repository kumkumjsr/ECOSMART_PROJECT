import { useState } from "react";
import axios from "axios";
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
    location: "",
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

      const token = localStorage.getItem("access");

      await axios.post(

        "https://ecosmart-project.onrender.com/api/accounts/create-staff/",

        formData,

        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }

      );

      alert("✅ Staff Created Successfully");


      setFormData({
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        phone: "",
        address: "",
        location: "",
      });


    } catch (error) {

      console.log(error);

      if (error.response) {

        alert(
          JSON.stringify(
            error.response.data
          )
        );

      } else {

        alert("Something went wrong.");

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
          👷 Create Staff
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


          {/* FIRST NAME */}

          <input
            type="text"
            name="first_name"
            placeholder="First Name"
            value={formData.first_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          {/* LAST NAME */}

          <input
            type="text"
            name="last_name"
            placeholder="Last Name"
            value={formData.last_name}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          {/* USERNAME */}

          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          {/* EMAIL */}

          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          {/* PHONE */}

          <input
            type="text"
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />


          {/* PASSWORD */}

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            className="border p-3 rounded-lg"
            required
          />


          {/* ADDRESS */}

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


          {/* BUTTON */}

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
                ? "Creating..."
                : "Create Staff"
              }

            </button>

          </div>

        </form>

      </div>

    </DashboardLayout>

  );

}


export default CreateStaff;