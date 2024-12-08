package org.example;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.transport.ElasticsearchTransport;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.HttpClients;
import org.elasticsearch.client.RestClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import java.util.concurrent.TimeUnit;
public class ElasticsearchConnector {

    //Singleton class
    private static ElasticsearchClient client;


    // (Create and) return an instance of ElasticsearchClient
    public static ElasticsearchClient getClient() {
        if (client == null) {
            synchronized (ElasticsearchConnector.class) {
                if (client == null) {
                    int maxRetries = 10;  // Maximum number of retries
                    int retryDelay = 5000; // Delay between retries in milliseconds

                    RestClient restClient = null;
                    boolean connected = false;

                    String elastic_host = System.getenv("ELASTIC_HOST");
                    int elastic_port = Integer.parseInt(System.getenv("ELASTIC_PORT"));

                    String elastic_username = System.getenv("ELASTIC_USERNAME");
                    String elastic_password = System.getenv("ELASTIC_PASSWORD");


                    for (int i = 1; i <= maxRetries; i++) {
                        try {

                            BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
                            credentialsProvider.setCredentials(
                                    AuthScope.ANY,
                                    new UsernamePasswordCredentials(elastic_username, elastic_password)
                            );

                            // Attempt to connect
                            restClient = RestClient.builder(new HttpHost(elastic_host, elastic_port)).setHttpClientConfigCallback(httpClientBuilder -> {
                                httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
                                return httpClientBuilder;
                            }).build();

                            ElasticsearchTransport transport = new RestClientTransport(restClient, new JacksonJsonpMapper());
                            // Create the Elasticsearch client
                            client = new ElasticsearchClient(transport);


                            System.out.println("Connected to Elasticsearch on attempt " + i);
                            break; // Exit loop on successful connection
                        } catch (Exception e) {
                            System.err.println("Attempt " + i + " to connect to Elasticsearch failed.");
                            if (i == maxRetries) {
                                throw new RuntimeException("Failed to connect to Elasticsearch after " + maxRetries + " attempts.", e);
                            }
                        }

                        // Wait before retrying
                        try {
                            TimeUnit.MILLISECONDS.sleep(retryDelay);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt(); // Restore interrupted status
                            throw new RuntimeException("Retry mechanism interrupted", e);
                        }
                    }

                }
            }
        }
        return client;
    }

}