import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface ContentModerationResponse {
    is_negative: boolean;
    severity?: 'low' | 'medium' | 'high';
    reason?: string;
}

const CreatePost = () => {
    const navigate = useNavigate();
    const [content, setContent] = useState('');
    const [error, setError] = useState('');
    const [moderationWarning, setModerationWarning] = useState<ContentModerationResponse | null>(null);

    const createPostMutation = useMutation({
        mutationFn: async (content: string) => {
            const response = await axios.post('/posts', { content });
            return response.data;
        },
        onSuccess: () => {
            navigate('/');
        },
        onError: (error: any) => {
            setError(error.response?.data?.detail || 'Failed to create post');
        },
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setModerationWarning(null);

        if (!content.trim()) {
            setError('Post content cannot be empty');
            return;
        }

        try {
            await createPostMutation.mutateAsync(content);
        } catch (err) {
            // Error is handled in mutation callbacks
        }
    };

    const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newContent = e.target.value;
        setContent(newContent);
        setModerationWarning(null);
    };

    const renderModerationWarning = () => {
        if (!moderationWarning?.is_negative) return null;

        const warningClasses = {
            low: 'bg-yellow-50 text-yellow-700 border-yellow-200',
            medium: 'bg-orange-50 text-orange-700 border-orange-200',
            high: 'bg-red-50 text-red-700 border-red-200',
        }[moderationWarning.severity || 'low'];

        return (
            <div className={`p-3 mb-4 rounded-md border ${warningClasses}`}>
                <p className="text-sm">
                    ⚠️ Content Warning: {moderationWarning.reason || 'This content may be inappropriate'}
                </p>
            </div>
        );
    };

    return (
        <div className="max-w-2xl mx-auto py-8 px-4">
            <h1 className="text-2xl font-bold mb-6">Create New Post</h1>

            <form onSubmit={handleSubmit} className="space-y-6">
                {error && (
                    <div className="rounded-md bg-red-50 p-4">
                        <p className="text-sm text-red-700">{error}</p>
                    </div>
                )}

                {renderModerationWarning()}

                <div>
                    <label
                        htmlFor="content"
                        className="block text-sm font-medium text-gray-700 mb-2"
                    >
                        What's on your mind?
                    </label>
                    <textarea
                        id="content"
                        rows={4}
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                        value={content}
                        onChange={handleContentChange}
                        maxLength={5000}
                        placeholder="Share your thoughts..."
                    />
                    <p className="mt-2 text-sm text-gray-500">
                        {content.length}/5000 characters
                    </p>
                </div>

                <div className="flex justify-end space-x-4">
                    <button
                        type="button"
                        onClick={() => navigate('/')}
                        className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={createPostMutation.isPending}
                        className="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                        {createPostMutation.isPending ? 'Creating...' : 'Create Post'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default CreatePost; 