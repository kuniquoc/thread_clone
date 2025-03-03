import { api } from '@/services/api';

export interface Notification {
    id: number;
    type: 'like' | 'comment' | 'follow' | 'mention' | 'moderation';
    message: string;
    isRead: boolean;
    createdAt: string;
    relatedUserId?: number;
    relatedPostId?: number;
    relatedCommentId?: number;
}

export const notificationsApi = {
    async getNotifications(page = 1, limit = 20): Promise<Notification[]> {
        const { data } = await api.get<Notification[]>('/api/notifications', {
            params: { page, limit },
        });
        return data;
    },

    async markAsRead(notificationId: number): Promise<void> {
        await api.put(`/api/notifications/${notificationId}/read`);
    },

    async markAllAsRead(): Promise<void> {
        await api.put('/api/notifications/read-all');
    },

    async deleteNotification(notificationId: number): Promise<void> {
        await api.delete(`/api/notifications/${notificationId}`);
    },
}; 