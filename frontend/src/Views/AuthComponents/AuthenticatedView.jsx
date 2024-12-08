import React, { useEffect, useState } from 'react';
import ProfileCreate from './ProfileCreate';
import ProfileUpdate from './ProfileUpdate';
import JobDashboard from './JobDashboard';
import { useContext } from 'react';
import { AuthContext } from './../AuthContext';

//const apiBaseUrl = "http://api_gateway:8080";
const apiBaseUrl = "http://localhost:8081";
//const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;

const AuthenticatedView = ({ userData, onLogout}) => {
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
    <div>
      <h2>Jobseeker Profile</h2>
      <p><strong>Username:</strong> {profile.username}</p>
      <p><strong>First Name:</strong> {profile.first_name}</p>
      <p><strong>Last Name:</strong> {profile.last_name}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <p><strong>Location:</strong> {profile.location}</p>
      <p><strong>Phone Number:</strong> {profile.phone_number || "Not provided"}</p>
      <p><strong>Qualifications:</strong> {profile.qualifications.join(', ')}</p>
      <p><strong>Salary:</strong> {JSON.stringify(profile.salary)}</p>
      <p><strong>Education Level:</strong> {profile.education_level}</p>
      <p><strong>Years of Experience:</strong> {profile.years_of_experience}</p>
      <p><strong>Availability:</strong> {profile.availability}</p>
      <p><strong>Date of Birth:</strong> {profile.date_of_birth || "Not provided"}</p>
      <p><strong>Interests:</strong> {profile.interests.join(', ')}</p>
      <ProfileUpdate profile={profile} username={userData.username} fetchProfile={fetchProfile} onLogout={onLogout} />
    </div>
  );

  const renderRecruiterProfile = (profile) => (
    <div>
      <h2>Recruiter Profile</h2>
      <p><strong>Username:</strong> {profile.username}</p>
      <p><strong>First Name:</strong> {profile.first_name}</p>
      <p><strong>Last Name:</strong> {profile.last_name}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <p><strong>Location:</strong> {profile.location}</p>
      <p><strong>Phone Number:</strong> {profile.phone_number || "Not provided"}</p>
      <p><strong>Company Name:</strong> {profile.company_name}</p>
      <ProfileUpdate profile={profile} username={userData.username} fetchProfile={fetchProfile} onLogout={onLogout} />
      <JobDashboard profile={profile} username={userData.username}/>
    </div>
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (hasError) {
    return <div>There was an error loading your profile. Please try again later.</div>;
  }

  return (
    <div>
      <h1>Welcome, {userData?.username} (ID: {userData?.id})</h1>
      <button onClick={onLogout}>Logout</button>

      {profile ? (
        profile.company_name
          ? renderRecruiterProfile(profile)
          : renderJobseekerProfile(profile)
      ) : (
        <div>
          <h2>No Profile Found</h2>
          <ProfileCreate username={userData.username} setProfile={setProfile} onLogout={onLogout} />
        </div>
      )}
    </div>
  );
};

export default AuthenticatedView;

