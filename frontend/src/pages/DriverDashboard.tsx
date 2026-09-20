import { useEffect, useState } from "react";

function DriverDashboard() {
  const [rides, setRides] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem("token");

  const getRides = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/rides/driver/history",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(JSON.stringify(data.detail, null, 2));
        return;
      }

      setRides(data);
    } catch (error) {
      alert("Serverə qoşulmaq mümkün olmadı");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getRides();
  }, []);

  const startRide = async (rideId: number) => {
    const response = await fetch(
      `http://127.0.0.1:8000/rides/${rideId}/start`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(JSON.stringify(data.detail, null, 2));
      return;
    }

    setRides((currentRides) =>
      currentRides.map((ride) =>
        ride.id === rideId ? data : ride
      )
    );
  };

  const completeRide = async (rideId: number) => {
    const response = await fetch(
      `http://127.0.0.1:8000/rides/${rideId}/complete`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(JSON.stringify(data.detail, null, 2));
      return;
    }

    setRides((currentRides) =>
      currentRides.map((ride) =>
        ride.id === rideId ? data : ride
      )
    );
  };

  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <div className="driver-dashboard">
      <h1>🚕 Driver Dashboard</h1>

      <p>Your rides</p>

      {rides.length === 0 ? (
        <div className="no-rides">
          No rides yet
        </div>
      ) : (
        rides.map((ride) => (
          <div
            className="driver-ride-card"
            key={ride.id}
          >
            <h2>Ride #{ride.id}</h2>

            <p>
              📍 {ride.pickup_location}
            </p>

            <p>
              🏁 {ride.destination}
            </p>

            <p>
              Distance: {ride.distance_km} km
            </p>

            <p>
              Status: <strong>{ride.status}</strong>
            </p>

            {ride.status === "accepted" && (
              <button
                onClick={() => startRide(ride.id)}
              >
                ▶ Start ride
              </button>
            )}

            {ride.status === "started" && (
              <button
                onClick={() => completeRide(ride.id)}
              >
                🏁 Complete ride
              </button>
            )}

            {ride.status === "completed" && (
              <p className="completed-price">
                💰 Price: ${ride.price}
              </p>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default DriverDashboard;