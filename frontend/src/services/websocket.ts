import { create } from 'zustand';
import { useAuth } from '@/hooks/useAuth';
import { useEffect } from 'react';

interface WebSocketMessage {
    type: 'post_created' | 'post_updated' | 'post_deleted' | 'comment_created' | 'comment_updated' | 'comment_deleted' | 'post_liked' | 'comment_liked';
    data: any;
}

interface WebSocketStore {
    socket: WebSocket | null;
    isConnected: boolean;
    connect: () => void;
    disconnect: () => void;
    subscribe: (callback: (message: WebSocketMessage) => void) => () => void;
}

export const useWebSocket = create<WebSocketStore>((set, get) => ({
    socket: null,
    isConnected: false,
    connect: () => {
        const { token } = useAuth.getState();
        if (!token) return;

        const wsUrl = `${import.meta.env.VITE_WS_URL}/ws?token=${token}`;
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            set({ socket, isConnected: true });
            console.log('WebSocket connected');
        };

        socket.onclose = () => {
            set({ socket: null, isConnected: false });
            console.log('WebSocket disconnected');
            // Attempt to reconnect after 5 seconds
            setTimeout(() => get().connect(), 5000);
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            socket.close();
        };
    },
    disconnect: () => {
        const { socket } = get();
        if (socket) {
            socket.close();
            set({ socket: null, isConnected: false });
        }
    },
    subscribe: (callback) => {
        const { socket } = get();
        if (!socket) return () => { };

        const handleMessage = (event: MessageEvent) => {
            try {
                const message: WebSocketMessage = JSON.parse(event.data);
                callback(message);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        socket.addEventListener('message', handleMessage);
        return () => socket.removeEventListener('message', handleMessage);
    },
}));

// React hook for WebSocket subscriptions
export const useWebSocketSubscription = (callback: (message: WebSocketMessage) => void) => {
    const { connect, subscribe, isConnected } = useWebSocket();

    useEffect(() => {
        if (!isConnected) {
            connect();
        }
        return subscribe(callback);
    }, [callback, connect, subscribe, isConnected]);

    return isConnected;
}; 