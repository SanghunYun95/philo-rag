import { Sparkles, SquareArrowOutUpRight } from "lucide-react";
import React, { useEffect, useRef, useCallback } from 'react';
import { Message, DocumentMetadata } from "../../types/chat";

const DUMMY_COVER_URL = "https://image.aladin.co.kr/product/dummy";
const DUMMY_BOOK_LINK = "https://www.aladin.co.kr/dummy-link";

interface Props {
    messages: Message[];
    onOpenCitation?: (meta: DocumentMetadata) => void;
    onVisibleMessageChange?: (meta: DocumentMetadata[]) => void;
}

export function MessageList({ messages, onOpenCitation, onVisibleMessageChange }: Props) {
    const observer = useRef<IntersectionObserver | null>(null);
    const visibleMessages = useRef<Map<string, number>>(new Map());
    const pendingElements = useRef<Set<HTMLDivElement>>(new Set());
    const elementById = useRef<Map<string, HTMLDivElement>>(new Map());

    const messagesRef = useRef(messages);
    const callbackRef = useRef(onVisibleMessageChange);

    // Keep refs in sync with latest props
    useEffect(() => {
        messagesRef.current = messages;
        callbackRef.current = onVisibleMessageChange;
    }, [messages, onVisibleMessageChange]);

    useEffect(() => {
        visibleMessages.current.clear();

        observer.current = new IntersectionObserver((entries) => {
            const currentMessages = messagesRef.current;
            const callback = callbackRef.current;

            const emitLatestMetadataOrEmpty = () => {
                if (!callback) return;
                const aiMessages = currentMessages.filter(m => m.role === "ai" && m.metadata && m.metadata.length > 0);
                if (aiMessages.length > 0) {
                    callback(aiMessages[aiMessages.length - 1].metadata!);
                } else {
                    callback([]);
                }
            };

            let changed = false;
            entries.forEach(entry => {
                const id = entry.target.getAttribute("data-message-id");
                if (id) {
                    if (entry.isIntersecting) {
                        visibleMessages.current.set(id, entry.intersectionRatio);
                    } else {
                        visibleMessages.current.delete(id);
                    }
                    changed = true;
                }
            });

            if (changed) {
                if (!callback) return;
                let maxRatio = -1;
                let mostVisibleId: string | null = null;
                visibleMessages.current.forEach((ratio, id) => {
                    if (ratio > maxRatio) {
                        maxRatio = ratio;
                        mostVisibleId = id;
                    }
                });

                if (mostVisibleId) {
                    const msg = currentMessages.find(m => m.id === mostVisibleId);
                    if (msg && msg.metadata && msg.metadata.length > 0) {
                        callback(msg.metadata);
                    } else {
                        emitLatestMetadataOrEmpty();
                    }
                } else {
                    emitLatestMetadataOrEmpty();
                }
            }
        }, {
            threshold: [0, 0.25, 0.5, 0.75, 1.0]
        });

        // The callback ref `observeElement` guarantees DOM readiness.
        // We observe any elements that rendered before the observer was initialized.
        pendingElements.current.forEach((el) => {
            observer.current?.observe(el);
        });

        // Capture ref values for cleanup to satisfy react-hooks/exhaustive-deps
        const visibleMessagesMap = visibleMessages.current;
        const pendingElementsSet = pendingElements.current;
        const elementByIdMap = elementById.current;

        return () => {
            observer.current?.disconnect();
            visibleMessagesMap.clear();
            pendingElementsSet.clear();
            elementByIdMap.clear();
        };
    }, []); // Empty deps because we rely on refs

    const observeElement = useCallback((id: string, el: HTMLDivElement | null) => {
        const prev = elementById.current.get(id);
        if (prev && prev !== el) {
            observer.current?.unobserve(prev);
            pendingElements.current.delete(prev);
            visibleMessages.current.delete(id);
        }

        if (el) {
            elementById.current.set(id, el);
            pendingElements.current.add(el);
            observer.current?.observe(el);
        } else {
            elementById.current.delete(id);
            visibleMessages.current.delete(id);
        }
    }, []);

    // getMessageRef를 반환하는 대신, 컴포넌트 내부에서 생성한 맵에 의존하지 않는
    // 컴포넌트 레벨의 메모이제이션 함수로 처리하여 react-hooks/refs 린팅 에러를 방지합니다.
    const messageRefMap = useRef<Map<string, HTMLDivElement>>(new Map());
    const setNodeRef = useCallback((id: string) => (el: HTMLDivElement | null) => {
        if (el) {
            messageRefMap.current.set(id, el);
            observeElement(id, el);
        } else {
            messageRefMap.current.delete(id);
        }
    }, [observeElement]);

    if (messages.length === 0) {
        return (
            <div className="w-full h-full flex flex-col items-center justify-center text-center p-8">
                <div className="h-16 w-16 rounded-full bg-gradient-to-br from-primary/20 to-transparent border border-primary/30 flex items-center justify-center mb-6 shadow-xl">
                    <Sparkles className="text-primary w-8 h-8" />
                </div>
                <h3 className="font-display text-2xl text-white/90 mb-2">무엇이 당신을 사유하게 만드나요?</h3>
                <p className="text-white/50 max-w-md mx-auto text-sm leading-relaxed">
                    크고 작은 고민부터 삶의 본질적인 질문까지, 위대한 철학자들의 지혜를 통해 새로운 관점을 발견해보세요.
                </p>
            </div>
        );
    }

    return (
        <div className="w-full px-4 md:px-8 pt-6 md:pt-10 pb-10">
            <div className="max-w-3xl mx-auto flex flex-col gap-8 md:gap-10">
                {messages.map((msg) => (
                    msg.role === "user" ? (
                        <div key={msg.id} className="flex justify-end group">
                            <div className="flex flex-col items-end max-w-[90%] md:max-w-[80%]">
                                <div className="bg-[#1a1a1e] border border-white/10 rounded-2xl rounded-tr-sm px-5 py-3 md:px-6 md:py-4 shadow-lg">
                                    <p className="text-white/90 font-sans leading-relaxed whitespace-pre-wrap text-sm md:text-base">
                                        {msg.content}
                                    </p>
                                </div>
                                <span className="text-[11px] text-white/20 mt-2 mr-2">사용자 • {msg.timestamp}</span>
                            </div>
                        </div>
                    ) : (
                        <div key={msg.id} ref={setNodeRef(msg.id)} data-message-id={msg.id} className="ai-message-card flex gap-4 md:gap-6 group">
                            <div className="shrink-0 flex flex-col items-center gap-3">
                                <div className="h-8 w-8 md:h-10 md:w-10 rounded-full bg-gradient-to-br from-[#1a1a1e] to-black border border-primary/30 flex items-center justify-center shadow-[0_0_15px_rgba(217,183,74,0.15)] relative">
                                    <Sparkles className="text-primary w-4 h-4 md:w-5 md:h-5" />
                                </div>
                                <div className="w-px h-full bg-gradient-to-b from-white/10 to-transparent"></div>
                            </div>
                            <div className="flex-1 pb-8 min-w-0">
                                <div className="flex items-center gap-3 mb-2">
                                    <span className="font-display font-bold text-primary text-base md:text-lg">PhiloRAG</span>
                                    {msg.isStreaming && !msg.content && (
                                        <span className="px-2 py-0.5 rounded-full bg-primary/10 text-[10px] text-primary uppercase tracking-wider border border-primary/20 animate-pulse">
                                            생각중...
                                        </span>
                                    )}
                                </div>

                                <div className="prose prose-invert max-w-none text-white/80">
                                    {msg.content ? (
                                        <div className="font-sans leading-7 text-white/80 whitespace-pre-wrap text-sm md:text-base break-words">
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
                                {msg.metadata && msg.metadata.length > 0 && Array.from(new Map(msg.metadata.map((m) => [m.id, m])).values()).map((meta) => {
                                    const title = meta.kr_title || meta.book_info?.title || meta.id;
                                    // Use newly added 'thumbnail' fallback to cover_url
                                    const coverUrl = meta.thumbnail || (meta.book_info?.cover_url !== DUMMY_COVER_URL ? meta.book_info?.cover_url : "");
                                    const bookLink = meta.link || meta.book_info?.link;

                                    const isClickable = Boolean(onOpenCitation);
                                    const interactiveProps = isClickable
                                        ? {
                                            role: "button" as const,
                                            tabIndex: 0,
                                            onClick: () => onOpenCitation?.(meta),
                                            onKeyDown: (e: React.KeyboardEvent<HTMLDivElement>) => {
                                                if (e.key === "Enter" || e.key === " ") {
                                                    e.preventDefault();
                                                    onOpenCitation?.(meta);
                                                }
                                            },
                                        }
                                        : {};
                                    return (
                                        <div
                                            key={meta.id}
                                            {...interactiveProps}
                                            className={`mt - 4 flex flex - col gap - 0 rounded - xl bg - white / 5 border border - white / 10 max - w - xl transition - all group / card overflow - hidden ${isClickable ? "hover:border-primary/30 hover:bg-white/[0.07] cursor-pointer" : ""} `}
                                        >
                                            <div className="flex gap-4 p-4">
                                                <div className="w-16 h-24 shrink-0 bg-[#2a2a2e] flex items-center justify-center rounded-md shadow-[0_2px_8px_rgba(0,0,0,0.5)] overflow-hidden border border-white/5">
                                                    {coverUrl && !coverUrl.includes("dummy") ? (
                                                        <>
                                                            {/* eslint-disable-next-line @next/next/no-img-element */}
                                                            <img src={coverUrl} alt={title} className="w-full h-full object-cover" />
                                                        </>
                                                    ) : (
                                                        <span className="font-display text-2xl text-primary/40 font-bold">{meta.scholar.charAt(0)}</span>
                                                    )}
                                                </div>
                                                <div className="flex-1 min-w-0 flex flex-col justify-center py-1">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-primary/20 text-primary border border-primary/20">Ref</span>
                                                        <p className="text-white/50 text-xs truncate">
                                                            {meta.scholar} • {meta.school}
                                                        </p>
                                                    </div>
                                                    <h5 className="text-white/90 font-display text-base font-medium leading-snug line-clamp-2">{title}</h5>

                                                    {bookLink && bookLink !== DUMMY_BOOK_LINK && (
                                                        <div className="mt-auto pt-2 flex items-center">
                                                            <a
                                                                href={bookLink}
                                                                target="_blank"
                                                                rel="noopener noreferrer"
                                                                onClick={(e) => e.stopPropagation()}
                                                                className="inline-flex items-center gap-1.5 text-xs text-primary/80 hover:text-primary transition-colors hover:underline"
                                                            >
                                                                도서 정보 보기 <SquareArrowOutUpRight className="w-3 h-3" />
                                                            </a>
                                                        </div>
                                                    )}
                                                </div>
                                                {onOpenCitation && (
                                                    <div className="self-center pl-2">
                                                        <button
                                                            type="button"
                                                            aria-label={`${title} 참고 문헌 열기`}
                                                            onClick={(e) => { e.stopPropagation(); onOpenCitation(meta); }}
                                                            className="h-8 w-8 rounded-full bg-white/5 flex items-center justify-center text-white/50 group-hover/card:bg-primary/20 group-hover/card:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 transition-all"
                                                        >
                                                            <SquareArrowOutUpRight className="w-4 h-4 ml-0.5 mb-0.5" />
                                                        </button>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    )
                                })}


                            </div>
                        </div>
                    )
                ))}
            </div>
        </div>
    );
}
