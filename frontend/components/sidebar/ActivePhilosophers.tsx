import { BrainCircuit, CheckCircle, Circle } from "lucide-react";

export function ActivePhilosophers() {
    return (
        <div>
            <h3 className="text-xs font-medium text-primary uppercase tracking-widest mb-4 flex items-center gap-2">
                <BrainCircuit className="w-4 h-4" />
                Active Philosophers
            </h3>
            <div className="space-y-3">
                {/* Card: Socrates */}
                <div className="group relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-4 hover:border-primary/50 transition-all duration-300 cursor-pointer">
                    <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative flex items-center gap-4">
                        <div
                            className="h-12 w-12 rounded-full bg-cover bg-center border border-white/10"
                            title="Classic marble bust of Socrates"
                            style={{
                                backgroundImage:
                                    "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBXK4XMP9l5KyHJ9syIoaqwwL3r7nVaNTaEzWXOniPvvE-822RA1SPpn4EGrYAzGPwG1KR3gmL8acZu3MEl-tyfavsKe6YiqGismcCqgYPz7LvX3mZiM0XP1P_hp9oTTliEOfns01tel4TnFlCEZNFleoSewQPUF0NKxynepVE1pasMwTCQlklrYw9fpWp4jGx-PJJllagqIwf9AAhJmOJTc6TYkrqSl_sqemG308t2wggfKqLK-eJG8YEZ2_cSFC7wVLTLxeNucek')",
                            }}
                        ></div>
                        <div>
                            <h4 className="font-display text-lg text-white">Socrates</h4>
                            <p className="text-xs text-white/50">Socratic Method, Ethics</p>
                        </div>
                        <CheckCircle className="ml-auto text-primary/50 group-hover:text-primary w-5 h-5" />
                    </div>
                </div>

                {/* Card: Nietzsche */}
                <div className="group relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-4 hover:border-primary/50 transition-all duration-300 cursor-pointer">
                    <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative flex items-center gap-4">
                        <div
                            className="h-12 w-12 rounded-full bg-cover bg-center border border-white/10"
                            title="Portrait painting of Friedrich Nietzsche"
                            style={{
                                backgroundImage:
                                    "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDErNgOWlAkVq6mRofu82tAsDD6uo_nA0PoHWBXQRzurO3DQn7HrKB4XTuPCO6H6_vRK3gCUIA-bdDQNh21vf2nQwgHW39ceCk7mkv8UZRMs4LMLnlaxScn9-sk99ie97owvAdVOyKfB3wMTLH2svh77GvE3_6_3bSfVzwg9Y3IOe0XEiYdgi_d-AdDCictbZxsV3fydwD-4GYdmKF-sE3uTYsZillX2ZOF1LE0zQFViZh2fqXMQdOj9lJXqRL7QHYatHg7PI5maTw')",
                            }}
                        ></div>
                        <div>
                            <h4 className="font-display text-lg text-white">Nietzsche</h4>
                            <p className="text-xs text-white/50">Existentialism, Will to Power</p>
                        </div>
                        <Circle className="ml-auto text-white/20 group-hover:text-white/40 w-5 h-5" />
                    </div>
                </div>
            </div>
        </div>
    );
}
