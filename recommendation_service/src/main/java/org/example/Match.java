package org.example;

public class Match {

    private String userId;
    private String jobId;
    private String recruiterId;


    public Match() {
    }


    public Match(String userId, String jobId, String recruiterId) {
        this.userId = userId;
        this.jobId = jobId;
        this.recruiterId = recruiterId;

    }

    // Getters and Setters
    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getJobId() {
        return jobId;
    }

    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public String getRecruiterIdId() {
        return recruiterId;
    }

    public void setRecruiterId(String jobId) {
        this.recruiterId = jobId;
    }



    // Overriding toString() for easier debugging
    @Override
    public String toString() {
        return "Match{" +
                "userId='" + userId + '\'' +
                ", jobId='" + jobId + '\'' +
                '}';
    }
}