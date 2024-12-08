import React, { useEffect, useState } from 'react';
import ProfileCreate from './ProfileCreate';
import ProfileUpdate from './ProfileUpdate';
import JobDashboard from './JobDashboard';
import { useContext } from 'react';
import { AuthContext } from './../AuthContext';
import { Button, Typography, CircularProgress, Box, Paper } from '@mui/material';

const apiBaseUrl = "http://localhost:8081";

const AuthenticatedView = ({ userData, onLogout }) => {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  // context for full application
  const { authData, setAuthData } = useContext(AuthContext);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('jwtToken');
      const response = await fetch(`${apiBaseUrl}/profile/${userData?.username}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 200) {
        const data = await response.json();
        setProfile(data); // update profile in component state
        setAuthData({
          selected_user_id: data.id,
          selected_profile_name: data.username,
          userType: data.company_name ? 'recruiter' : 'jobseeker',
          selected_job_id: null,
          selected_job_name: "",
        });
      } else if (response.status === 404) {
        const errorData = await response.json();
        console.warn('Profile not found:', errorData.detail.detail);
        setProfile(null);
      } else {
        setHasError(true);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
      setHasError(true);
      setAuthData({
        selected_user_id: '',
        userType: '',
        selected_job_id: null,
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (userData?.username) {
      fetchProfile();
    }
  }, [userData?.username]);

  const renderJobseekerProfile = (profile) => (
    <Box component={Paper} sx={{ padding: 4, marginTop: 2 }}>
      <Typography variant="h5">Jobseeker Profile</Typography>
      <Typography><strong>Username:</strong> {profile.username}</Typography>
      <Typography><strong>First Name:</strong> {profile.first_name}</Typography>
      <Typography><strong>Last Name:</strong> {profile.last_name}</Typography>
      <Typography><strong>Email:</strong> {profile.email}</Typography>
      <Typography><strong>Location:</strong> {profile.location}</Typography>
      <Typography><strong>Phone Number:</strong> {profile.phone_number || "Not provided"}</Typography>
      <Typography><strong>Qualifications:</strong> {profile.qualifications.join(', ')}</Typography>
      <Typography><strong>Salary:</strong> {JSON.stringify(profile.salary)}</Typography>
      <Typography><strong>Education Level:</strong> {profile.education_level}</Typography>
      <Typography><strong>Years of Experience:</strong> {profile.years_of_experience}</Typography>
      <Typography><strong>Availability:</strong> {profile.availability}</Typography>
      <Typography><strong>Date of Birth:</strong> {profile.date_of_birth || "Not provided"}</Typography>
      <Typography><strong>Interests:</strong> {profile.interests.join(', ')}</Typography>
      <Box sx={{ marginTop: 4 }}>
        <ProfileUpdate profile={profile} username={userData.username} fetchProfile={fetchProfile} onLogout={onLogout} />
      </Box>
    </Box >
  );

  const renderRecruiterProfile = (profile) => (
    <Box component={Paper} sx={{ padding: 4, marginTop: 2 }}>
      <Typography variant="h5">Recruiter Profile</Typography>
      <Typography><strong>Username:</strong> {profile.username}</Typography>
      <Typography><strong>First Name:</strong> {profile.first_name}</Typography>
      <Typography><strong>Last Name:</strong> {profile.last_name}</Typography>
      <Typography><strong>Email:</strong> {profile.email}</Typography>
      <Typography><strong>Location:</strong> {profile.location}</Typography>
      <Typography><strong>Phone Number:</strong> {profile.phone_number || "Not provided"}</Typography>
      <Typography><strong>Company Name:</strong> {profile.company_name}</Typography>
      {/* Profile Update Section with Margin */}
      <Box sx={{ marginTop: 4 }}>
        <ProfileUpdate profile={profile} username={userData.username} fetchProfile={fetchProfile} onLogout={onLogout} />
      </Box>

      {/* Job Dashboard Section with Margin */}
      <Box sx={{ marginTop: 4 }}>
        <JobDashboard profile={profile} username={userData.username} />
      </Box>
    </Box>
  );

  if (isLoading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 4 }}><CircularProgress /></Box>;
  }

  if (hasError) {
    return <Typography color="error" variant="h6" sx={{ marginTop: 2 }}>There was an error loading your profile. Please try again later.</Typography>;
  }

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        Welcome, {userData?.username}
      </Typography>
      <Typography variant="body2" sx={{ color: 'text.secondary', marginBottom: 2 }}>
        (ID: {userData?.id})
      </Typography>      <Button variant="contained" color="primary" onClick={onLogout} sx={{ marginBottom: 2 }}>
        Logout
      </Button>

      {profile ? (
        profile.company_name
          ? renderRecruiterProfile(profile)
          : renderJobseekerProfile(profile)
      ) : (
        <div>
          <Typography variant="h6" sx={{ marginBottom: 2 }}>No Profile Found</Typography>
          <ProfileCreate username={userData.username} userid={userData.id} setProfile={setProfile} onLogout={onLogout} />
        </div>
      )}
    </Box>
  );
};

export default AuthenticatedView;