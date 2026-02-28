import { Library, BookOpen } from "lucide-react";

export function ContextSources() {
    return (
        <div>
            <h3 className="text-xs font-medium text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                <Library className="w-4 h-4" />
                Context Sources
            </h3>
            <div className="space-y-3">
                <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer border border-transparent hover:border-white/5">
                    <div className="h-14 w-10 bg-neutral-800 rounded border border-white/10 flex items-center justify-center shrink-0 shadow-lg group-hover:border-primary/30 transition-colors">
                        <BookOpen className="text-white/30 w-5 h-5" />
                    </div>
                    <div>
                        <h5 className="font-display text-base text-white/90 group-hover:text-primary transition-colors">
                            Beyond Good and Evil
                        </h5>
                        <p className="text-xs text-white/40 mt-1">Chapter 4: Apothegms and Interludes</p>
                        <div className="flex items-center gap-1 mt-2">
                            <span className="px-1.5 py-0.5 rounded bg-primary/10 text-[10px] text-primary border border-primary/20">
                                High Relevance
                            </span>
                        </div>
                    </div>
                </div>

                <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer border border-transparent hover:border-white/5">
                    <div className="h-14 w-10 bg-neutral-800 rounded border border-white/10 flex items-center justify-center shrink-0 shadow-lg group-hover:border-primary/30 transition-colors">
                        <BookOpen className="text-white/30 w-5 h-5" />
                    </div>
                    <div>
                        <h5 className="font-display text-base text-white/90 group-hover:text-primary transition-colors">
                            The Republic
                        </h5>
                        <p className="text-xs text-white/40 mt-1">Book I: Justice</p>
                        <div className="flex items-center gap-1 mt-2">
                            <span className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-white/50 border border-white/10">
                                Reference
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
