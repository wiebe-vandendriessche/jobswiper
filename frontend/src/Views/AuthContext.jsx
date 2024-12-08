import React, { createContext, useEffect, useState } from "react";

// Create the context
export const AuthContext = createContext();

// Provide the context
export const AuthProvider = ({ children }) => {

    const [authData, setAuthData] = useState(() => {

        const storedData = localStorage.getItem("authData");
        return storedData ? JSON.parse(storedData) :
            {
                selected_user_id: "",
                selected_profile_name: "",
                userType: "",
                selected_job_id: null,
                selected_job_name: "",
            };
    });

    // Save to localStorage whenever authData changes
    useEffect(() => {
        localStorage.setItem("authData", JSON.stringify(authData));
    }, [authData]);

    return (
        <AuthContext.Provider value={{ authData, setAuthData }}>
            {children}
        </AuthContext.Provider>
    );
};