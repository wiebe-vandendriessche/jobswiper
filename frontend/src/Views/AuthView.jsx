import React, { useState } from "react";
import { useEffect } from "react";

// const apiBaseUrl = process.env.REACT_APP_API_BASE_URL; // Use this with docker
const apiBaseUrl = "http://localhost:8080";               // Use this with vite dev server


function AuthView() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState(null);  // Holds user info (username and id)
  const [profileData, setProfileData] = useState(null); // Holds profile data
  const [profileForm, setProfileForm] = useState({
    username: "", // Make sure this matches the authenticated user's username
    first_name: "",
    last_name: "",
    email: "",
    location: "",
    phone_number: "",
    qualifications: [],
    salary: { min: 0, max: 300000 },
    education_level: "",
    years_of_experience: 0,
    availability: "",
    date_of_birth: "",
    interests: []
  });

  // Fetch user info when logged in
  useEffect(() => {
    const token = localStorage.getItem("jwtToken");
    if (token) {
      setIsAuthenticated(true);
      fetchUserAccount(token);
    }
  }, []);

  const fetchUserAccount = async (token) => {
    try {
      const response = await fetch(`${apiBaseUrl}/get-user-account`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error("Failed to fetch user account");
      const data = await response.json();
      setUserData(data);  // Store username and ID
    } catch (err) {
      console.error(err);
      setError("Failed to fetch user account");
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleProfileInputChange = (e) => {
    setProfileForm({ ...profileForm, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const endpoint = isLogin ? `${apiBaseUrl}/login` : `${apiBaseUrl}/sign-up`;

    const body = isLogin
      ? new URLSearchParams({
          username: formData.username,
          password: formData.password,
          grant_type: "password",
        })
      : JSON.stringify(formData);

    const headers = isLogin
      ? { "Content-Type": "application/x-www-form-urlencoded" }
      : { "Content-Type": "application/json" };

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers,
        body,
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.detail?.[0]?.msg || "Authentication failed");
      }

      const data = await response.json();
      const token = isLogin ? data.access_token : data; // Token format varies by endpoint

      if (isLogin) {
        // Save the token
        localStorage.setItem("jwtToken", token);
        setIsAuthenticated(true);
        fetchUserAccount(token); // Fetch the user's account info
        alert("Login successful!");
      } else {
        alert("Sign-up successful! Please log in.");
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("jwtToken");
    setIsAuthenticated(false);
    setUserData(null);
    setProfileData(null);
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    
    // Log the profile data to verify what is being sent
    console.log(profileForm);
  
    const token = localStorage.getItem("jwtToken");
  
    if (!token) {
      setError("You need to log in first.");
      return;
    }
  
    try {
      const response = await fetch(`${apiBaseUrl}/profile/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(profileForm),
      });
  
      if (!response.ok) throw new Error("Failed to create/update profile");
  
      const data = await response.json();
      setProfileData(data);  // Store the profile data
      alert("Profile created/updated successfully!");
    } catch (err) {
      setError(err.message || "Something went wrong");
    }
  };

  return (
    <div className="authView">
      {isAuthenticated ? (
        <div>
          <h1>Welcome, {userData?.username} (ID: {userData?.id})</h1>
          <button onClick={handleLogout}>Logout</button>
          <div>
            <h2>Profile Section</h2>
            <form onSubmit={handleProfileSubmit}>
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={profileForm.first_name}
                onChange={handleProfileInputChange}
              />
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                value={profileForm.last_name}
                onChange={handleProfileInputChange}
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={profileForm.email}
                onChange={handleProfileInputChange}
              />
              <input
                type="text"
                name="location"
                placeholder="Location"
                value={profileForm.location}
                onChange={handleProfileInputChange}
              />
              <input
                type="text"
                name="phone_number"
                placeholder="Phone Number"
                value={profileForm.phone_number}
                onChange={handleProfileInputChange}
              />
              <textarea
                name="qualifications"
                placeholder="Qualifications"
                value={profileForm.qualifications}
                onChange={handleProfileInputChange}
              />
              {/* Add other profile fields */}
              <button type="submit">Create/Update Profile</button>
            </form>
          </div>
        </div>
      ) : (
        <div>
          <h1>{isLogin ? "Login" : "Sign Up"}</h1>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleInputChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Processing..." : isLogin ? "Login" : "Sign Up"}
            </button>
          </form>
          <p onClick={() => setIsLogin(!isLogin)}>
            {isLogin
              ? "Don't have an account? Sign up"
              : "Already have an account? Login"}
          </p>
        </div>
      )}
    </div>
  );
}

export default AuthView;