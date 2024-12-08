import React, { useState, useContext } from 'react';
import { AuthContext } from './../AuthContext';
import { TextField, Button, Box, Typography, FormControlLabel, Checkbox } from '@mui/material';

const apiBaseUrl = "http://localhost:8081";
//const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
//const apiBaseUrl = "http://api_gateway:8080";

const ProfileCreate = ({ username, userid, setProfile, onLogout }) => {
  const { authData, setAuthData } = useContext(AuthContext);

  const [isRecruiter, setIsRecruiter] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    location: "",
    phone_number: "",
    qualifications: [],
    salary: {},
    education_level: "",
    years_of_experience: 0,
    availability: "",
    date_of_birth: "",
    interests: [],
    company_name: ""
  });

  const handleToggle = () => {
    setIsRecruiter(!isRecruiter);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = isRecruiter
      ? {
          username,
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          location: formData.location,
          phone_number: formData.phone_number,
          company_name: formData.company_name,
        }
      : {
          username,
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          location: formData.location,
          phone_number: formData.phone_number,
          qualifications: formData.qualifications,
          salary: formData.salary,
          education_level: formData.education_level,
          years_of_experience: formData.years_of_experience,
          availability: formData.availability,
          date_of_birth: formData.date_of_birth,
          interests: formData.interests,
        };

    try {
      const token = localStorage.getItem('jwtToken');
      const response = await fetch(`${apiBaseUrl}/profile/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.status === 401) {
        alert("Session expired or invalid token. Please log in again.");
        onLogout();
      } else if (response.ok) {
        alert("Profile created successfully!");
        setAuthData({ ...authData, selected_profile_name: username, selected_user_id: userid, userType: isRecruiter ? "recruiter" : "jobseeker" });
        setProfile(payload);    
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error creating profile:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
      <Typography variant="h4" align="center" gutterBottom>Create Profile</Typography>
      
      <FormControlLabel
        control={<Checkbox checked={isRecruiter} onChange={handleToggle} />}
        label={`Toggle to ${isRecruiter ? "Jobseeker" : "Recruiter"}`}
        sx={{ marginBottom: 2 }}
      />
      
      <form onSubmit={handleSubmit}>
        <TextField
          label="First Name"
          name="first_name"
          variant="outlined"
          fullWidth
          value={formData.first_name}
          onChange={handleChange}
          required
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Last Name"
          name="last_name"
          variant="outlined"
          fullWidth
          value={formData.last_name}
          onChange={handleChange}
          required
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Email"
          name="email"
          type="email"
          variant="outlined"
          fullWidth
          value={formData.email}
          onChange={handleChange}
          required
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Location"
          name="location"
          variant="outlined"
          fullWidth
          value={formData.location}
          onChange={handleChange}
          required
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Phone Number"
          name="phone_number"
          variant="outlined"
          fullWidth
          value={formData.phone_number}
          onChange={handleChange}
          sx={{ marginBottom: 2 }}
        />
        
        {isRecruiter ? (
          <TextField
            label="Company Name"
            name="company_name"
            variant="outlined"
            fullWidth
            value={formData.company_name}
            onChange={handleChange}
            required
            sx={{ marginBottom: 2 }}
          />
        ) : (
          <>
            <TextField
              label="Qualifications"
              name="qualifications"
              variant="outlined"
              fullWidth
              value={formData.qualifications}
              onChange={(e) => setFormData({ ...formData, qualifications: e.target.value.split(",") })}
              placeholder="Comma-separated values"
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Salary"
              name="salary"
              variant="outlined"
              fullWidth
              value={JSON.stringify(formData.salary)}
              onChange={(e) => setFormData({ ...formData, salary: JSON.parse(e.target.value || "{}") })}
              placeholder="JSON format"
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Education Level"
              name="education_level"
              variant="outlined"
              fullWidth
              value={formData.education_level}
              onChange={handleChange}
              required
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Years of Experience"
              name="years_of_experience"
              type="number"
              variant="outlined"
              fullWidth
              value={formData.years_of_experience}
              onChange={handleChange}
              required
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Availability"
              name="availability"
              variant="outlined"
              fullWidth
              value={formData.availability}
              onChange={handleChange}
              required
              sx={{ marginBottom: 2 }}
            />
            <TextField
              label="Date of Birth"
              name="date_of_birth"
              type="date"
              variant="outlined"
              fullWidth
              value={formData.date_of_birth}
              onChange={handleChange}
              sx={{ marginBottom: 2 }}
              slotProps={{
                inputLabel: {
                  shrink: true,  // Keeps the label above the input field
                },
              }}
            />
            <TextField
              label="Interests"
              name="interests"
              variant="outlined"
              fullWidth
              value={formData.interests}
              onChange={(e) => setFormData({ ...formData, interests: e.target.value.split(",") })}
              placeholder="Comma-separated values"
              sx={{ marginBottom: 2 }}
            />
          </>
        )}

        <Button variant="contained" color="primary" type="submit" fullWidth sx={{ marginTop: 2 }}>
          Create Profile
        </Button>
      </form>
    </Box>
  );
};

export default ProfileCreate;
