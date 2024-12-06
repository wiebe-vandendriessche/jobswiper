import React, { useState, useRef } from 'react';
import TinderCard from 'react-tinder-card';
import SwipeButton from './../swipebutton/SwipeButton';
import './swipecards.css';

function SwipeCards(props) {
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
    const childRefs = useRef([]);

    const swiped = (direction, nameToDelete) => {
        console.log("removing:" + nameToDelete);
        setLastDirection(direction);
    };

    const outOfFrame = (name) => {
        console.log(`${name} left the screen`);
        setPeople((prev) => prev.filter((person) => person.name !== name));
    };

    const swipe = (dir) => {
        const activeIndex = people.length - 1; // Get the current top card index
        const activeCard = childRefs.current[activeIndex]; // Access the correct card ref
        if (activeCard) {
            activeCard.swipe(dir); // Programmatically swipe
        }
    };

    return (
        <>
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
            <div className="infoText">
                {lastDirection ? <h2>You swiped {lastDirection}</h2> : <h2>Swipe a card!</h2>}
            </div>
            {/* Pass swipe actions as props to SwipeButton */}
            <SwipeButton onSwipeLeft={() => swipe('left')} onSwipeRight={() => swipe('right')} />
        </>
    );
}

export default SwipeCards;