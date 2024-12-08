package org.example;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.FieldValue;
import co.elastic.clients.elasticsearch.core.IndexResponse;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.core.search.TotalHits;
import co.elastic.clients.json.JsonData;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class ElasticDB {

    private final ElasticsearchClient client;

    private final String JOBSEEKERINDEX = "jobseekers";
    private final String JOBINDEX = "jobs";

    public ElasticDB(ElasticsearchClient client) {
        this.client = client;
    }


    public void insertJob(Job job) {
        try {
            IndexResponse response = client.index(i -> i
                    .index(JOBINDEX)
                    .id(job.getId())
                    .document(job)
            );
            System.out.println("Job indexed with ID: " + response.id());
        } catch (IOException e) {
            System.out.println("Failed to index job");
            e.printStackTrace();
        }
    }

    public void insertJobSeeker(JobSeeker jobSeeker) {
        try {
            IndexResponse response = client.index(i -> i
                    .index(JOBSEEKERINDEX)
                    .id(jobSeeker.getId())
                    .document(jobSeeker)
            );
            System.out.println("JobSeeker indexed with ID: " + response.id());
        } catch (IOException e) {
            System.out.println("Failed to index jobseeker");
            e.printStackTrace();
        }
    }

    public List<Match> matchJobSeekerWithJobs(JobSeeker jobSeeker) {
        List<Match> matches = new ArrayList<>();
        try {
            // Search for matching jobs in the "jobs" index
            SearchResponse<Job> searchResponse = client.search(s -> s
                            .index(JOBINDEX) // The index name
                            .query(q -> q
                                    .bool(b -> b
                                            .must(m -> m
                                                    .match(t -> t
                                                            .field("location") // Match job's location with the job seeker's location
                                                            .query(jobSeeker.getLocation())
                                                    )
                                            )
                                            //at least one req/quali common

                                            .must(m -> m
                                                    .terms(t -> t
                                                            .field("requirements.keyword") // Match job's requirements with job seeker's skills
                                                            .terms(tn -> tn.value(
                                                                    jobSeeker.getQualifications().stream()
                                                                            .map(FieldValue::of) // Convert each String to FieldValue
                                                                            .collect(Collectors.toList()) // Collect the results into a list
                                                            ))
                                                    )
                                            )
                                    )
                            ),
                    Job.class // Map the result to Job class
            );

            // Process the search results
            TotalHits total = searchResponse.hits().total();
            System.out.println("Total matching jobs: " + total);

            List<Hit<Job>> hits = searchResponse.hits().hits();
            for (Hit<Job> hit : hits) {
                Job matchedJob = hit.source();
                System.out.println("Matched Job: " + matchedJob.getId()+ ", Score: " + hit.score());

                Match match = new Match(jobSeeker.getId(),matchedJob.getId() );
                matches.add(match);
            }
        } catch (IOException e) {
            System.out.println("Failed to match job seeker with jobs");
            e.printStackTrace();
        }
        return matches;
    }

    public List<Match> matchJobWithJobSeekers(Job job) {
        List<Match> matches = new ArrayList<>();
        try {
            // Search for all jobseekers in the "jobseekers" index
            SearchResponse<JobSeeker> searchResponse = client.search(s -> s
                            .index("jobseekers") // The index name
                            .query(q -> q
                                    .bool(b -> b
                                            .must(m -> m
                                                    .match(t -> t
                                                            .field("location") // Match job's location with the job seeker's location
                                                            .query(job.getLocation())
                                                    )
                                            )

                                            .must(m -> m
                                                    .terms(t -> t
                                                            .field("qualifications.keyword")
                                                            .terms(tn -> tn.value(
                                                                    job.getRequirements().stream()
                                                                            .map(FieldValue::of) // Convert each String to FieldValue
                                                                            .collect(Collectors.toList()) // Collect the results into a list
                                                            ))
                                                    )
                                            )
                                    )
                            ),
                    JobSeeker.class // Map the result to JobSeeker class
            );

            // Process the search results
            TotalHits total = searchResponse.hits().total();
            System.out.println("Total matching job seekers: " + total);

            List<Hit<JobSeeker>> hits = searchResponse.hits().hits();
            for (Hit<JobSeeker> hit : hits) {
                JobSeeker matchedJobSeeker = hit.source();
                System.out.println("Matched Job Seeker: " + matchedJobSeeker.getUsername() + ", Score: " + hit.score());

                Match match = new Match(matchedJobSeeker.getId(),job.getId() );
                matches.add(match);
            }
        } catch (IOException e) {
            System.out.println("Failed to match job with job seekers");
            e.printStackTrace();
        }

        return matches;
    }





    public void startService(){


        //Starting the whole service of Elastic takes some time
        //Try to add a doc to "test" index and when this finally succeeds, the ES service is up and running

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

        int attempt = 0;
        int MAX_ATTEMPTS = 150;



        while (attempt < MAX_ATTEMPTS) {
            try {




                IndexResponse response = client.index(i -> i
                        .index("jobseekertest")
                        .id(jobseeker.getId())
                        .document(jobseeker)
                );


                System.out.println("test successfully index. ES service is ready " + response.id());


                break;  // Exit the loop if successful
            } catch (IOException e) {
                attempt++;
                System.out.println("Failed to index test obj. ES service is not ready yet. Attempt " + attempt);
                //e.printStackTrace();
                if (attempt < MAX_ATTEMPTS) {
                    try {
                        Thread.sleep(5000); // Wait for 5 seconds
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt(); // Handle interruption
                    }
                }
            }
        }

        if (attempt == MAX_ATTEMPTS) {
            System.out.println("Failed to index jobseeker after " + MAX_ATTEMPTS + " attempts.");
        }





    }
}