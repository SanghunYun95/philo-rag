import "./globals.css";

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&family=Noto+Sans+KR:wght@100..900&display=swap" rel="stylesheet" />
            </head>
            <body
                className="bg-[#0f0f11] min-h-screen text-slate-100 font-sans antialiased"
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
