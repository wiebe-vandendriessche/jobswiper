import React, { useState, useEffect, useContext } from "react";
import { Box, Button, Paper, Typography, TextField, Dialog, DialogActions, DialogContent, DialogTitle } from "@mui/material";
import { AuthContext } from "./../AuthContext";

const apiBaseUrl = "http://localhost:8081";

const JobDashboard = ({ profile, username }) => {
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

  const [swipedJob, setSwipedJob] = useState(null); // Job selected for swiping
  const [updateJob, setUpdateJob] = useState(null); // Job selected for update

  useEffect(() => {
    setAuthData({
      ...authData,
      selected_job_id: swipedJob?.id,
      selected_job_name: swipedJob?.title,
    });
  }, [swipedJob]);

  const getJwtToken = () => {
    return localStorage.getItem("jwtToken");
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setIsLoading(true);
    const token = getJwtToken();
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
      setError("Error fetching jobs: " + err.message);
      console.error("Error fetching jobs:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateJob = async () => {
    const token = getJwtToken();
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
        setJobs([...jobs, createdJob]);
        setShowCreateForm(false);
        setNewJob({
          title: "",
          company_name: "",
          location: "",
          job_type: "",
          description: "",
          responsibilities: "",
          requirements: "",
          salary: { min: 0, max: 300000 },
        });
        fetchJobs();
      } else {
        console.error("Failed to create job");
      }
    } catch (err) {
      console.error("Error creating job:", err);
    }
  };

  const handleUpdateJob = async () => {
    const token = getJwtToken();
    try {
      const response = await fetch(`${apiBaseUrl}/jobs/${updateJob.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...updateJob,
          responsibilities: updateJob.responsibilities.split(",").map((r) => r.trim()),
          requirements: updateJob.requirements.split(",").map((r) => r.trim()),
        }),
      });

      if (response.ok) {
        const updatedJob = await response.json();
        setJobs(
          jobs.map((job) => (job.id === updatedJob.id ? updatedJob : job))
        );
        setUpdateJob(null); // Close the update dialog
        fetchJobs();
      } else {
        console.error("Failed to update job");
      }
    } catch (err) {
      console.error("Error updating job:", err);
    }
  };

  const handleJobClick = (job) => {
    // This will highlight the job in green for swiping
    setSwipedJob(job);
  };

  const handleJobChange = (e) => {
    const { name, value } = e.target;
    setUpdateJob({
      ...updateJob,
      [name]: value,
    });
  };

  return (
    <Box component={Paper} sx={{ padding: 3, marginTop: 2 }}>
      <Typography variant="h5">Job Dashboard</Typography>

      {/* Button to create a new job */}
      <Button
        variant="contained"
        color="primary"
        sx={{ marginBottom: 3 }}
        onClick={() => {
          setShowCreateForm(true);
        }}
      >
        Create Job
      </Button>

      {isLoading ? (
        <Typography>Loading jobs...</Typography>
      ) : error ? (
        <Typography>{error}</Typography>
      ) : (
        <Box>
          <Typography variant="h6">Jobs</Typography>
          {jobs.length === 0 ? (
            <Typography>No jobs available.</Typography>
          ) : (
            <Box>
              {jobs.map((job) => (
                <Paper
                  key={job.id}
                  sx={{
                    padding: 2,
                    marginBottom: 2,
                    backgroundColor: swipedJob?.id === job.id ? "lightgreen" : "white",
                    cursor: "pointer",
                  }}
                  onClick={() => handleJobClick(job)} // Select for swiping (highlight green)
                >
                  <Typography variant="h6">{job.title}</Typography>
                  <Typography>{job.company_name}</Typography>
                  <Button
                    variant="outlined"
                    color="primary"
                    sx={{ marginTop: 1 }}
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent closing dialog on button click
                      setUpdateJob(job); // Open update dialog
                    }}
                  >
                    Update
                  </Button>
                </Paper>
              ))}
            </Box>
          )}
        </Box>
      )}

      {/* Create Job Dialog */}
      <Dialog open={showCreateForm} onClose={() => setShowCreateForm(false)}>
        <DialogTitle>Create Job</DialogTitle>
        <DialogContent>
          <TextField
            label="Job Title"
            fullWidth
            variant="outlined"
            value={newJob.title}
            onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Company Name"
            fullWidth
            variant="outlined"
            value={newJob.company_name}
            onChange={(e) => setNewJob({ ...newJob, company_name: e.target.value })}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Location"
            fullWidth
            variant="outlined"
            value={newJob.location}
            onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Job Type"
            fullWidth
            variant="outlined"
            value={newJob.job_type}
            onChange={(e) => setNewJob({ ...newJob, job_type: e.target.value })}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Description"
            fullWidth
            variant="outlined"
            value={newJob.description}
            onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Responsibilities"
            fullWidth
            variant="outlined"
            value={newJob.responsibilities}
            onChange={(e) => setNewJob({ ...newJob, responsibilities: e.target.value })}
            helperText="Comma-separated values"
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Requirements"
            fullWidth
            variant="outlined"
            value={newJob.requirements}
            onChange={(e) => setNewJob({ ...newJob, requirements: e.target.value })}
            helperText="Comma-separated values"
            sx={{ marginBottom: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowCreateForm(false)}>Cancel</Button>
          <Button onClick={handleCreateJob}>Create Job</Button>
        </DialogActions>
      </Dialog>

      {/* Update Job Dialog */}
      <Dialog open={Boolean(updateJob)} onClose={() => setUpdateJob(null)} >
        <DialogTitle >Update Job</DialogTitle>
        <DialogContent >
          <TextField
            label="Job Title"
            fullWidth
            variant="outlined"
            value={updateJob?.title || ""}
            name="title"
            onChange={handleJobChange}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Location"
            fullWidth
            variant="outlined"
            value={updateJob?.location || ""}
            name="location"
            onChange={handleJobChange}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Job Type"
            fullWidth
            variant="outlined"
            value={updateJob?.job_type || ""}
            name="job_type"
            onChange={handleJobChange}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Description"
            fullWidth
            variant="outlined"
            value={updateJob?.description || ""}
            name="description"
            onChange={handleJobChange}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Responsibilities"
            fullWidth
            variant="outlined"
            value={updateJob?.responsibilities || ""}
            name="responsibilities"
            onChange={handleJobChange}
            helperText="Comma-separated values"
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Requirements"
            fullWidth
            variant="outlined"
            value={updateJob?.requirements || ""}
            name="requirements"
            onChange={handleJobChange}
            helperText="Comma-separated values"
            sx={{ marginBottom: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUpdateJob(null)}>Cancel</Button>
          <Button onClick={handleUpdateJob}>Update Job</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default JobDashboard;
