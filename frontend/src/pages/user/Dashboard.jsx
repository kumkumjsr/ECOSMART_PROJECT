import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";


function UserDashboard() {


  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(true);



  useEffect(() => {

    fetchDashboard();

  }, []);




  const fetchDashboard = async () => {


    try {


      const token = localStorage.getItem("access");


      const response = await axios.get(

        "https://ecosmart-project.onrender.com/api/dashboard/user/dashboard/",

        {

          headers: {

            Authorization: `Bearer ${token}`

          }

        }

      );


      setData(response.data);



    }

    catch(error){

      console.log(
        "Dashboard Error",
        error
      );

    }

    finally{

      setLoading(false);

    }


  };





  if(loading){

    return (

      <div className="p-6 text-xl font-semibold">

        Loading Dashboard...

      </div>

    );

  }





  const colors = [

    "#22c55e",

    "#3b82f6",

    "#eab308",

    "#ef4444",

    "#8b5cf6"

  ];





  return (

    <div className="p-6">



      {/* Header */}

      <div className="mb-8">


        <h1 className="text-3xl font-bold text-green-700">

          Welcome {data.username} 👋

        </h1>


        <p className="text-gray-600 mt-2">

          Track your environmental contribution.

        </p>


      </div>







      {/* Cards */}


      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">



        <div className="bg-white shadow-lg rounded-2xl p-6">

          <h3 className="text-gray-500">

            Total Scans

          </h3>


          <p className="text-3xl font-bold mt-3 text-green-600">

            {data.total_scans}

          </p>

        </div>





        <div className="bg-white shadow-lg rounded-2xl p-6">


          <h3 className="text-gray-500">

            Today's Scan

          </h3>


          <p className="text-3xl font-bold mt-3 text-blue-600">

            {data.today_scans}

          </p>


        </div>






        <div className="bg-white shadow-lg rounded-2xl p-6">


          <h3 className="text-gray-500">

            Eco Points 🌱

          </h3>


          <p className="text-3xl font-bold mt-3 text-yellow-600">

            {data.eco_points}

          </p>


        </div>







        <div className="bg-white shadow-lg rounded-2xl p-6">


          <h3 className="text-gray-500">

            Badge 🏆

          </h3>


          <p className="text-xl font-bold mt-3 text-purple-600">

            {data.badge}

          </p>


          <p className="text-sm text-gray-500 mt-2">

            Next: {data.next_badge}

          </p>


        </div>



      </div>









      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">





        {/* Waste Chart */}


        <div className="bg-white shadow-lg rounded-2xl p-6">


          <h2 className="text-xl font-bold mb-5">

            Waste Category Summary ♻️

          </h2>



          {
            data.category_data.length === 0 ?

            (

              <p className="text-gray-500">

                No Data Available

              </p>

            )

            :

            (

              <ResponsiveContainer width="100%" height={300}>


                <PieChart>


                  <Pie

                    data={data.category_data}

                    dataKey="value"

                    nameKey="name"

                    cx="50%"

                    cy="50%"

                    outerRadius={100}

                    label

                  >


                    {

                      data.category_data.map(

                        (entry,index)=>(

                          <Cell

                            key={index}

                            fill={
                              colors[index % colors.length]
                            }

                          />

                        )

                      )

                    }


                  </Pie>


                  <Tooltip />


                </PieChart>


              </ResponsiveContainer>


            )

          }


        </div>







        {/* Environment */}


        <div className="bg-white shadow-lg rounded-2xl p-6">


          <h2 className="text-xl font-bold mb-5">

            Environment Impact 🌍

          </h2>



          <div className="space-y-5">


            <div className="bg-green-100 p-5 rounded-xl">


              <h3 className="text-gray-600">

                CO2 Saved

              </h3>


              <p className="text-3xl font-bold text-green-700">

                {data.environment.co2_saved}

              </p>


            </div>





            <div className="bg-blue-100 p-5 rounded-xl">


              <h3 className="text-gray-600">

                Trees Saved

              </h3>


              <p className="text-3xl font-bold text-blue-700">

                {data.environment.trees_saved}

              </p>


            </div>



          </div>



        </div>



      </div>









      {/* Recent Scans */}



      <div className="bg-white shadow-lg rounded-2xl p-6 mt-8">


        <h2 className="text-xl font-bold mb-5">

          Recent Scans 📜

        </h2>





        {

          data.recent_scans.length === 0 ?

          (

            <p className="text-gray-500">

              No scans found

            </p>

          )

          :

          (

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">


            {

              data.recent_scans.map(scan=>(


                <div

                  key={scan.id}

                  className="border rounded-xl p-4 flex gap-4"


                >


                  <img

                    src={
                      `https://ecosmart-project.onrender.com${scan.image}`
                    }

                    className="w-24 h-24 object-cover rounded-lg"

                  />



                  <div>


                    <h3 className="font-bold text-lg">

                      {scan.waste_type}

                    </h3>



                    <p>

                      Confidence:
                      {" "}
                      {scan.confidence}%

                    </p>



                    <p className="text-sm text-gray-600 mt-2">

                      {scan.recommendation}

                    </p>



                  </div>


                </div>


              ))

            }


            </div>


          )

        }



      </div>



    </div>

  );

}


export default UserDashboard;
