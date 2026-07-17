import { api } from "./api.js";

export async function loadMessages(chatId) {

    const response = await api(`/chats/${chatId}/messages`);

    if (!response.ok)
        throw new Error("Cannot load messages");

    return await response.json();

}

export async function sendMessage(chatId, content) {

    const response = await api(`/chats/${chatId}/messages`, {

        method: "POST",

        body: JSON.stringify({
            content
        })

    });

    if (!response.ok)
        throw new Error("Cannot send message");

    return response.body;

}