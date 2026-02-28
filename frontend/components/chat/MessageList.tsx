import { Sparkles, SquareArrowOutUpRight, ThumbsUp, Copy, RotateCcw, ChevronRight, User } from "lucide-react";
import { Message } from "../../types/chat";

interface Props {
    messages: Message[];
}

export function MessageList({ messages }: Props) {
    if (messages.length === 0) {
        return (
            <div className="w-full h-full flex flex-col items-center justify-center text-center p-8">
                <div className="h-16 w-16 rounded-full bg-gradient-to-br from-primary/20 to-transparent border border-primary/30 flex items-center justify-center mb-6 shadow-xl">
                    <Sparkles className="text-primary w-8 h-8" />
                </div>
                <h3 className="font-display text-2xl text-white/90 mb-2">어떤 철학적 고민이 있으신가요?</h3>
                <p className="text-white/50 max-w-md mx-auto text-sm leading-relaxed">
                    미덕, 죽음, 사랑, 자아 등 삶의 본질적인 질문들을 과거의 위대한 철학자들과 함께 탐구해보세요.
                </p>
            </div>
        );
    }

    return (
        <div className="w-full px-8 pt-10 pb-10">
            <div className="max-w-3xl mx-auto flex flex-col gap-10">
                {messages.map((msg) => (
                    msg.role === "user" ? (
                        <div key={msg.id} className="flex justify-end group">
                            <div className="flex flex-col items-end max-w-[80%]">
                                <div className="bg-[#1a1a1e] border border-white/10 rounded-2xl rounded-tr-sm px-6 py-4 shadow-lg">
                                    <p className="text-white/90 font-sans leading-relaxed whitespace-pre-wrap">
                                        {msg.content}
                                    </p>
                                </div>
                                <span className="text-[11px] text-white/20 mt-2 mr-2">사용자 • {msg.timestamp}</span>
                            </div>
                        </div>
                    ) : (
                        <div key={msg.id} className="flex gap-6 group">
                            <div className="shrink-0 flex flex-col items-center gap-3">
                                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-[#1a1a1e] to-black border border-primary/30 flex items-center justify-center shadow-[0_0_15px_rgba(217,183,74,0.15)] relative">
                                    <Sparkles className="text-primary w-5 h-5" />
                                </div>
                                <div className="w-px h-full bg-gradient-to-b from-white/10 to-transparent"></div>
                            </div>
                            <div className="flex-1 pb-8">
                                <div className="flex items-center gap-3 mb-2">
                                    <span className="font-display font-bold text-primary text-lg">PhiloRAG</span>
                                    {msg.isStreaming && !msg.content && (
                                        <span className="px-2 py-0.5 rounded-full bg-primary/10 text-[10px] text-primary uppercase tracking-wider border border-primary/20 animate-pulse">
                                            생각중...
                                        </span>
                                    )}
                                </div>

                                <div className="prose prose-invert max-w-none text-white/80">
                                    {msg.content ? (
                                        <div className="font-sans leading-7 text-white/80 whitespace-pre-wrap">
                                            {msg.content}
                                        </div>
                                    ) : (
                                        msg.isStreaming ? (
                                            <div className="flex gap-1 items-center h-6">
                                                <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce"></div>
                                                <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                                <div className="w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                                            </div>
                                        ) : null
                                    )}
                                </div>

                                {/* Citation Cards if metadata exists */}
                                {msg.metadata && msg.metadata.length > 0 && Array.from(new Set(msg.metadata.map(m => m.book_info.title))).map((title, idx) => {
                                    const meta = msg.metadata!.find(m => m.book_info.title === title)!;
                                    return (
                                        <div key={idx} className="mt-8 flex gap-4 p-4 rounded-xl bg-white/5 border border-white/10 max-w-xl hover:border-primary/30 transition-colors cursor-pointer group/card">
                                            <div className="h-16 w-12 shrink-0 bg-white/10 flex items-center justify-center rounded shadow-inner overflow-hidden">
                                                {meta.book_info.cover_url && !meta.book_info.cover_url.includes("dummy") ? (
                                                    <img src={meta.book_info.cover_url} alt={title} className="w-full h-full object-cover opacity-80" />
                                                ) : (
                                                    <span className="font-display text-xl text-primary/60">{meta.scholar.charAt(0)}</span>
                                                )}
                                            </div>
                                            <div className="flex-1 min-w-0 flex flex-col justify-center">
                                                <h5 className="text-white font-display text-lg truncate">참조: {title}</h5>
                                                <p className="text-white/40 text-sm line-clamp-1 mt-1">
                                                    {meta.scholar} - {meta.school}
                                                </p>
                                            </div>
                                            <button
                                                type="button"
                                                aria-label={`${title} 참고 문헌 열기`}
                                                className="h-8 w-8 rounded-full bg-white/10 flex items-center justify-center text-white/60 group-hover/card:bg-primary group-hover/card:text-black focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 transition-all self-center"
                                            >
                                                <SquareArrowOutUpRight className="w-4 h-4" />
                                            </button>
                                        </div>
                                    )
                                })}

                                {!msg.isStreaming && (
                                    <div className="flex gap-4 mt-6">
                                        <button type="button" aria-label="유용함" className="text-xs text-white/40 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded flex items-center gap-1 transition-colors">
                                            <ThumbsUp className="w-3 h-3" /> 유용함
                                        </button>
                                        <button type="button" aria-label="복사" className="text-xs text-white/40 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded flex items-center gap-1 transition-colors">
                                            <Copy className="w-3 h-3" /> 복사
                                        </button>
                                        <button type="button" aria-label="재생성" className="text-xs text-white/40 hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 rounded flex items-center gap-1 transition-colors">
                                            <RotateCcw className="w-3 h-3" /> 재생성
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    )
                ))}
            </div>
        </div>
    );
}
