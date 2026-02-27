import { Sidebar } from "../components/sidebar/Sidebar";
import { ChatMain } from "../components/chat/ChatMain";

export default function Home() {
    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar />
            <ChatMain />
        </div>
    );
}
