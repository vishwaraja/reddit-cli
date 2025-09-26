#!/usr/bin/env python3
"""
Reddit CLI Tool
A command-line interface for posting to Reddit subreddits and retrieving responses.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

import praw
from praw.models import Submission, Comment
from praw.exceptions import RedditAPIException, ClientException


class RedditCLI:
    def __init__(self, config_file: str = "reddit_config.json"):
        """Initialize the Reddit CLI with configuration."""
        self.config_file = config_file
        self.reddit = None
        self.load_config()
    
    def load_config(self):
        """Load Reddit API configuration from file."""
        if not os.path.exists(self.config_file):
            self.create_config_template()
            print(f"Configuration template created at {self.config_file}")
            print("Please fill in your Reddit API credentials and run again.")
            sys.exit(1)
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self.reddit = praw.Reddit(
                client_id=config['client_id'],
                client_secret=config['client_secret'],
                user_agent=config.get('user_agent', 'RedditCLI/1.0'),
                username=config['username'],
                password=config['password']
            )
            
            # Add initial delay to avoid rate limiting
            print("⏳ Waiting 10 seconds to avoid rate limiting...")
            time.sleep(10)
            
            # Test the connection with rate limiting
            self._test_connection_with_retry()
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)
    
    def _test_connection_with_retry(self, max_retries=3, delay=5):
        """Test Reddit connection with retry logic and rate limiting."""
        for attempt in range(max_retries):
            try:
                # Test the connection
                user = self.reddit.user.me()
                print(f"✅ Connected to Reddit as: {user}")
                return True
                
            except RedditAPIException as e:
                if "RATE_LIMIT" in str(e) or "429" in str(e):
                    print(f"⏳ Rate limited. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}...")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                        continue
                    else:
                        print("❌ Rate limit exceeded. Please wait before trying again.")
                        sys.exit(1)
                else:
                    print(f"❌ Reddit API error: {e}")
                    sys.exit(1)
                    
            except ClientException as e:
                if "401" in str(e) or "unauthorized" in str(e).lower():
                    print(f"❌ Authentication failed: {e}")
                    print("💡 Please check your credentials in reddit_config.json")
                    sys.exit(1)
                else:
                    print(f"❌ Client error: {e}")
                    sys.exit(1)
                    
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    sys.exit(1)
        
        return False
    
    def _execute_with_retry(self, func, *args, max_retries=3, delay=5, **kwargs):
        """Execute a function with retry logic and rate limiting."""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
                
            except RedditAPIException as e:
                if "RATE_LIMIT" in str(e) or "429" in str(e):
                    print(f"⏳ Rate limited. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}...")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                        continue
                    else:
                        print("❌ Rate limit exceeded. Please wait before trying again.")
                        return None
                else:
                    print(f"❌ Reddit API error: {e}")
                    return None
                    
            except ClientException as e:
                if "401" in str(e) or "unauthorized" in str(e).lower():
                    print(f"❌ Authentication failed: {e}")
                    return None
                else:
                    print(f"❌ Client error: {e}")
                    return None
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    return None
        
        return None
    
    def create_config_template(self):
        """Create a configuration template file."""
        template = {
            "client_id": "your_client_id_here",
            "client_secret": "your_client_secret_here",
            "username": "your_reddit_username",
            "password": "your_reddit_password",
            "user_agent": "RedditCLI/1.0 by your_username"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(template, f, indent=2)
    
    def post_to_subreddit(self, subreddit_name: str, title: str, 
                         content: str = None, url: str = None, 
                         flair_id: str = None) -> Optional[Submission]:
        """Post to a subreddit with rate limiting."""
        return self._execute_with_retry(
            self._post_to_subreddit_impl,
            subreddit_name, title, content, url, flair_id
        )
    
    def _post_to_subreddit_impl(self, subreddit_name: str, title: str, 
                               content: str = None, url: str = None, 
                               flair_id: str = None) -> Optional[Submission]:
        """Internal implementation of posting to subreddit."""
        subreddit = self.reddit.subreddit(subreddit_name)
        
        if url:
            # Link post
            submission = subreddit.submit(
                title=title,
                url=url,
                flair_id=flair_id
            )
        else:
            # Text post
            submission = subreddit.submit(
                title=title,
                selftext=content or "",
                flair_id=flair_id
            )
        
        print(f"✅ Successfully posted to r/{subreddit_name}")
        print(f"📝 Title: {title}")
        print(f"🔗 URL: https://reddit.com{submission.permalink}")
        
        return submission
    
    def get_subreddit_flairs(self, subreddit_name: str) -> List[Dict]:
        """Get available flairs for a subreddit with rate limiting."""
        return self._execute_with_retry(
            self._get_subreddit_flairs_impl,
            subreddit_name
        ) or []
    
    def _get_subreddit_flairs_impl(self, subreddit_name: str) -> List[Dict]:
        """Internal implementation of getting subreddit flairs."""
        subreddit = self.reddit.subreddit(subreddit_name)
        flairs = []
        
        for flair in subreddit.flair.link_templates:
            flairs.append({
                'id': flair['id'],
                'text': flair['text'],
                'css_class': flair.get('css_class', '')
            })
        
        return flairs
    
    def _add_delay(self, seconds=2):
        """Add a delay to prevent rate limiting."""
        print(f"⏳ Waiting {seconds} seconds to avoid rate limiting...")
        time.sleep(seconds)
    
    def get_post_responses(self, submission: Submission, limit: int = 10) -> List[Dict]:
        """Get responses (comments) for a post."""
        try:
            responses = []
            submission.comments.replace_more(limit=0)
            
            for comment in submission.comments[:limit]:
                responses.append({
                    'author': str(comment.author) if comment.author else '[deleted]',
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'permalink': f"https://reddit.com{comment.permalink}"
                })
            
            return responses
            
        except Exception as e:
            print(f"❌ Error getting responses: {e}")
            return []
    
    def get_post_by_url(self, post_url: str) -> Optional[Submission]:
        """Get a Reddit post by its URL."""
        try:
            submission = self.reddit.submission(url=post_url)
            return submission
        except Exception as e:
            print(f"❌ Error getting post from URL: {e}")
            return None
    
    def delete_post(self, post_url: str) -> bool:
        """Delete a Reddit post by its URL."""
        return self._execute_with_retry(
            self._delete_post_impl,
            post_url
        ) or False
    
    def _delete_post_impl(self, post_url: str) -> bool:
        """Internal implementation of deleting a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            
            # Check if the post belongs to the current user
            if submission.author != self.reddit.user.me():
                print(f"❌ You can only delete your own posts")
                return False
            
            # Delete the post
            submission.delete()
            print(f"✅ Successfully deleted post: {submission.title}")
            print(f"🔗 URL: {post_url}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting post: {e}")
            return False
    
    def comment_on_post(self, post_url: str, comment_text: str) -> Optional[Comment]:
        """Comment on a Reddit post with rate limiting."""
        return self._execute_with_retry(
            self._comment_on_post_impl,
            post_url, comment_text
        )
    
    def _comment_on_post_impl(self, post_url: str, comment_text: str) -> Optional[Comment]:
        """Internal implementation of commenting on a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            comment = submission.reply(comment_text)
            
            print(f"✅ Successfully commented on post: {submission.title}")
            print(f"💭 Comment: {comment_text[:100]}...")
            print(f"🔗 Comment URL: https://reddit.com{comment.permalink}")
            
            return comment
            
        except Exception as e:
            print(f"❌ Error commenting on post: {e}")
            return None
    
    def reply_to_comment(self, comment_url: str, reply_text: str) -> Optional[Comment]:
        """Reply to a Reddit comment with rate limiting."""
        return self._execute_with_retry(
            self._reply_to_comment_impl,
            comment_url, reply_text
        )
    
    def _reply_to_comment_impl(self, comment_url: str, reply_text: str) -> Optional[Comment]:
        """Internal implementation of replying to a comment."""
        try:
            # Extract comment ID from URL
            comment_id = comment_url.split('/')[-1]
            comment = self.reddit.comment(id=comment_id)
            reply = comment.reply(reply_text)
            
            print(f"✅ Successfully replied to comment")
            print(f"💭 Reply: {reply_text[:100]}...")
            print(f"🔗 Reply URL: https://reddit.com{reply.permalink}")
            
            return reply
            
        except Exception as e:
            print(f"❌ Error replying to comment: {e}")
            return None
    
    def get_hot_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict]:
        """Get hot posts from a subreddit for commenting opportunities."""
        return self._execute_with_retry(
            self._get_hot_posts_impl,
            subreddit_name, limit
        ) or []
    
    def _get_hot_posts_impl(self, subreddit_name: str, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting hot posts."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for submission in subreddit.hot(limit=limit):
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'created_utc': datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'author': str(submission.author) if submission.author else '[deleted]'
                })
            
            return posts
            
        except Exception as e:
            print(f"❌ Error getting hot posts: {e}")
            return []
    
    def search_subreddits(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for subreddits by keywords."""
        return self._execute_with_retry(
            self._search_subreddits_impl,
            query, limit
        ) or []
    
    def _search_subreddits_impl(self, query: str, limit: int = 10) -> List[Dict]:
        """Internal implementation of searching subreddits."""
        try:
            subreddits = []
            
            for subreddit in self.reddit.subreddits.search(query, limit=limit):
                subreddits.append({
                    'name': subreddit.display_name,
                    'title': subreddit.title,
                    'description': subreddit.description[:200] + "..." if len(subreddit.description) > 200 else subreddit.description,
                    'subscribers': subreddit.subscribers,
                    'active_users': getattr(subreddit, 'active_user_count', 'N/A'),
                    'url': f"https://reddit.com/r/{subreddit.display_name}",
                    'nsfw': subreddit.over18
                })
            
            return subreddits
            
        except Exception as e:
            print(f"❌ Error searching subreddits: {e}")
            return []
    
    def get_subreddit_info(self, subreddit_name: str) -> Optional[Dict]:
        """Get detailed information about a subreddit."""
        return self._execute_with_retry(
            self._get_subreddit_info_impl,
            subreddit_name
        )
    
    def _get_subreddit_info_impl(self, subreddit_name: str) -> Optional[Dict]:
        """Internal implementation of getting subreddit info."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            info = {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.description,
                'public_description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'active_users': getattr(subreddit, 'active_user_count', 'N/A'),
                'created_utc': datetime.fromtimestamp(subreddit.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'url': f"https://reddit.com/r/{subreddit.display_name}",
                'nsfw': subreddit.over18,
                'quarantine': subreddit.quarantine,
                'submission_type': subreddit.submission_type,
                'lang': subreddit.lang
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Error getting subreddit info: {e}")
            return None
    
    def subscribe_to_subreddit(self, subreddit_name: str) -> bool:
        """Subscribe to a subreddit."""
        return self._execute_with_retry(
            self._subscribe_to_subreddit_impl,
            subreddit_name
        ) or False
    
    def _subscribe_to_subreddit_impl(self, subreddit_name: str) -> bool:
        """Internal implementation of subscribing to subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.subscribe()
            print(f"✅ Successfully subscribed to r/{subreddit_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error subscribing to subreddit: {e}")
            return False
    
    def unsubscribe_from_subreddit(self, subreddit_name: str) -> bool:
        """Unsubscribe from a subreddit."""
        return self._execute_with_retry(
            self._unsubscribe_from_subreddit_impl,
            subreddit_name
        ) or False
    
    def _unsubscribe_from_subreddit_impl(self, subreddit_name: str) -> bool:
        """Internal implementation of unsubscribing from subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.unsubscribe()
            print(f"✅ Successfully unsubscribed from r/{subreddit_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error unsubscribing from subreddit: {e}")
            return False
    
    def get_trending_subreddits(self, limit: int = 10) -> List[Dict]:
        """Get trending subreddits."""
        return self._execute_with_retry(
            self._get_trending_subreddits_impl,
            limit
        ) or []
    
    def _get_trending_subreddits_impl(self, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting trending subreddits."""
        try:
            subreddits = []
            
            # Get popular subreddits as a proxy for trending
            for subreddit in self.reddit.subreddits.popular(limit=limit):
                subreddits.append({
                    'name': subreddit.display_name,
                    'title': subreddit.title,
                    'description': subreddit.description[:200] + "..." if len(subreddit.description) > 200 else subreddit.description,
                    'subscribers': subreddit.subscribers,
                    'active_users': getattr(subreddit, 'active_user_count', 'N/A'),
                    'url': f"https://reddit.com/r/{subreddit.display_name}",
                    'nsfw': subreddit.over18
                })
            
            return subreddits
            
        except Exception as e:
            print(f"❌ Error getting trending subreddits: {e}")
            return []
    
    def get_subreddit_moderators(self, subreddit_name: str) -> List[Dict]:
        """Get moderators of a subreddit."""
        return self._execute_with_retry(
            self._get_subreddit_moderators_impl,
            subreddit_name
        ) or []
    
    def _get_subreddit_moderators_impl(self, subreddit_name: str) -> List[Dict]:
        """Internal implementation of getting subreddit moderators."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            moderators = []
            
            for moderator in subreddit.moderator():
                moderators.append({
                    'name': str(moderator),
                    'url': f"https://reddit.com/u/{moderator}"
                })
            
            return moderators
            
        except Exception as e:
            print(f"❌ Error getting subreddit moderators: {e}")
            return []
    
    def upvote_post(self, post_url: str) -> bool:
        """Upvote a Reddit post."""
        return self._execute_with_retry(
            self._upvote_post_impl,
            post_url
        ) or False
    
    def _upvote_post_impl(self, post_url: str) -> bool:
        """Internal implementation of upvoting a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            submission.upvote()
            print(f"✅ Successfully upvoted post: {submission.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error upvoting post: {e}")
            return False
    
    def downvote_post(self, post_url: str) -> bool:
        """Downvote a Reddit post."""
        return self._execute_with_retry(
            self._downvote_post_impl,
            post_url
        ) or False
    
    def _downvote_post_impl(self, post_url: str) -> bool:
        """Internal implementation of downvoting a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            submission.downvote()
            print(f"✅ Successfully downvoted post: {submission.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error downvoting post: {e}")
            return False
    
    def upvote_comment(self, comment_url: str) -> bool:
        """Upvote a Reddit comment."""
        return self._execute_with_retry(
            self._upvote_comment_impl,
            comment_url
        ) or False
    
    def _upvote_comment_impl(self, comment_url: str) -> bool:
        """Internal implementation of upvoting a comment."""
        try:
            comment_id = comment_url.split('/')[-1]
            comment = self.reddit.comment(id=comment_id)
            comment.upvote()
            print(f"✅ Successfully upvoted comment")
            return True
            
        except Exception as e:
            print(f"❌ Error upvoting comment: {e}")
            return False
    
    def downvote_comment(self, comment_url: str) -> bool:
        """Downvote a Reddit comment."""
        return self._execute_with_retry(
            self._downvote_comment_impl,
            comment_url
        ) or False
    
    def _downvote_comment_impl(self, comment_url: str) -> bool:
        """Internal implementation of downvoting a comment."""
        try:
            comment_id = comment_url.split('/')[-1]
            comment = self.reddit.comment(id=comment_id)
            comment.downvote()
            print(f"✅ Successfully downvoted comment")
            return True
            
        except Exception as e:
            print(f"❌ Error downvoting comment: {e}")
            return False
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """Get user profile information."""
        return self._execute_with_retry(
            self._get_user_profile_impl,
            username
        )
    
    def _get_user_profile_impl(self, username: str) -> Optional[Dict]:
        """Internal implementation of getting user profile."""
        try:
            user = self.reddit.redditor(username)
            
            profile = {
                'name': str(user),
                'created_utc': datetime.fromtimestamp(user.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'is_employee': user.is_employee,
                'is_mod': user.is_mod,
                'is_gold': user.is_gold,
                'url': f"https://reddit.com/u/{user}",
                'has_verified_email': getattr(user, 'has_verified_email', False)
            }
            
            return profile
            
        except Exception as e:
            print(f"❌ Error getting user profile: {e}")
            return None
    
    def get_user_posts(self, username: str, limit: int = 10) -> List[Dict]:
        """Get posts by a user."""
        return self._execute_with_retry(
            self._get_user_posts_impl,
            username, limit
        ) or []
    
    def _get_user_posts_impl(self, username: str, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting user posts."""
        try:
            user = self.reddit.redditor(username)
            posts = []
            
            for submission in user.submissions.new(limit=limit):
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'created_utc': datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return posts
            
        except Exception as e:
            print(f"❌ Error getting user posts: {e}")
            return []
    
    def get_user_comments(self, username: str, limit: int = 10) -> List[Dict]:
        """Get comments by a user."""
        return self._execute_with_retry(
            self._get_user_comments_impl,
            username, limit
        ) or []
    
    def _get_user_comments_impl(self, username: str, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting user comments."""
        try:
            user = self.reddit.redditor(username)
            comments = []
            
            for comment in user.comments.new(limit=limit):
                comments.append({
                    'id': comment.id,
                    'body': comment.body[:200] + "..." if len(comment.body) > 200 else comment.body,
                    'subreddit': str(comment.subreddit),
                    'score': comment.score,
                    'url': f"https://reddit.com{comment.permalink}",
                    'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return comments
            
        except Exception as e:
            print(f"❌ Error getting user comments: {e}")
            return []
    
    def save_post(self, post_url: str) -> bool:
        """Save a Reddit post."""
        return self._execute_with_retry(
            self._save_post_impl,
            post_url
        ) or False
    
    def _save_post_impl(self, post_url: str) -> bool:
        """Internal implementation of saving a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            submission.save()
            print(f"✅ Successfully saved post: {submission.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving post: {e}")
            return False
    
    def unsave_post(self, post_url: str) -> bool:
        """Unsave a Reddit post."""
        return self._execute_with_retry(
            self._unsave_post_impl,
            post_url
        ) or False
    
    def _unsave_post_impl(self, post_url: str) -> bool:
        """Internal implementation of unsaving a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            submission.unsave()
            print(f"✅ Successfully unsaved post: {submission.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error unsaving post: {e}")
            return False
    
    def get_saved_posts(self, limit: int = 10) -> List[Dict]:
        """Get user's saved posts."""
        return self._execute_with_retry(
            self._get_saved_posts_impl,
            limit
        ) or []
    
    def _get_saved_posts_impl(self, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting saved posts."""
        try:
            saved_posts = []
            
            for submission in self.reddit.user.me().saved(limit=limit):
                saved_posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'created_utc': datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return saved_posts
            
        except Exception as e:
            print(f"❌ Error getting saved posts: {e}")
            return []
    
    def send_message(self, username: str, subject: str, body: str) -> bool:
        """Send a private message to a user."""
        return self._execute_with_retry(
            self._send_message_impl,
            username, subject, body
        ) or False
    
    def _send_message_impl(self, username: str, subject: str, body: str) -> bool:
        """Internal implementation of sending a message."""
        try:
            self.reddit.redditor(username).message(subject, body)
            print(f"✅ Successfully sent message to u/{username}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def get_inbox(self, limit: int = 10) -> List[Dict]:
        """Get user's inbox messages."""
        return self._execute_with_retry(
            self._get_inbox_impl,
            limit
        ) or []
    
    def _get_inbox_impl(self, limit: int = 10) -> List[Dict]:
        """Internal implementation of getting inbox."""
        try:
            messages = []
            
            for message in self.reddit.inbox.unread(limit=limit):
                messages.append({
                    'id': message.id,
                    'author': str(message.author) if message.author else '[deleted]',
                    'subject': message.subject,
                    'body': message.body[:200] + "..." if len(message.body) > 200 else message.body,
                    'created_utc': datetime.fromtimestamp(message.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f"https://reddit.com/message/messages/{message.id}"
                })
            
            return messages
            
        except Exception as e:
            print(f"❌ Error getting inbox: {e}")
            return []
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """Search for posts across Reddit."""
        return self._execute_with_retry(
            self._search_posts_impl,
            query, subreddit, limit
        ) or []
    
    def _search_posts_impl(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """Internal implementation of searching posts."""
        try:
            posts = []
            
            if subreddit:
                search_target = self.reddit.subreddit(subreddit)
            else:
                search_target = self.reddit.subreddit("all")
            
            for submission in search_target.search(query, limit=limit):
                posts.append({
                    'id': submission.id,
                    'title': submission.title,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'created_utc': datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'author': str(submission.author) if submission.author else '[deleted]'
                })
            
            return posts
            
        except Exception as e:
            print(f"❌ Error searching posts: {e}")
            return []
    
    def search_comments(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """Search for comments across Reddit."""
        return self._execute_with_retry(
            self._search_comments_impl,
            query, subreddit, limit
        ) or []
    
    def _search_comments_impl(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """Internal implementation of searching comments."""
        try:
            comments = []
            
            if subreddit:
                search_target = self.reddit.subreddit(subreddit)
            else:
                search_target = self.reddit.subreddit("all")
            
            for comment in search_target.comments(limit=limit):
                if query.lower() in comment.body.lower():
                    comments.append({
                        'id': comment.id,
                        'body': comment.body[:200] + "..." if len(comment.body) > 200 else comment.body,
                        'subreddit': str(comment.subreddit),
                        'score': comment.score,
                        'url': f"https://reddit.com{comment.permalink}",
                        'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'author': str(comment.author) if comment.author else '[deleted]'
                    })
                    
                    if len(comments) >= limit:
                        break
            
            return comments
            
        except Exception as e:
            print(f"❌ Error searching comments: {e}")
            return []
    
    def edit_post(self, post_url: str, new_content: str) -> bool:
        """Edit a Reddit post."""
        return self._execute_with_retry(
            self._edit_post_impl,
            post_url, new_content
        ) or False
    
    def _edit_post_impl(self, post_url: str, new_content: str) -> bool:
        """Internal implementation of editing a post."""
        try:
            submission = self.reddit.submission(url=post_url)
            
            # Check if the post belongs to the current user
            if submission.author != self.reddit.user.me():
                print(f"❌ You can only edit your own posts")
                return False
            
            submission.edit(new_content)
            print(f"✅ Successfully edited post: {submission.title}")
            return True
            
        except Exception as e:
            print(f"❌ Error editing post: {e}")
            return False
    
    def edit_comment(self, comment_url: str, new_content: str) -> bool:
        """Edit a Reddit comment."""
        return self._execute_with_retry(
            self._edit_comment_impl,
            comment_url, new_content
        ) or False
    
    def _edit_comment_impl(self, comment_url: str, new_content: str) -> bool:
        """Internal implementation of editing a comment."""
        try:
            comment_id = comment_url.split('/')[-1]
            comment = self.reddit.comment(id=comment_id)
            
            # Check if the comment belongs to the current user
            if comment.author != self.reddit.user.me():
                print(f"❌ You can only edit your own comments")
                return False
            
            comment.edit(new_content)
            print(f"✅ Successfully edited comment")
            return True
            
        except Exception as e:
            print(f"❌ Error editing comment: {e}")
            return False
    
    def follow_user(self, username: str) -> bool:
        """Follow a Reddit user."""
        return self._execute_with_retry(
            self._follow_user_impl,
            username
        ) or False
    
    def _follow_user_impl(self, username: str) -> bool:
        """Internal implementation of following a user."""
        try:
            user = self.reddit.redditor(username)
            user.friend()
            print(f"✅ Successfully followed u/{username}")
            return True
            
        except Exception as e:
            print(f"❌ Error following user: {e}")
            return False
    
    def unfollow_user(self, username: str) -> bool:
        """Unfollow a Reddit user."""
        return self._execute_with_retry(
            self._unfollow_user_impl,
            username
        ) or False
    
    def _unfollow_user_impl(self, username: str) -> bool:
        """Internal implementation of unfollowing a user."""
        try:
            user = self.reddit.redditor(username)
            user.unfriend()
            print(f"✅ Successfully unfollowed u/{username}")
            return True
            
        except Exception as e:
            print(f"❌ Error unfollowing user: {e}")
            return False
    
    def get_friends(self) -> List[Dict]:
        """Get user's friends list."""
        return self._execute_with_retry(
            self._get_friends_impl
        ) or []
    
    def _get_friends_impl(self) -> List[Dict]:
        """Internal implementation of getting friends."""
        try:
            friends = []
            
            for friend in self.reddit.user.me().friends():
                friends.append({
                    'name': str(friend),
                    'url': f"https://reddit.com/u/{friend}"
                })
            
            return friends
            
        except Exception as e:
            print(f"❌ Error getting friends: {e}")
            return []
    
    def monitor_post(self, submission: Submission, check_interval: int = 30, 
                    max_checks: int = 10) -> List[Dict]:
        """Monitor a post for new responses."""
        print(f"🔍 Monitoring post: {submission.title}")
        print(f"⏰ Checking every {check_interval} seconds for {max_checks} times")
        
        all_responses = []
        seen_comment_ids = set()
        
        for check in range(max_checks):
            print(f"\n📊 Check {check + 1}/{max_checks}")
            
            # Refresh the submission to get latest comments
            submission.comments.replace_more(limit=0)
            
            new_responses = []
            for comment in submission.comments:
                if comment.id not in seen_comment_ids:
                    seen_comment_ids.add(comment.id)
                    response_data = {
                        'author': str(comment.author) if comment.author else '[deleted]',
                        'body': comment.body,
                        'score': comment.score,
                        'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'permalink': f"https://reddit.com{comment.permalink}"
                    }
                    new_responses.append(response_data)
                    all_responses.append(response_data)
            
            if new_responses:
                print(f"🆕 Found {len(new_responses)} new responses:")
                for response in new_responses:
                    print(f"  👤 {response['author']}: {response['body'][:100]}...")
            else:
                print("📭 No new responses")
            
            if check < max_checks - 1:  # Don't sleep on the last check
                time.sleep(check_interval)
        
        return all_responses


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Reddit CLI - A comprehensive command-line interface for Reddit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 QUICK START EXAMPLES:

📝 Content Management:
  %(prog)s post askreddit "What's your favorite programming language?" --content "I'm curious about what developers prefer and why."
  %(prog)s comment "https://reddit.com/r/askreddit/comments/abc123/post/" "Great question! I think Python is excellent."
  %(prog)s edit-post "https://reddit.com/r/askreddit/comments/abc123/post/" "Updated content"

🔍 Discovery & Search:
  %(prog)s search-subreddits "machine learning" --limit 10
  %(prog)s search-posts "Python tutorial" --subreddit "learnpython" --limit 5
  %(prog)s hot programming --limit 10
  %(prog)s trending --limit 10

👥 User Management:
  %(prog)s user-profile "spez"
  %(prog)s user-posts "username" --limit 10
  %(prog)s follow "username"
  %(prog)s friends

🗳️ Voting & Engagement:
  %(prog)s upvote "https://reddit.com/r/askreddit/comments/abc123/post/"
  %(prog)s downvote "https://reddit.com/r/askreddit/comments/abc123/post/"
  %(prog)s save "https://reddit.com/r/askreddit/comments/abc123/post/"

📬 Messaging:
  %(prog)s message "username" "Subject" "Message body"
  %(prog)s inbox --limit 10

🏷️ Subreddit Management:
  %(prog)s flairs askreddit
  %(prog)s subreddit-info "MachineLearning"
  %(prog)s subscribe "MachineLearning"
  %(prog)s moderators "MachineLearning"

📊 Monitoring:
  %(prog)s responses "https://reddit.com/r/askreddit/comments/abc123/post/" --limit 20
  %(prog)s monitor "https://reddit.com/r/askreddit/comments/abc123/post/" --interval 60

💡 TIP: Use --help with any command for detailed options!
        """
    )
    parser.add_argument("--config", default="reddit_config.json", help="Configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Post command
    post_parser = subparsers.add_parser("post", help="📝 Post content to a subreddit (text or link posts)")
    post_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    post_parser.add_argument("title", help="Post title")
    post_parser.add_argument("--content", help="Post content (for text posts)")
    post_parser.add_argument("--url", help="URL (for link posts)")
    post_parser.add_argument("--flair", help="Flair ID")
    
    # Get responses command
    responses_parser = subparsers.add_parser("responses", help="💬 Get comments and responses for a post")
    responses_parser.add_argument("post_url", help="Reddit post URL")
    responses_parser.add_argument("--limit", type=int, default=10, help="Number of responses to fetch")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="📊 Monitor a post for new responses over time")
    monitor_parser.add_argument("post_url", help="Reddit post URL")
    monitor_parser.add_argument("--interval", type=int, default=30, help="Check interval in seconds")
    monitor_parser.add_argument("--max-checks", type=int, default=10, help="Maximum number of checks")
    
    # Flairs command
    flairs_parser = subparsers.add_parser("flairs", help="🏷️ Get available flairs for a subreddit")
    flairs_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="🗑️ Delete a post (only your own posts)")
    delete_parser.add_argument("post_url", help="Reddit post URL")
    
    # Comment command
    comment_parser = subparsers.add_parser("comment", help="💬 Comment on a Reddit post")
    comment_parser.add_argument("post_url", help="Reddit post URL")
    comment_parser.add_argument("text", help="Comment text")
    
    # Reply command
    reply_parser = subparsers.add_parser("reply", help="↩️ Reply to a Reddit comment")
    reply_parser.add_argument("comment_url", help="Reddit comment URL")
    reply_parser.add_argument("text", help="Reply text")
    
    # Hot posts command
    hot_parser = subparsers.add_parser("hot", help="🔥 Get hot/trending posts from a subreddit")
    hot_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    hot_parser.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    
    # Search subreddits command
    search_parser = subparsers.add_parser("search-subreddits", help="🔍 Search for subreddits by keywords")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=10, help="Number of subreddits to fetch")
    
    # Subreddit info command
    info_parser = subparsers.add_parser("subreddit-info", help="ℹ️ Get detailed information about a subreddit")
    info_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Subscribe command
    subscribe_parser = subparsers.add_parser("subscribe", help="➕ Subscribe to a subreddit")
    subscribe_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Unsubscribe command
    unsubscribe_parser = subparsers.add_parser("unsubscribe", help="➖ Unsubscribe from a subreddit")
    unsubscribe_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Trending subreddits command
    trending_parser = subparsers.add_parser("trending", help="📈 Get trending subreddits across Reddit")
    trending_parser.add_argument("--limit", type=int, default=10, help="Number of subreddits to fetch")
    
    # Moderators command
    moderators_parser = subparsers.add_parser("moderators", help="👮 Get moderators of a subreddit")
    moderators_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Voting commands
    upvote_parser = subparsers.add_parser("upvote", help="⬆️ Upvote a post or comment")
    upvote_parser.add_argument("url", help="Post or comment URL")
    
    downvote_parser = subparsers.add_parser("downvote", help="⬇️ Downvote a post or comment")
    downvote_parser.add_argument("url", help="Post or comment URL")
    
    # User management commands
    user_profile_parser = subparsers.add_parser("user-profile", help="👤 Get user profile information")
    user_profile_parser.add_argument("username", help="Reddit username")
    
    user_posts_parser = subparsers.add_parser("user-posts", help="📝 Get posts by a user")
    user_posts_parser.add_argument("username", help="Reddit username")
    user_posts_parser.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    
    user_comments_parser = subparsers.add_parser("user-comments", help="💬 Get comments by a user")
    user_comments_parser.add_argument("username", help="Reddit username")
    user_comments_parser.add_argument("--limit", type=int, default=10, help="Number of comments to fetch")
    
    # Content management commands
    save_parser = subparsers.add_parser("save", help="💾 Save a post for later")
    save_parser.add_argument("post_url", help="Reddit post URL")
    
    unsave_parser = subparsers.add_parser("unsave", help="🗑️ Unsave a post")
    unsave_parser.add_argument("post_url", help="Reddit post URL")
    
    saved_posts_parser = subparsers.add_parser("saved-posts", help="📚 Get user's saved posts")
    saved_posts_parser.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    
    # Messaging commands
    message_parser = subparsers.add_parser("message", help="📬 Send a private message")
    message_parser.add_argument("username", help="Recipient username")
    message_parser.add_argument("subject", help="Message subject")
    message_parser.add_argument("body", help="Message body")
    
    inbox_parser = subparsers.add_parser("inbox", help="📥 Get inbox messages")
    inbox_parser.add_argument("--limit", type=int, default=10, help="Number of messages to fetch")
    
    # Search commands
    search_posts_parser = subparsers.add_parser("search-posts", help="🔍 Search for posts across Reddit")
    search_posts_parser.add_argument("query", help="Search query")
    search_posts_parser.add_argument("--subreddit", help="Subreddit to search in")
    search_posts_parser.add_argument("--limit", type=int, default=10, help="Number of posts to fetch")
    
    search_comments_parser = subparsers.add_parser("search-comments", help="🔍 Search for comments across Reddit")
    search_comments_parser.add_argument("query", help="Search query")
    search_comments_parser.add_argument("--subreddit", help="Subreddit to search in")
    search_comments_parser.add_argument("--limit", type=int, default=10, help="Number of comments to fetch")
    
    # Editing commands
    edit_post_parser = subparsers.add_parser("edit-post", help="✏️ Edit a post (only your own posts)")
    edit_post_parser.add_argument("post_url", help="Reddit post URL")
    edit_post_parser.add_argument("new_content", help="New post content")
    
    edit_comment_parser = subparsers.add_parser("edit-comment", help="✏️ Edit a comment (only your own comments)")
    edit_comment_parser.add_argument("comment_url", help="Reddit comment URL")
    edit_comment_parser.add_argument("new_content", help="New comment content")
    
    # User relationships commands
    follow_parser = subparsers.add_parser("follow", help="➕ Follow a user")
    follow_parser.add_argument("username", help="Reddit username")
    
    unfollow_parser = subparsers.add_parser("unfollow", help="➖ Unfollow a user")
    unfollow_parser.add_argument("username", help="Reddit username")
    
    friends_parser = subparsers.add_parser("friends", help="👥 Get friends list")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = RedditCLI(args.config)
    
    if args.command == "post":
        submission = cli.post_to_subreddit(
            args.subreddit, 
            args.title, 
            args.content, 
            args.url, 
            args.flair
        )
        
        if submission:
            print(f"\n📊 Post Stats:")
            print(f"  🔗 URL: https://reddit.com{submission.permalink}")
            print(f"  📈 Score: {submission.score}")
            print(f"  💬 Comments: {submission.num_comments}")
    
    elif args.command == "responses":
        submission = cli.get_post_by_url(args.post_url)
        if submission:
            responses = cli.get_post_responses(submission, args.limit)
            print(f"\n💬 Found {len(responses)} responses:")
            for i, response in enumerate(responses, 1):
                print(f"\n{i}. 👤 {response['author']} (Score: {response['score']})")
                print(f"   📅 {response['created_utc']}")
                print(f"   💭 {response['body']}")
                print(f"   🔗 {response['permalink']}")
    
    elif args.command == "monitor":
        submission = cli.get_post_by_url(args.post_url)
        if submission:
            responses = cli.monitor_post(submission, args.interval, args.max_checks)
            print(f"\n📊 Total responses collected: {len(responses)}")
    
    elif args.command == "flairs":
        flairs = cli.get_subreddit_flairs(args.subreddit)
        if flairs:
            print(f"\n🏷️  Available flairs for r/{args.subreddit}:")
            for flair in flairs:
                print(f"  ID: {flair['id']} | Text: {flair['text']} | CSS: {flair['css_class']}")
        else:
            print(f"No flairs available for r/{args.subreddit}")
    
    elif args.command == "delete":
        success = cli.delete_post(args.post_url)
        if success:
            print(f"\n🗑️  Post successfully deleted!")
        else:
            print(f"\n❌ Failed to delete post")
    
    elif args.command == "comment":
        comment = cli.comment_on_post(args.post_url, args.text)
        if comment:
            print(f"\n💬 Comment successfully posted!")
        else:
            print(f"\n❌ Failed to post comment")
    
    elif args.command == "reply":
        reply = cli.reply_to_comment(args.comment_url, args.text)
        if reply:
            print(f"\n💬 Reply successfully posted!")
        else:
            print(f"\n❌ Failed to post reply")
    
    elif args.command == "hot":
        posts = cli.get_hot_posts(args.subreddit, args.limit)
        if posts:
            print(f"\n🔥 Hot posts from r/{args.subreddit}:")
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. 📝 {post['title']}")
                print(f"   👤 by {post['author']} | 📈 {post['score']} | 💬 {post['num_comments']} comments")
                print(f"   📅 {post['created_utc']}")
                print(f"   🔗 {post['url']}")
        else:
            print(f"No hot posts found for r/{args.subreddit}")
    
    elif args.command == "search-subreddits":
        subreddits = cli.search_subreddits(args.query, args.limit)
        if subreddits:
            print(f"\n🔍 Subreddits matching '{args.query}':")
            for i, subreddit in enumerate(subreddits, 1):
                print(f"\n{i}. 📍 r/{subreddit['name']}")
                print(f"   📝 {subreddit['title']}")
                print(f"   📄 {subreddit['description']}")
                print(f"   👥 {subreddit['subscribers']:,} subscribers | 🔥 {subreddit['active_users']} active")
                print(f"   🔗 {subreddit['url']}")
                if subreddit['nsfw']:
                    print(f"   ⚠️  NSFW")
        else:
            print(f"No subreddits found matching '{args.query}'")
    
    elif args.command == "subreddit-info":
        info = cli.get_subreddit_info(args.subreddit)
        if info:
            print(f"\n📊 Information about r/{args.subreddit}:")
            print(f"   📝 Title: {info['title']}")
            print(f"   📄 Description: {info['description']}")
            print(f"   📄 Public Description: {info['public_description']}")
            print(f"   👥 Subscribers: {info['subscribers']:,}")
            print(f"   🔥 Active Users: {info['active_users']}")
            print(f"   📅 Created: {info['created_utc']}")
            print(f"   🔗 URL: {info['url']}")
            print(f"   📝 Submission Type: {info['submission_type']}")
            print(f"   🌐 Language: {info['lang']}")
            if info['nsfw']:
                print(f"   ⚠️  NSFW: Yes")
            if info['quarantine']:
                print(f"   🚫 Quarantined: Yes")
        else:
            print(f"Could not get information for r/{args.subreddit}")
    
    elif args.command == "subscribe":
        success = cli.subscribe_to_subreddit(args.subreddit)
        if success:
            print(f"\n✅ Successfully subscribed to r/{args.subreddit}!")
        else:
            print(f"\n❌ Failed to subscribe to r/{args.subreddit}")
    
    elif args.command == "unsubscribe":
        success = cli.unsubscribe_from_subreddit(args.subreddit)
        if success:
            print(f"\n✅ Successfully unsubscribed from r/{args.subreddit}!")
        else:
            print(f"\n❌ Failed to unsubscribe from r/{args.subreddit}")
    
    elif args.command == "trending":
        subreddits = cli.get_trending_subreddits(args.limit)
        if subreddits:
            print(f"\n🔥 Trending Subreddits:")
            for i, subreddit in enumerate(subreddits, 1):
                print(f"\n{i}. 📍 r/{subreddit['name']}")
                print(f"   📝 {subreddit['title']}")
                print(f"   📄 {subreddit['description']}")
                print(f"   👥 {subreddit['subscribers']:,} subscribers | 🔥 {subreddit['active_users']} active")
                print(f"   🔗 {subreddit['url']}")
                if subreddit['nsfw']:
                    print(f"   ⚠️  NSFW")
        else:
            print(f"No trending subreddits found")
    
    elif args.command == "moderators":
        moderators = cli.get_subreddit_moderators(args.subreddit)
        if moderators:
            print(f"\n👮 Moderators of r/{args.subreddit}:")
            for i, moderator in enumerate(moderators, 1):
                print(f"   {i}. 👤 u/{moderator['name']}")
                print(f"      🔗 {moderator['url']}")
        else:
            print(f"No moderators found for r/{args.subreddit}")
    
    elif args.command == "upvote":
        if "comment" in args.url:
            success = cli.upvote_comment(args.url)
        else:
            success = cli.upvote_post(args.url)
        if success:
            print(f"\n✅ Successfully upvoted!")
        else:
            print(f"\n❌ Failed to upvote")
    
    elif args.command == "downvote":
        if "comment" in args.url:
            success = cli.downvote_comment(args.url)
        else:
            success = cli.downvote_post(args.url)
        if success:
            print(f"\n✅ Successfully downvoted!")
        else:
            print(f"\n❌ Failed to downvote")
    
    elif args.command == "user-profile":
        profile = cli.get_user_profile(args.username)
        if profile:
            print(f"\n👤 Profile of u/{args.username}:")
            print(f"   📅 Created: {profile['created_utc']}")
            print(f"   💬 Comment Karma: {profile['comment_karma']:,}")
            print(f"   🔗 Link Karma: {profile['link_karma']:,}")
            print(f"   🏆 Total Karma: {profile['comment_karma'] + profile['link_karma']:,}")
            print(f"   🔗 URL: {profile['url']}")
            if profile['is_employee']:
                print(f"   👨‍💼 Reddit Employee: Yes")
            if profile['is_mod']:
                print(f"   👮 Moderator: Yes")
            if profile['is_gold']:
                print(f"   🥇 Reddit Gold: Yes")
        else:
            print(f"Could not get profile for u/{args.username}")
    
    elif args.command == "user-posts":
        posts = cli.get_user_posts(args.username, args.limit)
        if posts:
            print(f"\n📝 Posts by u/{args.username}:")
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. 📝 {post['title']}")
                print(f"   📍 r/{post['subreddit']} | 📈 {post['score']} | 💬 {post['num_comments']} comments")
                print(f"   📅 {post['created_utc']}")
                print(f"   🔗 {post['url']}")
        else:
            print(f"No posts found for u/{args.username}")
    
    elif args.command == "user-comments":
        comments = cli.get_user_comments(args.username, args.limit)
        if comments:
            print(f"\n💬 Comments by u/{args.username}:")
            for i, comment in enumerate(comments, 1):
                print(f"\n{i}. 💬 {comment['body']}")
                print(f"   📍 r/{comment['subreddit']} | 📈 {comment['score']}")
                print(f"   📅 {comment['created_utc']}")
                print(f"   🔗 {comment['url']}")
        else:
            print(f"No comments found for u/{args.username}")
    
    elif args.command == "save":
        success = cli.save_post(args.post_url)
        if success:
            print(f"\n✅ Post saved successfully!")
        else:
            print(f"\n❌ Failed to save post")
    
    elif args.command == "unsave":
        success = cli.unsave_post(args.post_url)
        if success:
            print(f"\n✅ Post unsaved successfully!")
        else:
            print(f"\n❌ Failed to unsave post")
    
    elif args.command == "saved-posts":
        posts = cli.get_saved_posts(args.limit)
        if posts:
            print(f"\n💾 Your Saved Posts:")
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. 📝 {post['title']}")
                print(f"   📍 r/{post['subreddit']} | 📈 {post['score']} | 💬 {post['num_comments']} comments")
                print(f"   📅 {post['created_utc']}")
                print(f"   🔗 {post['url']}")
        else:
            print(f"No saved posts found")
    
    elif args.command == "message":
        success = cli.send_message(args.username, args.subject, args.body)
        if success:
            print(f"\n✅ Message sent successfully!")
        else:
            print(f"\n❌ Failed to send message")
    
    elif args.command == "inbox":
        messages = cli.get_inbox(args.limit)
        if messages:
            print(f"\n📬 Your Inbox:")
            for i, message in enumerate(messages, 1):
                print(f"\n{i}. 📧 {message['subject']}")
                print(f"   👤 From: u/{message['author']}")
                print(f"   💭 {message['body']}")
                print(f"   📅 {message['created_utc']}")
                print(f"   🔗 {message['url']}")
        else:
            print(f"No messages in inbox")
    
    elif args.command == "search-posts":
        posts = cli.search_posts(args.query, args.subreddit, args.limit)
        if posts:
            search_scope = f"r/{args.subreddit}" if args.subreddit else "all of Reddit"
            print(f"\n🔍 Posts matching '{args.query}' in {search_scope}:")
            for i, post in enumerate(posts, 1):
                print(f"\n{i}. 📝 {post['title']}")
                print(f"   📍 r/{post['subreddit']} | 👤 u/{post['author']} | 📈 {post['score']} | 💬 {post['num_comments']} comments")
                print(f"   📅 {post['created_utc']}")
                print(f"   🔗 {post['url']}")
        else:
            print(f"No posts found matching '{args.query}'")
    
    elif args.command == "search-comments":
        comments = cli.search_comments(args.query, args.subreddit, args.limit)
        if comments:
            search_scope = f"r/{args.subreddit}" if args.subreddit else "all of Reddit"
            print(f"\n🔍 Comments matching '{args.query}' in {search_scope}:")
            for i, comment in enumerate(comments, 1):
                print(f"\n{i}. 💬 {comment['body']}")
                print(f"   📍 r/{comment['subreddit']} | 👤 u/{comment['author']} | 📈 {comment['score']}")
                print(f"   📅 {comment['created_utc']}")
                print(f"   🔗 {comment['url']}")
        else:
            print(f"No comments found matching '{args.query}'")
    
    elif args.command == "edit-post":
        success = cli.edit_post(args.post_url, args.new_content)
        if success:
            print(f"\n✅ Post edited successfully!")
        else:
            print(f"\n❌ Failed to edit post")
    
    elif args.command == "edit-comment":
        success = cli.edit_comment(args.comment_url, args.new_content)
        if success:
            print(f"\n✅ Comment edited successfully!")
        else:
            print(f"\n❌ Failed to edit comment")
    
    elif args.command == "follow":
        success = cli.follow_user(args.username)
        if success:
            print(f"\n✅ Successfully followed u/{args.username}!")
        else:
            print(f"\n❌ Failed to follow u/{args.username}")
    
    elif args.command == "unfollow":
        success = cli.unfollow_user(args.username)
        if success:
            print(f"\n✅ Successfully unfollowed u/{args.username}!")
        else:
            print(f"\n❌ Failed to unfollow u/{args.username}")
    
    elif args.command == "friends":
        friends = cli.get_friends()
        if friends:
            print(f"\n👥 Your Friends:")
            for i, friend in enumerate(friends, 1):
                print(f"   {i}. 👤 u/{friend['name']}")
                print(f"      🔗 {friend['url']}")
        else:
            print(f"No friends found")


if __name__ == "__main__":
    main()
