import { api } from '@/services/api';
import type { Post } from '@/types';

export interface CreatePostData {
    content: string;
}

export interface UpdatePostData {
    content: string;
}

export const postsApi = {
    async getPosts(page = 1, limit = 10): Promise<Post[]> {
        const { data } = await api.get<Post[]>('/api/v1/posts', {
            params: { skip: (page - 1) * limit, limit },
        });
        return data;
    },

    async getUserPosts(userId: string, page = 1, limit = 10): Promise<Post[]> {
        const { data } = await api.get<Post[]>(`/api/v1/users/${userId}/posts`, {
            params: { skip: (page - 1) * limit, limit },
        });
        return data;
    },

    async getPost(postId: number): Promise<Post> {
        const { data } = await api.get<Post>(`/api/v1/posts/${postId}`);
        return data;
    },

    async createPost(postData: CreatePostData): Promise<Post> {
        const { data } = await api.post<Post>('/api/v1/posts', postData);
        return data;
    },

    async updatePost(postId: number, postData: UpdatePostData): Promise<Post> {
        const { data } = await api.put<Post>(`/api/v1/posts/${postId}`, postData);
        return data;
    },

    async deletePost(postId: number): Promise<void> {
        await api.delete(`/api/v1/posts/${postId}`);
    },

    async likePost(postId: number): Promise<void> {
        await api.post(`/api/v1/posts/${postId}/like`);
    },
}; 