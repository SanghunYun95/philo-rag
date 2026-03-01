import { Settings, History, User } from "lucide-react";
import { ActivePhilosophers } from "./ActivePhilosophers";
import { ContextSources } from "./ContextSources";
import { Message } from "../../types/chat";

interface SidebarProps {
    messages?: Message[];
}

export function Sidebar({ messages = [] }: SidebarProps) {
    const aiMessages = messages.filter(m => m.role === "ai" && m.metadata && m.metadata.length > 0);
    const currentMetadata = aiMessages.length > 0 ? aiMessages[aiMessages.length - 1].metadata! : [];

    return (
        <aside className="w-[30%] min-w-[320px] max-w-[400px] h-full border-r border-white/5 bg-[#1a1a1e] flex flex-col relative z-20 shadow-xl">
            {/* Header */}
            <div className="p-6 border-b border-white/5 flex items-center gap-4">
                <div className="h-10 w-10 shrink-0 rounded-full bg-gradient-to-br from-[#d9b74a] to-amber-700 flex items-center justify-center text-[#0f0f11] font-display font-bold text-xl">
                    P
                </div>
                <div className="flex-1 min-w-0">
                    <h1 className="font-display text-2xl font-medium tracking-tight text-white truncate">PhiloRAG</h1>
                    <p className="text-[10px] text-white/40 uppercase tracking-widest mt-0.5 truncate">철학적 담론</p>
                </div>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8">
                <ActivePhilosophers metadata={currentMetadata} onPhilosopherClick={(scholar) => console.log('Philosopher clicked:', scholar)} />
                <ContextSources metadata={currentMetadata} />
            </div>

            {/* System Status */}
            <div className="mt-auto pt-6 border-t border-white/5">
                <div className="flex items-center justify-between text-xs text-white/40 px-6 pb-2">
                    <span>모델: Philo-GPT-4</span>
                    <div className="flex items-center gap-2">
                        <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
                        <span className="text-emerald-500/80">정상 작동중</span>
                    </div>
                </div>
            </div>

            {/* Bottom Controls */}
            <div className="p-4 border-t border-white/5 bg-black/20">
                <div className="flex items-center justify-around">
                    <button type="button" aria-label="설정" aria-disabled="true" disabled tabIndex={-1} className="p-2 rounded-lg text-white/20 cursor-not-allowed transition-colors focus-visible:outline-none" title="설정 (준비 중)">
                        <Settings className="w-5 h-5" />
                    </button>
                    <button type="button" aria-label="대화 기록" aria-disabled="true" disabled tabIndex={-1} className="p-2 rounded-lg text-white/20 cursor-not-allowed transition-colors focus-visible:outline-none" title="대화 기록 (준비 중)">
                        <History className="w-5 h-5" />
                    </button>
                    <button type="button" aria-label="프로필" aria-disabled="true" disabled tabIndex={-1} className="p-2 rounded-lg text-white/20 cursor-not-allowed transition-colors focus-visible:outline-none" title="프로필 (준비 중)">
                        <User className="w-5 h-5" />
                    </button>
                </div>
            </div>
        </aside>
    );
}
