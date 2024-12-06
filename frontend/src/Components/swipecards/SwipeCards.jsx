import React, { useState } from 'react';
import TinderCard from 'react-tinder-card';
import "./swipecards.css"

function SwipeCards(props) {
    const [people,] = useState([
        {
            name: "Elon Musk",
            url: "https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg",
        }, {
            name: "Jeff Bezos",
            url: "https://upload.wikimedia.org/wikipedia/commons/6/6c/Jeff_Bezos_at_Amazon_Spheres_Grand_Opening_in_Seattle_-_2018_%2839074799225%29_%28cropped%29.jpg",
        }, {
            name: "Johnny Depp",
            url: "https://upload.wikimedia.org/wikipedia/commons/3/3b/Johnny_Depp-2757_%28cropped%29.jpg"
        }, {
            name: "Tom Cruise",
            url: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Tom_Cruise_by_Gage_Skidmore_2.jpg/800px-Tom_Cruise_by_Gage_Skidmore_2.jpg"
        }
    ]);

    const [lastDirection, setLastDirection] = useState()


    const swiped = (direction, nameToDelete) => {
        console.log("removing:" + nameToDelete);
        setLastDirection(direction)
    };
    const outOfFrame = (name) => {
        console.log(name + "left the screen");
    };


    return (
        <>
            <div className="swipeCards">
                <div className="swipeCards__cardContainer">
                    {people.map((person) => (
                        <TinderCard
                            className="swipe"
                            key={person.name}
                            preventSwipe={["up", "down"]}
                            onSwipe={(dir) => swiped(dir, person.name)}
                            onCardLeftScreen={() => outOfFrame(person.name)}>
                            <div style={{ backgroundImage: `url(${person.url})` }} className="card">
                                <h3>{person.name}</h3>
                            </div>
                        </TinderCard>
                    ))}
                </div>
            </div>
            {lastDirection ? <h2 className='infoText'>You swiped {lastDirection}</h2> : <h2 className='infoText' />}
        </>
    );
}

export default SwipeCards;