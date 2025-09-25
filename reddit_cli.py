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
    parser = argparse.ArgumentParser(description="Reddit CLI - Post to subreddits and get responses")
    parser.add_argument("--config", default="reddit_config.json", help="Configuration file path")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Post command
    post_parser = subparsers.add_parser("post", help="Post to a subreddit")
    post_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    post_parser.add_argument("title", help="Post title")
    post_parser.add_argument("--content", help="Post content (for text posts)")
    post_parser.add_argument("--url", help="URL (for link posts)")
    post_parser.add_argument("--flair", help="Flair ID")
    
    # Get responses command
    responses_parser = subparsers.add_parser("responses", help="Get responses for a post")
    responses_parser.add_argument("post_url", help="Reddit post URL")
    responses_parser.add_argument("--limit", type=int, default=10, help="Number of responses to fetch")
    
    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor a post for new responses")
    monitor_parser.add_argument("post_url", help="Reddit post URL")
    monitor_parser.add_argument("--interval", type=int, default=30, help="Check interval in seconds")
    monitor_parser.add_argument("--max-checks", type=int, default=10, help="Maximum number of checks")
    
    # Flairs command
    flairs_parser = subparsers.add_parser("flairs", help="Get available flairs for a subreddit")
    flairs_parser.add_argument("subreddit", help="Subreddit name (without r/)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a post")
    delete_parser.add_argument("post_url", help="Reddit post URL")
    
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


if __name__ == "__main__":
    main()
