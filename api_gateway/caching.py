from datetime import timedelta
from typing import Union
import redis

from rest_interfaces.profile_interfaces import IJobSeeker, IRecruiter

# implementing caching
redis_client = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


# Cache profile function
def cache_profile(
    username: str, jobSeeker: Union[IJobSeeker, IRecruiter], ttl: int = 3600
):
    redis_client.setex(f"profile:{username}", ttl, jobSeeker.model_dump_json())


# Get profile function
def get_profile(username: str):
    return redis_client.get(f"profile:{username}")


# Remove profile from cache
def remove_profile_cache(username: str):
    redis_client.delete(f"profile:{username}")


def cache_token(token, username, ttl: int = timedelta(minutes=15).seconds):
    redis_client.setex(f"{token}", ttl, username)


def remove_token(token: str):
    redis_client.delete(f"{token}")
