import React, { useState, useEffect } from "react";

//const apiBaseUrl = "http://api_gateway:8080";
const apiBaseUrl = "http://localhost:8081";
//const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;

const ProfileUpdate = ({ profile, username, fetchProfile, onLogout }) => {
    const [formData, setFormData] = useState({});
    const [isRecruiter, setIsRecruiter] = useState(false);

    useEffect(() => {
        // Determine if the user is a recruiter based on the presence of "company_name" in the profile
        setIsRecruiter(profile.hasOwnProperty("company_name"));

        setFormData(profile.hasOwnProperty("company_name")
            ? { company_name: profile.company_name || "" }
            : {
                email: profile.email || "",
                phone_number: profile.phone_number || "",
                location: profile.location || "",
                availability: profile.availability || "",
                salary: profile.salary || {},
                interests: profile.interests || [],
                qualifications: profile.qualifications || [],
            });
    }, [profile]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('jwtToken');
            const endpoint = isRecruiter
                ? `${apiBaseUrl}/profile/recruiter/${username}`
                : `${apiBaseUrl}/profile/jobseeker/${username}`;

            const response = await fetch(endpoint, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (response.status === 401) {
                alert("Session expired or invalid token. Please log in again.");
                onLogout();
            } else if (response.ok) {
                alert("Profile updated successfully!");
                // refetch the user profile
                fetchProfile();
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error("Error updating profile:", error);
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <div>
            <h2>Profile Update</h2>
            <form onSubmit={handleSubmit}>
                {isRecruiter ? (
                    <div>
                        <label>Company Name:</label>
                        <input
                            type="text"
                            name="company_name"
                            value={formData.company_name}
                            onChange={handleChange}
                            required
                        />
                    </div>
                ) : (
                    <>
                        <div>
                            <label>Email:</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <label>Phone Number:</label>
                            <input
                                type="text"
                                name="phone_number"
                                value={formData.phone_number}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <label>Location:</label>
                            <input
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <label>Availability:</label>
                            <input
                                type="text"
                                name="availability"
                                value={formData.availability}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <label>Salary:</label>
                            <input
                                type="text"
                                name="salary"
                                value={JSON.stringify(formData.salary)}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        salary: JSON.parse(e.target.value || "{}"),
                                    })
                                }
                                placeholder="JSON format"
                            />
                        </div>
                        <div>
                            <label>Interests:</label>
                            <input
                                type="text"
                                name="interests"
                                value={formData.interests?.join(",") || ""} // Safely handle undefined or empty array
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        interests: e.target.value.split(","),
                                    })
                                }
                                placeholder="Comma-separated values"
                            />
                        </div>
                        <div>
                            <label>Qualifications:</label>
                            <input
                                type="text"
                                name="qualifications"
                                value={formData.qualifications?.join(",") || ""} // Safely handle undefined or empty array
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        qualifications: e.target.value.split(","),
                                    })
                                }
                                placeholder="Comma-separated values"
                            />
                        </div>
                    </>
                )}
                <button type="submit">Update Profile</button>
            </form>
        </div>
    );
};

export default ProfileUpdate;
