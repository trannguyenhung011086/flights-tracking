import React, { useState, useEffect } from 'react';
import useFlightArrivals from '../hooks/useFlightArrivals';

const FlightArrivals = () => {
  const [airportCode, setAirportCode] = useState('');
  const [error, setError] = useState('');

  const { data: flights, error: queryError, refetch } = useFlightArrivals(airportCode);

  const handleChange = (e) => {
    setAirportCode(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (airportCode) {
      try {
        await refetch();
      } catch (error) {
        console.error(error);
        setError(`Failed to fetch flight data: ${error.message}`);
      }
    } else {
      setError('Missing airport code!');
    }
  };

  useEffect(() => {
    if (queryError) {
      setError(`${queryError.response?.data.detail || queryError.message}`);
    }
  }, [queryError]);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" value={airportCode} onChange={handleChange} placeholder="Enter Airport Code" />
        <button type="submit">Get Flight Arrivals</button>
      </form>

      <h2>Flight Arrivals for {airportCode}</h2>

      {error && <div>{`Error: ${error}`}</div>}

      {flights && (
        <table>
          <thead>
            <tr>
              <th>Country</th>
              <th># of Flights</th>
            </tr>
          </thead>
          <tbody>
            {flights?.map((flight, index) => (
              <tr key={index}>
                <td>{flight.country}</td>
                <td>{flight.flights}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FlightArrivals;
