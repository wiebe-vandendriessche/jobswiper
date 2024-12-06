import React, { useState, useEffect } from "react";
import AuthForm from "./AuthComponents/AuthForm";
import AuthenticatedView from "./AuthComponents/AuthenticatedView";

//const apiBaseUrl = "http://api_gateway:8080";
const apiBaseUrl = "http://localhost:8080";
//const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
console.log("API Base URL:", apiBaseUrl);

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
  
      if (response.status === 401) {
        handleLogout(); // Call logout to reset state
      } else if (!response.ok) {
        throw new Error("Failed to fetch user account");
      } else {
        const data = await response.json();
        setUserData(data);
      }
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
        <AuthenticatedView userData={userData} onLogout={handleLogout}/>
      ) : (
        <AuthForm
          setIsAuthenticated={setIsAuthenticated}
          fetchUserAccount={fetchUserAccount}
        />
      )}
    </div>
  );
}
export default AuthView;