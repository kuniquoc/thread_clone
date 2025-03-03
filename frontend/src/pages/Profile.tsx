import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { postsApi } from '@/services/posts';
import Post from '@/components/Post';
import type { Post as PostType } from '@/types';

const Profile: React.FC = () => {
    const { user } = useAuth();
    const [posts, setPosts] = useState<PostType[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUserPosts = async () => {
            try {
                if (user) {
                    const userPosts = await postsApi.getUserPosts(user.id.toString());
                    setPosts(userPosts);
                }
            } catch (err) {
                setError('Failed to load posts');
            } finally {
                setLoading(false);
            }
        };

        fetchUserPosts();
    }, [user]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-8">
                <p className="text-red-500">{error}</p>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto p-4">
            <div className="bg-white shadow rounded-lg p-6 mb-8">
                <div className="flex items-center space-x-4">
                    <div className="h-16 w-16 rounded-full bg-gray-200 flex items-center justify-center">
                        <span className="text-2xl text-gray-600">
                            {user?.username.charAt(0).toUpperCase()}
                        </span>
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold">{user?.username}</h1>
                        <p className="text-gray-600">{user?.email}</p>
                    </div>
                </div>
            </div>

            <div className="space-y-4">
                <h2 className="text-xl font-semibold mb-4">Your Posts</h2>
                {posts.length === 0 ? (
                    <p className="text-center text-gray-500 py-8">No posts yet</p>
                ) : (
                    posts.map((post) => (
                        <Post
                            key={post.id}
                            id={post.id}
                            content={post.content}
                            authorId={post.authorId}
                            authorUsername={post.authorUsername}
                            createdAt={post.createdAt}
                            updatedAt={post.updatedAt}
                            isNegative={post.isNegative}
                            moderationSeverity={post.moderationSeverity}
                            isHidden={post.isHidden}
                            likeCount={post.likeCount}
                            commentCount={post.commentCount}
                            onLike={async () => {
                                try {
                                    await postsApi.likePost(post.id);
                                    setPosts(posts.map(p =>
                                        p.id === post.id
                                            ? { ...p, likeCount: p.likeCount + 1 }
                                            : p
                                    ));
                                } catch (err) {
                                    setError('Failed to like post');
                                }
                            }}
                        />
                    ))
                )}
            </div>
        </div>
    );
};

export default Profile; 