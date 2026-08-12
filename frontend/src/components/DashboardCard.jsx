import { useEffect, useState } from "react";
import axios from "axios";
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer
} from "recharts";



function UserDashboard(){


    const [data,setData] = useState(null);

    const [loading,setLoading] = useState(true);






    useEffect(()=>{

        fetchDashboard();

    },[]);







    const fetchDashboard = async()=>{


        try{


            const token = localStorage.getItem("access");



            const response = await axios.get(

                "https://ecosmart-project.onrender.com/api/dashboard/user/dashboard/",

                {

                    headers:{

                        Authorization:
                        `Bearer ${token}`

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


        return(

            <div className="p-6">

                Loading Dashboard...

            </div>

        )

    }






    const cards=[


        {
            title:"Total Scans",
            value:data.total_scans,
            icon:"♻️"
        },


        {
            title:"Today's Scan",
            value:data.today_scans,
            icon:"📅"
        },


        {
            title:"Eco Points",
            value:data.eco_points,
            icon:"🌱"
        },


        {
            title:"Badge",
            value:data.badge,
            icon:"🏆"
        }

    ];








return(


<div className="p-6 bg-gray-100 min-h-screen">





<h1 className="text-3xl font-bold mb-2">

Welcome Back 👋

</h1>


<p className="text-gray-600 mb-8">

Track your contribution towards a cleaner environment.

</p>









{/* Cards */}


<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">



{
cards.map((card,index)=>(


<div

key={index}

className="bg-white rounded-2xl shadow p-6 flex justify-between items-center"

>


<div>

<p className="text-gray-500">

{card.title}

</p>


<h2 className="text-2xl font-bold mt-2">

{card.value}

</h2>


</div>


<div className="text-4xl">

{card.icon}

</div>



</div>


))

}


</div>









{/* Analytics Section */}



<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">





{/* Chart */}


<div className="bg-white rounded-2xl shadow p-6">


<h2 className="text-xl font-bold mb-4">

Waste Category Summary

</h2>




<div className="h-72">


<ResponsiveContainer>


<PieChart>


<Pie

data={data.category_data}

dataKey="value"

nameKey="name"

outerRadius={100}

label

>


{
data.category_data.map(
(item,index)=>(


<Cell

key={index}

/>


)

)

}



</Pie>


<Tooltip />



</PieChart>


</ResponsiveContainer>


</div>



</div>









{/* Impact */}



<div className="bg-white rounded-2xl shadow p-6">



<h2 className="text-xl font-bold mb-5">

🌍 Your Environmental Impact

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

Trees Equivalent

</h3>


<p className="text-3xl font-bold text-blue-700">

{data.environment.trees_saved}

</p>


</div>


</div>



</div>





</div>









{/* Badge */}



<div className="bg-white rounded-2xl shadow p-6 mt-8">


<h2 className="text-xl font-bold">

🏆 Achievement

</h2>



<p className="mt-3 text-lg">

Current Badge:

<b className="text-green-700">

{" "}{data.badge}

</b>


</p>



<p className="text-gray-500 mt-2">

Next Badge:

{data.next_badge}

</p>



</div>









{/* Recent Scan */}



<div className="bg-white rounded-2xl shadow p-6 mt-8">


<h2 className="text-xl font-bold mb-4">

Recent Scans

</h2>





<table className="w-full">


<thead>


<tr className="border-b">


<th className="text-left p-3">

Waste

</th>


<th className="text-left p-3">

Confidence

</th>


<th className="text-left p-3">

Date

</th>


</tr>


</thead>






<tbody>


{
data.recent_scans.map(scan=>(


<tr

key={scan.id}

className="border-b"


>


<td className="p-3">

♻️ {scan.waste_type}

</td>


<td className="p-3">

{scan.confidence}%

</td>


<td className="p-3">

{
new Date(scan.date)
.toLocaleDateString()
}

</td>



</tr>


))

}


</tbody>


</table>



</div>







</div>


)


}


export default UserDashboard;

