import axios from "axios";


axios.interceptors.request.use(config => {
    config.headers["Content-Type"] = "application/json";
})

const api = axios.create({
    baseURL : "http://127.0.0.1:5000/api/"
});


export default api;