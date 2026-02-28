import { Share, Plus } from "lucide-react";
import { MessageList } from "./MessageList";
import { FloatingInput } from "./FloatingInput";

export function ChatMain() {
    return (
        <main className="flex-1 flex flex-col relative min-h-0 bg-[#0f0f11] overflow-hidden">
            {/* Top Navigation / Context Header */}
            <div className="flex-none p-6 flex justify-between items-start bg-[#0f0f11] border-b border-white/5 z-30">
                <div>
                    <h2 className="font-display text-3xl text-white/90">Dialogue on Virtue</h2>
                    <p className="text-sm text-white/40 mt-1">Session started today at 10:42 AM</p>
                </div>
                <div className="flex gap-2">
                    <button className="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-white/60 text-sm hover:bg-white/10 hover:text-white transition-colors flex items-center gap-2">
                        <Share className="w-4 h-4" />
                        Export
                    </button>
                    <button className="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-white/60 text-sm hover:bg-white/10 hover:text-white transition-colors flex items-center gap-2">
                        <Plus className="w-4 h-4" />
                        New Chat
                    </button>
                </div>
            </div>

            {/* Scrollable Message Area */}
            <div className="flex-1 overflow-y-auto w-full relative">
                <MessageList />
            </div>

            {/* Bottom Input Area Container */}
            <div className="flex-none w-full bg-[#0f0f11] border-t border-white/5 p-4 z-30">
                <FloatingInput />
            </div>
        </main>
    );
}
