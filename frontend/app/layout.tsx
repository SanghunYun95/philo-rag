import type { Metadata } from "next";
import { Inter, Newsreader, Noto_Sans_KR } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });
const newsreader = Newsreader({ subsets: ["latin"], variable: "--font-newsreader", display: "swap", style: ['normal', 'italic'] });
const notoSansKr = Noto_Sans_KR({ subsets: ["latin"], weight: ["100", "400", "700", "900"], variable: "--font-noto-sans-kr", display: "swap" });

export const metadata: Metadata = {
    title: "PhiloRAG",
    description: "PhiloRAG - 철학 대화형 RAG 인터페이스",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="ko" className="dark">
            <body
                className={`${inter.variable} ${newsreader.variable} ${notoSansKr.variable} bg-[#0f0f11] min-h-screen text-slate-100 font-sans antialiased`}
                style={{
                    backgroundColor: "#0f0f11",
                    color: "#f8f7f6"
                }}
            >
                {children}
            </body>
        </html>
    );
}
