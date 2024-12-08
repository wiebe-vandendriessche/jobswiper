package org.example;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;




public class JobSeeker {
    private String username;

    @JsonProperty("first_name")
    private String firstName;
    @JsonProperty("last_name")
    private String lastName;
    private String email;
    private List<String> interests;
    private List<String> qualifications;
    private String location;
    @JsonProperty("education_level")
    private String educationLevel;
    @JsonProperty("years_of_experience")
    private int yearsOfExperience;
    private String availability;
    private Salary salary;
    @JsonProperty("date_of_birth")
    private String dateOfBirth;
    @JsonProperty("phone_number")
    private String phoneNumber;
    private String id;

    //vereist voor JSON serialisatie
    public JobSeeker() {}

    public JobSeeker(String json){

    }

    // Constructor
    public JobSeeker(
            String username,
            String firstName,
            String lastName,
            String email,
            List<String> interests,
            List<String> qualifications,
            String location,
            String educationLevel,
            int yearsOfExperience,
            String availability,
            Salary salary,
            String dateOfBirth,
            String phoneNumber,
            String id
    ) {
        this.username = username;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.interests = interests;
        this.qualifications = qualifications;
        this.location = location;
        this.educationLevel = educationLevel;
        this.yearsOfExperience = yearsOfExperience;
        this.availability = availability;
        this.salary = salary;
        this.dateOfBirth = dateOfBirth;
        this.phoneNumber = phoneNumber;
        this.id = id;
    }

    // Getters and Setters
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public List<String> getInterests() {
        return interests;
    }

    public void setInterests(List<String> interests) {
        this.interests = interests;
    }

    public List<String> getQualifications() {
        return qualifications;
    }

    public void setQualifications(List<String> qualifications) {
        this.qualifications = qualifications;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getEducationLevel() {
        return educationLevel;
    }

    public void setEducationLevel(String educationLevel) {
        this.educationLevel = educationLevel;
    }

    public int getYearsOfExperience() {
        return yearsOfExperience;
    }

    public void setYearsOfExperience(int yearsOfExperience) {
        this.yearsOfExperience = yearsOfExperience;
    }

    public String getAvailability() {
        return availability;
    }

    public void setAvailability(String availability) {
        this.availability = availability;
    }

    public Salary getSalary() {
        return salary;
    }

    public void setSalary(Salary salary) {
        this.salary = salary;
    }

    public String getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirthString(String dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    // toString method for displaying object information
    @Override
    public String toString() {
        return "JobSeeker{" +
                "username='" + username + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", email='" + email + '\'' +
                ", interests=" + interests +
                ", qualifications=" + qualifications +
                ", location='" + location + '\'' +
                ", educationLevel='" + educationLevel + '\'' +
                ", yearsOfExperience=" + yearsOfExperience +
                ", availability='" + availability + '\'' +
                ", salary=" + salary +
                ", dateOfBirth=" + dateOfBirth +
                ", phoneNumber=" + phoneNumber +
                ", id=" + id +
                '}';
    }
}