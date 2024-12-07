from datetime import timedelta
import os
from typing import Union
import redis

from rest_interfaces.profile_interfaces import IJobSeeker, IRecruiter
from rest_interfaces.job_interfaces import IJob  # Assuming IJob exists

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


# Cache job function
def cache_job(job_id: str, recruiter_id: str, job_details: str, ttl: int = 3600):
    """
    Cache job details for a specified job ID.
    
    Args:
        job_id (int): The ID of the job.
        job_details (str): The details of the job in string format (e.g., JSON).
        ttl (int): Time-to-live in seconds. Default is 3600 seconds (1 hour).
    """
    redis_client.setex(f"job:{recruiter_id}/{job_id}", ttl, job_details)


# Get job function
def get_job(job_id: str, recruiter_id: str):
    """
    Retrieve cached job details by job ID.
    
    Args:
        job_id (int): The ID of the job to retrieve.
    
    Returns:
        str: Cached job details if available, else None.
    """
    return redis_client.get(f"job:{recruiter_id}/{job_id}")

def cache_all_jobs(recruiter_id:str, jobs_details: str, ttl: int = 3600):
    """
    Cache all job postings.
    
    Args:
        jobs_details (str): The details of all jobs in string format (e.g., JSON).
        ttl (int): Time-to-live in seconds. Default is 3600 seconds (1 hour).
    """
    redis_client.setex(f"jobs:all/{recruiter_id}", ttl, jobs_details)

def get_all_jobs_cache(recruiter_id: str) -> Union[str, None]:
    """
    Retrieve cached job postings.
    
    Returns:
        str or None: The cached job postings as a string (e.g., JSON), or None if not cached.
    """
    cached_data = redis_client.get(f"jobs:all/{recruiter_id}")
    return cached_data.decode("utf-8") if cached_data else None


# Remove job from cache
def remove_job_cache(job_id: str, recruiter_id: str):
    """
    Remove cached job details by job ID.
    
    Args:
        job_id (int): The ID of the job to remove from cache.
    """
    redis_client.delete(f"job:{recruiter_id}/{job_id}")

# Remove job from cache
def remove_all_jobs_cache(recruiter_id: str):
    """
    Remove cached job details by job ID.
    
    Args:
        job_id (int): The ID of the job to remove from cache.
    """
    redis_client.delete(f"jobs:all/{recruiter_id}")


# Cache token function
def cache_token(token, user_data, ttl: int = timedelta(minutes=15).seconds):
    redis_client.setex(f"{token}", ttl, user_data)


# Get user from cached token
def get_user_from_cached_token(token):
    return redis_client.get(f"{token}")


# Remove token from cache
def remove_token(token: str):
    redis_client.delete(f"{token}")