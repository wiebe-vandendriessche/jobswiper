import React, { useState, useEffect } from "react";
import { TextField, Button, Box, Typography, Paper, Grid } from "@mui/material";

// const apiBaseUrl = "http://api_gateway:8080";
const apiBaseUrl = "http://localhost:8081";
// const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;

const ProfileUpdate = ({ profile, username, fetchProfile, onLogout }) => {
  const [formData, setFormData] = useState({});
  const [isRecruiter, setIsRecruiter] = useState(false);

  useEffect(() => {
    // Determine if the user is a recruiter based on the presence of "company_name" in the profile
    setIsRecruiter(profile.hasOwnProperty("company_name"));

    setFormData(
      profile.hasOwnProperty("company_name")
        ? { company_name: profile.company_name || "" }
        : {
            email: profile.email || "",
            phone_number: profile.phone_number || "",
            location: profile.location || "",
            availability: profile.availability || "",
            salary: profile.salary || {},
            interests: profile.interests || [],
            qualifications: profile.qualifications || [],
          }
    );
  }, [profile]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("jwtToken");
      const endpoint = isRecruiter
        ? `${apiBaseUrl}/profile/recruiter/${username}`
        : `${apiBaseUrl}/profile/jobseeker/${username}`;

      const response = await fetch(endpoint, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.status === 401) {
        alert("Session expired or invalid token. Please log in again.");
        onLogout();
      } else if (response.ok) {
        alert("Profile updated successfully!");
        // refetch the user profile
        fetchProfile();
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <Box component={Paper} sx={{ padding: 3, marginTop: 2 }}>
      <Typography variant="h5" gutterBottom>
        Profile Update
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {isRecruiter ? (
            <Grid item xs={12}>
              <TextField
                label="Company Name"
                name="company_name"
                value={formData.company_name}
                onChange={handleChange}
                fullWidth
                required
                variant="outlined"
              />
            </Grid>
          ) : (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Email"
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  fullWidth
                  required
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Phone Number"
                  name="phone_number"
                  value={formData.phone_number}
                  onChange={handleChange}
                  fullWidth
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  fullWidth
                  required
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Availability"
                  name="availability"
                  value={formData.availability}
                  onChange={handleChange}
                  fullWidth
                  required
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Salary (JSON format)"
                  name="salary"
                  value={JSON.stringify(formData.salary)}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      salary: JSON.parse(e.target.value || "{}"),
                    })
                  }
                  fullWidth
                  placeholder="JSON format"
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Interests (comma-separated)"
                  name="interests"
                  value={formData.interests?.join(",") || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      interests: e.target.value.split(","),
                    })
                  }
                  fullWidth
                  placeholder="Comma-separated values"
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Qualifications (comma-separated)"
                  name="qualifications"
                  value={formData.qualifications?.join(",") || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      qualifications: e.target.value.split(","),
                    })
                  }
                  fullWidth
                  placeholder="Comma-separated values"
                  variant="outlined"
                />
              </Grid>
            </>
          )}
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Update Profile
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
};

export default ProfileUpdate;
