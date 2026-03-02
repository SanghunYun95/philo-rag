export interface BookInfo {
    title: string;
    cover_url: string;
    link: string;
}

export interface DocumentMetadata {
    id: string;
    school: string;
    scholar: string;
    book_info: BookInfo;
    chunk_index: number;
    kr_title?: string;
    thumbnail?: string;
    link?: string;
}

export interface Message {
    id: string;
    role: "user" | "ai";
    content: string;
    timestamp: string;
    isStreaming?: boolean;
    metadata?: DocumentMetadata[];
}
