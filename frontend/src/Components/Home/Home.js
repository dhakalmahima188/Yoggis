import React, { useState, useEffect } from 'react';

//fetch data from django backend http://127.0.0.1:8000/api/yoga/
//use axios to fetch data from backend

//create function that fetches data from http://127.0.0.1:8000/api/yoga/

const Home = () => {
    const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch('http://127.0.0.1:8000/api/yoga/');
      const json = await response.json();
      setData(json);
    }
    fetchData();
  }, []);

  return (
    <div>
      { data ? JSON.stringify(data) : 'Loading...' }
    </div>
  );
}







export default Home;