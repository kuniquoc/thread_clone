import { api } from '@/services/api';

export interface Comment {
    id: number;
    content: string;
    authorId: number;
    authorUsername: string;
    postId: number;
    createdAt: string;
    updatedAt: string;
    isModerated: boolean;
    isNegative: boolean;
    moderationSeverity: 'low' | 'medium' | 'high' | null;
    moderationReason: string | null;
    isHidden: boolean;
    likeCount: number;
}

export interface CreateCommentData {
    content: string;
    postId: number;
}

export interface UpdateCommentData {
    content: string;
}

export const commentsApi = {
    async getPostComments(postId: number, page = 1, limit = 10): Promise<Comment[]> {
        const { data } = await api.get<Comment[]>(`/api/posts/${postId}/comments`, {
            params: { page, limit },
        });
        return data;
    },

    async createComment(commentData: CreateCommentData): Promise<Comment> {
        const { data } = await api.post<Comment>('/api/comments', commentData);
        return data;
    },

    async updateComment(commentId: number, commentData: UpdateCommentData): Promise<Comment> {
        const { data } = await api.put<Comment>(`/api/comments/${commentId}`, commentData);
        return data;
    },

    async deleteComment(commentId: number): Promise<void> {
        await api.delete(`/api/comments/${commentId}`);
    },

    async likeComment(commentId: number): Promise<void> {
        await api.post(`/api/comments/${commentId}/like`);
    },
}; 