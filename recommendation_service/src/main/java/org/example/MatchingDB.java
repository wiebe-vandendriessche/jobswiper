package org.example;

import java.sql.*;
import java.util.List;

public class MatchingDB {
    private String URL;
    private String USERNAME;
    private String PASSWORD;




    public MatchingDB(){

        String database = System.getenv("MYSQL_DATABASE");
        String user = System.getenv("MYSQL_USER");
        String password = System.getenv("MYSQL_PASSWORD");
        String host = System.getenv("MYSQL_HOST");
        String port = "3306";

        String url = "jdbc:mysql://"+host+":"+port+"/"+database;

        this.URL = url;
        this.USERNAME = user;
        this.PASSWORD = password;


    }

    private Connection getConnection() {
        while (true) {
            try {
                Connection connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
                System.out.println("Database connection established.");
                return connection;
            } catch (SQLException e) {
                System.err.println("Failed to connect to the database: " + e.getMessage());
                System.out.println("Retrying in 3 seconds...");
                try {
                    Thread.sleep(3000); // Wait for 5 seconds before retrying
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt(); // Restore the interrupted status
                    throw new RuntimeException("Retry interrupted", ie);
                }
            }
        }
    }




    public void insertUserJobMapping(List<Match> matches) {
        String checkQuery = "SELECT COUNT(*) FROM user_job_mapping WHERE user_id = ? AND job_id = ?";
        String insertQuery = "INSERT INTO user_job_mapping (user_id, job_id, recruiter_id, user_likes, recruiter_likes) VALUES (?, ?, ?, ?, ?)";

        try (Connection connection = getConnection();
             PreparedStatement checkStmt = connection.prepareStatement(checkQuery);
             PreparedStatement insertStmt = connection.prepareStatement(insertQuery)) {

            for (Match match : matches) {
                // Check if the record already exists
                checkStmt.setString(1, match.getUserId());
                checkStmt.setString(2, match.getJobId());
                ResultSet rs = checkStmt.executeQuery();

                boolean exists = false;
                if (rs.next()) {
                    exists = rs.getInt(1) > 0;
                }

                if (!exists) {
                    // Insert if the record does not exist
                    insertStmt.setString(1, match.getUserId());
                    insertStmt.setString(2, match.getJobId());
                    insertStmt.setString(3, match.getRecruiterIdId());
                    insertStmt.setNull(4, java.sql.Types.BOOLEAN);
                    insertStmt.setNull(5, java.sql.Types.BOOLEAN);

                    int rowsInserted = insertStmt.executeUpdate();
                    if (rowsInserted > 0) {
                        System.out.println("Inserted new match: " + match);
                    }
                } else {
                    System.out.println("Match already exists: " + match);
                }
            }

        } catch (SQLException e) {
            System.err.println("Error processing matches: " + e.getMessage());
        }
    }


    public void createTable() {
        String createTableQuery = "CREATE TABLE IF NOT EXISTS user_job_mapping (" +
                "user_id VARCHAR(36) NOT NULL," +
                "job_id VARCHAR(36) NOT NULL," +
                "user_likes BOOLEAN," +
                "recruiter_likes BOOLEAN," +
                "PRIMARY KEY (user_id, job_id))";

        try (Connection conn = DriverManager.getConnection(URL, USERNAME, PASSWORD);
             PreparedStatement pstmt = conn.prepareStatement(createTableQuery)) {

            pstmt.executeUpdate();
            System.out.println("Table created successfully!");

        } catch (SQLException e) {
            System.err.println("Error creating table: " + e.getMessage());
        }
    }
}
