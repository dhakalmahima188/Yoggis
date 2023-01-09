import React, { useState, useEffect } from 'react';

function Home() {
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
      {data ? (
        <ul>
          {data.map((item) => (
            <li key={item.id}>
              <h1>{item.title}</h1>
              <p>{item.description}</p>
              <img src={item.image} alt={item.title} />
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Home;
