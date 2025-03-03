import React, { useState } from 'react';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

interface PostProps {
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
    onLike: () => void;
}

const Post: React.FC<PostProps> = ({
    id,
    content,
    authorId,
    authorUsername,
    createdAt,
    isNegative,
    moderationSeverity,
    isHidden,
    likeCount,
    commentCount,
    onLike,
}) => {
    const { user } = useAuth();
    const [showContent, setShowContent] = useState(!isHidden);
    const isAuthor = user?.id === authorId;

    const getWarningClass = () => {
        switch (moderationSeverity) {
            case 'low':
                return 'bg-yellow-50 border-yellow-400 text-yellow-800';
            case 'medium':
                return 'bg-orange-50 border-orange-400 text-orange-800';
            case 'high':
                return 'bg-red-50 border-red-400 text-red-800';
            default:
                return '';
        }
    };

    const getWarningMessage = () => {
        if (!isNegative) return null;
        switch (moderationSeverity) {
            case 'low':
                return 'This post may contain inappropriate content';
            case 'medium':
                return 'This post contains potentially offensive content';
            case 'high':
                return 'This post has been hidden due to violation of community guidelines';
            default:
                return null;
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
            {/* Author and timestamp */}
            <div className="flex items-center justify-between mb-3">
                <Link
                    to={`/profile/${authorUsername}`}
                    className="flex items-center space-x-2"
                >
                    <div className="font-medium text-gray-900">{authorUsername}</div>
                </Link>
                <div className="text-sm text-gray-500">
                    {format(new Date(createdAt), 'MMM d, yyyy')}
                </div>
            </div>

            {/* Content warning */}
            {isNegative && (
                <div className={`border-l-4 p-4 mb-4 ${getWarningClass()}`}>
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <p className="text-sm">{getWarningMessage()}</p>
                            {isHidden && !showContent && (
                                <button
                                    onClick={() => setShowContent(true)}
                                    className="mt-2 text-sm font-medium underline"
                                >
                                    Show content anyway
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Post content */}
            {(!isHidden || showContent || isAuthor) && (
                <div className="mb-4">
                    <p className="text-gray-900">{content}</p>
                </div>
            )}

            {/* Actions */}
            <div className="flex items-center space-x-4 text-sm text-gray-500">
                <button
                    onClick={onLike}
                    className="flex items-center space-x-1 hover:text-blue-600"
                >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    <span>{likeCount}</span>
                </button>
                <Link
                    to={`/post/${id}`}
                    className="flex items-center space-x-1 hover:text-blue-600"
                >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                    <span>{commentCount}</span>
                </Link>
            </div>
        </div>
    );
};

export default Post; 