CREATE TABLE user_job_mapping (
                                  user_id VARCHAR(36) NOT NULL,
                                  job_id VARCHAR(36) NOT NULL,
                                  user_likes BOOLEAN,
                                  recruiter_likes BOOLEAN,
                                  PRIMARY KEY (user_id, job_id)
);