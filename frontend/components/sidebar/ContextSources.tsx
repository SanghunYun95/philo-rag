import { BookOpen, Star } from "lucide-react";
import { DocumentMetadata } from "../../types/chat";

interface Props {
    metadata: DocumentMetadata[];
}

export function ContextSources({ metadata }: Props) {
    // extract unique books
    const uniqueBooks = Array.from(new Set(metadata.map(m => m.book_info.title)))
        .map(title => metadata.find(m => m.book_info.title === title)!);

    return (
        <div>
            <h3 className="text-xs font-medium text-primary uppercase tracking-widest mb-4 flex items-center gap-2 mt-8">
                <BookOpen className="w-4 h-4" />
                참고 자료
            </h3>
            {uniqueBooks.length === 0 ? (
                <p className="text-white/30 text-xs italic">답변에 사용된 참고 문헌이 없습니다.</p>
            ) : (
                <ul className="space-y-4">
                    {uniqueBooks.map((meta, i) => (
                        <li key={i} className="-m-2">
                            <button
                                type="button"
                                className="w-full text-left group flex gap-4 cursor-pointer hover:bg-white/5 p-2 rounded-xl transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
                            >
                                <div className="h-16 w-12 shrink-0 bg-white/5 rounded border border-white/10 shadow-sm relative overflow-hidden flex items-center justify-center">
                                    {meta.book_info.cover_url && !meta.book_info.cover_url.includes("dummy") ? (
                                        <img src={meta.book_info.cover_url} alt={meta.book_info.title} className="w-full h-full object-cover grayscale opacity-70 group-hover:grayscale-0 group-hover:opacity-100 transition-all" />
                                    ) : (
                                        <BookOpen className="w-5 h-5 text-white/20" />
                                    )}
                                </div>
                                <div className="flex-1 min-w-0 flex flex-col justify-center">
                                    <h4 className="font-display text-white text-sm truncate group-hover:text-primary transition-colors">{meta.book_info.title}</h4>
                                    <p className="text-xs text-white/40 mt-1">{meta.scholar}</p>
                                    <div className="flex items-center gap-1 mt-2">
                                        <Star className="w-3 h-3 text-primary/60 fill-primary/60" />
                                        <span className="text-[10px] text-white/30 uppercase tracking-widest">높은 관련도</span>
                                    </div>
                                </div>
                            </button>
                        </li>
                    ))}
                </ul>
            )}

        </div>
    );
}
