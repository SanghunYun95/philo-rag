"use client";

import { Paperclip, ArrowUp } from "lucide-react";
import { useState, useRef } from "react";

interface FloatingInputProps {
    onSendMessage: (query: string) => void;
    isSubmitting: boolean;
}

export function FloatingInput({ onSendMessage, isSubmitting }: FloatingInputProps) {
    const [inputValue, setInputValue] = useState("");
    const isComposing = useRef(false);
    const lastCompositionEndAt = useRef(0);

    const handleSend = () => {
        if (!inputValue.trim() || isSubmitting) return;
        onSendMessage(inputValue);
        setInputValue("");
    };
    return (
        <div className="w-full max-w-3xl mx-auto relative group">
            {/* Glow effect behind input */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#d9b74a]/10 via-white/5 to-[#d9b74a]/10 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>

            <div className="relative flex items-end gap-1 md:gap-2 bg-[#1e1e24] p-1.5 md:p-2 pr-1.5 md:pr-2 pl-3 md:pl-4 rounded-2xl border border-white/10 shadow-xl">
                <button
                    type="button"
                    aria-label="컨텍스트 업로드"
                    className="mb-1.5 md:mb-2 p-1.5 md:p-2 rounded-lg text-white/30 hover:text-[#d9b74a] hover:bg-white/5 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#d9b74a]/60"
                    title="컨텍스트 업로드"
                >
                    <Paperclip className="w-4 h-4 md:w-5 md:h-5" />
                </button>
                <div className="flex-1 py-2 md:py-3">
                    <label htmlFor="chat-input" className="sr-only">질문 입력</label>
                    <textarea
                        id="chat-input"
                        className="w-full bg-transparent border-0 text-white/90 placeholder-white/30 focus:ring-0 p-0 resize-none font-sans leading-relaxed text-sm md:text-base max-h-32 outline-none"
                        placeholder="미덕, 형이상학 등에 대해 편하게 물어보세요..."
                        rows={1}
                        style={{ minHeight: "24px" }}
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onCompositionStart={() => { isComposing.current = true; }}
                        onCompositionEnd={() => {
                            isComposing.current = false;
                            lastCompositionEndAt.current = Date.now();
                        }}
                        onKeyDown={(e) => {
                            if (e.nativeEvent.isComposing || isComposing.current || Date.now() - lastCompositionEndAt.current < 50) return;

                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                    ></textarea>
                </div>
                <div className="flex items-center gap-1 mb-1 md:mb-1">
                    <button
                        type="button"
                        aria-label="메시지 전송"
                        onClick={handleSend}
                        className="h-8 w-8 md:h-10 md:w-10 rounded-xl bg-white text-[#0f0f11] flex items-center justify-center hover:bg-[#d9b74a] transition-colors shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60 disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={!inputValue.trim() || isSubmitting}
                    >
                        <ArrowUp className="w-4 h-4 md:w-5 md:h-5" />
                    </button>
                </div>
            </div>
            <div className="text-center mt-2">
                <p className="text-[10px] text-white/30">
                    PhiloRAG는 실수를 할 수 있습니다. 중요한 철학적 출처는 문헌을 직접 확인하세요.
                </p>
            </div>
        </div >
    );
}
