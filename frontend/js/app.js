import { initAuth } from "./auth.js";
import {
    loadChats,
    createChat,
    renameChat,
    deleteChat,
} from "./chats.js";

import {
    loadMessages,
    sendMessage,
} from "./messages.js";

initAuth();

const chatList = document.querySelector("#chat-list");
const messages = document.querySelector("#messages");
const textarea = document.querySelector("#message");

const sendButton = document.querySelector("#send");
const newChatButton = document.querySelector("#new-chat");

let currentChatId = null;

/* -------------------- Chats -------------------- */

async function refreshChats() {

    const chats = await loadChats();

    chatList.innerHTML = "";

    for (const chat of chats) {

        const row = document.createElement("div");
        row.className = "chat-row";

        if (chat.id === currentChatId)
            row.classList.add("active");

        const title = document.createElement("span");
        title.className = "chat-title";
        title.textContent = chat.title;

        title.onclick = async () => {

            currentChatId = chat.id;

            await refreshChats();
            await refreshMessages();

        };

        const rename = document.createElement("button");
        rename.textContent = "✏️";

        rename.onclick = async (e) => {

            e.stopPropagation();

            const newTitle = prompt("Chat title", chat.title);

            if (!newTitle)
                return;

            await renameChat(chat.id, newTitle);

            await refreshChats();

        };

        const remove = document.createElement("button");
        remove.textContent = "🗑";

        remove.onclick = async (e) => {

            e.stopPropagation();

            if (!confirm("Delete chat?"))
                return;

            await deleteChat(chat.id);

            if (currentChatId === chat.id)
                currentChatId = null;

            await refreshChats();

        };

        row.append(title);
        row.append(rename);
        row.append(remove);

        chatList.appendChild(row);

    }

    if (!currentChatId && chats.length) {

        currentChatId = chats[0].id;

        await refreshMessages();

    }

}

async function createNewChat() {

    const chat = await createChat();

    currentChatId = chat.id;

    await refreshChats();

}

newChatButton.onclick = createNewChat;

/* -------------------- Messages -------------------- */

function appendMessage(role, content) {

    const div = document.createElement("div");

    div.className = `message ${role}`;

    div.textContent = content;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;

    return div;

}

async function refreshMessages() {

    if (!currentChatId)
        return;

    messages.innerHTML = "";

    const history = await loadMessages(currentChatId);

    for (const message of history) {

        appendMessage(
            message.role,
            message.content
        );

    }

}

sendButton.onclick = async () => {

    if (!currentChatId)
        return;

    const text = textarea.value.trim();

    if (!text)
        return;

    appendMessage("user", text);

    textarea.value = "";

    const assistantMessage = appendMessage(
        "assistant",
        ""
    );

    const stream = await sendMessage(
        currentChatId,
        text
    );

    const reader = stream.getReader();

    const decoder = new TextDecoder();

    while (true) {

        const { done, value } = await reader.read();

        if (done)
            break;

        assistantMessage.textContent += decoder.decode(value);

        messages.scrollTop = messages.scrollHeight;

    }

        const chats = await loadChats();

    const current = chats.find(chat => chat.id === currentChatId);

    if (current && current.title === "New Chat") {

        await renameChat(
            currentChatId,
            text.slice(0, 30)
        );

    }

    await refreshChats();

};

/* -------------------- Init -------------------- */

refreshChats();