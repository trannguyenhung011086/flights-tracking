import { QueryClient, QueryClientProvider } from 'react-query';
import FlightArrivals from './components/FlightArrivals';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <FlightArrivals />
    </QueryClientProvider>
  );
}

export default App;
