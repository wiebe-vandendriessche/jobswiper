package org.example;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.rabbitmq.client.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.List;

public class RabbitClient {
    private static final int MAX_RETRIES = 12; // Maximum number of retry attempts
    private static final int RETRY_DELAY_MS = 5000; // Delay between retries in milliseconds
    private static final Logger logger = LoggerFactory.getLogger(RabbitClient.class);




    private static final String QUEUENAME_JOBSEEKER = System.getenv("JOBSEEKER_BUS");
    private static final String QUEUENAME_JOB = System.getenv("JOB_BUS");

    private ObjectMapper objectMapper = new ObjectMapper();

    private ConnectionFactory factory;

    private ElasticDB elasticDB;
    private MatchingDB matchingDB;

    public RabbitClient(ElasticDB elasticDB, MatchingDB matchingDB) {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUsername(System.getenv("BUS_USERNAME"));
        factory.setPassword(System.getenv("BUS_PASSWORD"));
        factory.setVirtualHost("/");
        factory.setHost(System.getenv("BUS_SERVICE"));
        factory.setPort(Integer.parseInt(System.getenv("BUS_PORT")));
        this.factory = factory;
        this.elasticDB = elasticDB;
        this.matchingDB = matchingDB;


    }

    private void processJobseeker(String json) throws JsonProcessingException {
        System.out.println("processing jobseeker");

        JobSeeker jobseeker = objectMapper.readValue(json, JobSeeker.class);

        System.out.println("new jobseekser made");
        //System.out.println(jobseeker);

        //add the newly created jobseeker to the ES database
        //If the jobseeker doesn't exist already, it will just be added
        //IF the jobseeker already existed in the DB, it will get updated

        elasticDB.insertJobSeeker(jobseeker);

        List<Match> matches =  elasticDB.matchJobSeekerWithJobs(jobseeker);

        if (matches != null && !matches.isEmpty()) {
            matchingDB.insertUserJobMapping(matches);
        }




    }

    private void processJob(String json) throws JsonProcessingException {
        System.out.println("processing job");

        Job job = objectMapper.readValue(json, Job.class);

        System.out.println("new job made");
        //System.out.println(job);

        //add the newly created jobseeker to the ES database
        //If the jobseeker doesn't exist already, it will just be added
        //IF the jobseeker already existed in the DB, it will get updated

        elasticDB.insertJob(job);

        List<Match> matches =  elasticDB.matchJobWithJobSeekers(job);

        if (matches != null && !matches.isEmpty()) {
            matchingDB.insertUserJobMapping(matches);
        }
    }


    public void consume(){
        int attempts = 0;
        boolean connected = false;

        while (attempts < MAX_RETRIES && !connected) {
            try {
                attempts++;
                System.out.println("Attempt " + attempts + " to connect to RabbitMQ...");


                Connection connection = factory.newConnection();
                Channel channel = connection.createChannel();


                //declaring the two queues
                channel.queueDeclare(QUEUENAME_JOBSEEKER, true, false, false, null);
                channel.queueDeclare(QUEUENAME_JOB, true, false, false, null);


                System.out.println("Connected to RabbitMQ and waiting for messages from queue: " + QUEUENAME_JOBSEEKER);

                //Consume from the jobseeker queueu
                channel.basicConsume(QUEUENAME_JOBSEEKER, false, (consumerTag, message) -> {
                    String m = new String(message.getBody(), "UTF8");
                    System.out.println("new message received" + QUEUENAME_JOBSEEKER + ": " + m);

                    //VOOR de processfunctie, want als er iets mis is met de input, dan wordt het pakket gedropt
                    channel.basicAck(message.getEnvelope().getDeliveryTag(), false);


                    processJobseeker(m);

                }, consumerTag -> {
                    System.out.println("new message received fail: ");

                });



                System.out.println("Connected to RabbitMQ and waiting for messages from queue: " + QUEUENAME_JOB);

                //Consume from the job queue
                channel.basicConsume(QUEUENAME_JOB, false, (consumerTag, message) -> {
                    String m = new String(message.getBody(), "UTF8");
                    System.out.println("new message received on" + QUEUENAME_JOB  + ": " + m);

                    //VOOR de processfunctie, want als er iets mis is met de input, dan wordt het pakket gedropt
                    channel.basicAck(message.getEnvelope().getDeliveryTag(), false);

                    processJob(m);



                }, consumerTag -> {
                    System.out.println("new message received fail: ");

                });



                connected = true; // Successfully connected, exit retry loop

            } catch (Exception e) {
                System.err.println("Failed to connect to RabbitMQ: " + e.getMessage());
                if (attempts < MAX_RETRIES) {
                    System.out.println("Retrying in " + (RETRY_DELAY_MS / 1000) + " seconds...");
                    try {
                        Thread.sleep(RETRY_DELAY_MS); // Wait before retrying
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        break; // Exit if interrupted
                    }
                } else {
                    System.err.println("Max retries reached. Could not connect to RabbitMQ.");
                }
            }
        }
    }




}
