import { api, setToken } from "./api.js";

export async function login(username, password) {

    const response = await api("/auth/login", {

        method: "POST",

        body: JSON.stringify({
            username,
            password,
        }),

    });

    if (!response.ok) {
        alert("Wrong username or password");
        return;
    }

    const data = await response.json();

    localStorage.setItem("token", data.access_token);

    setToken(data.access_token);

    window.location.href = "index.html";

}

export async function register(username, password) {

    const response = await api("/auth/register", {

        method: "POST",

        body: JSON.stringify({
            username,
            password,
        }),

    });

    if (!response.ok) {

        alert("Registration failed");

        return;

    }

    await login(username, password);

}

export function logout() {

    localStorage.removeItem("token");

    window.location.href = "login.html";

}

export function initAuth() {

    const token = localStorage.getItem("token");

    if (!token) {

        window.location.href = "login.html";

        return false;

    }

    setToken(token);

    return true;

}