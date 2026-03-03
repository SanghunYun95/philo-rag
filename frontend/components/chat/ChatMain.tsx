"use client";

import { Share, Plus, Menu } from "lucide-react";
import { useRef, useEffect, useState } from "react";
import { MessageList } from "./MessageList";
import { FloatingInput } from "./FloatingInput";
import { Message, DocumentMetadata } from "../../types/chat";

interface ChatMainProps {
    messages: Message[];
    chatTitle?: string;
    onSendMessage: (query: string) => void;
    isSubmitting: boolean;
    onClearChat: () => void;
    onMenuClick?: () => void;
    onVisibleMessageChange?: (meta: DocumentMetadata[]) => void;
}

export function ChatMain({ messages, chatTitle = "미덕에 관한 대화", onSendMessage, isSubmitting, onClearChat, onMenuClick, onVisibleMessageChange }: ChatMainProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [shouldAutoScroll, setShouldAutoScroll] = useState(true);
    const [startTime, setStartTime] = useState<string>("");
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setStartTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        setMounted(true);
    }, []);

    const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
        const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
        const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
        setShouldAutoScroll(isNearBottom);
    };

    // Auto-scroll to bottom of messages conditionally
    useEffect(() => {
        if (shouldAutoScroll) {
            messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, shouldAutoScroll]);

    return (
        <main className="flex-1 flex flex-col relative min-h-0 bg-[#0f0f11] overflow-hidden">
            {/* Top Navigation / Context Header */}
            <div className="flex-none p-4 md:p-6 flex justify-between items-start bg-[#0f0f11] border-b border-white/5 z-30">
                <div className="flex items-center gap-3">
                    <button
                        onClick={onMenuClick}
                        className="md:hidden p-2 text-white/60 hover:text-white rounded-lg bg-white/5 border border-white/10"
                    >
                        <Menu className="w-5 h-5" />
                    </button>
                    <div>
                        <h2 className="font-display text-xl md:text-3xl text-white/90 transition-all duration-300">{chatTitle}</h2>
                        <p className="text-xs md:text-sm text-white/40 mt-1">세션 시작: {mounted ? startTime : ""}</p>
                    </div>
                </div>
                <div className="flex gap-2">
                    <button onClick={() => alert("준비 중입니다.")} className="hidden sm:flex px-4 py-2 rounded-full bg-white/5 border border-white/10 text-white/60 text-sm hover:bg-white/10 hover:text-white transition-colors items-center gap-2">
                        <Share className="w-4 h-4" />
                        내보내기
                    </button>
                    <button onClick={onClearChat} className="p-2 sm:px-4 sm:py-2 rounded-full bg-white/5 border border-white/10 text-white/60 text-sm hover:bg-white/10 hover:text-white transition-colors flex items-center gap-2">
                        <Plus className="w-4 h-4 md:w-4 md:h-4" />
                        <span className="hidden sm:inline">새 대화</span>
                    </button>
                </div>
            </div>

            {/* Scrollable Message Area */}
            <div className="flex-1 overflow-y-auto w-full relative" onScroll={handleScroll}>
                <MessageList messages={messages} onVisibleMessageChange={onVisibleMessageChange} />
                <div ref={messagesEndRef} />
            </div>

            {/* Bottom Input Area Container */}
            <div className="flex-none w-full bg-[#0f0f11] border-t border-white/5 p-4 z-30">
                <FloatingInput onSendMessage={onSendMessage} isSubmitting={isSubmitting} />
            </div>
        </main>
    );
}
