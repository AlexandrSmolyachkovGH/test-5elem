import { api } from "./api.js";

export async function loadChats() {

    const response = await api("/chats");

    if (!response.ok)
        throw new Error("Cannot load chats");

    return await response.json();

}

export async function createChat(title = "New Chat") {

    const response = await api("/chats", {

        method: "POST",

        body: JSON.stringify({
            title
        })

    });

    if (!response.ok)
        throw new Error("Cannot create chat");

    return await response.json();

}

export async function renameChat(chatId, title) {

    const response = await api(`/chats/${chatId}`, {

        method: "PATCH",

        body: JSON.stringify({
            title
        })

    });

    if (!response.ok)
        throw new Error("Cannot rename chat");

    return await response.json();

}

export async function deleteChat(chatId) {

    const response = await api(`/chats/${chatId}`, {

        method: "DELETE"

    });

    return response.ok;

}