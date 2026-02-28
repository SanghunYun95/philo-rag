import { Settings, History, User } from "lucide-react";
import { ActivePhilosophers } from "./ActivePhilosophers";
import { ContextSources } from "./ContextSources";

export function Sidebar() {
    return (
        <aside className="w-[30%] min-w-[320px] max-w-[400px] h-full border-r border-white/5 bg-[#1a1a1e] flex flex-col relative z-20 shadow-xl">
            {/* Header */}
            <div className="p-6 border-b border-white/5 flex items-center gap-4">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-[#d9b74a] to-amber-700 flex items-center justify-center text-[#0f0f11] font-display font-bold text-xl">
                    P
                </div>
                <div>
                    <h1 className="font-display text-2xl font-medium tracking-tight text-white">PhiloRAG</h1>
                    <p className="text-xs text-white/40 uppercase tracking-widest mt-0.5">Philosophical Discourse</p>
                </div>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8">
                <ActivePhilosophers />
                <ContextSources />
            </div>

            {/* System Status */}
            <div className="mt-auto pt-6 border-t border-white/5">
                <div className="flex items-center justify-between text-xs text-white/40 px-6 pb-2">
                    <span>Model: Philo-GPT-4</span>
                    <div className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
                        <span className="text-emerald-500/80">Operational</span>
                    </div>
                </div>
            </div>

            {/* Bottom Controls */}
            <div className="p-4 border-t border-white/5 bg-black/20">
                <div className="flex items-center justify-around">
                    <button className="p-2 rounded-lg text-white/40 hover:text-white hover:bg-white/5 transition-colors" title="Settings">
                        <Settings className="w-5 h-5" />
                    </button>
                    <button className="p-2 rounded-lg text-white/40 hover:text-white hover:bg-white/5 transition-colors" title="History">
                        <History className="w-5 h-5" />
                    </button>
                    <button className="p-2 rounded-lg text-white/40 hover:text-white hover:bg-white/5 transition-colors" title="Profile">
                        <User className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </aside>
    );
}
