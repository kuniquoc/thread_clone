import { api } from '@/services/api';

export interface AnalyticsData {
    date: string;
    totalPosts: number;
    totalComments: number;
    moderatedContent: number;
}

export const adminApi = {
    async getAnalytics(): Promise<AnalyticsData[]> {
        const { data } = await api.get<AnalyticsData[]>('/api/admin/analytics');
        return data;
    },

    async getModerationStats() {
        const { data } = await api.get('/api/admin/moderation-stats');
        return data;
    },

    async getSystemHealth() {
        const { data } = await api.get('/api/admin/health');
        return data;
    }
}; 