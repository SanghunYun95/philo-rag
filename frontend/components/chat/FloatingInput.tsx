"use client";

import { Paperclip, Mic, ArrowUp } from "lucide-react";
import { useState } from "react";

interface FloatingInputProps {
    onSendMessage: (query: string) => void;
    isSubmitting: boolean;
}

export function FloatingInput({ onSendMessage, isSubmitting }: FloatingInputProps) {
    const [inputValue, setInputValue] = useState("");

    const handleSend = () => {
        if (!inputValue.trim() || isSubmitting) return;
        onSendMessage(inputValue);
        setInputValue("");
    };
    return (
        <div className="w-full max-w-3xl mx-auto relative group">
            {/* Glow effect behind input */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#d9b74a]/10 via-white/5 to-[#d9b74a]/10 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>

            <div className="relative flex items-end gap-2 bg-[#1e1e24] p-2 pr-2 pl-4 rounded-2xl border border-white/10 shadow-xl">
                <button
                    type="button"
                    aria-label="컨텍스트 업로드"
                    className="mb-2 p-2 rounded-lg text-white/30 hover:text-[#d9b74a] hover:bg-white/5 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#d9b74a]/60"
                    title="컨텍스트 업로드"
                >
                    <Paperclip className="w-5 h-5" />
                </button>
                <div className="flex-1 py-3">
                    <label htmlFor="chat-input" className="sr-only">질문 입력</label>
                    <textarea
                        id="chat-input"
                        className="w-full bg-transparent border-0 text-white/90 placeholder-white/30 focus:ring-0 p-0 resize-none font-sans leading-relaxed max-h-32 outline-none"
                        placeholder="미덕, 형이상학, 혹은 윤리에 대해 질문해보세요..."
                        rows={1}
                        style={{ minHeight: "24px" }}
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                    ></textarea>
                </div>
                <div className="flex items-center gap-1 mb-1">
                    <button
                        type="button"
                        aria-label="음성 입력"
                        className="p-2 rounded-lg text-white/30 hover:text-[#d9b74a] hover:bg-white/5 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#d9b74a]/60"
                        title="음성 입력"
                    >
                        <Mic className="w-5 h-5" />
                    </button>
                    <button
                        type="button"
                        aria-label="메시지 전송"
                        onClick={handleSend}
                        className="h-10 w-10 rounded-xl bg-white text-[#0f0f11] flex items-center justify-center hover:bg-[#d9b74a] transition-colors shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60 disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={!inputValue.trim() || isSubmitting}
                    >
                        <ArrowUp className="w-5 h-5" />
                    </button>
                </div>
            </div>
            <div className="text-center mt-2">
                <p className="text-[10px] text-white/30">
                    PhiloRAG는 실수를 할 수 있습니다. 중요한 철학적 출처는 문헌을 직접 확인하세요.
                </p>
            </div>
        </div>
    );
}
