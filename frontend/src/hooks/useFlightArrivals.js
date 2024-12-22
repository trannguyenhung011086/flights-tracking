import { useQuery } from 'react-query';
import axios from 'axios';

const fetchArrivals = async (airportCode) => {
  const { data } = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/flights/arrivals/${airportCode}`);
  return data;
};

const useFlightArrivals = (airportCode) => {
  return useQuery(
    ['flightArrivals', airportCode], // unique key for caching
    () => fetchArrivals(airportCode),
    {
      enabled: false, // disable auto fetch on mounting
      refetchOnWindowFocus: false,
      retry: false,
      cacheTime: 1000 * 60 * 5, // Cache data for 5 minutes
    }
  );
};

export default useFlightArrivals;
