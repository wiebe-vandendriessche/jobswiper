package org.example;


import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.core.search.TotalHits;

import java.io.IOException;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world");



        ElasticsearchConnector connector = new ElasticsearchConnector();
        ElasticsearchClient client = connector.getClient();

        ElasticDB elasticDB = new ElasticDB(client);

        elasticDB.startService();


        Salary salary = new Salary(50000, 120000); // Example salary range
        JobSeeker jobseeker = new JobSeeker(
                "john_doe",
                "John",
                "Doe",
                "john.doe@example.com",
                List.of("Tech", "DevOps"),
                List.of("Bachelor's in Computer Science", "AWS Certified"),
                "New York",
                "Bachelor's",
                5,
                "Available Immediately",
                salary,
                "1999-01-01",
                "123-456-7890",
                "1"
        );

        elasticDB.insertJobSeeker(jobseeker);

        
        String title = "Software Engineer";
        String companyName = "Tech Corp";
        String location = "San Francisco, CA";
        String jobType = "Full-time";
        String description = "Develop and maintain software applications.";
        List<String> responsibilities = List.of("Write code", "Review code", "Deploy applications");
        List<String> requirements = List.of("Java", "Spring", "AWS");
        Salary salary2 = new Salary(100000, 120000);
        String postedByUuid = "1234-5678-uuid";
        String id = "job-001";
        String datePosted = "2024-12-07";

        // Create Job instance
        Job job = new Job(
                title, companyName, location, jobType, description, responsibilities, requirements, salary2, postedByUuid, id, datePosted
        );

        elasticDB.insertJob(job);


        MatchingDB matchingdb = new MatchingDB();
        RabbitClient rbClient = new RabbitClient(elasticDB, matchingdb);
        rbClient.consume();

    }
}