export interface User {
    id: number;
    username: string;
    email: string;
}

export interface Post {
    id: number;
    content: string;
    authorId: number;
    authorUsername: string;
    createdAt: string;
    updatedAt: string;
    isNegative: boolean;
    moderationSeverity: 'low' | 'medium' | 'high' | null;
    isHidden: boolean;
    likeCount: number;
    commentCount: number;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    fullName: string;
}

export interface LoginData {
    email: string;
    password: string;
} 