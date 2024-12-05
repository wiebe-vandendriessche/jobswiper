import Header from "./../Components/header/Header";
import SwipeButton from "./../Components/swipebutton/SwipeButton";
import SwipeCards from "./../Components/swipecards/SwipeCards";

function MainView() {
  return (
    <div className="MainView">
      <SwipeCards />
      <SwipeButton />
    </div>
  );
}

export default MainView;