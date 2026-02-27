import { Sparkles, SquareArrowOutUpRight, ThumbsUp, Copy, RotateCcw, ChevronRight } from "lucide-react";

export function MessageList() {
    return (
        <div className="w-full px-8 pt-10 pb-10">
            <div className="max-w-3xl mx-auto flex flex-col gap-10">

                {/* User Message */}
                <div className="flex justify-end group">
                    <div className="flex flex-col items-end max-w-[80%]">
                        <div className="bg-[#1a1a1e] border border-white/10 rounded-2xl rounded-tr-sm px-6 py-4 shadow-lg">
                            <p className="text-white/90 font-sans leading-relaxed">
                                How would Socrates define virtue in the context of modern ethics, particularly regarding digital privacy?
                            </p>
                        </div>
                        <span className="text-[11px] text-white/20 mt-2 mr-2">User • 10:43 AM</span>
                    </div>
                </div>

                {/* AI Response */}
                <div className="flex gap-6 group">
                    <div className="shrink-0 flex flex-col items-center gap-3">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-[#1a1a1e] to-black border border-[#d9b74a]/30 flex items-center justify-center shadow-[0_0_15px_rgba(217,183,74,0.15)] relative">
                            <Sparkles className="text-[#d9b74a] w-5 h-5" />
                        </div>
                        <div className="w-px h-full bg-gradient-to-b from-white/10 to-transparent"></div>
                    </div>
                    <div className="flex-1 pb-8">
                        <div className="flex items-center gap-3 mb-2">
                            <span className="font-display font-bold text-[#d9b74a] text-lg">PhiloRAG</span>
                            <span className="px-2 py-0.5 rounded-full bg-[#d9b74a]/10 text-[10px] text-[#d9b74a] uppercase tracking-wider border border-[#d9b74a]/20">
                                Thinking
                            </span>
                        </div>
                        <div className="prose prose-invert max-w-none text-white/80">
                            <p className="font-display text-xl leading-relaxed mb-6">
                                To understand virtue through the Socratic lens in our digital age, one must first return to his fundamental premise:{" "}
                                <em className="text-white">virtue is knowledge</em>.
                            </p>
                            <p className="font-sans leading-7 mb-6 text-white/60">
                                Socrates argued that no one errs willingly; rather, vice is the result of ignorance. In the context of digital privacy, he might argue that the "evil" of surveillance or data exploitation stems not from malice, but from a profound ignorance of the{" "}
                                <span className="text-[#d9b74a]/80 border-b border-[#d9b74a]/30 pb-0.5">True Good</span> regarding the self and the community.
                            </p>

                            <div className="pl-6 border-l-2 border-[#d9b74a]/40 my-8 py-1">
                                <p className="font-display italic text-white/70 text-lg">
                                    "The unexamined life is not worth living."
                                </p>
                                <p className="text-xs text-[#d9b74a] mt-2 uppercase tracking-widest">— Apology, 38a</p>
                            </div>

                            <p className="font-sans leading-7 text-white/60">
                                If we apply this to your question, a "virtuous" digital existence would require:
                            </p>
                            <ul className="list-none space-y-3 mt-4 text-white/70 font-sans pl-0">
                                <li className="flex gap-3">
                                    <ChevronRight className="text-[#d9b74a] w-4 h-4 mt-1 shrink-0" />
                                    <span>
                                        <strong>Knowledge of the Self:</strong> Understanding what data constitutes the "digital soul" and protecting it as one protects their character.
                                    </span>
                                </li>
                                <li className="flex gap-3">
                                    <ChevronRight className="text-[#d9b74a] w-4 h-4 mt-1 shrink-0" />
                                    <span>
                                        <strong>Knowledge of the Good:</strong> Recognizing that privacy is not merely hiding, but maintaining the autonomy required for moral agency.
                                    </span>
                                </li>
                            </ul>
                        </div>

                        {/* Interactive Citation Card */}
                        <div className="mt-8 flex gap-4 p-4 rounded-xl bg-white/5 border border-white/10 max-w-xl hover:border-[#d9b74a]/30 transition-colors cursor-pointer group/card">
                            <div
                                className="h-16 w-12 shrink-0 bg-cover bg-center rounded shadow-inner opacity-80"
                                title="Cover of Plato's Republic book"
                                style={{
                                    backgroundImage:
                                        "url('https://lh3.googleusercontent.com/aida-public/AB6AXuB0kzQPApdugd8DAq405iPtJUN3KwxNoOhnU6U_-gIAFVlKHj9ecCztHeXwVafq5nL4ADGFDuozS_iOYdD1eXlVrP471L_bmhpz8tLheZ8TQSo9kxClvJiZdltmO1Ysngs29XLzkGdCjYIBNrnpG1n0rEmEmcbTsX5dfrTi-QBZcNusirPuXskWMZiVqQmrbNP_aTJM44KlUmvB_t5RfGl8lg8ER20GNWCCu_destp9BAopuVohFr65NGdqaI9sJmaWK1TBow_Zw1A')",
                                }}
                            ></div>
                            <div className="flex-1 min-w-0">
                                <h5 className="text-white font-display text-lg truncate">Reference: The Republic, Book I</h5>
                                <p className="text-white/40 text-sm line-clamp-2 mt-1">
                                    Socrates discusses the nature of justice and whether the just man is happier than the unjust man.
                                </p>
                            </div>
                            <button className="h-8 w-8 rounded-full bg-white/10 flex items-center justify-center text-white/60 group-hover/card:bg-[#d9b74a] group-hover/card:text-black transition-all self-center">
                                <SquareArrowOutUpRight className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="flex gap-4 mt-6">
                            <button className="text-xs text-white/40 hover:text-[#d9b74a] flex items-center gap-1 transition-colors">
                                <ThumbsUp className="w-3 h-3" /> Helpful
                            </button>
                            <button className="text-xs text-white/40 hover:text-[#d9b74a] flex items-center gap-1 transition-colors">
                                <Copy className="w-3 h-3" /> Copy
                            </button>
                            <button className="text-xs text-white/40 hover:text-[#d9b74a] flex items-center gap-1 transition-colors">
                                <RotateCcw className="w-3 h-3" /> Regenerate
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
