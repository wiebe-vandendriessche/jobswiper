import React, { useState, useEffect } from "react";

const apiBaseUrl = "http://localhost:8080";

function AuthView() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState(null);

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
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Failed to fetch user account");
      const data = await response.json();
      setUserData(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("jwtToken");
    setIsAuthenticated(false);
    setUserData(null);
  };

  return (
    <div className="authView">
      {isAuthenticated ? (
        <AuthenticatedView userData={userData} onLogout={handleLogout} />
      ) : (
        <AuthForm setIsAuthenticated={setIsAuthenticated} fetchUserAccount={fetchUserAccount} />
      )}
    </div>
  );
}

function AuthForm({ setIsAuthenticated, fetchUserAccount }) {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const endpoint = isLogin ? `${apiBaseUrl}/login` : `${apiBaseUrl}/sign-up`;
    const body = isLogin
      ? new URLSearchParams({ username: formData.username, password: formData.password, grant_type: "password" })
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
      if (isLogin) {
        const token = data.access_token;
        localStorage.setItem("jwtToken", token);
        setIsAuthenticated(true);
        fetchUserAccount(token);
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

  return (
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
        {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
      </p>
    </div>
  );
}

function AuthenticatedView({ userData, onLogout }) {
  const [profileData, setProfileData] = useState(null);
  const [profileForm, setProfileForm] = useState({
    username: "",
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
    interests: [],
  });

  useEffect(() => {
    if (userData?.username) {
      setProfileForm((prevForm) => ({
        ...prevForm,
        username: userData.username, // Update the username field when userData changes
      }));
    }
  }, [userData]);

  const handleProfileInputChange = (e) => {
    setProfileForm({ ...profileForm, [e.target.name]: e.target.value });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("jwtToken");
    if (!token) return;

    try {
      const response = await fetch(`${apiBaseUrl}/profile/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(profileForm),
      });

      if (!response.ok) throw new Error("Failed to create/update profile");

      const data = await response.json();
      setProfileData(data);
      alert("Profile created/updated successfully!");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Welcome, {userData?.username} (ID: {userData?.id})</h1>
      <button onClick={onLogout}>Logout</button>
      <ProfileForm
        profileForm={profileForm}
        onInputChange={handleProfileInputChange}
        onSubmit={handleProfileSubmit}
      />
    </div>
  );
}

function ProfileForm({ profileForm, onInputChange, onSubmit }) {
  const handleDateChange = (e) => {
    const value = e.target.value;
    const isValidDate = !isNaN(new Date(value).getTime());
    onInputChange({
      target: {
        name: "date_of_birth",
        value: isValidDate ? value : null, // Send null if the date is invalid or empty
      },
    });
  };

  return (
    <form onSubmit={onSubmit}>
      <input
        type="text"
        name="first_name"
        placeholder="First Name"
        value={profileForm.first_name}
        onChange={onInputChange}
      />
      <input
        type="text"
        name="last_name"
        placeholder="Last Name"
        value={profileForm.last_name}
        onChange={onInputChange}
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={profileForm.email}
        onChange={onInputChange}
      />
      <input
        type="text"
        name="location"
        placeholder="Location"
        value={profileForm.location}
        onChange={onInputChange}
      />
      <input
        type="text"
        name="phone_number"
        placeholder="Phone Number"
        value={profileForm.phone_number}
        onChange={onInputChange}
      />
      <textarea
        name="qualifications"
        placeholder="Qualifications"
        value={profileForm.qualifications}
        onChange={onInputChange}
      />
      <input
        type="date"
        name="date_of_birth"
        placeholder="Date of Birth"
        value={profileForm.date_of_birth || ""}
        onChange={handleDateChange}
      />
      {/* Add other profile fields as needed */}
      <button type="submit">Create/Update Profile</button>
    </form>
  );
}

export default AuthView;