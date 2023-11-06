import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import PostCard from "./PostCard";
import FilterField from "./FilterField";
import SortBy from "./SortBy";
import SearchBar from "./SearchBar";

// this is mock data, to be replaced later once database is setup
const postCardData = {
  title: "Fall Career Week",
  date: new Date(),
  location: "Myhal 5th Floor",
  description:
    "Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
  tags: ["Professional Development"],
};

const filterOptions = [
  {
    title: "Tag",
    values: [
      "All",
      "Professional Development",
      "Dance",
      "Design Club",
      "Sport",
    ],
  },
  {
    title: "Location",
    values: ["All", "Myhal 5th Floor", "Bahen Lobby", "Remote"],
  },
  {
    title: "Club",
    values: ["All", "YNCN", "Dance Club", "Design Club", "Sport Club"],
  },
  {
    title: "Date",
    values: ["All", "Today", "Tomorrow", "Never"],
  },
];

const numberOfCards = 10;

const LandingPage: React.FC = () => {
  const [searchResults, setSearchResults] = useState(null);

  const handleSearchData = (data: any) => {
    setSearchResults(data);
  };

  return (
    <div className="row">
      <div className="custom-col-md-3">
        {filterOptions.map((option, index) => (
          <FilterField
            key={index}
            title={option.title}
            values={option.values}
          />
        ))}
      </div>
      <div className="col-md-9">
        <div className="row">
          <div className="col-12">
            <SearchBar onDataReceived={handleSearchData} />
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <SortBy options={["Sort Option 1", "Sort Option 2"]} />
          </div>
        </div>
        <div className="row row-cols-1 row-cols-sm-2 row-cols-md-2 row-cols-lg-3 gx-3 gy-3">
          {Array.from({ length: numberOfCards }).map((_, index) => (
            <PostCard key={index} {...postCardData} postId={index} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default LandingPage;