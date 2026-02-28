"use client";

import { useState } from "react";
import { Sidebar } from "../components/sidebar/Sidebar";
import { ChatMain } from "../components/chat/ChatMain";
import { Message } from "../types/chat";

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSendMessage = async (query: string) => {
        if (!query.trim() || isSubmitting) return;

        const userMsgId = Date.now().toString();
        const aiMsgId = (Date.now() + 1).toString();

        const newUserMsg: Message = {
            id: userMsgId,
            role: "user",
            content: query,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        const placeholderAiMsg: Message = {
            id: aiMsgId,
            role: "ai",
            content: "",
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            isStreaming: true,
            metadata: []
        };

        setMessages((prev) => [...prev, newUserMsg, placeholderAiMsg]);
        setIsSubmitting(true);

        try {
            const res = await fetch("http://localhost:8000/api/v1/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });

            if (!res.ok) throw new Error("Failed to fetch");

            const reader = res.body?.getReader();
            const decoder = new TextDecoder();
            if (!reader) throw new Error("No reader");

            let currentEvent = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith("event: ")) {
                        currentEvent = line.substring(7).trim();
                    } else if (line.startsWith("data: ")) {
                        const currentData = line.substring(6);

                        if (currentEvent === "metadata" && currentData.trim() !== "") {
                            try {
                                const metaJson = JSON.parse(currentData);
                                setMessages((prev) =>
                                    prev.map(msg => msg.id === aiMsgId ? { ...msg, metadata: metaJson.philosophers } : msg)
                                );
                            } catch (e) { console.error("Could not parse metadata event:", currentData) }
                        } else if (currentEvent === "content") {
                            // un-escape \\n to real newlines
                            const char = currentData.replace(/\\n/g, '\n');
                            setMessages((prev) =>
                                prev.map(msg => msg.id === aiMsgId ? { ...msg, content: msg.content + char } : msg)
                            );
                        } else if (currentEvent === "error") {
                            console.error("Chat error:", currentData);
                        }
                    }
                }
            }

            // Finish
            setMessages((prev) =>
                prev.map(msg => msg.id === aiMsgId ? { ...msg, isStreaming: false } : msg)
            );

        } catch (error) {
            console.error(error);
            setMessages((prev) =>
                prev.map(msg => msg.id === aiMsgId ? { ...msg, isStreaming: false, content: "죄송합니다. 오류가 발생했습니다." } : msg)
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar messages={messages} />
            <ChatMain messages={messages} onSendMessage={handleSendMessage} isSubmitting={isSubmitting} onClearChat={() => setMessages([])} />
        </div>
    );
}
