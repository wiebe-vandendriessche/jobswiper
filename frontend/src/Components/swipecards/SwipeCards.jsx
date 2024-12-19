import React, { useState, useEffect, useRef } from 'react';
import TinderCard from 'react-tinder-card';
import SwipeButton from './../swipebutton/SwipeButton';
import './swipecards.css';
import { useContext } from 'react';
import { AuthContext } from '../../Views/AuthContext';
import Alert from "@mui/material/Alert";
import { Box, Typography } from "@mui/material";
import { useLocation } from 'react-router-dom'; // Import useLocation

const apiBaseUrl = "http://localhost:8081";

function SwipeCards(props) {
    // Get the authData from the context
    const { authData, setAuthData } = useContext(AuthContext);

    const [recoms, setRecoms] = useState([]); // Will hold the recommendations (jobs or profiles)
    const [details, setDetails] = useState([]); // Will hold detailed data for each recommendation
    const [lastDirection, setLastDirection] = useState();
    const [isSwiping, setIsSwiping] = useState(false); // Track swipe state
    const childRefs = useRef([]);
    const location = useLocation(); // Track the current location (route)

    const jwtToken = localStorage.getItem("jwtToken");

    // Fetch details of jobseeker or job preview by UUID
    const fetchDetails = async (uuid) => {
        const headers = {
            'Authorization': `Bearer ${jwtToken}`,
            'Content-Type': 'application/json',
        };

        let response;
        let data;

        if (authData.userType === "recruiter") {
            // Fetch jobseeker details
            response = await fetch(`${apiBaseUrl}/profile/${uuid}/preview`, { method: 'GET', headers });
            data = await response.json();
            console.log("Jobseeker details:", data);
        } else if (authData.userType === "jobseeker") {
            // Fetch job details
            response = await fetch(`${apiBaseUrl}/jobs/${uuid}/preview`, { method: 'GET', headers });
            data = await response.json();
            console.log("Job details:", data);
        }

        return data;
    };

    // Fetch recommendations based on the user type (jobseeker or recruiter)
    useEffect(() => {
        console.log("useEffect triggered");

        const fetchRecommendations = async () => {
            // Ensure necessary data exists before attempting to fetch recommendations
            if (!authData.userType || (!authData.selected_user_id && !authData.selected_job_id)) {
                console.log("No valid user/job ID found, skipping recommendation fetch.");
                return; // Exit early if no selected user/job id
            }

            try {
                const headers = {
                    'Authorization': `Bearer ${jwtToken}`,
                    'Content-Type': 'application/json',
                };

                let response;
                let data;

                if (authData.userType === "jobseeker") {
                    response = await fetch(`${apiBaseUrl}/matches/recommendations/user/${authData.selected_user_id}`, {
                        method: 'GET',
                        headers: headers,
                    });
                    data = await response.json();
                    console.log("Jobseeker recommendations:", data);
                } else if (authData.userType === "recruiter" && authData.selected_job_id) {
                    response = await fetch(`${apiBaseUrl}/matches/recommendations/job/${authData.selected_job_id}`, {
                        method: 'GET',
                        headers: headers,
                    });
                    data = await response.json();
                    console.log("Recruiter recommendations:", data);
                }

                // Check if the data is an array before attempting to filter or map
                if (Array.isArray(data)) {
                    setRecoms((prevRecoms) => {
                        const newRecoms = data.filter(item => !prevRecoms.includes(item));
                        return [...prevRecoms, ...newRecoms]; // Append the new recommendations
                    });

                    // Fetch details for each UUID
                    const fetchedDetails = await Promise.all(data.map(async (uuid) => {
                        const detailsData = await fetchDetails(uuid);
                        return { uuid, details: detailsData };
                    }));

                    // Update the details state with the fetched details
                    setDetails((prevDetails) => [
                        ...prevDetails,
                        ...fetchedDetails
                    ]);
                }
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            }
        };

        fetchRecommendations()
    }, [authData, jwtToken, location]); // Trigger only when authData or jwtToken changes

    const swipe = (dir) => {
        if (isSwiping) {
            console.log('Swipe action blocked because a swipe is already in progress.');
            return;
        }
        const activeIndex = recoms.length - 1;
        const activeCard = childRefs.current[activeIndex];
        if (activeCard) {
            console.log(`Swipe started: ${dir}`);
            setIsSwiping(true); // Set swiping state
            activeCard.swipe(dir); // Programmatically trigger swipe
        }
    };

    const swiped = async (direction, uuid) => {
        console.log(`Swiping: ${uuid} - Direction: ${direction}`);  // Confirm function execution
        setLastDirection(direction);

        try {
            const headers = {
                'Authorization': `Bearer ${jwtToken}`,
                'Content-Type': 'application/json',
            };

            const decision = direction === "right"; // Convert direction to a boolean
            let payload;
            let endpoint;

            console.log('authData:', authData);  // Check if user IDs and type are valid

            if (authData.userType === "jobseeker") {
                payload = {
                    user_id: authData.selected_user_id,
                    job_id: uuid,
                    recruiter_id: "", // Leave empty for jobseeker
                    decision: decision,
                };
                endpoint = `${apiBaseUrl}/matches/swipe/user`;
            } else if (authData.userType === "recruiter") {
                if (!authData.selected_job_id) {
                    console.error("No job selected for the recruiter. Cannot register swipe.");
                    return;
                }

                payload = {
                    user_id: uuid,
                    job_id: authData.selected_job_id,
                    recruiter_id: authData.selected_user_id,
                    decision: decision,
                };
                endpoint = `${apiBaseUrl}/matches/swipe/job`;
            }

            // Log the payload and endpoint
            console.log('Payload:', payload);
            console.log('Endpoint:', endpoint);

            // Make the POST request to register the swipe
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`Failed to register swipe: ${response.statusText}`);
            }

            console.log("Swipe successfully registered!");
        } catch (error) {
            console.error("Error registering swipe:", error);
        }
    };

    const outOfFrame = (name) => {
        console.log(`${name} left the screen`);
        setRecoms((prevRecoms) => prevRecoms.filter((item) => item !== name)); // Remove card
        setIsSwiping(false); // Reset swiping state
    };

    return (
        <>
            <div className="swipeCards__contextContainer">
                <div className="swipeCards__contextInfo">
                    <Box sx={{ marginBottom: 2 }}>
                        {authData.selected_profile_name && (
                            <Typography variant="h6">
                                Swiping for {authData.userType}: {authData.selected_profile_name}{" "}
                                {authData.userType === "recruiter" && authData.selected_job_id && (
                                    <span>on job: {authData.selected_job_name}</span>
                                )}
                            </Typography>
                        )}
                    </Box>
                </div>

                {authData.userType === "recruiter" && !authData.selected_job_id && (
                    <Alert severity="warning">
                        Please select a job before swiping on jobseeker profiles.
                    </Alert>
                )}
            </div>
            <div className="swipeCards">
                <div className="swipeCards__cardContainer">
                    {details.length > 0 ? (
                        details.map(({ uuid, details }, index) => (
                            <TinderCard
                                ref={(el) => (childRefs.current[index] = el)}
                                key={uuid}
                                className="swipe"
                                preventSwipe={["up", "down"]}
                                onSwipe={(dir) => swiped(dir, uuid)}
                                onCardLeftScreen={() => outOfFrame(uuid)}
                            >
                                <div className="card">
                                    {authData.userType === "jobseeker" && details.title && (
                                        <>
                                            <img
                                                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTg88MX4ZhY_1jrNfztu9qY4zSF1oWLNqv2Jw&s" // Elon Musk's image URL
                                                alt="Elon Musk"
                                                className="jobseeker-avatar"
                                            />
                                            <h3>Job: {details.title}</h3>
                                            <p><strong>Company:</strong> {details.company_name}</p>
                                            <p><strong>Location:</strong> {details.location}</p>
                                            <p><strong>Job Type:</strong> {details.job_type}</p>
                                            <p><strong>Salary:</strong> {details.salary ? `${details.salary.min} - ${details.salary.max}` : "Salary not listed"}</p>
                                            <p><strong>Description:</strong> {details.description}</p>
                                            <p><strong>Responsibilities:</strong> {details.responsibilities ? details.responsibilities.join(', ') : "Not listed"}</p>
                                            <p><strong>Requirements:</strong> {details.requirements ? details.requirements.join(', ') : "Not listed"}</p>
                                        </>
                                    )}

                                    {authData.userType === "recruiter" && details.first_name && (
                                        <>
                                            <img
                                                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Elon_Musk_Royal_Society_crop.jpg/330px-Elon_Musk_Royal_Society_crop.jpg" // Elon Musk's image URL
                                                alt="Elon Musk"
                                                className="jobseeker-avatar"
                                            />
                                            <h3>Person: {details.first_name} {details.last_name}</h3>
                                            <p><strong>Location:</strong> {details.location}</p>
                                            <p><strong>Salary:</strong> {details.salary ? `${details.salary.min} - ${details.salary.max}` : "Salary not listed"}</p>
                                            <p><strong>Education Level:</strong> {details.education_level}</p>
                                            <p><strong>Years of Experience:</strong> {details.years_of_experience}</p>
                                            <p><strong>Availability:</strong> {details.availability}</p>
                                            <p><strong>Date of Birth:</strong> {details.date_of_birth}</p>
                                            <p><strong>Qualifications:</strong> {details.qualifications ? details.qualifications.join(', ') : "Not listed"}</p>
                                            <p><strong>Interests:</strong> {details.interests ? details.interests.join(', ') : "Not listed"}</p>
                                        </>
                                    )}
                                </div>
                            </TinderCard>
                        ))
                    ) : (
                        <div>No recommendations available try to refresh the page</div>
                    )}
                </div>
            </div>

            {lastDirection && (
                <Typography
                    className="infoText"
                    variant="body2"
                    sx={{ textAlign: "center", marginY: 2 }}
                >
                    You swiped {lastDirection}
                </Typography>
            )}

            <SwipeButton
                onSwipeLeft={() => swipe('left')}
                onSwipeRight={() => swipe('right')}
            />
        </>
    );
}

export default SwipeCards;
