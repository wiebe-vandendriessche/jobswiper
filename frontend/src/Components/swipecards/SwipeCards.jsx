import React, { useState, useRef, useEffect } from 'react';
import TinderCard from 'react-tinder-card';
import SwipeButton from './../swipebutton/SwipeButton';
import './swipecards.css';
import { useContext } from 'react';
import { AuthContext } from '../../Views/AuthContext';
import Alert from "@mui/material/Alert";
import { Box, Typography, Button, Paper } from "@mui/material";

const apiBaseUrl = "http://localhost:8081";

function SwipeCards(props) {
    // Get the authData from the context
    const { authData, setAuthData } = useContext(AuthContext);

    const [recoms, setRecoms] = useState([]); // Will hold the recommendations (jobs or profiles)

    const [lastDirection, setLastDirection] = useState();
    const [isSwiping, setIsSwiping] = useState(false); // Track swipe state
    const childRefs = useRef([]);

    // Get JWT token from localStorage
    const jwtToken = localStorage.getItem("jwtToken");

    // Fetch recommendations based on the user type (jobseeker or recruiter)
    useEffect(() => {
        const fetchRecommendations = async () => {
            if (!authData.userType || !authData.selected_user_id) return; // Ensure userType and selected_user_id exist

            try {
                const headers = {
                    'Authorization': `Bearer ${jwtToken}`,
                    'Content-Type': 'application/json',
                };

                let response;

                if (authData.userType === "jobseeker") {
                    // Fetch job recommendations for the jobseeker
                    response = await fetch(`${apiBaseUrl}/matches/recommendations/user/${authData.selected_user_id}`, {
                        method: 'GET',
                        headers: headers,
                    });
                    const data = await response.json();
                    setRecoms(data.recommendations || []); // Set recommendations (job IDs)
                } else if (authData.userType === "recruiter" && authData.selected_job_id) {
                    // Fetch jobseeker profile recommendations for the recruiter based on selected job
                    response = await fetch(`${apiBaseUrl}/matches/recommendations/job/${authData.selected_job_id}`, {
                        method: 'GET',
                        headers: headers,
                    });
                    const data = await response.json();
                    setRecoms(data.recommendations || []); // Set recommendations (profile IDs of jobseekers)
                }
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            }
        };

        fetchRecommendations();
    }, [authData, jwtToken]); // Ensure jwtToken is included as dependency



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

    const swiped = (direction, nameToDelete) => {
        console.log(`Removing: ${nameToDelete}`);
        setLastDirection(direction);
    };

    const outOfFrame = (name) => {
        console.log(`${name} left the screen`);
        setRecoms((prevRecoms) => prevRecoms.filter((item) => item.name !== name)); // Remove card
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
                    {recoms.length > 0 ? (
                        recoms.map((item, index) => (
                            <TinderCard
                                ref={(el) => (childRefs.current[index] = el)}
                                key={item.id || item.name}
                                className="swipe"
                                preventSwipe={["up", "down"]}
                                onSwipe={(dir) => swiped(dir, item.name)}
                                onCardLeftScreen={() => outOfFrame(item.name)}
                            >
                                <div
                                    style={{ backgroundImage: `url(${item.url || ''})` }}
                                    className="card"
                                >
                                    <h3>{item.name}</h3>
                                </div>
                            </TinderCard>
                        ))
                    ) : (
                        <div>No recommendations available</div> // Placeholder if no recommendations are loaded
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
            {/* Pass swipe actions as props to SwipeButton */}
            <SwipeButton
                onSwipeLeft={() => swipe('left')}
                onSwipeRight={() => swipe('right')}
            />
        </>
    );

}

export default SwipeCards;