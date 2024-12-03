import React, { useState } from "react";

const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:8080";


function AuthView() {
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

    const endpoint = isLogin
      ? (apiBaseUrl + "/login")
      : (apiBaseUrl + "/sign-up");

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
    <div className="authView">
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

export default AuthView;