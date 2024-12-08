import React, { useState, useRef, useEffect } from 'react';
import TinderCard from 'react-tinder-card';
import SwipeButton from './../swipebutton/SwipeButton';
import './swipecards.css';
import { useContext } from 'react';
import { AuthContext } from '../../Views/AuthContext';

function SwipeCards(props) {
    // Get the authData from the context
    const { authData, setAuthData } = useContext(AuthContext);

    const [people, setPeople] = useState([
        {
            name: "Elon Musk",
            url: "https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg",
        },
        {
            name: "Jeff Bezos",
            url: "https://upload.wikimedia.org/wikipedia/commons/6/6c/Jeff_Bezos_at_Amazon_Spheres_Grand_Opening_in_Seattle_-_2018_%2839074799225%29_%28cropped%29.jpg",
        },
        {
            name: "Johnny Depp",
            url: "https://upload.wikimedia.org/wikipedia/commons/3/3b/Johnny_Depp-2757_%28cropped%29.jpg",
        },
        {
            name: "Tom Cruise",
            url: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Tom_Cruise_by_Gage_Skidmore_2.jpg/800px-Tom_Cruise_by_Gage_Skidmore_2.jpg",
        },
    ]);

    const [lastDirection, setLastDirection] = useState();
    const [isSwiping, setIsSwiping] = useState(false); // Track swipe state
    const childRefs = useRef([]);

    const swipe = (dir) => {
        if (isSwiping) {
            console.log('Swipe action blocked because a swipe is already in progress.');
            return;
        }
        const activeIndex = people.length - 1;
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
        setPeople((prevPeople) => prevPeople.filter((person) => person.name !== name)); // Remove card
        setIsSwiping(false); // Reset swiping state
    };

    // Check if authData is complete
    const isContextComplete =
        authData.userType &&
        authData.selected_profile_name &&
        (authData.userType === "jobseeker" || (authData.userType === "recruiter" && authData.selected_job_id));


    return (
        <>
            {isContextComplete ? (
                <>
                    <div className="swipeCards__contextInfo">
                        <div>
                            Swiping for {authData.userType}: {authData.selected_profile_name}{" "}
                            {authData.userType === "recruiter" && authData.selected_job_id && (
                                <span>on job: {authData.selected_job_name}</span>
                            )}
                        </div>
                    </div>
                    <div className="swipeCards">
                        <div className="swipeCards__cardContainer">
                            {people.map((person, index) => (
                                <TinderCard
                                    ref={(el) => (childRefs.current[index] = el)}
                                    key={person.name}
                                    className="swipe"
                                    preventSwipe={["up", "down"]}
                                    onSwipe={(dir) => swiped(dir, person.name)}
                                    onCardLeftScreen={() => outOfFrame(person.name)}
                                >
                                    <div
                                        style={{ backgroundImage: `url(${person.url})` }}
                                        className="card"
                                    >
                                        <h3>{person.name}</h3>
                                    </div>
                                </TinderCard>
                            ))}
                        </div>
                    </div>
                    {lastDirection ? (
                        <h2 className="infoText">You swiped {lastDirection}</h2>
                    ) : (
                        <h2 className="infoText" />
                    )}
                    <SwipeButton
                        onSwipeLeft={() => swipe('left')}
                        onSwipeRight={() => swipe('right')}
                    />
                </>
            ) : (
                <div className="placeholder">
                    <h2>Please log in as a jobseeker or recruiter with a selected job to view cards.</h2>
                </div>
            )}
        </>
    );
}

export default SwipeCards;