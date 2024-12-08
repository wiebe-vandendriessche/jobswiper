import React from "react";
import { useState, useEffect } from "react";
import { useContext } from "react";
import { AuthContext } from "./../AuthContext";

const apiBaseUrl = "http://localhost:8081";

const JobDashboard = ({ profile, username }) => {
    // context
    const { authData, setAuthData } = useContext(AuthContext);

    const [jobs, setJobs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [newJob, setNewJob] = useState({
        title: "",
        company_name: "",
        location: "",
        job_type: "",
        description: "",
        responsibilities: "",
        requirements: "",
        salary: { min: 0, max: 300000 },
    });
    const [selectedJob, setSelectedJob] = useState(null);

    // Function to get the JWT token from localStorage
    const getJwtToken = () => {
        return localStorage.getItem("jwtToken");
    };

    useEffect(() => {
        fetchJobs();
    }, []);

    // Fetch all jobs for the recruiter
    const fetchJobs = async () => {
        setIsLoading(true);
        const token = getJwtToken(); // Get token from localStorage
        try {
            const response = await fetch(`${apiBaseUrl}/jobs/`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                // Convert responsibilities and requirements back to comma-separated strings for display
                const updatedData = data.map((job) => ({
                    ...job,
                    responsibilities: job.responsibilities.join(", "),
                    requirements: job.requirements.join(", "),
                }));
                setJobs(updatedData);
                setError(null);
            } else {
                throw new Error("Failed to fetch jobs");
            }
        } catch (err) {
            setError("Error fetching jobs: " + err.message); // Set error state
            console.error("Error fetching jobs:", err);
        } finally {
            setIsLoading(false); // Set loading state to false after data fetching
        }
    };

    // Create a new job
    const handleCreateJob = async () => {
        const token = getJwtToken(); // Get token from localStorage
        try {
            const response = await fetch(`${apiBaseUrl}/jobs/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    id: "",
                    ...newJob,
                    responsibilities: newJob.responsibilities.split(",").map((r) => r.trim()),
                    requirements: newJob.requirements.split(",").map((r) => r.trim()),
                }),
            });

            if (response.ok) {
                const createdJob = await response.json();
                setJobs([...jobs, createdJob]); // Add the newly created job to the list
                setShowCreateForm(false); // Close the form
                setNewJob({
                    title: "",
                    company_name: "",
                    location: "",
                    job_type: "",
                    description: "",
                    responsibilities: "",
                    requirements: "",
                    salary: { min: null, max: null },
                });
                fetchJobs(); // Fetch jobs again to update the list
            } else {
                console.error("Failed to create job");
            }
        } catch (err) {
            console.error("Error creating job:", err);
        }
    };

    // Update an existing job
    const handleUpdateJob = async () => {
        const token = getJwtToken(); // Get token from localStorage
        try {
            const response = await fetch(`${apiBaseUrl}/jobs/${selectedJob.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    ...selectedJob,
                    responsibilities: selectedJob.responsibilities.split(",").map((r) => r.trim()),
                    requirements: selectedJob.requirements.split(",").map((r) => r.trim()),
                }),
            });

            if (response.ok) {
                const updatedJob = await response.json();
                setJobs(
                    jobs.map((job) => (job.id === updatedJob.id ? updatedJob : job))
                );
                setSelectedJob(null); // Close update form
            } else {
                console.error("Failed to update job");
            }
        } catch (err) {
            console.error("Error updating job:", err);
        }
    };

    // Handle clicking a job to edit it
    const handleJobClick = (job) => {
        setSelectedJob(job); // Set the selected job for updating
        setAuthData({
            ...authData,
            selected_job_id: job.id,
            selected_job_name: job.title,
        });
        setShowCreateForm(false); // Close the create form when updating a job
    };

    // Handle form changes for creating or updating a job
    const handleJobChange = (e) => {
        const { name, value } = e.target;
        if (selectedJob) {
            setSelectedJob({
                ...selectedJob,
                [name]: value,
            });
        } else {
            setNewJob({
                ...newJob,
                [name]: value,
            });
        }
    };

    // Close the update form
    const handleCloseUpdateForm = () => {
        setSelectedJob(null); // Close the update form
    };


    return (
        <div>
            <h1>Job Dashboard</h1>
            <button
                onClick={() => {
                    setShowCreateForm(!showCreateForm);
                    setSelectedJob(null); // Close the update form when creating a new job
                }}
            >
                {showCreateForm ? "Cancel" : "Create Job"}
            </button>

            {showCreateForm && (
                <div>
                    <h2>Create Job</h2>
                    <form onSubmit={(e) => e.preventDefault()}>
                        <div>
                            <label htmlFor="title">Job Title</label>
                            <input
                                type="text"
                                id="title"
                                name="title"
                                placeholder="Job Title"
                                value={newJob.title}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="company_name">Company Name</label>
                            <input
                                type="text"
                                id="company_name"
                                name="company_name"
                                placeholder="Company Name"
                                value={newJob.company_name}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="location">Location</label>
                            <input
                                type="text"
                                id="location"
                                name="location"
                                placeholder="Location"
                                value={newJob.location}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="job_type">Job Type</label>
                            <input
                                type="text"
                                id="job_type"
                                name="job_type"
                                placeholder="Job Type"
                                value={newJob.job_type}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="description">Description</label>
                            <textarea
                                id="description"
                                name="description"
                                placeholder="Description"
                                value={newJob.description}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="responsibilities">Responsibilities</label>
                            <textarea
                                id="responsibilities"
                                name="responsibilities"
                                placeholder="Responsibilities (comma-separated)"
                                value={newJob.responsibilities}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="requirements">Requirements</label>
                            <textarea
                                id="requirements"
                                name="requirements"
                                placeholder="Requirements (comma-separated)"
                                value={newJob.requirements}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="salary">Salary (min, max)</label>
                            <input
                                type="text"
                                id="salary"
                                name="salary"
                                value={JSON.stringify(newJob.salary)}  // Convert salary object to JSON string for display
                                onChange={handleJobChange}  // Handle JSON input change
                                placeholder='{"min": 0, "max": 300000}'  // Provide example of JSON format
                            />
                        </div>
                        <button type="button" onClick={handleCreateJob}>
                            Create Job
                        </button>
                    </form>
                </div>
            )}

            {isLoading ? (
                <div>Loading jobs...</div>
            ) : error ? (
                <div>{error}</div>
            ) : (
                <div>
                    <h2>Jobs</h2>
                    <ul>
                        {jobs.length === 0 ? (
                            <li>No jobs available.</li>
                        ) : (
                            jobs.map((job) => (
                                <li key={job.id}>
                                    <h3 onClick={() => handleJobClick(job)}>{job.title}</h3>
                                </li>
                            ))
                        )}
                    </ul>
                </div>
            )}

            {selectedJob && (
                <div>
                    <h2>Update Job</h2>
                    <button onClick={handleCloseUpdateForm}>Close Update</button>
                    <form onSubmit={(e) => e.preventDefault()}>
                        <div>
                            <label htmlFor="title">Job Title</label>
                            <input
                                type="text"
                                id="title"
                                name="title"
                                value={selectedJob.title}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="location">Location</label>
                            <input
                                type="text"
                                id="location"
                                name="location"
                                value={selectedJob.location}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="job_type">Job Type</label>
                            <input
                                type="text"
                                id="job_type"
                                name="job_type"
                                value={selectedJob.job_type}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="description">Description</label>
                            <textarea
                                id="description"
                                name="description"
                                value={selectedJob.description}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="responsibilities">Responsibilities</label>
                            <textarea
                                id="responsibilities"
                                name="responsibilities"
                                value={selectedJob.responsibilities}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="requirements">Requirements</label>
                            <textarea
                                id="requirements"
                                name="requirements"
                                value={selectedJob.requirements}
                                onChange={handleJobChange}
                            />
                        </div>
                        <div>
                            <label htmlFor="salary">Salary (min, max)</label>
                            <input
                                type="text"
                                id="salary"
                                name="salary"
                                value={JSON.stringify(selectedJob.salary)}  // Convert salary object to JSON string for display
                                onChange={handleJobChange}  // Handle JSON input change
                                placeholder='{"min": 0, "max": 300000}'  // Provide example of JSON format
                            />
                        </div>
                        <button type="button" onClick={handleUpdateJob}>
                            Update Job
                        </button>
                    </form>
                </div>
            )}
        </div>
    );
};
export default JobDashboard;