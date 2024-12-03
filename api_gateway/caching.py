from datetime import timedelta
import os
from typing import Union
import redis

from rest_interfaces.profile_interfaces import IJobSeeker, IRecruiter


try:
    redis_client = redis.Redis(host=f"localhost", port=6379, db=0)
    if redis_client.ping():
        print("Redis is connected!")
except redis.ConnectionError:
    print("Redis connection failed!")


# Cache profile function
def cache_profile(username: str, profile: str, ttl: int = 3600):
    redis_client.setex(f"profile:{username}", ttl, profile)


# Get profile function
def get_profile(username: str):
    return redis_client.get(f"profile:{username}")


# Remove profile from cache
def remove_profile_cache(username: str):
    redis_client.delete(f"profile:{username}")


def cache_token(token, user_data, ttl: int = timedelta(minutes=15).seconds):
    redis_client.setex(f"{token}", ttl, user_data)


def get_user_from_cached_token(token):
    return redis_client.get(f"{token}")


def remove_token(token: str):
    redis_client.delete(f"{token}")
