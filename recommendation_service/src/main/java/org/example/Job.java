package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;



public class Job {
    private String title;
    @JsonProperty("company_name")
    private String companyName;
    private String location;
    @JsonProperty("job_type")
    private String jobType;
    private String description;
    private List<String> responsibilities;
    private List<String> requirements;
    private Salary salary;
    @JsonProperty("posted_by_uuid")
    private String postedByUuid;
    private String id;
    @JsonProperty("date_posted")
    private String date_posted;

    // Default constructor (needed for JSON deserialization)
    public Job() {}

    // Fully parameterized constructor
    public Job(
            String title,
            String companyName,
            String location,
            String jobType,
            String description,
            List<String> responsibilities,
            List<String> requirements,
            Salary salary,
            String postedByUuid,
            String id,
            String date_posted
    ) {
        this.title = title;
        this.companyName = companyName;
        this.location = location;
        this.jobType = jobType;
        this.description = description;
        this.responsibilities = responsibilities;
        this.requirements = requirements;
        this.salary = salary;
        this.postedByUuid = postedByUuid;
        this.id = id;
        this.date_posted = date_posted;
    }

    // Getters and Setters
    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyName) {
        this.companyName = companyName;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getJobType() {
        return jobType;
    }

    public void setJobType(String jobType) {
        this.jobType = jobType;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public List<String> getResponsibilities() {
        return responsibilities;
    }

    public void setResponsibilities(List<String> responsibilities) {
        this.responsibilities = responsibilities;
    }

    public List<String> getRequirements() {
        return requirements;
    }

    public void setRequirements(List<String> requirements) {
        this.requirements = requirements;
    }

    public Salary getSalary() {
        return salary;
    }

    public void setSalary(Salary salary) {
        this.salary = salary;
    }


    public String getPostedByUuid() {
        return postedByUuid;
    }

    public void setPostedByUuid(String postedByUuid) {
        this.postedByUuid = postedByUuid;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDatePosted() {
        return date_posted;
    }

    public void setDatePosted(String date_posted) {
        this.date_posted = date_posted;
    }


    // toString method for displaying object information
    @Override
    public String toString() {
        return "Job{" +
                "title='" + title + '\'' +
                ", companyName='" + companyName + '\'' +
                ", location='" + location + '\'' +
                ", jobType='" + jobType + '\'' +
                ", description='" + description + '\'' +
                ", responsibilities=" + responsibilities +
                ", requirements=" + requirements +
                ", salary=" + salary +
                ", postedByUuid='" + postedByUuid + '\'' +
                ", DatePosted='" + date_posted + '\'' +
                ", id='" + id + '\'' +
                '}';
    }
}