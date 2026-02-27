import { Paperclip, Mic, ArrowUp } from "lucide-react";

export function FloatingInput() {
    return (
        <div className="w-full max-w-3xl mx-auto relative group">
            {/* Glow effect behind input */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#d9b74a]/10 via-white/5 to-[#d9b74a]/10 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>

            <div className="relative flex items-end gap-2 bg-[#1e1e24] p-2 pr-2 pl-4 rounded-2xl border border-white/10 shadow-xl">
                <button
                    className="mb-2 p-2 rounded-lg text-white/30 hover:text-[#d9b74a] hover:bg-white/5 transition-colors"
                    title="Upload Context"
                >
                    <Paperclip className="w-5 h-5" />
                </button>
                <div className="flex-1 py-3">
                    <textarea
                        className="w-full bg-transparent border-0 text-white placeholder-white/20 focus:ring-0 p-0 resize-none font-sans leading-relaxed max-h-32 outline-none"
                        placeholder="Inquire about virtue, metaphysics, or ethics..."
                        rows={1}
                        style={{ minHeight: "24px" }}
                    ></textarea>
                </div>
                <div className="flex items-center gap-1 mb-1">
                    <button
                        className="p-2 rounded-lg text-white/30 hover:text-[#d9b74a] hover:bg-white/5 transition-colors"
                        title="Voice Input"
                    >
                        <Mic className="w-5 h-5" />
                    </button>
                    <button className="h-10 w-10 rounded-xl bg-white text-[#0f0f11] flex items-center justify-center hover:bg-[#d9b74a] transition-colors shadow-lg">
                        <ArrowUp className="w-5 h-5" />
                    </button>
                </div>
            </div>
            <div className="text-center mt-2">
                <p className="text-[10px] text-white/20">
                    PhiloRAG can make mistakes. Verify important philosophical references.
                </p>
            </div>
        </div>
    );
}
