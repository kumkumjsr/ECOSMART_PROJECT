import { useEffect, useState } from "react";
import axios from "axios";


function ReportedDustbins() {


    const [dustbins, setDustbins] = useState([]);

    const [workers, setWorkers] = useState([]);

    const [loading, setLoading] = useState(true);


    const [showModal, setShowModal] = useState(false);

    const [selectedDustbin, setSelectedDustbin] = useState(null);

    const [selectedWorker, setSelectedWorker] = useState("");





    useEffect(() => {

        fetchReports();

    }, []);





    // ============================
    // FETCH REPORTED DUSTBINS
    // ============================


    const fetchReports = async () => {


        try {


            const token = localStorage.getItem("access");


            const response = await axios.get(

                "http://127.0.0.1:8000/api/dustbins/reported/",

                {

                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                }

            );


            setDustbins(response.data);



        }

        catch (error) {

            console.log(error);

        }


        finally {

            setLoading(false);

        }


    };







    // ============================
    // FETCH WORKERS
    // ============================


    const fetchWorkers = async () => {


        try {


            const token = localStorage.getItem("access");


            const response = await axios.get(

                "http://127.0.0.1:8000/api/employees/available/",

                {

                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                }

            );


            setWorkers(response.data);



        }

        catch (error) {

            console.log(error);

        }


    };







    // ============================
    // OPEN ASSIGN MODAL
    // ============================


    const openAssignModal = (dustbin) => {


        setSelectedDustbin(dustbin);

        fetchWorkers();

        setShowModal(true);


    };








    // ============================
    // ASSIGN WORKER
    // ============================
    const assignWorker = async () => {


        if (!selectedWorker) {


            alert("Please select worker");


            return;


        }



        try {


            const token = localStorage.getItem("access");



            const response = await axios.post(


                "http://127.0.0.1:8000/api/tasks/create/",


                {


                    dustbin_id: selectedDustbin.id,


                    worker_id: selectedWorker


                },


                {


                    headers: {


                        Authorization: `Bearer ${token}`


                    }


                }


            );



            alert(
                response.data.message
            );



            setShowModal(false);


            setSelectedWorker("");



            // refresh reported dustbins

            fetchReports();



        }


        catch (error) {


            console.log(
                "Assign Error",
                error.response?.data || error
            );


            alert(
                "Task Assignment Failed"
            );


        }


    };








    if (loading) {


        return (

            <div className="p-6">

                Loading Reports...

            </div>

        );


    }







    return (


        <div className="p-6">


            <h1 className="text-3xl font-bold mb-6">

                🚨 Reported Full Dustbins

            </h1>





            {


                dustbins.length === 0 ?



                    <div className="bg-white shadow p-6 rounded-xl">

                        No Full Dustbins Reported ✅

                    </div>



                    :



                    <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">



                        {

                            dustbins.map((item) => (


                                <div

                                    key={item.id}

                                    className="bg-white shadow-xl rounded-2xl p-6"

                                >



                                    <div className="bg-red-100 text-red-700 px-3 py-1 rounded-full inline-block">

                                        FULL

                                    </div>




                                    <h2 className="text-xl font-bold mt-4">

                                        🗑️ {item.name}

                                    </h2>



                                    <p className="text-gray-600 mt-2">

                                        Type: {item.type}

                                    </p>



                                    <p className="text-gray-600">

                                        📍 {item.address}

                                    </p>





                                    <a

                                        href={`https://maps.google.com/?q=${item.latitude},${item.longitude}`}

                                        target="_blank"

                                        rel="noreferrer"

                                        className="block mt-5 bg-green-700 text-white text-center py-3 rounded-xl"

                                    >

                                        View Location

                                    </a>






                                    <button

                                        onClick={() => openAssignModal(item)}

                                        className="mt-3 w-full bg-blue-600 text-white py-3 rounded-xl"

                                    >

                                        👷 Assign Worker

                                    </button>




                                </div>


                            ))


                        }


                    </div>


            }






            {/* ==========================
                ASSIGN WORKER MODAL
            ========================== */}





            {

                showModal &&


                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">



                    <div className="bg-white rounded-2xl p-8 w-96">



                        <h2 className="text-xl font-bold mb-4">

                            Assign Worker

                        </h2>




                        <p className="mb-4">

                            Dustbin:

                            <b>

                                {" "}{selectedDustbin?.name}

                            </b>

                        </p>





                        <select

                            value={selectedWorker}

                            onChange={(e) => setSelectedWorker(e.target.value)}

                            className="w-full border rounded-xl p-3"

                        >


                            <option value="">

                                Select Worker

                            </option>



                            {

                                workers.map((worker) => (


                                    <option

                                        key={worker.id}

                                        value={worker.id}

                                    >

                                        {worker.name} - {worker.department}

                                    </option>


                                ))


                            }


                        </select>






                        <button

                            onClick={assignWorker}

                            className="w-full mt-5 bg-green-700 text-white py-3 rounded-xl"

                        >

                            Assign

                        </button>






                        <button

                            onClick={() => setShowModal(false)}

                            className="w-full mt-3 bg-gray-200 py-3 rounded-xl"

                        >

                            Cancel

                        </button>



                    </div>



                </div>


            }



        </div>


    );


}


export default ReportedDustbins;
