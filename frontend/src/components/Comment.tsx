import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';

interface CommentProps {
    id: number;
    content: string;
    authorUsername: string;
    createdAt: string;
    isNegative: boolean;
    moderationSeverity: 'low' | 'medium' | 'high' | null;
    isHidden: boolean;
    likeCount: number;
    onLike: () => void;
    onDelete: () => void;
}

const Comment: React.FC<CommentProps> = ({
    content,
    authorUsername,
    createdAt,
    isNegative,
    moderationSeverity,
    isHidden,
    likeCount,
    onLike,
    onDelete,
}) => {
    const [showContent, setShowContent] = useState(!isHidden);

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
                return 'This comment may contain inappropriate content';
            case 'medium':
                return 'This comment contains potentially offensive content';
            case 'high':
                return 'This comment has been hidden due to violation of community guidelines';
            default:
                return null;
        }
    };

    return (
        <div className="bg-gray-50 rounded-lg p-4 mb-2">
            {/* Author and timestamp */}
            <div className="flex items-center justify-between mb-2">
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
                <div className={`border-l-4 p-3 mb-2 ${getWarningClass()}`}>
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path
                                    fillRule="evenodd"
                                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                                    clipRule="evenodd"
                                />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <p className="text-sm">{getWarningMessage()}</p>
                            {isHidden && !showContent && (
                                <button
                                    onClick={() => setShowContent(true)}
                                    className="mt-1 text-sm font-medium underline"
                                >
                                    Show content anyway
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Comment content */}
            {(!isHidden || showContent) && (
                <div className="text-gray-900 mb-2">{content}</div>
            )}

            {/* Actions */}
            <div className="flex items-center space-x-4 text-sm text-gray-500">
                <button
                    onClick={onLike}
                    className="flex items-center space-x-1 hover:text-blue-600"
                >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                        />
                    </svg>
                    <span>{likeCount}</span>
                </button>
                <button
                    onClick={onDelete}
                    className="flex items-center space-x-1 hover:text-red-600"
                >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                        />
                    </svg>
                    <span>Delete</span>
                </button>
            </div>
        </div>
    );
};

export default Comment; 