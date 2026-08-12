import axios from "axios";

const BASE_URL = "https://ecosmart-project.onrender.com/api";

// =======================
// REGISTER
// =======================

export const registerUser = async (userData) => {
    const response = await axios.post(
        `${BASE_URL}/accounts/register/`,
        userData
    );

    return response.data;
};


// =======================
// LOGIN
// =======================

export const loginUser = async (username, password) => {

    const response = await axios.post(
        `${BASE_URL}/accounts/login/`,
        {
            username,
            password,
        }
    );

    localStorage.setItem(
        "access",
        response.data.access
    );

    localStorage.setItem(
        "refresh",
        response.data.refresh
    );

    localStorage.setItem(
        "role",
        response.data.role
    );

    localStorage.setItem(
        "username",
        response.data.username
    );

    return response.data;
};