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

        const userMsgId = crypto.randomUUID();
        const aiMsgId = crypto.randomUUID();

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
            const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
            const res = await fetch(`${baseUrl}/api/v1/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            });

            if (!res.ok) throw new Error("Failed to fetch");

            const reader = res.body?.getReader();
            const decoder = new TextDecoder();
            if (!reader) throw new Error("No reader");

            const processLine = (line: string, eventObj: { current: string }) => {
                if (line.startsWith("event: ")) {
                    eventObj.current = line.substring(7).trim();
                } else if (line.startsWith("data: ")) {
                    const currentData = line.substring(6);

                    if (eventObj.current === "metadata" && currentData.trim() !== "") {
                        try {
                            const metaJson = JSON.parse(currentData);
                            setMessages((prev) =>
                                prev.map(msg => msg.id === aiMsgId ? { ...msg, metadata: metaJson.philosophers } : msg)
                            );
                        } catch (e) { console.error("Could not parse metadata event:", currentData) }
                    } else if (eventObj.current === "content") {
                        // un-escape \\n to real newlines
                        const char = currentData.replace(/\\n/g, '\n');
                        setMessages((prev) =>
                            prev.map(msg => msg.id === aiMsgId ? { ...msg, content: msg.content + char } : msg)
                        );
                    } else if (eventObj.current === "error") {
                        console.error("Chat error:", currentData);
                        setMessages((prev) =>
                            prev.map(msg => msg.id === aiMsgId ? { ...msg, content: currentData, isStreaming: false } : msg)
                        );
                    }
                }
            };

            let eventObj = { current: "" };
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    // Process any remaining data in the buffer
                    if (buffer) {
                        const lines = buffer.split('\n');
                        for (const line of lines) {
                            processLine(line, eventObj);
                        }
                    }
                    break;
                }

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');

                // Keep the last partial line in the buffer
                buffer = lines.pop() || "";

                for (const line of lines) {
                    processLine(line, eventObj);
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
