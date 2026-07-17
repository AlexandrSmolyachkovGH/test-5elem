const BASE_URL = window.location.origin;
const API_PREFIX = "/api";

let token = "";

export function setToken(jwt) {
    token = jwt;
}

export function getToken() {
    return token;
}

export async function api(path, options = {}) {
    const response = await fetch(BASE_URL + API_PREFIX + path, {
        ...options,

        headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "login.html";
        throw new Error("Unauthorized");
    }

    return response;
}