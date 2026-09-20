import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import DriverDashboard from "./pages/DriverDashboard";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/driver"
          element={<DriverDashboard />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;