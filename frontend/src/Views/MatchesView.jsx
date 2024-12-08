import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../Views/AuthContext"; // Assuming the context is set up
import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";

const apiBaseUrl = "http://localhost:8081"; // Replace with actual API URL

function MatchesView() {
  const { authData } = useContext(AuthContext); // Get user data from AuthContext
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch conversations (matches) based on user type
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        if (!authData || !authData.selected_user_id) {
          console.error("User not logged in or missing user ID.");
          return;
        }

        const response = await fetch(
          `${apiBaseUrl}/messaging/conversations/${authData.selected_user_id}`,
          {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("jwtToken")}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          console.log("Conversations:", data);
          // Remove duplicates based on job_id or jobseeker_id
          const uniqueMatches = data.matches.filter((match, index, self) => {
            return index === self.findIndex((m) => m.job_id === match.job_id || m.jobseeker_id === match.jobseeker_id);
          });
          
          setMatches(uniqueMatches); // Set the unique matches
        } else {
          console.error("Failed to fetch conversations:", response.status);
        }
      } catch (error) {
        console.error("Error fetching conversations:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, [authData]);

  return (
    <div className="matches-view">
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4" gutterBottom>
          Your Matches
        </Typography>
        {loading ? (
          <Typography variant="body1">Loading...</Typography>
        ) : (
          <>
            {matches.length > 0 ? (
              <List>
                {matches.map((match, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={
                        authData.userType === "jobseeker"
                          ? `Job ID: ${match.job_id}`
                          : `Jobseeker ID: ${match.jobseeker_id}`
                      }
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body1">No matches found.</Typography>
            )}
          </>
        )}
      </Box>
    </div>
  );
}

export default MatchesView;

