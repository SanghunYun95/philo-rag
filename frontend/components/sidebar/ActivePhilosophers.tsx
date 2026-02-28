import { BrainCircuit, CheckCircle, Circle } from "lucide-react";
import { DocumentMetadata } from "../../types/chat";

interface Props {
    metadata: DocumentMetadata[];
}

export function ActivePhilosophers({ metadata }: Props) {
    // extract unique philosophers
    const uniquePhilosophers = Array.from(new Set(metadata.map(m => m.scholar)))
        .map(scholar => metadata.find(m => m.scholar === scholar)!);

    return (
        <div>
            <h3 className="text-xs font-medium text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                <BrainCircuit className="w-4 h-4" />
                활성화된 철학자
            </h3>
            {uniquePhilosophers.length === 0 ? (
                <p className="text-white/30 text-xs italic">현재 참조 중인 철학자가 없습니다.</p>
            ) : (
                <div className="space-y-3">
                    {uniquePhilosophers.map((meta, i) => (
                        <button
                            key={i}
                            type="button"
                            className="w-full text-left group relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-4 hover:border-primary/50 transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/60"
                        >
                            <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            <div className="relative flex items-center gap-4">
                                <div
                                    className="h-12 w-12 shrink-0 rounded-full border border-white/20 bg-gradient-to-br from-white/10 to-transparent flex items-center justify-center shadow-inner"
                                    title={meta.scholar}
                                >
                                    <span className="font-display text-xl text-primary/90">{meta.scholar.charAt(0)}</span>
                                </div>
                                <div className="flex-1">
                                    <h4 className="font-display text-lg text-white">{meta.scholar}</h4>
                                    <p className="text-xs text-white/50">{meta.school}</p>
                                </div>
                                <CheckCircle className="ml-auto text-primary/50 group-hover:text-primary w-5 h-5 shrink-0" />
                            </div>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
