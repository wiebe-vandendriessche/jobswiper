import React, { useState } from "react";
import { TextField, Button, CircularProgress, Box, Typography } from "@mui/material";

const apiBaseUrl = "http://localhost:8081";
//const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
//const apiBaseUrl = "http://api_gateway:8080";

const AuthForm = ({ setIsAuthenticated, fetchUserAccount, handleSignedUp, setProfileUnCompleted }) => {
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
        setIsLogin(true); // Switch to login after sign-up
      }
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 400, margin: "auto", padding: 2 }}>
      <Typography variant="h4" align="center" gutterBottom>
        {isLogin ? "Login" : "Sign Up"}
      </Typography>

      {error && <Typography color="error" variant="body2" align="center">{error}</Typography>}

      <form onSubmit={handleSubmit}>
        <TextField
          label="Username"
          name="username"
          variant="outlined"
          fullWidth
          value={formData.username}
          onChange={handleInputChange}
          required
          sx={{ marginBottom: 2 }}
        />
        <TextField
          label="Password"
          name="password"
          type="password"
          variant="outlined"
          fullWidth
          value={formData.password}
          onChange={handleInputChange}
          required
          sx={{ marginBottom: 2 }}
        />

        <Button
          type="submit"
          variant="contained"
          fullWidth
          color="primary"
          disabled={loading}
          sx={{ marginBottom: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : isLogin ? "Login" : "Sign Up"}
        </Button>
      </form>

      <Box sx={{ textAlign: "center" }}>
        <Typography variant="body2" color="textSecondary" onClick={() => setIsLogin(!isLogin)} sx={{ cursor: "pointer" }}>
          {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
        </Typography>
      </Box>
    </Box>
  );
};

export default AuthForm;