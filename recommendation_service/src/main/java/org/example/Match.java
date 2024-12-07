package org.example;

public class Match {

    private String userId;
    private String jobId;


    public Match() {
    }


    public Match(String userId, String jobId) {
        this.userId = userId;
        this.jobId = jobId;

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



    // Overriding toString() for easier debugging
    @Override
    public String toString() {
        return "Match{" +
                "userId='" + userId + '\'' +
                ", jobId='" + jobId + '\'' +
                '}';
    }
}