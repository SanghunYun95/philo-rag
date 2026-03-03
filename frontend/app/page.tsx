"use client";

import { useState, useCallback } from "react";
import { Sidebar } from "../components/sidebar/Sidebar";
import { ChatMain } from "../components/chat/ChatMain";
import { Message, DocumentMetadata } from "../types/chat";

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [chatTitle, setChatTitle] = useState<string>("미덕에 관한 대화");
    const [activeMetadata, setActiveMetadata] = useState<DocumentMetadata[]>([]);

    const processLine = useCallback((line: string, eventObj: { current: string }, aiMsgId: string): boolean => {
        if (line.startsWith("event: ")) {
            eventObj.current = line.substring(7).trim();
        } else if (line.startsWith("data: ")) {
            const currentData = line.substring(6).replace(/\r$/, "");
            const currentEvent = eventObj.current;

            if (currentEvent === "metadata" && currentData.trim() !== "") {
                try {
                    const metaJson = JSON.parse(currentData);
                    const philosophersArray = Array.isArray(metaJson.philosophers) ? metaJson.philosophers : [];
                    setMessages((prev) =>
                        prev.map(msg => msg.id === aiMsgId ? { ...msg, metadata: philosophersArray } : msg)
                    );
                } catch (e) { console.error("Could not parse metadata event:", currentData, e) }
            } else if (currentEvent === "content") {
                // un-escape \\n to real newlines
                const char = currentData.replace(/\\n/g, '\n');
                setMessages((prev) =>
                    prev.map(msg => msg.id === aiMsgId ? { ...msg, content: msg.content + char } : msg)
                );
            } else if (currentEvent === "error") {
                console.error("Chat error:", currentData);
                setMessages((prev) =>
                    prev.map(msg => msg.id === aiMsgId ? { ...msg, content: currentData, isStreaming: false } : msg)
                );
                return true;
            }
        }
        return false;
    }, []);

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

        const isFirstMessage = messages.length === 0;
        const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

        if (isFirstMessage) {
            fetch(`${baseUrl}/api/v1/chat/title`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.title) setChatTitle(data.title);
                })
                .catch(err => console.error("Failed to fetch title:", err));
        }

        try {
            const historyToSend = messages.slice(-10).map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            const res = await fetch(`${baseUrl}/api/v1/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query, history: historyToSend })
            });

            if (res.status === 429) {
                setMessages((prev) =>
                    prev.map(msg => msg.id === aiMsgId ? { ...msg, isStreaming: false, content: "입력량이 너무 많습니다. 잠시 후 1분 뒤에 다시 철학자와 대화를 시도해 주세요." } : msg)
                );
                return;
            }

            if (!res.ok) throw new Error(`Failed to fetch: ${res.status} ${res.statusText}`);

            const reader = res.body?.getReader();
            const decoder = new TextDecoder();
            if (!reader) throw new Error("No reader");

            // Process line memoized above

            const eventObj = { current: "" };
            let buffer = "";

            let shouldStop = false;
            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    // Flush the internal buffer of the decoder (for incomplete multi-byte chars)
                    buffer += decoder.decode();
                    // Process any remaining data in the buffer
                    if (buffer) {
                        const lines = buffer.split('\n');
                        for (const line of lines) {
                            if (processLine(line, eventObj, aiMsgId)) {
                                shouldStop = true;
                                break;
                            }
                        }
                    }
                    break;
                }

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');

                // Keep the last partial line in the buffer
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (processLine(line, eventObj, aiMsgId)) {
                        shouldStop = true;
                        break;
                    }
                }
                if (shouldStop) {
                    await reader.cancel();
                    break;
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
        <div className="flex h-screen overflow-hidden relative">
            <Sidebar messages={messages} activeMetadata={activeMetadata} isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
            <ChatMain
                chatTitle={chatTitle}
                messages={messages}
                onSendMessage={handleSendMessage}
                isSubmitting={isSubmitting}
                onClearChat={() => {
                    setMessages([]);
                    setChatTitle("미덕에 관한 대화");
                    setActiveMetadata([]);
                }}
                onMenuClick={() => setIsSidebarOpen(true)}
                onVisibleMessageChange={setActiveMetadata}
            />
        </div>
    );
}
