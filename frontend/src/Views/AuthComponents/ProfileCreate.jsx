import React, { useState } from 'react';

const ProfileCreate = ({ username, setProfile, onLogout }) => {
    const [isRecruiter, setIsRecruiter] = useState(false);
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        location: "",
        phone_number: "",
        qualifications: [],
        salary: {},
        education_level: "",
        years_of_experience: 0,
        availability: "",
        date_of_birth: "",
        interests: [],
        company_name: ""
    });

    const handleToggle = () => {
        setIsRecruiter(!isRecruiter);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = isRecruiter
            ? {
                  username,
                  first_name: formData.first_name,
                  last_name: formData.last_name,
                  email: formData.email,
                  location: formData.location,
                  phone_number: formData.phone_number,
                  company_name: formData.company_name,
              }
            : {
                  username,
                  first_name: formData.first_name,
                  last_name: formData.last_name,
                  email: formData.email,
                  location: formData.location,
                  phone_number: formData.phone_number,
                  qualifications: formData.qualifications,
                  salary: formData.salary,
                  education_level: formData.education_level,
                  years_of_experience: formData.years_of_experience,
                  availability: formData.availability,
                  date_of_birth: formData.date_of_birth,
                  interests: formData.interests,
              };

        try {
            const token = localStorage.getItem('jwtToken');
            const response = await fetch("http://localhost:8080/profile/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            });

            if (response.status === 401) {
                alert("Session expired or invalid token. Please log in again.");
                onLogout();
            } else if (response.ok) {
                alert("Profile created successfully!");
                setProfile(payload);    
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error("Error creating profile:", error);
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <div>
            <h1>Create Profile</h1>
            <button onClick={handleToggle}>
                Toggle to {isRecruiter ? "Jobseeker" : "Recruiter"}
            </button>

            <form onSubmit={handleSubmit}>
                <div>
                    <label>First Name:</label>
                    <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Last Name:</label>
                    <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                    />
                </div>
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
                    <label>Phone Number:</label>
                    <input
                        type="text"
                        name="phone_number"
                        value={formData.phone_number}
                        onChange={handleChange}
                    />
                </div>

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
                            <label>Qualifications:</label>
                            <input
                                type="text"
                                name="qualifications"
                                value={formData.qualifications}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        qualifications: e.target.value.split(","),
                                    })
                                }
                                placeholder="Comma-separated values"
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
                            <label>Education Level:</label>
                            <input
                                type="text"
                                name="education_level"
                                value={formData.education_level}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <label>Years of Experience:</label>
                            <input
                                type="number"
                                name="years_of_experience"
                                value={formData.years_of_experience}
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
                            <label>Date of Birth:</label>
                            <input
                                type="date"
                                name="date_of_birth"
                                value={formData.date_of_birth}
                                onChange={handleChange}
                            />
                        </div>
                        <div>
                            <label>Interests:</label>
                            <input
                                type="text"
                                name="interests"
                                value={formData.interests}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        interests: e.target.value.split(","),
                                    })
                                }
                                placeholder="Comma-separated values"
                            />
                        </div>
                    </>
                )}

                <button type="submit">Create Profile</button>
            </form>
        </div>
    );
};

export default ProfileCreate;
