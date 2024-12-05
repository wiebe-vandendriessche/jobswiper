import React, { useState, useEffect } from "react";
import ProfileUpdate from "./AuthComponents/ProfileUpdate";

const apiBaseUrl = "http://localhost:8080";

function AuthView() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState(null);
  const [profileUnCompleted, setProfileUnCompleted] = useState(false);

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
    setProfileUnCompleted(false); // Reset profile state on logout
  };

  const handleSignedUp = () => {
    setProfileUnCompleted(true); // Show CreateProfileView after sign-up
  };

  const handleProfileCreated = () => {
    setProfileUnCompleted(false); // Profile is now complete
    // After profile creation, log the user in (simulated)
    handleLogout();
  };

  return (
    <div className="authView">
      {isAuthenticated ? (
        <AuthenticatedView userData={userData} onLogout={handleLogout} />
      ) : (
        profileUnCompleted ? (
          <CreateProfileView handleProfileCreated={handleProfileCreated} />
        ) : (
          <AuthForm
          setIsAuthenticated={setIsAuthenticated}
          fetchUserAccount={fetchUserAccount}
          handleSignedUp={handleSignedUp}
          setProfileUnCompleted={setProfileUnCompleted}
        />
        )
      )}
    </div>
  );
}


function AuthForm({ setIsAuthenticated, fetchUserAccount, handleSignedUp, setProfileUnCompleted }) {
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
        alert("Sign-up successful! Please create your profile.");
        handleSignedUp(); // Trigger the profile creation flow
        setIsLogin(true); // Switch to login after sign-up
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
  return (
    <div>
      <h1>Welcome, {userData?.username} (ID: {userData?.id})</h1>
      <button onClick={onLogout}>Logout</button>
      <ProfileUpdate />
    </div>
  );
}

function CreateProfileView({ handleProfileCreated }) {
  const handleCreateProfile = () => {
    // Simulate profile creation (this could be a form submission or similar)
    alert("Profile created successfully!");
    handleProfileCreated(); // Notify that the profile is created
  };

  return (
    <div>
      <h1>Create Profile</h1>
      <button onClick={handleCreateProfile}>Create Profile</button>
    </div>
  );
}


export default AuthView;