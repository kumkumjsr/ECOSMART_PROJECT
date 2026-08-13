import axios from "axios";

const BASE_URL = "https://ecosmart-project.onrender.com/api";

const api = axios.create({
  baseURL: BASE_URL,
});

// JWT TOKEN
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// REGISTER
export const registerUser = async (userData) => {
  const response = await api.post(
    "/accounts/register/",
    userData
  );

  return response.data;
};

// LOGIN
export const loginUser = async (username, password) => {
  const response = await api.post(
    "/accounts/login/",
    {
      username,
      password,
    }
  );

  localStorage.setItem("access", response.data.access);
  localStorage.setItem("refresh", response.data.refresh);
  localStorage.setItem("role", response.data.role);
  localStorage.setItem("username", response.data.username);

  return response.data;
};

export default api;

