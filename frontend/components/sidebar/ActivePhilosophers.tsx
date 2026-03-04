import { BrainCircuit, CheckCircle } from "lucide-react";
import { DocumentMetadata } from "../../types/chat";

interface Props {
    metadata: DocumentMetadata[]; // all seen philosophers
    activeMetadata?: DocumentMetadata[]; // active philosophers
}

export function ActivePhilosophers({ metadata, activeMetadata = [] }: Props) {
    const uniquePhilosophers = Array.from(new Set(metadata.map(m => m.scholar)))
        .map(scholar => metadata.find(m => m.scholar === scholar))
        .filter((m): m is DocumentMetadata => m !== undefined);

    const activeScholarSet = new Set(activeMetadata.map(m => m.scholar));

    // Sort to put highlighted philosophers at the top
    const sortedPhilosophers = [...uniquePhilosophers].sort((a, b) => {
        const aActive = activeScholarSet.has(a.scholar);
        const bActive = activeScholarSet.has(b.scholar);
        if (aActive && !bActive) return -1;
        if (!aActive && bActive) return 1;
        return 0;
    });

    return (
        <div>
            <h3 className="text-xs font-medium text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                <BrainCircuit className="w-4 h-4" />
                활성화된 철학자
            </h3>
            {sortedPhilosophers.length === 0 ? (
                <p className="text-white/30 text-xs italic">현재 참조 중인 철학자가 없습니다.</p>
            ) : (
                <div className="space-y-3">
                    {sortedPhilosophers.map((meta) => {
                        const isActive = activeScholarSet.has(meta.scholar);
                        return (
                            <div
                                key={meta.scholar}
                                className={`w-full text-left group relative overflow-hidden rounded-xl border p-4 transition-all duration-300
                                    ${isActive
                                        ? "border-primary/50 bg-primary/10 shadow-[0_0_15px_rgba(217,183,74,0.1)]"
                                        : "border-white/10 bg-white/5"
                                    }`}
                            >
                                <div className={`absolute inset-0 bg-gradient-to-r ${isActive ? "from-primary/10" : "from-primary/5"} to-transparent opacity-0 group-hover:opacity-20 transition-opacity`}></div>
                                <div className="relative flex items-center gap-4">
                                    <div
                                        className={`h-12 w-12 shrink-0 rounded-full border ${isActive ? "border-primary/30" : "border-white/20"} bg-gradient-to-br from-white/10 to-transparent flex items-center justify-center shadow-inner`}
                                        title={meta.scholar}
                                    >
                                        <span className={`font-display text-xl ${isActive ? "text-primary/90" : "text-white/70"}`}>{meta.scholar.charAt(0)}</span>
                                    </div>
                                    <div className="flex-1">
                                        <h4 className={`font-display text-lg ${isActive ? "text-white" : "text-white/80"}`}>{meta.scholar}</h4>
                                        <p className={`text-xs ${isActive ? "text-white/60" : "text-white/40"}`}>{meta.school}</p>
                                    </div>
                                    <CheckCircle className={`ml-auto w-5 h-5 shrink-0 transition-colors ${isActive ? "text-primary" : "text-primary/20 group-hover:text-primary/50"}`} />
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
